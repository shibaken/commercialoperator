"""Replacement or substitute ("stub") models for ledger models, fields, or foreign keys
    that are not available anymore after segregating cols from the ledger database.
"""

from django.db import models

from commercialoperator.components.main.models import CommunicationsLogEntry, UserAction

from commercialoperator.components.main.mixins import SanitiseMixin

from ledger_api_client.ledger_models import EmailUserRO as EmailUser

from commercialoperator.components.segregation.utils import retrieve_email_user

import logging

logger = logging.getLogger(__name__)


class EmailUserLogEntryManager(models.Manager):
    def create(self, *args, **kwargs):
        logger.error("EmailUserLogEntry model does not exist during segregation")

        return False


class EmailUserLogEntry(CommunicationsLogEntry):
    objects = EmailUserLogEntryManager()

    emailuser = models.IntegerField()

    def __str__(self):
        return f"Email User ID: {self.email_user} - {self.subject}"

    class Meta:
        managed = False
        app_label = "commercialoperator"


class EmailUserAction(UserAction):
    email_user = models.IntegerField()

    @classmethod
    def log_action(cls, email_user, action, request_user):
        return cls.objects.create(
            email_user=email_user.id,
            who=request_user.id,
            what=str(action),
        )

    class Meta:
        managed = False
        app_label = "commercialoperator"


class LedgerOrganisation(SanitiseMixin):
    organisation_id = models.IntegerField(
        unique=True, verbose_name="Ledger Organisation ID"
    )  # Ledger Organisation
    organisation_name = models.CharField(
        max_length=255,
        verbose_name="Ledger Organisation Name",
        editable=False,
        default="",
    )
    organisation_trading_name = models.CharField(
        max_length=255,
        verbose_name="Ledger Organisation Trading Name",
        editable=False,
        null=True,
    )
    organisation_abn = models.CharField(
        max_length=50,
        verbose_name="Ledger Organisation ABN",
        editable=False,
        default="",
    )
    organisation_email = models.EmailField(
        verbose_name="Ledger Organisation Email",
        null=True,
        blank=True,
        editable=False,
    )
    admin_pin_one = models.CharField(max_length=50, blank=True)
    admin_pin_two = models.CharField(max_length=50, blank=True)
    user_pin_one = models.CharField(max_length=50, blank=True)
    user_pin_two = models.CharField(max_length=50, blank=True)

    class Meta:
        app_label = "commercialoperator"

    def __str__(self):
        if self.organisation_name and self.organisation_abn:
            return f"{self.organisation_name} (ABN: {self.organisation_abn})"
        if self.organisation_name:
            return self.organisation_name
        return f"Ledger Organisation ID: {self.organisation_id})"


def m2m_field_through_model_factory(model_name, m2m_field_name="members"):
    """Returns a through model for a m2m field (e.g. members) that mirrors the existing django-managed through table of the m2m field"""

    class MembersThroughModel(models.Model):
        class Meta:
            app_label = "commercialoperator"
            # Mirror the existing django-managed through table of the m2m field
            db_table = f"commercialoperator_{model_name.lower()}_{m2m_field_name}"
            abstract = True
            managed = False
            unique_together = (f"{model_name.lower()}", "emailuser")

        @property
        def emailuser_object(self):
            return retrieve_email_user(self.emailuser_id)

    # Fk to model instance
    MembersThroughModel.add_to_class(
        f"{model_name.lower()}",
        models.ForeignKey(
            f"{model_name}",
            on_delete=models.PROTECT,
            related_name=f"{model_name.lower()}_{m2m_field_name}",
        ),
    )
    # Fk to EmailUserRO
    MembersThroughModel.add_to_class(
        "emailuser",
        models.ForeignKey(
            EmailUser,
            on_delete=models.PROTECT,
            related_name=f"{model_name.lower()}_{m2m_field_name}",
        ),
    )
    return MembersThroughModel


class ReferralRecipientGroupMembers(
    m2m_field_through_model_factory("ReferralRecipientGroup")
):
    pass


class QAOfficerGroupMembers(m2m_field_through_model_factory("QAOfficerGroup")):
    pass


class ProposalAssessorGroupMembers(
    m2m_field_through_model_factory("ProposalAssessorGroup")
):
    pass


class ProposalApproverGroupMembers(
    m2m_field_through_model_factory("ProposalApproverGroup")
):
    pass


class DistrictProposalAssessorGroupMembers(
    m2m_field_through_model_factory("DistrictProposalAssessorGroup")
):
    pass


class DistrictProposalApproverGroupMembers(
    m2m_field_through_model_factory("DistrictProposalApproverGroup")
):
    pass


class OrganisationAccessGroupMembers(
    m2m_field_through_model_factory("OrganisationAccessGroup")
):
    pass
