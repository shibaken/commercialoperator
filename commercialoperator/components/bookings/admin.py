from django.contrib import admin
from commercialoperator.components.bookings import models

@admin.register(models.Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ["admission_number", "booking_type", "proposal__lodgement_number"]
    fields = (
        "booking_type",
        "admission_number",
    )
    readonly_fields = (
        "proposal",
    )
    search_fields = ["admission_number", "booking_type", "proposal__lodgement_number"]