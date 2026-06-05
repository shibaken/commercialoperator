from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action as list_route

from commercialoperator.components.bookings.models import (
    Booking,
    ParkBooking,
    BookingInvoice,
)
from commercialoperator.components.bookings.serializers import (
    BookingSerializer,
    DTParkBookingSerializer,
    OverdueBookingInvoiceSerializer,
)
from commercialoperator.components.organisations.models import Organisation
from commercialoperator.components.segregation.utils import retrieve_delegate_organisation_ids
from commercialoperator.helpers import is_internal
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from commercialoperator.components.proposals.api import ProposalFilterBackend


class BookingPaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ProposalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    page_size = 10
    queryset = Booking.objects.none()
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Booking.objects.all().exclude(
                booking_type=Booking.BOOKING_TYPE_TEMPORARY
            )
        else:
            ledger_user_orgs = retrieve_delegate_organisation_ids(user)
            cols_org_ids = Organisation.objects.filter(
                organisation_id__in=ledger_user_orgs
            ).values_list("id", flat=True)

            return Booking.objects.filter(
                Q(proposal__org_applicant_id__in=cols_org_ids)
                | Q(proposal__submitter_id=user.id)
            ).exclude(booking_type=Booking.BOOKING_TYPE_TEMPORARY)

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def bookings_external(self, request, *args, **kwargs):
        """
        Paginated serializer for datatables - used by the internal and external dashboard (filtered by the get_queryset method)
        """

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = BookingSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)


class OverdueBookingInvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookingInvoice.objects.none()
    serializer_class = OverdueBookingInvoiceSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            bi = BookingInvoice.objects.exclude(
                booking__booking_type=Booking.BOOKING_TYPE_TEMPORARY
            ).filter(
                (Q(property_cache__payment_status="Unpaid")|Q(property_cache__payment_status="Partially Paid")) &
                Q(deferred_payment_date__lt=timezone.now().date())
            )

            return bi
        else:
            ledger_org_ids = retrieve_delegate_organisation_ids(user)
            cols_org_ids = Organisation.objects.filter(
                organisation_id__in=ledger_org_ids
            ).values_list("id", flat=True)

            bi = BookingInvoice.objects.filter(
                Q(booking__proposal__org_applicant_id__in=cols_org_ids)
                | Q(booking__proposal__submitter_id=user.id)
            ).exclude(booking__booking_type=Booking.BOOKING_TYPE_TEMPORARY).filter(
                (Q(property_cache__payment_status="Unpaid")|Q(property_cache__payment_status="Partially Paid")) &
                Q(deferred_payment_date__lt=timezone.now().date())
            )
            return bi


class ParkBookingPaginatedViewSet(viewsets.ReadOnlyModelViewSet):
    filter_backends = (ProposalFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    page_size = 10
    queryset = ParkBooking.objects.none()
    serializer_class = DTParkBookingSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return ParkBooking.objects.all().exclude(
                booking__booking_type=Booking.BOOKING_TYPE_TEMPORARY
            )
        else:
            user_orgs = [org.id for org in user.commercialoperator_organisations.all()]
            return ParkBooking.objects.filter(
                Q(booking__proposal__org_applicant_id__in=user_orgs)
                | Q(booking__proposal__submitter=user)
            ).exclude(booking__booking_type=Booking.BOOKING_TYPE_TEMPORARY)

    @list_route(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def park_bookings(self, request, *args, **kwargs):
        """
        Paginated serializer for datatables - used by the internal and external dashboard (filtered by the get_queryset method)
        """

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        result_page = self.paginator.paginate_queryset(qs, request)
        serializer = DTParkBookingSerializer(
            result_page, context={"request": request}, many=True
        )
        return self.paginator.get_paginated_response(serializer.data)
