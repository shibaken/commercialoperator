from django.contrib import admin
from commercialoperator.components.approvals import models
from reversion.admin import VersionAdmin

class ApprovalDocumentInline(admin.TabularInline):
    model = models.ApprovalDocument
    extra = 0

@admin.register(models.Approval)
class ApprovalAdmin(VersionAdmin):
    raw_id_fields = (
        "submitter",
        "org_applicant",
        "proxy_applicant",
        "licence_document",
        "cover_letter_document",
        "replaced_by",
        "renewal_document",
    )
    inlines = [
        ApprovalDocumentInline,
    ]
    list_display = ["id", "lodgement_number", "current_proposal__lodgement_number", "status", "applicant", "submitter"]
    search_fields = ["id", "lodgement_number", "status"]