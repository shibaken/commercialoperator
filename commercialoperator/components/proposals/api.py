import traceback
import os
import json
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets, serializers, status, views, mixins
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from commercialoperator.components.proposals.utils import (
    get_chained_list,
    get_proposal_serializer_by_application_type,
    save_proponent_data,
    save_assessor_data,
    proposal_submit,
    get_proposal_processing_status,
    get_district_proposal_processing_status,
    paginate_chained_list,
    searchKeyWords,
    search_in_emailuser_fields,
    search_organisation_properties,
)
from commercialoperator.components.proposals.models import (
    search_reference,
    ProposalUserAction,
)

from commercialoperator.components.main.models import (
    Region,
    District,
    ApplicationType,
    RequiredDocument,
    LicencePeriod,
)
from commercialoperator.components.proposals.models import (
    ProposalType,
    Proposal,
    Referral,
    ReferralRecipientGroup,
    QAOfficerGroup,
    ProposalRequirement,
    ProposalStandardRequirement,
    AmendmentRequest,
    AmendmentReason,
    Vehicle,
    Vessel,
    ProposalAccreditation,
    ProposalAssessment,
    ProposalAssessmentAnswer,
    RequirementDocument,
    DistrictProposal,
    ProposalEmissionStandard,
    ProposalInformationStandard,
)
from commercialoperator.components.proposals.serializers import (
    SendReferralSerializer,
    ProposalSerializer,
    InternalProposalSerializer,
    SaveProposalSerializer,
    ProposalUserActionSerializer,
    ProposalLogEntrySerializer,
    DTReferralSerializer,
    ReferralSerializer,
    ProposalRequirementSerializer,
    ProposalStandardRequirementSerializer,
    ProposedApprovalSerializer,
    PropedDeclineSerializer,
    AmendmentRequestSerializer,
    SearchReferenceSerializer,
    SearchKeywordSerializer,
    ListProposalSerializer,
    AmendmentRequestDisplaySerializer,
    SaveVehicleSerializer,
    VehicleSerializer,
    VesselSerializer,
    SaveProposalOtherDetailsSerializer,
    ProposalParkSerializer,
    ProposalAssessmentSerializer,
    ProposalAssessmentAnswerSerializer,
    ParksAndTrailSerializer,
    ProposalFilmingSerializer,
    InternalFilmingProposalSerializer,
    ProposalEventSerializer,
    InternalEventProposalSerializer,
    DistrictProposalSerializer,
    ListDistrictProposalSerializer,
)
from commercialoperator.components.proposals.serializers_filming import (
    ProposalFilmingOtherDetailsSerializer,
    ProposalFilmingParksSerializer,
    ProposalFilmingActivitySerializer,
    ProposalFilmingAccessSerializer,
    ProposalFilmingEquipmentSerializer,
)
from commercialoperator.components.proposals.serializers_event import (
    ProposalEventOtherDetailsSerializer,
    ProposalEventsParksSerializer,
    AbseilingClimbingActivitySerializer,
    ProposalPreEventsParksSerializer,
    ProposalEventManagementSerializer,
    ProposalEventActivitiesSerializer,
    ProposalEventVehiclesVesselsSerializer,
    ProposalEventsTrailsSerializer,
)


from commercialoperator.components.bookings.models import (
    Booking,
    ParkBooking,
    BookingInvoice,
)
from commercialoperator.components.compliances.models import Compliance

from commercialoperator.components.segregation.decorators import basic_exception_handler
from commercialoperator.components.segregation.utils import (
    QuerySetChain,
    retrieve_delegate_organisation_ids,
    retrieve_group_members,
    retrieve_user_groups,
)
from commercialoperator.helpers import is_internal, is_assessor
from django.core.files.base import ContentFile

from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend

from commercialoperator.components.permission.permission import (
    InternalPermission, ProposalAssessorPermission, 
    QAOfficerPermission, ProposalApproverPermission, 
    ReferrerPermission,
    DistrictProposalAssessorPermission, DistrictProposalApproverPermission
)
from django.core.exceptions import PermissionDenied

import logging
logger = logging.getLogger(__name__)

from commercialoperator.components.main.models import private_storage

def proposal_search_filter(qs, search_value):

    if search_value:
        matching_ids = search_in_emailuser_fields(search_value)
        org_matching_ids = search_organisation_properties(search_value, False)

        # Apply both filters only if we found any matching submitters
        qs = qs.filter(
            Q(submitter_id__in=matching_ids) | Q(proxy_applicant_id__in=matching_ids) | Q(assigned_officer_id__in=matching_ids) | Q(org_applicant_id__in=org_matching_ids)
        )

    return qs

def district_proposal_search_filter(qs, search_value):

    if search_value:
        matching_ids = search_in_emailuser_fields(search_value)
        org_matching_ids = search_organisation_properties(search_value, False)

        # Apply both filters only if we found any matching submitters
        qs = qs.filter(
            Q(proposal__submitter_id__in=matching_ids) | Q(proposal__proxy_applicant_id__in=matching_ids) | Q(assigned_officer_id__in=matching_ids) | Q(proposal__org_applicant_id__in=org_matching_ids)
        )

    return qs, matching_ids+org_matching_ids

def referral_search_filter(qs, search_value):

    if search_value:
        matching_ids = search_in_emailuser_fields(search_value)
        org_matching_ids = search_organisation_properties(search_value, False)

        # Apply both filters only if we found any matching submitters
        qs = qs.filter(
            Q(proposal__submitter_id__in=matching_ids) | Q(proposal__proxy_applicant_id__in=matching_ids) | Q(proposal__assigned_officer_id__in=matching_ids) | Q(proposal__org_applicant_id__in=org_matching_ids)
        )

    return qs, matching_ids+org_matching_ids

def compliance_search_filter(qs, search_value):
    matching_ids = []
    org_matching_ids = []

    if search_value:
        search_value = search_value.strip()

        # Always search Number and License (fast indexed string matching paths).
        search_q = (
            Q(lodgement_number__icontains=search_value)
            | Q(approval__lodgement_number__icontains=search_value)
        )

        # Holder search relies on broader email/organisation lookups.
        # For very short text (e.g. "sc"), those lookups are high-cardinality and slow.
        if len(search_value) >= 3:
            matching_ids = search_in_emailuser_fields(search_value)
            org_matching_ids = search_organisation_properties(search_value, False)
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


def user_can_edit(request, instance):
    """
    Return True or False based on whether or not the user is authorised to edit
    """
    if not request.user:
        return False
    
    user = request.user 
    user_orgs = retrieve_delegate_organisation_ids(user)

    #if in draft check if the user if either an allowed org member or an assessor, return True if so
    if (
        (instance.org_applicant_id in user_orgs or instance.submitter_id == user.id) and 
        instance.processing_status == Proposal.PROCESSING_STATUS_DRAFT
    ):
        return True

    #if under assessment stages (including with referrers and similar statuses) only assessors can edit
    #(referrer operations should not use this test function)
    if (
        is_assessor(request) and 
        instance.processing_status in [
            Proposal.PROCESSING_STATUS_DRAFT,
            Proposal.PROCESSING_STATUS_WITH_ASSESSOR,
            Proposal.PROCESSING_STATUS_WITH_DISTRICT_ASSESSOR,
            Proposal.PROCESSING_STATUS_ONHOLD,
            Proposal.PROCESSING_STATUS_WITH_QA_OFFICER,
            Proposal.PROCESSING_STATUS_WITH_REFERRAL,
            Proposal.PROCESSING_STATUS_WITH_ASSESSOR_REQUIREMENTS,
        ]
    ):
        return True

    #otherwise return False (approver operations should also not use this test function)
    return False


class ProposalFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """

    def filter_queryset(self, request, queryset, view):

        total_count = queryset.count()
        super_queryset = None
        try:
            super_queryset = super(ProposalFilterBackend, self).filter_queryset(request, queryset, view).distinct()
        except Exception as e:
            logger.exception(f'Failed to filter the queryset.  Error: [{e}]')

        search_text = request.GET.get('search[value]')

        # on the internal dashboard, the Region filter is multi-select - have to use the custom filter below
        regions = request.GET.get("regions")
        if regions:
            if queryset.model is Proposal:
                queryset = queryset.filter(
                    region__name__iregex=regions.replace(",", "|")
                )
            elif queryset.model is Referral or queryset.model is Compliance:
                queryset = queryset.filter(
                    proposal__region__name__iregex=regions.replace(",", "|")
                )
               
        date_from = request.GET.get("date_from")
        date_to = request.GET.get("date_to")
        
        if queryset.model is Proposal:

            processing_status = request.GET.get("datatable_filter_processing_status")
            application_type = request.GET.get("datatable_filter_application_type__name")

            if date_from:
                queryset = queryset.filter(lodgement_date__gte=date_from)

            if date_to:
                queryset = queryset.filter(lodgement_date__lte=date_to)

            if processing_status and processing_status.lower() != "all":
                queryset = queryset.filter(processing_status=processing_status)

            if application_type and application_type.lower() != "all":
                queryset = queryset.filter(application_type__name=application_type)

            if search_text and super_queryset != None:
                search_queryset = proposal_search_filter(queryset, search_text)
                if search_queryset.exists():
                    queryset = search_queryset.distinct() | super_queryset   
                else:
                    queryset = queryset.distinct() & super_queryset   

        elif queryset.model is Compliance:

            processing_status = request.GET.get("datatable_filter_processing_status")
            application_type = request.GET.get("datatable_filter_proposal__application_type__name")

            if date_from:
                queryset = queryset.filter(due_date__gte=date_from)

            if date_to:
                queryset = queryset.filter(due_date__lte=date_to)

            if processing_status and processing_status.lower() != "all":
                queryset = queryset.filter(processing_status=processing_status)

            if application_type and application_type.lower() != "all":
                queryset = queryset.filter(proposal__application_type__name=application_type)

            if search_text:
                search_queryset, results_found = compliance_search_filter(queryset, search_text)
                if super_queryset != None:
                    queryset = search_queryset.distinct() & super_queryset
                else:
                    queryset = search_queryset.distinct()

        elif queryset.model is Referral:

            processing_status = request.GET.get("datatable_filter_processing_status")
            application_type = request.GET.get("datatable_filter_proposal__application_type__name")
            
            if date_from:
                queryset = queryset.filter(proposal__lodgement_date__gte=date_from)

            if date_to:
                queryset = queryset.filter(proposal__lodgement_date__lte=date_to)

            if processing_status and processing_status.lower() != "all":
                queryset = queryset.filter(proposal__processing_status=processing_status)

            if application_type and application_type.lower() != "all":
                queryset = queryset.filter(proposal__application_type__name=application_type)

            if search_text and super_queryset != None:
                search_queryset, results_found = referral_search_filter(queryset, search_text)
                if results_found:
                    queryset = search_queryset.distinct() | super_queryset   
                else:
                    queryset = queryset.distinct() & super_queryset 

        elif queryset.model is Booking:
            if date_from and date_to:
                queryset = queryset.filter(
                    park_bookings__arrival__range=[date_from, date_to]
                )
            elif date_from:
                queryset = queryset.filter(park_bookings__arrival__gte=date_from)
            elif date_to:
                queryset = queryset.filter(park_bookings__arrival__lte=date_to)

            payment_method = request.GET.get("payment_method")
            payment_status = request.GET.get("payment_status")
            park = request.GET.get("park")

            if payment_method:
                if payment_method == str(
                    BookingInvoice.PAYMENT_METHOD_MONTHLY_INVOICING
                ):
                    # for deferred payment where invoice not yet created (monthly invoicing), append the following qs
                    queryset = queryset.filter(
                        Q(invoices__payment_method=payment_method)
                        | Q(
                            booking_type=Booking.BOOKING_TYPE_MONTHLY_INVOICING
                        )
                    )
                else:
                    queryset = queryset.filter(
                        Q(invoices__payment_method=payment_method)
                    )


            if payment_status:
                payment_status_filter = payment_status.replace("_", " ")
                if payment_status_filter.lower() != "all":
                    queryset = queryset.filter(
                        invoices__property_cache__payment_status__iexact=payment_status_filter
                    )

            if search_text and super_queryset != None:
                queryset = queryset.distinct() & super_queryset   

            if park and park.lower() != "all":
                queryset = queryset.filter(park_bookings__park__id=park)
        elif queryset.model is ParkBooking:
            if date_from and date_to:
                queryset = queryset.filter(arrival__range=[date_from, date_to])
            elif date_from:
                queryset = queryset.filter(arrival__gte=date_from)
            elif date_to:
                queryset = queryset.filter(arrival__lte=date_to)

            payment_method = request.GET.get("payment_method")
            payment_status = request.GET.get("payment_status")
            park = request.GET.get("park")

            if payment_method:
                if payment_method == str(
                    BookingInvoice.PAYMENT_METHOD_MONTHLY_INVOICING
                ):
                    # for deferred payment where invoice not yet created (monthly invoicing), append the following qs
                    queryset = queryset.filter(
                        Q(booking__invoices__payment_method=payment_method)
                        | Q(
                            booking__booking_type=Booking.BOOKING_TYPE_MONTHLY_INVOICING
                        )
                    )
                else:
                    queryset = queryset.filter(
                        Q(booking__invoices__payment_method=payment_method)
                    )

            if payment_status:
                payment_status_filter = payment_status.replace("_", " ")
                if payment_status_filter.lower() != "all":
                    queryset = queryset.filter(
                        booking__invoices__property_cache__payment_status__iexact=payment_status_filter
                    )
            if park and park.lower() != "all":
                queryset = queryset.filter(park_bookings__park__id=park)

            if search_text and super_queryset != None:
                queryset = queryset.distinct() & super_queryset

        elif queryset.model is DistrictProposal:

            processing_status = request.GET.get("datatable_filter_processing_status")

            if date_from:
                queryset = queryset.filter(proposal__lodgement_date__gte=date_from)

            if date_to:
                queryset = queryset.filter(proposal__lodgement_date__lte=date_to)

            if processing_status and processing_status.lower() != "all":
                queryset = queryset.filter(processing_status=processing_status)

            if search_text and super_queryset != None:
                search_queryset, results_found = district_proposal_search_filter(queryset, search_text)
                if results_found:
                    queryset = search_queryset.distinct() | super_queryset   
                else:
                    queryset = queryset.distinct() & super_queryset 

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        setattr(view, "_datatables_total_count", total_count)

        return queryset


class ProposalPaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ProposalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    queryset = Proposal.objects.none()
    serializer_class = ListProposalSerializer
    page_size = 10

    @property
    def excluded_type(self):
        try:
            return ApplicationType.objects.get(name="E Class")
        except:
            return ApplicationType.objects.none()
        
    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            qs = Proposal.objects.all().exclude(application_type=self.excluded_type)
            return qs.exclude(migrated=True)
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            user_id = user.id
            queryset = Proposal.objects.filter(
                Q(org_applicant_id__in=user_orgs) | Q(submitter_id=user_id)
            ).exclude(migrated=True)

            return queryset.exclude(application_type=self.excluded_type)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    def proposals_internal(self, request, *args, **kwargs):
        """
        Internal dashboard endpoint (DataTables server-side).
        """
        if not is_internal(request):
            return Response([])

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListProposalSerializer(
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
    def referrals_internal(self, request, *args, **kwargs):
        """
        Used by the internal dashboard
        """
        self.serializer_class = ReferralSerializer

        request_user_id = request.user.id
        # Query the through-table on the existing m2m field with `emailuser`, rather than using the set with (now) `emailuserro`
        request_user_referralrecipientgroup_set = retrieve_user_groups(
            "ReferralRecipientGroup", request_user_id
        )

        qs = Referral.objects.filter(
                referral_group__in=request_user_referralrecipientgroup_set
            ) if is_internal(self.request) else Referral.objects.none()
        
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = DTReferralSerializer(
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
    def qaofficer_info(self, request, *args, **kwargs):
        """
        Used by the internal dashboard

        http://localhost:8499/api/proposal_paginated/qaofficer_internal/?format=datatables&draw=1&length=2
        """

        qaofficergroup_set = retrieve_group_members(
            QAOfficerGroup.objects.filter(default=True)
        )

        qa_officers = EmailUser.objects.filter(
            id__in=[id for id in qaofficergroup_set]
        ).values_list("email", flat=True)

        if request.user.email in qa_officers:
            return Response({"QA_Officer": True})
        else:
            return Response({"QA_Officer": False})

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    def qaofficer_internal(self, request, *args, **kwargs):
        """
        Used by the internal dashboard

        http://localhost:8499/api/proposal_paginated/qaofficer_internal/?format=datatables&draw=1&length=2
        """
        qaofficergroup_set = retrieve_group_members(
            QAOfficerGroup.objects.filter(default=True)
        )

        qa_officers = EmailUser.objects.filter(
            id__in=[id for id in qaofficergroup_set]
        ).values_list("email", flat=True)

        if request.user.email not in qa_officers:
            return Response([])

        qs = self.get_queryset()
        qs = qs.filter(qaofficer_referrals__gt=0)
        qs = self.filter_queryset(qs)

        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        applicant_id = request.GET.get("org_id")
        if applicant_id:
            qs = qs.filter(org_applicant_id=applicant_id)
        submitter_id = request.GET.get("submitter_id", None)
        if submitter_id:
            qs = qs.filter(submitter_id=submitter_id)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListProposalSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def proposals_external(self, request, *args, **kwargs):
        """
        Used by the external dashboard
        """
        qs = self.get_queryset().exclude(processing_status="discarded")
        qs = self.filter_queryset(qs)

        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        applicant_id = request.GET.get("org_id")
        if applicant_id:
            qs = qs.filter(org_applicant_id=applicant_id)
        submitter_id = request.GET.get("submitter_id", None)
        if submitter_id:
            qs = qs.filter(submitter_id=submitter_id)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListProposalSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)


class ProposalParkViewSet(mixins.ListModelMixin, viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """
    Similar to ProposalViewSet, except get_queryset include migrated_licences
    """

    queryset = Proposal.objects.none()
    serializer_class = ProposalSerializer
    lookup_field = "id"

    @property
    def excluded_type(self):
        try:
            return ApplicationType.objects.get(name="E Class")
        except:
            return ApplicationType.objects.none()

    def get_queryset(self):
        """
        Now excludes parks with free admission
        """
        user = self.request.user
        if is_internal(self.request):
            qs = Proposal.objects.all().exclude(application_type=self.excluded_type)
            return qs
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            queryset = Proposal.objects.filter(
                Q(org_applicant_id__in=user_orgs) | Q(submitter_id=user.id)
            )
            return queryset.exclude(application_type=self.excluded_type)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def proposal_parks(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProposalParkSerializer(instance, context={"request": request})
        return Response(serializer.data)


class ProposalViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Proposal.objects.none()
    serializer_class = ProposalSerializer
    lookup_field = "id"

    @property
    def excluded_type(self):
        try:
            return ApplicationType.objects.get(name="E Class")
        except:
            return ApplicationType.objects.none()

    def get_queryset(self):
        user = self.request.user

        if is_internal(self.request):
            qs = Proposal.objects.all().exclude(application_type=self.excluded_type)
            return qs.exclude(migrated=True)
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            user_id = user.id
            queryset = Proposal.objects.filter(
                Q(org_applicant_id__in=user_orgs) | Q(submitter_id=user_id)
            ).exclude(migrated=True)

            return queryset.exclude(application_type=self.excluded_type)

    def get_serializer_class(self):
        try:
            application_type = Proposal.objects.get(
                id=self.kwargs.get("id")
            ).application_type.name
            if application_type == ApplicationType.TCLASS:
                return ProposalSerializer
            elif application_type == ApplicationType.FILMING:
                return ProposalFilmingSerializer
            elif application_type == ApplicationType.EVENT:
                return ProposalEventSerializer
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

    def internal_serializer_class(self):
        try:
            application_type = Proposal.objects.get(
                id=self.kwargs.get("id")
            ).application_type.name
            if application_type == ApplicationType.TCLASS:
                return InternalProposalSerializer
            elif application_type == ApplicationType.FILMING:
                return InternalFilmingProposalSerializer
            elif application_type == ApplicationType.EVENT:
                return InternalEventProposalSerializer
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
        detail=False,
    )
    def filter_list(self, request, *args, **kwargs):
        """Used by the internal/external dashboard filters"""

        application_types = ApplicationType.objects.all().values_list("name", flat=True)
        data = dict(
            application_types=application_types,
        )
        return Response(data)


    @action(methods=["POST"], detail=True)
    @renderer_classes((JSONRenderer,))
    def process_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            action = request.POST.get("action")
            section = request.POST.get("input_name")
            
            if user_can_edit(request,instance):
                if action == "delete" and "document_id" in request.POST:
                    document_id = request.POST.get("document_id")
                    document = instance.documents.get(id=document_id)

                    if (
                        document._file
                        and os.path.isfile(document._file.path)
                        and document.can_delete
                    ):
                        os.remove(document._file.path)

                    document.delete()
                    instance.save(
                        version_comment="Approval File Deleted: {}".format(document.name)
                    )  # to allow revision to be added to reversion history

                elif action == "hide" and "document_id" in request.POST:
                    document_id = request.POST.get("document_id")
                    document = instance.documents.get(id=document_id)

                    document.hidden = True
                    document.save()
                    instance.save(
                        version_comment="File hidden: {}".format(document.name)
                    )  # to allow revision to be added to reversion history

                elif (
                    action == "save"
                    and "input_name" in request.POST
                    and "filename" in request.POST
                ):
                    proposal_id = request.POST.get("proposal_id")

                    filename = request.data.get('filename')
                    _file = request.data.get('_file')

                    document = instance.documents.get_or_create(
                        input_name=section, name=filename
                    )[0]

                    document.save(
                        path_to_file="{}/proposals/{}/documents/".format(
                            settings.MEDIA_APP_DIR, proposal_id
                        ),
                        storage=private_storage,
                        file_content=_file
                    )

                    instance.save(
                        version_comment="File Added: {}".format(filename)
                    )  # to allow revision to be added to reversion history

            return Response(
                [
                    dict(
                        input_name=d.input_name,
                        name=d.name,
                        file=d._file.url,
                        id=d.id,
                        can_delete=d.can_delete,
                        can_hide=d.can_hide,
                    )
                    for d in instance.documents.filter(input_name=section, hidden=False)
                    if d._file
                ]
            )

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

    @action(methods=["POST"], detail=True, permission_classes=[ProposalAssessorPermission])
    @renderer_classes((JSONRenderer,))
    def process_onhold_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            action = request.POST.get("action")
            section = request.POST.get("input_name")

            if action == "delete" and "document_id" in request.POST:
                document_id = request.POST.get("document_id")
                document = instance.onhold_documents.get(id=document_id)

                document.visible = False
                document.save()
                instance.save(
                    version_comment="OnHold File Hidden: {}".format(document.name)
                )  # to allow revision to be added to reversion history

            elif (
                action == "save"
                and "input_name" in request.POST
                and "filename" in request.POST
            ):
                proposal_id = request.POST.get("proposal_id")
                filename = request.POST.get("filename")
                _file = request.POST.get("_file")
                if not _file:
                    _file = request.FILES.get("_file")


                document = instance.onhold_documents.get_or_create(
                    input_name=section, name=filename
                )[0]
                document.save(
                    path_to_file="{}/proposals/{}/onhold/".format(
                        settings.MEDIA_APP_DIR, proposal_id
                    ),
                    storage=private_storage,
                    file_content=_file
                )

                instance.save(
                    version_comment="On Hold File Added: {}".format(filename)
                )  # to allow revision to be added to reversion history

            return Response(
                [
                    dict(
                        input_name=d.input_name,
                        name=d.name,
                        file=d._file.url,
                        id=d.id,
                        can_delete=d.can_delete,
                    )
                    for d in instance.onhold_documents.filter(
                        input_name=section, visible=True
                    )
                    if d._file
                ]
            )

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

    @action(methods=["POST"], detail=True, permission_classes=[QAOfficerPermission])
    @renderer_classes((JSONRenderer,))
    def process_qaofficer_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            action = request.POST.get("action")
            section = request.POST.get("input_name")
            if action == "list" and "input_name" in request.POST:
                pass

            elif action == "delete" and "document_id" in request.POST:
                document_id = request.POST.get("document_id")
                document = instance.qaofficer_documents.get(id=document_id)

                document.visible = False
                document.save()
                instance.save(
                    version_comment="QA Officer File Hidden: {}".format(document.name)
                )  # to allow revision to be added to reversion history

            elif (
                action == "save"
                and "input_name" in request.POST
                and "filename" in request.POST
            ):
                proposal_id = request.POST.get("proposal_id")
                filename = request.POST.get("filename")
                _file = request.POST.get("_file")
                if not _file:
                    _file = request.FILES.get("_file")

                document = instance.qaofficer_documents.get_or_create(
                    input_name=section, name=filename
                )[0]

                document.save(
                    path_to_file="{}/proposals/{}/qaofficer/".format(
                        settings.MEDIA_APP_DIR, proposal_id
                    ),
                    storage=private_storage,
                    file_content=_file
                )

                instance.save(
                    version_comment="QA Officer File Added: {}".format(filename)
                )  # to allow revision to be added to reversion history

            return Response(
                [
                    dict(
                        input_name=d.input_name,
                        name=d.name,
                        file=d._file.url,
                        id=d.id,
                        can_delete=d.can_delete,
                    )
                    for d in instance.qaofficer_documents.filter(
                        input_name=section, visible=True
                    )
                    if d._file
                ]
            )

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
            serializer = ProposalUserActionSerializer(qs, many=True)
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
            serializer = ProposalLogEntrySerializer(qs, many=True)
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
                request.data["proposal"] = "{}".format(instance.id)
                request.data["staff"] = "{}".format(request.user.id)
                request.data._mutable = mutable
                serializer = ProposalLogEntrySerializer(data=request.data)
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

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def requirements(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.requirements.all().exclude(is_deleted=True)
            qs = qs.order_by("order")
            serializer = ProposalRequirementSerializer(
                qs, many=True, context={"request": request}
            )
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
            serializer = AmendmentRequestDisplaySerializer(qs, many=True)
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
    def vehicles(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.vehicles
            serializer = VehicleSerializer(qs, many=True)
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
    def vessels(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.vessels
            serializer = VesselSerializer(qs, many=True)
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
    def filming_parks(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.filming_parks
            serializer = ProposalFilmingParksSerializer(
                qs, many=True, context={"request": request}
            )
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
    def events_parks(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.events_parks
            serializer = ProposalEventsParksSerializer(qs, many=True)
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
    def events_trails(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.events_trails
            serializer = ProposalEventsTrailsSerializer(qs, many=True)
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
    def pre_event_parks(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.pre_event_parks
            serializer = ProposalPreEventsParksSerializer(qs, many=True)
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
    def abseiling_climbing_activities(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.event_abseiling_climbing_activity.all()
            serializer = AbseilingClimbingActivitySerializer(qs, many=True)
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
    @basic_exception_handler
    def district_proposals(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.district_proposals.all()
        serializer = ListDistrictProposalSerializer(
            qs, context={"request": request}, many=True
        )
        return Response(serializer.data)


    # Documents on Activities(land)and Activities(Marine) tab for T-Class related to required document questions
    @action(methods=["POST"], detail=True)
    @renderer_classes((JSONRenderer,))
    def process_required_document(self, request, *args, **kwargs):
        try:

            instance = self.get_object()
            
            instance = self.get_object()
            action = request.POST.get("action")
            section = request.POST.get("input_name")
            required_doc_id = request.POST.get("required_doc_id")

            if user_can_edit(request,instance):
                if action == "delete" and "document_id" in request.POST:
                    document_id = request.POST.get("document_id")
                    document = instance.required_documents.get(id=document_id)

                    if (
                        document._file
                        and os.path.isfile(document._file.path)
                        and document.can_delete
                    ):
                        os.remove(document._file.path)

                    document.delete()
                    instance.save(
                        version_comment="Required document File Deleted: {}".format(
                            document.name
                        )
                    )  # to allow revision to be added to reversion history
                    # instance.current_proposal.save(version_comment='File Deleted: {}'.format(document.name)) # to allow revision to be added to reversion history

                elif action == "hide" and "document_id" in request.POST:
                    document_id = request.POST.get("document_id")
                    document = instance.required_documents.get(id=document_id)

                    document.hidden = True
                    document.save()
                    instance.save(
                        version_comment="File hidden: {}".format(document.name)
                    )  # to allow revision to be added to reversion history

                elif (
                    action == "save"
                    and "input_name"
                    and "required_doc_id" in request.POST
                    and "filename" in request.POST
                ):
                    proposal_id = request.POST.get("proposal_id")
                    filename = request.POST.get("filename")
                    _file = request.POST.get("_file")
                    if not _file:
                        _file = request.FILES.get("_file")

                    required_doc_instance = RequiredDocument.objects.get(id=required_doc_id)
                    document = instance.required_documents.get_or_create(
                        input_name=section,
                        name=filename,
                        required_doc=required_doc_instance,
                    )[0]

                    document.save(
                        path_to_file="{}/proposals/{}/required_documents/".format(
                            settings.MEDIA_APP_DIR, proposal_id
                        ),
                        storage=private_storage,
                        file_content=_file
                    )
                    
                    instance.save(
                        version_comment="File Added: {}".format(filename)
                    )  # to allow revision to be added to reversion history
                    # instance.current_proposal.save(version_comment='File Added: {}'.format(filename)) # to allow revision to be added to reversion history

            return Response(
                [
                    dict(
                        input_name=d.input_name,
                        name=d.name,
                        file=d._file.url,
                        id=d.id,
                        can_delete=d.can_delete,
                        can_hide=d.can_hide,
                    )
                    for d in instance.required_documents.filter(
                        required_doc=required_doc_id, hidden=False
                    )
                    if d._file
                ]
            )

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
    )
    # @renderer_classes((JSONRenderer,))
    def parks_and_trails(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ParksAndTrailSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def internal_proposal(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = get_proposal_serializer_by_application_type(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    @basic_exception_handler
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        instance = self.get_object()
        if not user_can_edit(request,instance):
            raise PermissionDenied
        proposal_submit(instance, request)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission, ProposalApproverPermission]
    )
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request, request.user)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalAssessorPermission, ProposalApproverPermission]
    )
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get("assessor_id", None)
            user = None
            if not user_id:
                raise serializers.ValidationError("An assessor id is required")
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    "A user with the id passed in does not exist"
                )
            instance.assign_officer(request, user)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalAssessorPermission, ProposalApproverPermission]
    )
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[InternalPermission] #auth group membership changing status handled by model func
    )
    def switch_status(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get("status")
            approver_comment = request.data.get("approver_comment")
            if not status:
                raise serializers.ValidationError("Status is required")
            else:
                if not status in [
                    "with_assessor",
                    "with_assessor_requirements",
                    "with_approver",
                ]:
                    raise serializers.ValidationError(
                        "The status provided is not allowed"
                    )
            instance.move_to_status(request, status, approver_comment)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalAssessorPermission] 
    )
    def reissue_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get("status")
            if not status:
                raise serializers.ValidationError("Status is required")
            else:
                if (
                    instance.application_type.name == ApplicationType.FILMING
                    and instance.filming_approval_type == "lawful_authority"
                ):
                    status = "with_assessor"
                else:
                    if not status in ["with_approver"]:
                        raise serializers.ValidationError(
                            "The status provided is not allowed"
                        )
            instance.reissue_approval(request, status)
            serializer = InternalProposalSerializer(
                instance, context={"request": request}
            )
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
    )
    def renew_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.renew_approval(request)
            serializer = SaveProposalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            if hasattr(e, "message"):
                raise serializers.ValidationError(e.message)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def amend_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.amend_approval(request)
            serializer = SaveProposalSerializer(instance, context={"request": request})
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            if hasattr(e, "message"):
                raise serializers.ValidationError(e.message)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    def proposed_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_approval(request, serializer.validated_data)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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

    #TODO it is unclear if this endpoint is used or not - consider removal (has been set internal for now)
    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def approval_level_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.passing_approval_level_document(request)
            serializer = InternalProposalSerializer(
                instance, context={"request": request}
            )
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
        permission_classes=[ProposalApproverPermission]
    )
    def final_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_approval(request, serializer.validated_data)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalAssessorPermission]
    )
    def proposed_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_decline(request, serializer.validated_data)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalApproverPermission]
    )
    def final_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_decline(request, serializer.validated_data)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[ProposalAssessorPermission]
    )
    @renderer_classes((JSONRenderer,))
    def on_hold(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                is_onhold = eval(request.data.get("onhold"))
                data = {}
                if is_onhold:
                    data["type"] = "onhold"
                    instance.on_hold(request)
                else:
                    data["type"] = "onhold_remove"
                    instance.on_hold_remove(request)

                data["proposal"] = "{}".format(instance.id)
                data["staff"] = "{}".format(request.user.id)
                data["text"] = request.user.get_full_name() + ": {}".format(
                    request.data["text"]
                )
                data["subject"] = request.user.get_full_name() + ": {}".format(
                    request.data["text"]
                )
                serializer = ProposalLogEntrySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()

                # save the files
                documents_qs = instance.onhold_documents.filter(
                    input_name="on_hold_file", visible=True
                )
                for f in documents_qs:
                    document = comms.documents.create(_file=f._file, name=f.name)
                    # document = comms.documents.create()
                    # document.name = f.name
                    # document._file = f._file #.strip('/media')
                    document.input_name = f.input_name
                    document.can_delete = True
                    document.save()
                # end save documents

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
        permission_classes=[ProposalAssessorPermission, QAOfficerPermission]
    )
    @renderer_classes((JSONRenderer,))
    def with_qaofficer(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                is_with_qaofficer = eval(request.data.get("with_qaofficer"))
                data = {}
                if is_with_qaofficer:
                    data["type"] = "with_qaofficer"
                    instance.with_qaofficer(request)
                else:
                    data["type"] = "with_qaofficer_completed"
                    instance.with_qaofficer_completed(request)

                data["proposal"] = "{}".format(instance.id)
                data["staff"] = "{}".format(request.user.id)
                data["text"] = request.user.get_full_name() + ": {}".format(
                    request.data["text"]
                )
                data["subject"] = request.user.get_full_name() + ": {}".format(
                    request.data["text"]
                )
                serializer = ProposalLogEntrySerializer(data=data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()

                # Save the files
                document_qs = []
                if is_with_qaofficer:
                    # Get the list of documents attached by assessor when sending application to QA officer
                    documents_qs = instance.qaofficer_documents.filter(
                        input_name="assessor_qa_file", visible=True
                    )
                else:
                    # Get the list of documents attached by QA officer when sending application back to assessor
                    documents_qs = instance.qaofficer_documents.filter(
                        input_name="qaofficer_file", visible=True
                    )
                for f in documents_qs:
                    document = comms.documents.create(_file=f._file, name=f.name)
                    # document = comms.documents.create()
                    # document.name = f.name
                    # document._file = f._file #.strip('/media')
                    document.input_name = f.input_name
                    document.can_delete = True
                    document.save()
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

    @action(methods=["post"], detail=True, permission_classes=[ProposalAssessorPermission])
    @basic_exception_handler
    def assesor_send_referral(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = SendReferralSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.send_referral(
            request,
            serializer.validated_data["email_group"],
            serializer.validated_data["text"],
        )
        serializer = InternalProposalSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(methods=["post"], detail=True)
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    def draft(self, request, *args, **kwargs):
        instance = self.get_object()

        if not user_can_edit(request, instance):
            raise PermissionDenied

        save_proponent_data(instance, request, self)

        serializer = get_proposal_serializer_by_application_type(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    #TODO the training is entirely assessed client-side and endpoint can be used to bypass it - lower priority security item but must be addressed eventually
    @action(methods=["post"], detail=True)
    def update_training_flag(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            today = timezone.now().date()
            if request.data.get("training_completed"):
                instance.training_completed = True
                instance.save()
                if instance.application_type.name == ApplicationType.EVENT:
                    if instance.org_applicant:
                        instance.org_applicant.event_training_completed = True
                        instance.org_applicant.event_training_date = today
                        instance.org_applicant.save()
                    elif instance.proxy_applicant:
                        instance.proxy_applicant.system_settings.event_training_completed = (
                            True
                        )
                        instance.proxy_applicant.system_settings.event_training_date = (
                            today
                        )
                        instance.proxy_applicant.system_settings.save()
                    else:
                        instance.submitter.system_settings.event_training_completed = (
                            True
                        )
                        instance.submitter.system_settings.event_training_date = today
                        instance.submitter.system_settings.save()
            return Response({"training_completed": True})
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

    @action(methods=["post"], detail=True, permission_classes=[ProposalAssessorPermission])
    def send_to_districts(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.send_to_districts(request)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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

    @action(methods=["post"], detail=True, permission_classes=[ProposalAssessorPermission])
    def send_to_kensington(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.send_to_kensington(request)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
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

    @action(methods=["post"], detail=True, permission_classes=[ProposalAssessorPermission])
    @renderer_classes((JSONRenderer,))
    def assessor_save(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            save_assessor_data(instance, request, self)
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance, context={"request": request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            application_type = request.data.get("application")
            region = request.data.get("region")
            district = request.data.get("district")
            activity = request.data.get("activity")
            sub_activity1 = request.data.get("sub_activity1")
            sub_activity2 = request.data.get("sub_activity2")
            category = request.data.get("category")
            approval_level = request.data.get("approval_level")
            selected_copy_from = request.data.get("selected_copy_from", None)

            application_name = ApplicationType.objects.get(id=application_type).name
            # Get most recent versions of the Proposal Types
            qs_proposal_type = (
                ProposalType.objects.all().order_by("name", "-version").distinct("name")
            )
            proposal_type = qs_proposal_type.get(name=application_name)

            if application_name == ApplicationType.EVENT and selected_copy_from:
                copy_from_proposal = Proposal.objects.get(id=selected_copy_from)
                instance = copy_from_proposal.reapply_event(request)

            else:
                data = {
                    "schema": proposal_type.schema,
                    "submitter": request.user.id,
                    "org_applicant": request.data.get("org_applicant"),
                    "application_type": application_type,
                    "region": region,
                    "district": district,
                    "activity": activity,
                    "approval_level": approval_level,
                    "data": [
                        {
                            "regionActivitySection": [
                                {
                                    "Region": (
                                        Region.objects.get(id=region).name
                                        if region
                                        else None
                                    ),
                                    "District": (
                                        District.objects.get(id=district).name
                                        if district
                                        else None
                                    ),
                                    #'Tenure': Tenure.objects.get(id=tenure).name if tenure else None,
                                    #'ApplicationType': ApplicationType.objects.get(id=application_type).name
                                    "ActivityType": activity,
                                    "Sub-activity level 1": sub_activity1,
                                    "Sub-activity level 2": sub_activity2,
                                    "Management area": category,
                                }
                            ]
                        }
                    ],
                }
                serializer = SaveProposalSerializer(data=data)
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                # Create ProposalOtherDetails instance for T Class/Filming/Event licence
                if application_name == ApplicationType.TCLASS:
                    other_details_data = {"proposal": instance.id}
                    serializer = SaveProposalOtherDetailsSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif application_name == ApplicationType.FILMING:
                    other_details_data = {"proposal": instance.id}
                    # serializer=SaveProposalOtherDetailsFilmingSerializer(data=other_details_data)
                    serializer = ProposalFilmingActivitySerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    serializer = ProposalFilmingAccessSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    serializer = ProposalFilmingEquipmentSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    serializer = ProposalFilmingOtherDetailsSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                elif application_name == ApplicationType.EVENT:
                    other_details_data = {"proposal": instance.id}
                    serializer = ProposalEventOtherDetailsSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    serializer = ProposalEventActivitiesSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    serializer = ProposalEventVehiclesVesselsSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    serializer = ProposalEventManagementSerializer(
                        data=other_details_data
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

            serializer = SaveProposalSerializer(instance)
            return Response(serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            if not user_can_edit(request, instance):
                raise PermissionDenied
            
            http_status = status.HTTP_200_OK
            serializer = SaveProposalSerializer(
                instance,
                {"processing_status": "discarded", "previous_application": None},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=http_status)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ReferralViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Referral.objects.none()
    serializer_class = ReferralSerializer
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and is_internal(self.request):
            queryset = Referral.objects.all()
            return queryset
        return Referral.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def filter_list(self, request, *args, **kwargs):
        """Used by the external dashboard filters"""

        qs = self.get_queryset()
        qs = Proposal.objects.filter(
            id__in=qs.filter(proposal__submitter_id__isnull=False).values_list(
                "proposal_id", flat=True
            )
        )
        processing_status = get_proposal_processing_status()
        application_types = ApplicationType.objects.all().values_list("name", flat=True)
        data = dict(
            processing_status_choices=processing_status,
            application_types=application_types,
        )
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def user_group_list(self, request, *args, **kwargs):
        qs = ReferralRecipientGroup.objects.filter().values_list("name", flat=True)
        return Response(qs)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def datatable_list(self, request, *args, **kwargs):
        proposal = request.GET.get("proposal", None)
        qs = self.get_queryset().all()
        if proposal:
            qs = qs.filter(proposal_id=int(proposal))
        serializer = DTReferralSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def referral_list(self, request, *args, **kwargs):
        instance = self.get_object()

        request_user_id = request.user.id
        # Query the through-table on the existing m2m field with `emailuser`, rather than using the set with (now) `emailuserro`
        request_user_referralrecipientgroup_set = retrieve_user_groups(
            "ReferralRecipientGroup", request_user_id
        )

        qs = Referral.objects.filter(
            referral_group__in=request_user_referralrecipientgroup_set,
            proposal=instance.proposal,
        )
        serializer = DTReferralSerializer(qs, context={"request": request}, many=True)

        return Response(serializer.data)

    @action(methods=["GET", "POST"], detail=True, permission_classes=[ReferrerPermission])
    @basic_exception_handler
    def complete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.complete(request)
        data = {}
        data["type"] = "referral_complete"
        data["fromm"] = "{}".format(instance.referral_group.name)
        data["proposal"] = "{}".format(instance.proposal.id)
        data["staff"] = "{}".format(request.user.id)
        data["text"] = "{}".format(instance.referral_text)
        data["subject"] = "{}".format(instance.referral_text)
        serializer = ProposalLogEntrySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        comms = serializer.save()
        if instance.document:
            document = comms.documents.create(
                _file=instance.document._file, name=instance.document.name
            )
            document.input_name = instance.document.input_name
            document.can_delete = True
            document.save()

        serializer = self.get_serializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    @basic_exception_handler
    def remind(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.remind(request)
        serializer = get_proposal_serializer_by_application_type(
            instance.proposal, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    @basic_exception_handler
    def recall(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.recall(request)
        serializer = get_proposal_serializer_by_application_type(
            instance.proposal, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    @basic_exception_handler
    def resend(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.resend(request)
        serializer = get_proposal_serializer_by_application_type(
            instance.proposal, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ReferrerPermission]
    )
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request, request.user)
            serializer = self.get_serializer(instance, context={"request": request})
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
        permission_classes=[ReferrerPermission]
    )
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get("user_id", None)
            user = None
            if not user_id:
                raise serializers.ValidationError("An assessor id is required")
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    "A user with the id passed in does not exist"
                )
            instance.assign_officer(request, user)
            serializer = self.get_serializer(instance, context={"request": request})
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
        permission_classes=[ReferrerPermission]
    )
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            serializer = self.get_serializer(instance, context={"request": request})
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


class ProposalRequirementViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = ProposalRequirement.objects.none()
    serializer_class = ProposalRequirementSerializer
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return ProposalRequirement.objects.exclude(is_deleted=True)
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            qs = ProposalRequirement.objects.exclude(is_deleted=True).filter(
                Q(proposal_id__org_applicant_id__in=user_orgs)
                | Q(proposal_id__submitter_id=user.id)
            )
            return qs

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[ProposalAssessorPermission]
    )
    @basic_exception_handler
    def move_up(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.up()
            instance.save()
            serializer = self.get_serializer(instance)
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
    @basic_exception_handler
    def move_down(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.down()
            instance.save()
            serializer = self.get_serializer(instance)
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
    @basic_exception_handler
    def discard(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_deleted = True
            instance.save()
            serializer = self.get_serializer(instance)
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
        permission_classes=[ProposalAssessorPermission]
    )
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            RequirementDocument.objects.get(id=request.data.get("id")).delete()
            return Response(
                [
                    dict(id=i.id, name=i.name, _file=i._file.url)
                    for i in instance.requirement_documents.all()
                ]
            )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @basic_exception_handler
    def update(self, request, *args, **kwargs):
        try:
            if is_assessor(request):
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=json.loads(request.data.get("data"))
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                instance.add_documents(request)
                return Response(serializer.data)
            else:
                raise PermissionDenied
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @basic_exception_handler
    def create(self, request, *args, **kwargs):
        try:
            if is_assessor(request):
                serializer = self.get_serializer(data=json.loads(request.data.get("data")))
                serializer.is_valid(raise_exception=True)
                instance = serializer.save()
                instance.add_documents(request)
                return Response(serializer.data)
            else:
                raise PermissionDenied
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


class ProposalStandardRequirementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProposalStandardRequirement.objects.none()
    serializer_class = ProposalStandardRequirementSerializer
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ProposalStandardRequirement.objects.all()
        return ProposalStandardRequirement.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        search = request.GET.get("search")
        if search:
            queryset = queryset.filter(text__icontains=search)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AmendmentRequestViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = AmendmentRequest.objects.none()
    serializer_class = AmendmentRequestSerializer
    permission_classes = [ProposalAssessorPermission]

    def get_queryset(self):
        if is_internal(self.request):
            return AmendmentRequest.objects.all()
        return AmendmentRequest.objects.none()

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
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class AccreditationTypeView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        choices_list = cache.get(settings.CACHE_KEY_ACCREDITATION_CHOICES)

        if choices_list is None:
            choices_list = []
            choices = ProposalAccreditation.ACCREDITATION_TYPE_CHOICES
            if choices:
                for c in choices:
                    choices_list.append({"key": c[0], "value": c[1]})

            cache.set(
                settings.CACHE_KEY_ACCREDITATION_CHOICES,
                choices_list,
                settings.CACHE_TIMEOUT_24_HOURS,
            )

        return Response(choices_list)

class TourismStandardsView(views.APIView):

    renderer_classes = [JSONRenderer,]
    def get(self,request, format=None):
        information_standard_choices = []
        emission_standard_choices = []
        emission_choices = ProposalEmissionStandard.EMISSION_STANDARD_TYPE_CHOICES
        if emission_choices:
            for c in emission_choices:
                emission_standard_choices.append({'key': c[0],'value': c[1]})
        #choices = ProposalOtherDetails.ACCREDITATION_TYPE_CHOICES
        information_choices=ProposalInformationStandard.INFORMATION_STANDARD_TYPE_CHOICES
        if information_choices:
            for c in information_choices:
                information_standard_choices.append({'key': c[0],'value': c[1]})
        choices_list = {
            'information_standard_choices': information_standard_choices,
            'emission_standard_choices': emission_standard_choices,
        }
        return Response(choices_list)



class LicencePeriodChoicesView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        choices_list = cache.get(settings.CACHE_KEY_LICENCE_PERIOD_CHOICES)

        if choices_list is None:
            choices_list = []
            choices = LicencePeriod.LICENCE_PERIOD_CHOICES
            if choices:
                for c in choices:
                    choices_list.append({"key": c[0], "value": c[1]})

            cache.set(
                settings.CACHE_KEY_LICENCE_PERIOD_CHOICES,
                choices_list,
                settings.CACHE_TIMEOUT_24_HOURS,
            )
        return Response(choices_list)


class AmendmentRequestReasonChoicesView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        choices_list = cache.get(settings.CACHE_KEY_AMENDMENT_REQUEST_REASON_CHOICES)
        if choices_list is None:
            choices_list = []
            choices = AmendmentReason.objects.all()

            if choices:
                for c in choices:
                    choices_list.append({"key": c.id, "value": c.reason})

            cache.set(
                settings.CACHE_KEY_AMENDMENT_REQUEST_REASON_CHOICES,
                choices_list,
                settings.CACHE_TIMEOUT_24_HOURS,
            )
        return Response(choices_list)


class FilmingLicenceChargeView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        choices_list = cache.get(settings.CACHE_KEY_FILMING_LICENCE_CHARGE_CHOICES)

        if choices_list is None:
            choices_list = []
            choices = Proposal.FILMING_LICENCE_CHARGE_CHOICES
            if choices:
                for c in choices:
                    choices_list.append({"key": c[0], "value": c[1]})

            cache.set(
                settings.CACHE_KEY_FILMING_LICENCE_CHARGE_CHOICES,
                choices_list,
                settings.CACHE_TIMEOUT_24_HOURS,
            )

        return Response(choices_list)


class SearchKeywordsView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]
    permission_classes=[InternalPermission]

    def post(self, request, format=None):
        qs = []
        searchWords = request.data.get("searchKeywords")
        searchProposal = request.data.get("searchProposal")
        searchApproval = request.data.get("searchApproval")
        searchCompliance = request.data.get("searchCompliance")
        if searchWords:
            qs = searchKeyWords(
                request, searchWords, searchProposal, searchApproval, searchCompliance
            )
        # queryset = list(set(qs))
        serializer = SearchKeywordSerializer(qs, many=True)
        return Response(serializer.data)


class SearchProposalsFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """

    def filter_queryset(self, request, queryset, view):
        searchWords = json.loads(request.GET.get("searchKeywords"))
        searchProposal = json.loads(request.GET.get("searchProposal"))
        searchApproval = json.loads(request.GET.get("searchApproval"))
        searchCompliance = json.loads(request.GET.get("searchCompliance"))

        fields = self.get_fields(request)
        ordering = self.get_ordering(request, view, fields)

        proposal_list, approval_list, compliance_list = get_chained_list(
            view,
            searchWords,
            searchProposal,
            searchApproval,
            searchCompliance,
            is_internal=True,
        )
        chained_qs = QuerySetChain(proposal_list, approval_list, compliance_list)
        chained_qs.order_by(*ordering)

        setattr(view, "_datatables_total_count", chained_qs.count())
        return chained_qs


class SearchProposalsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Proposal.objects.none()
    serializer_class = SearchKeywordSerializer
    filter_backends = (SearchProposalsFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    permission_classes=[InternalPermission]
    
    def get_queryset(self):
        qs = super().get_queryset()

        return qs

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def search_keywords(self, request, *args, **kwargs):
        qs = self.get_queryset()
        searchWords = json.loads(request.GET.get("searchKeywords"))
        chained_qs = self.filter_queryset(qs)
        result_page = paginate_chained_list(self, request, chained_qs, searchWords)
        serializer = SearchKeywordSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)


class SearchReferenceView(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]
    permission_classes=[InternalPermission]

    def post(self, request, format=None):
        try:
            qs = []
            reference_number = request.data.get("reference_number")
            if reference_number:
                qs = search_reference(reference_number)
            # queryset = list(set(qs))
            serializer = SearchReferenceSerializer(qs)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                print(e)
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class VehicleViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Vehicle.objects.none()
    serializer_class = VehicleSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Vehicle.objects.all().order_by("id")
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            qs = Vehicle.objects.filter(
                Q(proposal_id__org_applicant_id__in=user_orgs)
                | Q(proposal_id__submitter_id=user.id)
            ).order_by("id")
            return qs

    @action(methods=["post"], detail=True)
    @basic_exception_handler
    def edit_vehicle(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance.proposal or not user_can_edit(request, instance.proposal):
            raise PermissionDenied

        serializer = SaveVehicleSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance.proposal.log_user_action(
            ProposalUserAction.ACTION_EDIT_VEHICLE.format(instance.id), request.user
        )
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.proposal or not user_can_edit(request, instance.proposal):
            raise PermissionDenied
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @basic_exception_handler
    def create(self, request, *args, **kwargs):
        
        proposal = Proposal.objects.get(id=request.data["proposal"])
        if not proposal or not user_can_edit(request, proposal):
            raise PermissionDenied

        serializer = SaveVehicleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.proposal.log_user_action(
            ProposalUserAction.ACTION_CREATE_VEHICLE.format(instance.id), request.user
        )
        return Response(serializer.data)


class VesselViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Vessel.objects.none()
    serializer_class = VesselSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Vessel.objects.all().order_by("id")
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            qs = Vessel.objects.filter(
                Q(proposal_id__org_applicant_id__in=user_orgs)
                | Q(proposal_id__submitter_id=user.id)
            ).order_by("id")
            return qs

    @action(methods=["post"], detail=True)
    def edit_vessel(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if not instance.proposal or not user_can_edit(request, instance.proposal):
                raise PermissionDenied
            
            serializer = VesselSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.proposal.log_user_action(
                ProposalUserAction.ACTION_EDIT_VESSEL.format(instance.id), request.user
            )
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.proposal or not user_can_edit(request, instance.proposal):
            raise PermissionDenied
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        try:
            proposal = Proposal.objects.get(id=request.data["proposal"])
            if not proposal or not user_can_edit(request, proposal):
                raise PermissionDenied
            serializer = VesselSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            instance.proposal.log_user_action(
                ProposalUserAction.ACTION_CREATE_VESSEL.format(instance.id), request.user
            )
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

#TODO this does not actually appear to be in use - permissions set in case needed but this may just need to be removed
class ProposalAssessmentViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = ProposalAssessment.objects.none()
    serializer_class = ProposalAssessmentSerializer
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return ProposalAssessment.objects.all().order_by("id")
        else:
            user_orgs = retrieve_delegate_organisation_ids(user)
            qs = ProposalAssessment.objects.filter(
                Q(proposal_id__org_applicant_id__in=user_orgs)
                | Q(proposal_id__submitter_id=user.id)
            ).order_by("id")
            return qs

    @action(methods=["post"], detail=True, permission_classes=[ProposalAssessorPermission])
    def update_assessment(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data["submitter"] = request.user.id
            serializer = ProposalAssessmentSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            checklist = request.data["checklist"]
            if checklist:
                for chk in checklist:
                    try:
                        chk_instance = ProposalAssessmentAnswer.objects.get(
                            id=chk["id"]
                        )
                        serializer_chk = ProposalAssessmentAnswerSerializer(
                            chk_instance, data=chk
                        )
                        serializer_chk.is_valid(raise_exception=True)
                        serializer_chk.save()
                    except:
                        raise
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


class DistrictProposalViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = DistrictProposal.objects.none()
    serializer_class = DistrictProposalSerializer
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and is_internal(self.request):
            # queryset =  Referral.objects.filter(referral=user)
            queryset = DistrictProposal.objects.all()
            return queryset
        return DistrictProposal.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[DistrictProposalAssessorPermission, DistrictProposalApproverPermission]
    )
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request, request.user)
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[DistrictProposalAssessorPermission, DistrictProposalApproverPermission]
    )
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get("assessor_id", None)
            user = None
            if not user_id:
                raise serializers.ValidationError("An assessor id is required")
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    "A user with the id passed in does not exist"
                )
            instance.assign_officer(request, user)
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[DistrictProposalAssessorPermission, DistrictProposalApproverPermission]
    )
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
    def switch_status(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get("status")
            approver_comment = request.data.get("approver_comment")
            if not status:
                raise serializers.ValidationError("Status is required")
            else:
                if not status in [
                    "with_assessor",
                    "with_assessor_requirements",
                    "with_approver",
                ]:
                    raise serializers.ValidationError(
                        "The status provided is not allowed"
                    )
            instance.move_to_status(request, status, approver_comment)
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[DistrictProposalAssessorPermission]
    )
    def proposed_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_decline(request, serializer.validated_data)
            # serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[DistrictProposalApproverPermission]
    )
    def final_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_decline(request, serializer.validated_data)
            # serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        detail=False,
    )
    def filter_list(self, request, *args, **kwargs):
        """Used by the external dashboard filters"""

        qs = self.get_queryset()

        processing_status = get_district_proposal_processing_status()
        data = dict(
            processing_status_choices=processing_status,
        )
        return Response(data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[DistrictProposalAssessorPermission]
    )
    def proposed_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_approval(request, serializer.validated_data)
            # serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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
        permission_classes=[DistrictProposalApproverPermission]
    )
    def final_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_approval(request, serializer.validated_data)
            # serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = DistrictProposalSerializer
            serializer = serializer_class(instance, context={"request": request})
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


class DistrictProposalPaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ProposalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    queryset = DistrictProposal.objects.none()
    serializer_class = ListDistrictProposalSerializer
    page_size = 10
    permission_classes=[InternalPermission]

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):

            #TODO review and adjust this so it can work securely without the manager classes
            user_id = user.id
            user_assessor_groups = list(retrieve_user_groups(
                "districtproposalassessorgroup", user_id
            ).values_list("district",flat=True))

            user_approver_groups = list(retrieve_user_groups(
                "districtproposalapprovergroup", user_id
            ).values_list("district",flat=True))

            return (
                DistrictProposal.objects.filter(
                    Q(district_id__in=user_approver_groups)
                    | Q(district_id__in=user_assessor_groups)
                )
            )

        return DistrictProposal.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def district_proposals_internal(self, request, *args, **kwargs):
        """
        Used by the internal dashboard
        """
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = ListDistrictProposalSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)
