from tabnanny import verbose
from django.contrib import admin
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from commercialoperator.components.organisations import models
from commercialoperator.components.organisations.forms import (
    OrganisationAccessGroupAdminForm,
)
from commercialoperator.components.segregation.models import OrganisationAccessGroupMembers


class UserDelegationAdminInline(admin.TabularInline):
    model = models.UserDelegation
    extra = 0
    raw_id_fields = ("user",)
    verbose_name = "User Delegation"
    verbose_name_plural = "User Delegations"


@admin.register(models.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = [
        "organisation_id",
        "admin_pin_one",
        "admin_pin_two",
        "user_pin_one",
        "user_pin_two",
    ]
    search_fields = (
        "organisation__name",
        "admin_pin_one",
        "admin_pin_two",
        "user_pin_one",
        "user_pin_two",
    )

    inlines = [UserDelegationAdminInline]


@admin.register(models.OrganisationRequest)
class OrganisationRequestAdmin(admin.ModelAdmin):
    list_display = ["name", "requester_id", "abn", "status"]
    search_fields= ["name", "abn", "status"]
    raw_id_fields = ["requester", "assigned_officer"]
    ordering = ["-lodgement_date"]


class OrganisationAccessGroupMembersInline(admin.TabularInline):
    model = OrganisationAccessGroupMembers
    extra = 0
    raw_id_fields = ["emailuser"]
    verbose_name = "Organisation Access Group Member"
    verbose_name_plural = "Organisation Access Group Members"


@admin.register(models.OrganisationAccessGroup)
class OrganisationAccessGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ("members",)
    form = OrganisationAccessGroupAdminForm
    exclude = ("site",)
    actions = None
    inlines = [OrganisationAccessGroupMembersInline]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "members":
            kwargs["queryset"] = EmailUser.objects.filter(is_staff=True)
        return super(OrganisationAccessGroupAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )

    def has_add_permission(self, request):
        return True if models.OrganisationAccessGroup.objects.count() == 0 else False

    def has_delete_permission(self, request, obj=None):
        return False
