import traceback
import logging
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from rest_framework import viewsets, serializers, views, mixins
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from commercialoperator.components.compliances.models import (
    Compliance,
    ComplianceAmendmentRequest,
    ComplianceAmendmentReason,
)
from commercialoperator.components.main.models import ApplicationType
from commercialoperator.components.compliances.serializers import (
    ComplianceSerializer,
    InternalComplianceSerializer,
    SaveComplianceSerializer,
    ComplianceActionSerializer,
    ComplianceCommsSerializer,
    ComplianceAmendmentRequestSerializer,
    CompAmendmentRequestDisplaySerializer,
)
from commercialoperator.components.segregation.utils import (
    retrieve_cols_organisations_from_ledger_org_ids,
    retrieve_delegate_organisation_ids,
)
from commercialoperator.helpers import is_internal, is_assessor
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from commercialoperator.components.proposals.utils import (
    search_in_emailuser_fields,
    search_organisation_properties,
)
from commercialoperator.components.permission.permission import InternalPermission, ProposalAssessorPermission
from django.core.exceptions import PermissionDenied
from commercialoperator.components.organisations.models import Organisation
from ledger_api_client.utils import get_search_organisation


logger = logging.getLogger(__name__)


def _get_matching_organisation_ids(search_value):
    """Resolve local Organisation ids from cached props, then fallback to ledger search by name."""
    org_matching_ids = set(search_organisation_properties(search_value, False))

    if org_matching_ids:
        return list(org_matching_ids)

    ledger_organisation_response = get_search_organisation(search_value, None)
    if ledger_organisation_response.get("status") != 200:
        return []

    ledger_org_ids = [
        org.get("organisation_id")
        for org in ledger_organisation_response.get("data", [])
        if org.get("organisation_id")
    ]

    if not ledger_org_ids:
        return []

    local_org_ids = Organisation.objects.filter(
        organisation_id__in=ledger_org_ids
    ).values_list("id", flat=True)
    org_matching_ids.update(local_org_ids)
    return list(org_matching_ids)


def compliance_search_filter(qs, search_value):
    matching_ids = []
    org_matching_ids = []

    if search_value:
        search_value = search_value.strip()
        search_q = (
            Q(lodgement_number__icontains=search_value)
            | Q(approval__lodgement_number__icontains=search_value)
            | Q(approval__current_proposal__event_activity__event_name__icontains=search_value)
        )

        # Holder search is broader and expensive for very short strings.
        if len(search_value) >= 3:
            matching_ids = search_in_emailuser_fields(search_value)
            org_matching_ids = _get_matching_organisation_ids(search_value)
            search_q = search_q | (
                Q(proposal__proxy_applicant_id__in=matching_ids)
                | Q(proposal__org_applicant_id__in=org_matching_ids)
                | (
                    Q(proposal__org_applicant__isnull=True)
                    & Q(proposal__proxy_applicant__isnull=True)
                    & Q(proposal__submitter_id__in=matching_ids)
                )
            )

        qs = qs.filter(search_q)

    return qs, matching_ids + org_matching_ids


class ComplianceFilterBackend(DatatablesFilterBackend):
    """Datatables filters dedicated to compliances to keep global search deterministic."""

    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        super_queryset = None
        try:
            super_queryset = super(ComplianceFilterBackend, self).filter_queryset(request, queryset, view).distinct()
        except Exception as e:
            logger.exception(f"Failed to filter the queryset. Error: [{e}]")

        search_text = request.GET.get("search[value]")
        regions = request.GET.get("regions")
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        processing_status = request.GET.get("datatable_filter_processing_status")
        application_type = request.GET.get("datatable_filter_proposal__application_type__name")

        if regions:
            queryset = queryset.filter(
                proposal__region__name__iregex=regions.replace(",", "|")
            )

        if date_from:
            queryset = queryset.filter(due_date__gte=date_from)

        if date_to:
            queryset = queryset.filter(due_date__lte=date_to)

        if processing_status and processing_status.lower() != "all":
            queryset = queryset.filter(processing_status=processing_status)

        if application_type and application_type.lower() != "all":
            queryset = queryset.filter(proposal__application_type__name=application_type)

        if search_text:
            search_queryset, _ = compliance_search_filter(queryset, search_text)
            queryset = search_queryset.distinct()
        elif super_queryset is not None:
            queryset = queryset.distinct() & super_queryset

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        setattr(view, "_datatables_total_count", total_count)
        return queryset

def user_can_edit(request, instance):
    """
    Return True or False based on whether or not the user is authorised to edit
    """
    if not request.user or not instance.proposal:
        return False
    
    user = request.user 
    user_orgs = retrieve_delegate_organisation_ids(user)

    #if in draft check if the user if either an allowed org member or an assessor, return True if so
    if (
        (instance.proposal.org_applicant_id in user_orgs or instance.proposal.submitter_id == user.id) and 
        instance.processing_status == "due"
    ):
        return True

    #if under assessment stages only assessors can edit
    if (
        is_assessor(request) and 
        (instance.processing_status == "with_assessor" or instance.processing_status == "due")
    ):
        return True

    #otherwise return False
    return False


class CompliancePaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ComplianceFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    page_size = 10
    queryset = Compliance.objects.none()
    serializer_class = ComplianceSerializer

    def get_queryset(self):
        if is_internal(self.request):
            return Compliance.objects.all().exclude(
                Q(processing_status="discarded")
                | Q(requirement__notification_only=True)
            )
        else:
            user = self.request.user

            commercialoperator_organisations = (
                retrieve_cols_organisations_from_ledger_org_ids(user)
            )

            user_orgs = [o["organisation_id"] for o in commercialoperator_organisations]

            queryset = Compliance.objects.filter(
                Q(proposal__org_applicant_id__in=user_orgs)
                | Q(proposal__submitter_id=user.id)
            ).exclude(
                Q(processing_status="discarded")
                | Q(requirement__notification_only=True)
            )
            return queryset

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def compliances_external(self, request, *args, **kwargs):
        """
        Paginated serializer for datatables - used by the external dashboard
        """

        qs = self.get_queryset().exclude(processing_status="future")
        qs = self.filter_queryset(qs)

        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        applicant_id = request.GET.get("org_id")
        if applicant_id:
            qs = qs.filter(proposal__org_applicant_id=applicant_id)
        submitter_id = request.GET.get("submitter_id", None)
        if submitter_id:
            qs = qs.filter(proposal__submitter_id=submitter_id)
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ComplianceSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    def compliances_internal(self, request, *args, **kwargs):
        """Same as external compliance endpoint but including future compliances"""
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        applicant_id = request.GET.get("org_id")
        if applicant_id:
            qs = qs.filter(proposal__org_applicant_id=applicant_id)
        submitter_id = request.GET.get("submitter_id", None)
        if submitter_id:
            qs = qs.filter(proposal__submitter_id=submitter_id)
        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ComplianceSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)


class ComplianceViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = ComplianceSerializer
    queryset = Compliance.objects.none()

    def get_queryset(self):
        if is_internal(self.request):
            return Compliance.objects.all().exclude(processing_status="discarded")
        else:
            user = self.request.user
            user_orgs = retrieve_delegate_organisation_ids(user.id)
            queryset = Compliance.objects.filter(
                Q(proposal__org_applicant_id__in=user_orgs)
                | Q(proposal__submitter_id=user.id)
            ).exclude(processing_status="discarded")
            return queryset

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def filter_list(self, request, *args, **kwargs):
        """Used by the external dashboard filters"""

        application_types = ApplicationType.objects.all().values_list("name", flat=True)
        data = dict(
            application_types=application_types,
        )
        return Response(data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def internal_compliance(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = InternalComplianceSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()

                if not user_can_edit(request, instance):
                    raise PermissionDenied
                
                data = {
                    "text": request.data.get("detail"),
                    "num_participants": request.data.get("num_participants"),
                    "num_child_participants": request.data.get(
                        "num_child_participants"
                    ),
                }

                serializer = SaveComplianceSerializer(instance, data=data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()

                # if request.data.has_key('num_participants'):
                if "num_participants" in request.data:
                    if request.FILES:
                        # if num_adults is present instance.submit is executed after payment in das_payment/views.py
                        for f in request.FILES:
                            document = instance.documents.create(
                                name=str(request.FILES[f])
                            )
                            document._file = request.FILES[f]
                            document.save()
                else:
                    instance.submit(request)

                serializer = self.get_serializer(instance)
                # Save the files
                """for f in request.FILES:
                    document = instance.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents"""
                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "message"):
                raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_to(request.user, request)
            serializer = InternalComplianceSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not user_can_edit(request, instance):
                raise PermissionDenied
            doc = request.data.get("document")
            instance.delete_document(request, doc)
            serializer = ComplianceSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "message"):
                raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get("user_id", None)
            user = None
            if not user_id:
                raise serializers.ValiationError("A user id is required")
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    "A user with the id passed in does not exist"
                )
            instance.assign_to(user, request)
            serializer = InternalComplianceSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            serializer = InternalComplianceSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    def accept(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.accept(request)
            serializer = InternalComplianceSerializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def amendment_request(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.amendment_requests
            qs = qs.filter(status="requested")
            serializer = CompAmendmentRequestDisplaySerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = ComplianceActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = ComplianceCommsSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable = request.data._mutable
                request.data._mutable = True
                request.data["compliance"] = "{}".format(instance.id)
                request.data["staff"] = "{}".format(request.user.id)
                request.data._mutable = mutable
                serializer = ComplianceCommsSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    comms.documents.create(
                        name = str(request.FILES[f]),
                        _file = request.FILES[f]
                    )
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ComplianceAmendmentRequestViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = ComplianceAmendmentRequest.objects.none()
    serializer_class = ComplianceAmendmentRequestSerializer
    permission_classes=[ProposalAssessorPermission]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            instance.generate_amendment(request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ComplianceAmendmentReasonChoicesView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        choices_list = cache.get(settings.CACHE_KEY_COMPLIANCE_AMENDMENT_REASON_CHOICES)

        if choices_list is None:
            choices_list = []
            choices = ComplianceAmendmentReason.objects.all()

            if choices:
                for c in choices:
                    choices_list.append({"key": c.id, "value": c.reason})
            cache.set(
                settings.CACHE_KEY_COMPLIANCE_AMENDMENT_REASON_CHOICES,
                choices_list,
                settings.CACHE_TIMEOUT_24_HOURS,
            )
        return Response(choices_list)
