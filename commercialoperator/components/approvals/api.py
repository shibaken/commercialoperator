import traceback
import datetime
import re
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, generics
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from datetime import datetime
from commercialoperator.components.permission.permission import InternalPermission
from commercialoperator.components.proposals.models import (
    Proposal,
    ApplicationType,
)
from commercialoperator.components.proposals.utils import (
    search_in_emailuser_fields,
    search_organisation_properties,
)
from commercialoperator.components.approvals.models import Approval, ApprovalDocument
from commercialoperator.components.approvals.serializers import (
    ApprovalSerializer,
    ApprovalCancellationSerializer,
    ApprovalExtendSerializer,
    ApprovalSuspensionSerializer,
    ApprovalSurrenderSerializer,
    ApprovalUserActionSerializer,
    ApprovalLogEntrySerializer,
    ApprovalPaymentSerializer,
)
from commercialoperator.components.organisations.models import (
    Organisation,
    OrganisationContact,
)
from commercialoperator.components.segregation.decorators import basic_exception_handler
from rest_framework_datatables.filters import DatatablesFilterBackend
from commercialoperator.components.segregation.utils import (
    retrieve_delegate_organisation_ids,
)
from commercialoperator.helpers import is_internal
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework import filters, mixins


import logging

logger = logging.getLogger(__name__)

def approval_search_filter(qs, search_value):
    matching_ids = []
    org_matching_ids = []

    if search_value:
        search_value = search_value.strip()
        search_q = (
            Q(lodgement_number__icontains=search_value)
            | Q(current_proposal__lodgement_number__icontains=search_value)
            | Q(current_proposal__event_activity__event_name__icontains=search_value)
        )

        if len(search_value) >= 3:
            matching_ids = search_in_emailuser_fields(search_value)
            org_matching_ids = search_organisation_properties(search_value, False)
            search_q = search_q | (
                Q(proxy_applicant_id__in=matching_ids)
                | Q(org_applicant_id__in=org_matching_ids)
                | (
                    Q(org_applicant__isnull=True)
                    & Q(proxy_applicant__isnull=True)
                    & Q(submitter_id__in=matching_ids)
                )
            )

        qs = qs.filter(search_q)

    return qs, matching_ids + org_matching_ids


class ApprovalFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """

    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()

        super_queryset = None
        try:
            super_queryset = super(ApprovalFilterBackend, self).filter_queryset(request, queryset, view).distinct()
        except Exception as e:
            logger.exception(f'Failed to filter the queryset.  Error: [{e}]')

        search_text = request.GET.get('search[value]')

        status = request.GET.get("datatable_filter_status")
        licence_type = request.GET.get("datatable_filter_current_proposal__application_type__name")
        start_date_from = request.GET.get("start_date_from")
        start_date_to = request.GET.get("start_date_to")
        expiry_date_from = request.GET.get("expiry_date_from")
        expiry_date_to = request.GET.get("expiry_date_to")

        if queryset.model is Approval:
            if status and status.lower() != "all":
                queryset = queryset.filter(status=status)
            if licence_type and licence_type.lower() != "all":
                queryset = queryset.filter(current_proposal__application_type__name=licence_type)
            if start_date_from:
                queryset = queryset.filter(start_date__gte=start_date_from)

            if start_date_to:
                queryset = queryset.filter(start_date__lte=start_date_to)

            if expiry_date_from:
                queryset = queryset.filter(expiry_date__gte=expiry_date_from)

            if expiry_date_to:
                queryset = queryset.filter(expiry_date__lte=expiry_date_to)


        if search_text:
            search_queryset, results_found = approval_search_filter(queryset, search_text)
            queryset = search_queryset.distinct()
    

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        setattr(view, "_datatables_total_count", total_count)
        return queryset


class ApprovalPaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ApprovalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    page_size = 10
    queryset = Approval.objects.none()
    serializer_class = ApprovalSerializer

    def get_queryset(self):
        if is_internal(self.request):
            return Approval.objects.all()
        else:
            user = self.request.user
            user_orgs = retrieve_delegate_organisation_ids(user.id)
            queryset = Approval.objects.filter(
                Q(org_applicant_id__in=user_orgs) | Q(submitter_id=user.id)
            )
            return queryset

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def approvals_external(self, request, *args, **kwargs):
        """
        Paginated serializer for datatables - used by the internal and external dashboard (filtered by the get_queryset method)
        """

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ApprovalSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)


class ApprovalPaymentFilterViewSet(generics.ListAPIView):

    queryset = Approval.objects.none()
    serializer_class = ApprovalPaymentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("id",)

    def get_queryset(self):
        """
        Return All approvals associated with user (proxy_applicant and org_applicant)
        """
        user = self.request.user

        # get all orgs associated with user
        user_org_ids = OrganisationContact.objects.filter(email=user.email).values_list(
            "organisation_id", flat=True
        )

        now = datetime.now().date()
        approval_qs = Approval.objects.filter(
            Q(proxy_applicant=user)
            | Q(org_applicant_id__in=user_org_ids)
            | Q(submitter_id=user)
        )
        approval_qs = approval_qs.exclude(
            current_proposal__application_type__name="E Class"
        )
        approval_qs = approval_qs.exclude(expiry_date__lt=now)
        approval_qs = approval_qs.exclude(
            replaced_by__isnull=False
        )  # get lastest licence, ignore the amended
        return approval_qs


class ApprovalViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Approval.objects.none()
    serializer_class = ApprovalSerializer

    def get_queryset(self):
        if is_internal(self.request):
            return Approval.objects.all()
        else:
            user = self.request.user
            user_orgs = retrieve_delegate_organisation_ids(user.id)
            queryset = Approval.objects.filter(
                Q(org_applicant_id__in=user_orgs) | Q(submitter_id=user.id)
            )
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
            approval_status_choices=[i[1] for i in Approval.STATUS_CHOICES],
            application_types=application_types,
        )
        return Response(data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    @transaction.atomic
    def add_eclass_licence(self, request, *args, **kwargs):

        def raiser(exception):
            raise serializers.ValidationError(exception)

        org_applicant = None
        proxy_applicant = None

        _file = (
            request.data.get("file")
            if request.data.get("file")
            else raiser("Licence File is required")
        )
        try:
            if request.data.get("applicant_type") == "org":
                org_applicant = Organisation.objects.get(
                    organisation_id=request.data.get("holder-selected")
                )
            else:
                proxy_applicant = EmailUser.objects.get(
                    id=request.data.get("holder-selected")
                )
        except:
            raise serializers.ValidationError("Licence holder is required")

        reserved_licence = request.data.get("reserved_licence", None)
        if reserved_licence:
            # check format is correct 'L001234'
            pattern = re.compile("L[^0-9]*[0-9]{6}$")
            if not bool(re.search(pattern, reserved_licence)):
                raise serializers.ValidationError(
                    "Reserved Licence format must be 'L001234'"
                )

            if Approval.objects.filter(
                lodgement_number=reserved_licence
            ).exists():
                raise serializers.ValidationError(
                    f"Reserved Licence (Lodgement Number) already exists: {reserved_licence}"
                )

        start_date = (
            datetime.strptime(request.data.get("start_date"), "%Y-%m-%d")
            if request.data.get("start_date")
            else raiser("Start Date is required")
        )
        issue_date = (
            datetime.strptime(request.data.get("issue_date"), "%Y-%m-%d")
            if request.data.get("issue_date")
            else raiser("Issue Date is required")
        )
        expiry_date = (
            datetime.strptime(request.data.get("expiry_date"), "%Y-%m-%d")
            if request.data.get("expiry_date")
            else raiser("Expiry Date is required")
        )

        application_type, app_type_created = (
            ApplicationType.objects.get_or_create(
                name="E Class",
                defaults={
                    "visible": False,
                    "max_renewals": 1,
                    "max_renewal_period": 5,
                },
            )
        )

        proposal, proposal_created = (
            Proposal.objects.get_or_create(  # Dummy 'E Class' proposal
                id=0,
                defaults={
                    "application_type": application_type,
                    "submitter": request.user,
                    "schema": [],
                },
            )
        )

        approval = Approval.objects.create(
            lodgement_number=reserved_licence,
            reserved_licence=True if reserved_licence else False,
            issue_date=issue_date,
            expiry_date=expiry_date,
            start_date=start_date,
            org_applicant=org_applicant,
            proxy_applicant=proxy_applicant,
            current_proposal=proposal,
        )

        doc = ApprovalDocument.objects.create(approval=approval, _file=_file)
        approval.licence_document = doc
        approval.save()

        return Response({"approval": approval.lodgement_number})


    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    def approval_extend(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ApprovalExtendSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.approval_extend(request, serializer.validated_data)
            serializer = ApprovalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
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
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    def approval_cancellation(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ApprovalCancellationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.approval_cancellation(request, serializer.validated_data)
            serializer = ApprovalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
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
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    def approval_suspension(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ApprovalSuspensionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.approval_suspension(request, serializer.validated_data)
            serializer = ApprovalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
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
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    def approval_reinstate(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.reinstate_approval(request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
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
        permission_classes=[InternalPermission] #TODO not apparent if higher permission required, keeping to internal for now
    )
    def approval_surrender(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ApprovalSurrenderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.approval_surrender(request, serializer.validated_data)
            serializer = ApprovalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
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
        permission_classes=[InternalPermission]
    )
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = ApprovalUserActionSerializer(qs, many=True)
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
            serializer = ApprovalLogEntrySerializer(qs, many=True)
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
                request.data["approval"] = "{}".format(instance.id)
                request.data["staff"] = "{}".format(request.user.id)
                request.data._mutable = mutable
                serializer = ApprovalLogEntrySerializer(data=request.data)
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
