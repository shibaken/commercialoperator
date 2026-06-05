from django.db import models, transaction
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from rest_framework import status

from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.utils import (
    get_organisation,
    get_search_organisation,
    create_organisation,
)
from commercialoperator.components.main.models import (
    UserAction,
    CommunicationsLogEntry,
    Document,
)
from commercialoperator.components.organisations.utils import (
    random_generator,
    can_admin_org,
    has_atleast_one_admin,
)
from commercialoperator.components.organisations.emails import (
    send_organisation_request_accept_email_notification,
    send_organisation_request_decline_email_notification,
    send_organisation_link_email_notification,
    send_organisation_unlink_email_notification,
    send_org_access_group_request_accept_email_notification,
    send_organisation_contact_adminuser_email_notification,
    send_organisation_contact_user_email_notification,
    send_organisation_contact_suspend_email_notification,
    send_organisation_reinstate_email_notification,
    send_organisation_contact_decline_email_notification,
    send_organisation_request_email_notification,
    send_organisation_request_link_email_notification,
)
from commercialoperator.components.segregation.decorators import basic_exception_handler
from commercialoperator.components.segregation.mixins import MembersPropertiesMixin
from commercialoperator.components.segregation.utils import (
    retrieve_delegate_organisation_ids,
    retrieve_email_user,
    retrieve_organisation_delegate_ids,
)
from commercialoperator.components.main.mixins import SanitiseFileMixin, SanitiseMixin

from django.db.models import JSONField

import logging

logger = logging.getLogger(__name__)

from commercialoperator.components.main.models import private_storage

class Organisation(SanitiseMixin):
    organisation_id = models.IntegerField(
        unique=True, verbose_name="Ledger Organisation ID"
    )
    delegates = models.ManyToManyField(
        EmailUser,
        blank=True,
        through="UserDelegation",
        related_name="commercialoperator_organisations",
    )
    admin_pin_one = models.CharField(max_length=50, blank=True)
    admin_pin_two = models.CharField(max_length=50, blank=True)
    user_pin_one = models.CharField(max_length=50, blank=True)
    user_pin_two = models.CharField(max_length=50, blank=True)
    bpay_allowed = models.BooleanField("BPAY Allowed", default=False)
    monthly_invoicing_allowed = models.BooleanField(default=False)
    monthly_invoicing_period = models.SmallIntegerField(
        "Monthly Invoicing Period (in #days from beginning of the following month)",
        default=0,
    )
    monthly_payment_due_period = models.SmallIntegerField(
        "Monthly Payment Due Period (in #days from Invoicing Date)", default=20
    )

    apply_application_discount = models.BooleanField(default=False)
    application_discount = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )

    apply_licence_discount = models.BooleanField(default=False)
    licence_discount = models.FloatField(
        default=0.0, validators=[MinValueValidator(0.0)]
    )
    event_training_completed = models.BooleanField(default=False)
    event_training_date = models.DateField(blank=True, null=True)

    charge_once_per_year = models.DateField(
        "Charge Application Fee once per year from given start date (Charge always if null)",
        blank=True,
        null=True,
    )
    last_event_application_fee_date = models.DateField(
        "The last date a fee was charged for an Event Application",
        blank=True,
        null=True,
    )
    max_num_months_ahead = models.SmallIntegerField(
        "Maximum number of months ahead an Event can be booked (Any if equal to zero)",
        default=0,
    )

    #Property Caches to store Org Name and ABN without having to constantly query ledger - update on save or via management command - use for filtering
    #NOTE: this is a temporary solution for until we are able to fully migrate ledger organisation tables
    property_cache = JSONField(null=True, blank=True, default=dict)

    class Meta:
        app_label = "commercialoperator"

    def __str__(self):

        return_str = ""

        if 'name' in self.property_cache:
            return_str = self.property_cache["name"]
        if 'abn' in self.property_cache:
            return_str += f" (ABN: {self.property_cache["abn"]})"
        
        if not return_str:
            return str(f"{self.name} (ABN: {self.abn})")
        
        return return_str

    def update_property_cache(self, save=True):

        #Update Cache
        self.property_cache['name'] = self.name
        self.property_cache['abn'] = self.abn

        if save is True:
            self.save()
        
        return self.property_cache

    def save(self, *args, **kwargs):
        if self.pk:
            self.update_property_cache(False) #NOTE: very important that this is False to prevent an infinite save loop
        super(Organisation, self).save(*args, **kwargs)

    @classmethod
    def organisations_user_can_admin(cls, user_id):
        delegate_organisations = retrieve_delegate_organisation_ids(user_id)
        emailuser = retrieve_email_user(user_id)

        if not emailuser:
            return cls.objects.none()

        return (
            cls.objects.filter(
                organisation_id__in=delegate_organisations,  # delegates__user=user_id
                contacts__email=emailuser.email,  # contacts__user=user_id
                contacts__user_status=OrganisationContact.USER_STATUS_CHOICES[2][
                    0
                ],  # active
                contacts__user_role=OrganisationContact.USER_ROLE_CHOICES[0][
                    0
                ],  # organisation_admin
            )
            .distinct()
            .only(
                "id",
            )
        )

    def log_user_action(self, action, user):
        return OrganisationAction.log_action(self, action, user)

    def validate_pins(self, pin1, pin2, request):
        try:
            val_admin = self.admin_pin_one == pin1 and self.admin_pin_two == pin2
            val_user = self.user_pin_one == pin1 and self.user_pin_two == pin2
            if val_admin:
                val = val_admin
                admin_flag = True
                role = "organisation_admin"
            elif val_user:
                val = val_user
                admin_flag = False
                role = "organisation_user"
            else:
                val = False
                return val

            self.add_user_contact(request.user, request, admin_flag, role)
            return val
        except Exception:
            return None

    def check_user_contact(self, request, admin_flag, role):
        user = request.user
        try:
            org = OrganisationContact.objects.create(
                organisation=self,
                first_name=user.first_name,
                last_name=user.last_name,
                mobile_number=user.mobile_number,
                phone_number=user.phone_number,
                fax_number=user.fax_number,
                email=user.email,
                user_role=role,
                user_status="pending",
                is_admin=admin_flag,
            )
            return org
        except Exception:
            return False

    @transaction.atomic
    def add_user_contact(self, user, request, admin_flag, role):
        contact, created = OrganisationContact.objects.get_or_create(
            organisation=self,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            defaults={
                "mobile_number": user.mobile_number,
                "phone_number": user.phone_number,
                "fax_number": user.fax_number,
                "user_role": role,
                "user_status": "pending",
                "is_admin": admin_flag,
            },
        )

        if not created:
            contact.mobile_number = user.mobile_number
            contact.phone_number = user.phone_number
            contact.fax_number = user.fax_number
            contact.user_role = role
            contact.user_status = "pending"
            contact.is_admin = admin_flag
            contact.save()

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_CONTACT_ADDED.format(
                "{} {}({})".format(user.first_name, user.last_name, user.email)
            ),
            request.user,
        )

    @transaction.atomic
    def update_organisation(self, request):
        # log organisation details updated (eg ../internal/organisations/access/2) - incorrect - this is for OrganisationRequesti not Organisation
        # should be ../internal/organisations/1
        self.log_user_action(OrganisationAction.ACTION_UPDATE_ORGANISATION, request.user)

    def update_address(self, request):
        self.log_user_action(OrganisationAction.ACTION_UPDATE_ADDRESS, request.user)

    def update_contacts(self, request):
        try:
            contact = self.contact.last()
            self.log_user_action(
                OrganisationAction.ACTION_UPDATE_CONTACTS.format(
                    "{} {}({})".format(
                        contact.first_name, contact.last_name, contact.email
                    )
                ),
                request.user,
            )
        except:
            pass

    def generate_pins(self):
        # self.pin_one = self._generate_pin()
        # self.pin_two = self._generate_pin()
        self.admin_pin_one = self._generate_pin()
        self.admin_pin_two = self._generate_pin()
        self.user_pin_one = self._generate_pin()
        self.user_pin_two = self._generate_pin()
        self.save()

    def _generate_pin(self):
        return random_generator()

    def send_organisation_request_link_notification(self, request):
        # Notify each Admin member of request to be linked to org.
        contacts = OrganisationContact.objects.filter(
            organisation_id=self.id,
            user_role="organisation_admin",
            user_status="active",
            is_admin=True,
        )
        recipients = [c.email for c in contacts]
        send_organisation_request_link_email_notification(self, request, recipients)

    @staticmethod
    @basic_exception_handler
    def existence(name, abn):
        exists = True
        org = None

        organisation_response = get_search_organisation(name, abn)
        response_status = organisation_response.get("status", None)

        if response_status == status.HTTP_200_OK:
            ledger_org = organisation_response.get("data", {})[0]
            try:
                org = Organisation.objects.get(
                    organisation_id=ledger_org["organisation_id"]
                )
            except Organisation.DoesNotExist:
                exists = False
        else:
            exists = False

        if exists:
            if has_atleast_one_admin(org):
                return {
                    "exists": exists,
                    "id": org.id,
                    "first_five": org.first_five,
                }
            else:
                return {"exists": has_atleast_one_admin(org)}
        return {"exists": exists}

    @transaction.atomic
    def accept_user(self, user, request):
        delegate = UserDelegation.objects.create(organisation=self, user=user)

        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_status = "active"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_LINK.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        send_organisation_link_email_notification(user, request.user, self, request)

    def decline_user(self, user, request):
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=user.email
            )
            org_contact.user_status = "declined"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        OrganisationContactDeclinedDetails.objects.create(
            officer=request.user, request=org_contact
        )

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_CONTACT_DECLINED.format(
                "{} {}({})".format(user.first_name, user.last_name, user.email)
            ),
            request.user,
        )
        send_organisation_contact_decline_email_notification(
            user, request.user, self, request
        )

    @transaction.atomic
    def link_user(self, user, request, admin_flag):
        try:
            UserDelegation.objects.get(organisation=self, user=user)
            raise ValidationError(
                "This user has already been linked to {}".format(str(self.organisation))
            )
        except UserDelegation.DoesNotExist:
            delegate = UserDelegation.objects.create(organisation=self, user=user)
        if self.first_five_admin:
            is_admin = True
            role = "organisation_admin"
        elif admin_flag:
            role = "organisation_admin"
            is_admin = True
        else:
            role = "organisation_user"
            is_admin = False

        # Create contact person
        try:
            OrganisationContact.objects.create(
                organisation=self,
                first_name=user.first_name,
                last_name=user.last_name,
                mobile_number=user.mobile_number,
                phone_number=user.phone_number,
                fax_number=user.fax_number,
                email=user.email,
                user_role=role,
                user_status="pending",
                is_admin=is_admin,
            )
        except:
            pass  # user already exists

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_LINK.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_link_email_notification(user, request.user, self, request)

    @transaction.atomic
    def accept_declined_user(self, user, request):
        try:
            UserDelegation.objects.get(organisation=self, user=user)
            raise ValidationError(
                "This user has already been linked to {}".format(str(self.organisation))
            )
        except UserDelegation.DoesNotExist:
            delegate = UserDelegation.objects.create(organisation=self, user=user)
        # if self.first_five_admin:
        #     is_admin = True
        #     role = 'organisation_admin'
        # elif admin_flag:
        #     role = 'organisation_admin'
        #     is_admin = True
        # else:
        #     role = 'organisation_user'
        #     is_admin = False

        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_status = "active"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_LINK.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_link_email_notification(user, request.user, self, request)

    @transaction.atomic
    def relink_user(self, user, request):
        try:
            UserDelegation.objects.get(organisation=self, user=user)
            raise ValidationError(f"This user has already been linked to {self.name}")
        except UserDelegation.DoesNotExist:
            delegate = UserDelegation.objects.create(organisation=self, user=user)
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_status = "active"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_MAKE_CONTACT_REINSTATE.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_reinstate_email_notification(
            user, request.user, self, request
        )

    @transaction.atomic
    def unlink_user(self, user, request):
        try:
            delegate = UserDelegation.objects.get(organisation=self, user=user)
        except UserDelegation.DoesNotExist:
            raise ValidationError(
                "This user is not a member of {}".format(str(self.organisation))
            )
        # delete contact person
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            if org_contact.user_role == "organisation_admin":
                if (
                    OrganisationContact.objects.filter(
                        organisation=self,
                        user_role="organisation_admin",
                        user_status="active",
                    ).count()
                    > 1
                ):
                    org_contact.user_status = "unlinked"
                    org_contact.save()
                    # delete delegate
                    delegate.delete()
                else:
                    raise ValidationError(
                        "This user is last Organisation Administrator."
                    )

            else:
                org_contact.user_status = "unlinked"
                org_contact.save()
                # delete delegate
                delegate.delete()
        except OrganisationContact.DoesNotExist:
            pass

        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_UNLINK.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_unlink_email_notification(user, request.user, self, request)

    @transaction.atomic
    def make_admin_user(self, user, request):
        try:
            delegate = UserDelegation.objects.get(organisation=self, user=user)
        except UserDelegation.DoesNotExist:
            raise ValidationError(
                "This user is not a member of {}".format(str(self.organisation))
            )
        # delete contact person
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_role = "organisation_admin"
            org_contact.is_admin = True
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_MAKE_CONTACT_ADMIN.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_contact_adminuser_email_notification(
            user, request.user, self, request
        )

    @transaction.atomic
    def make_user(self, user, request):
        try:
            delegate = UserDelegation.objects.get(organisation=self, user=user)
        except UserDelegation.DoesNotExist:
            raise ValidationError(
                "This user is not a member of {}".format(str(self.organisation))
            )
        # delete contact person
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            if org_contact.user_role == "organisation_admin":
                # Last admin user should not be able to make himself user.
                if (
                    OrganisationContact.objects.filter(
                        organisation=self,
                        user_role="organisation_admin",
                        user_status="active",
                    ).count()
                    > 1
                ):
                    org_contact.user_role = "organisation_user"
                    org_contact.is_admin = False
                    org_contact.save()
                else:
                    raise ValidationError(
                        "This user is last Organisation Administrator."
                    )
            else:
                org_contact.user_role = "organisation_user"
                org_contact.is_admin = False
                org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_MAKE_CONTACT_USER.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_contact_user_email_notification(
            user, request.user, self, request
        )

    @transaction.atomic
    def suspend_user(self, user, request):
        try:
            delegate = UserDelegation.objects.get(organisation=self, user=user)
        except UserDelegation.DoesNotExist:
            raise ValidationError(
                "This user is not a member of {}".format(str(self.organisation))
            )
        # delete contact person
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_status = "suspended"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_MAKE_CONTACT_SUSPEND.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_contact_suspend_email_notification(
            user, request.user, self, request
        )

    @transaction.atomic
    def reinstate_user(self, user, request):
        try:
            delegate = UserDelegation.objects.get(organisation=self, user=user)
        except UserDelegation.DoesNotExist:
            raise ValidationError(
                "This user is not a member of {}".format(str(self.organisation))
            )
        # delete contact person
        try:
            org_contact = OrganisationContact.objects.get(
                organisation=self, email=delegate.user.email
            )
            org_contact.user_status = "active"
            org_contact.save()
        except OrganisationContact.DoesNotExist:
            pass
        # log linking
        self.log_user_action(
            OrganisationAction.ACTION_MAKE_CONTACT_REINSTATE.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # send email
        send_organisation_reinstate_email_notification(
            user, request.user, self, request
        )

    @property
    def name(self):
        organisation_response = get_organisation(self.organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("organisation_name", "")
        return None

    @property
    def trading_name(self):
        organisation_response = get_organisation(self.organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("organisation_trading_name", "")
        return None

    @property
    def abn(self):
        organisation_response = get_organisation(self.organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("organisation_abn", "")
        return None

    @property
    def address(self):
        organisation_id = self.organisation_id
        # organisation_id = 1
        organisation_response = get_organisation(organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("postal_address", "")
        return None

    @property
    def address_summary(self):
        organisation_id = self.organisation_id
        # organisation_id = 1
        organisation_response = get_organisation(organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            address = organisation_response.get("data", {}).get("postal_address", "")
            address_values = [
                a.encode("utf-8").decode("unicode-escape").strip()
                for a in address.values()
                if a
            ]
            return ", ".join(address_values)
        return None

    @property
    def phone_number(self):
        # Note: There doesn't seem to be a phone number field in the ledger organisation model
        organisation_response = get_organisation(self.organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("phone_number", "")
        return None

    @property
    def email(self):
        organisation_response = get_organisation(self.organisation_id)
        if organisation_response.get("status", None) == status.HTTP_200_OK:
            return organisation_response.get("data", {}).get("organisation_email", "")
        return None

    @property
    def first_five(self):
        delegates_all_5 = retrieve_organisation_delegate_ids(self.id)[:5]
        delegates_all_5 = [retrieve_email_user(user_id) for user_id in delegates_all_5]
        return ",".join(
            [
                user.get_full_name()
                for user in delegates_all_5
                if can_admin_org(self, user.id)
            ]
        )

    @property
    def all_admin_emails(self):
        delegate_user_ids = retrieve_organisation_delegate_ids(self.id)
        # delegate_user_ids = [1] # for testing
        delegates_all = [retrieve_email_user(user_id) for user_id in delegate_user_ids]
        delegates_all = [
            user for user in delegates_all if user
        ]  # Get rid of None values
        return [user.email for user in delegates_all if can_admin_org(self, user.id)]


class OrganisationContact(SanitiseMixin):
    USER_STATUS_CHOICES = (
        ("draft", "Draft"),
        ("pending", "Pending"),
        ("active", "Active"),
        ("declined", "Declined"),
        ("unlinked", "Unlinked"),
        ("suspended", "Suspended"),
        (
            "contact_form",
            "ContactForm",
        ), 
    )
    USER_ROLE_CHOICES = (
        ("organisation_admin", "Organisation Admin"),
        ("organisation_user", "Organisation User"),
        ("consultant", "Consultant"),
    )
    user_status = models.CharField(
        "Status",
        max_length=40,
        choices=USER_STATUS_CHOICES,
        default=USER_STATUS_CHOICES[0][0],
    )
    user_role = models.CharField(
        "Role", max_length=40, choices=USER_ROLE_CHOICES, default="organisation_user"
    )
    is_admin = models.BooleanField(default=False)
    organisation = models.ForeignKey(
        Organisation, related_name="contacts", on_delete=models.CASCADE
    )
    email = models.EmailField(blank=False)
    first_name = models.CharField(
        max_length=128, blank=False, verbose_name="Given name(s)"
    )
    last_name = models.CharField(max_length=128, blank=False)
    phone_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="phone number", help_text=""
    )
    mobile_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="mobile number", help_text=""
    )
    fax_number = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="fax number", help_text=""
    )

    class Meta:
        app_label = "commercialoperator"
        unique_together = (("organisation", "email"),)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def can_edit(self):
        """
        :return: True if the application is in one of the editable status.
        """
        return (
            self.is_admin
            and self.user_status == "active"
            and self.user_role == "organisation_admin"
        )

    @property
    def check_consultant(self):
        """
        :return: True if the application is in one of the editable status.
        """
        return self.user_status == "active" and self.user_role == "consultant"

    @property
    def check_delegate(self):
        cols_org_id = self.organisation_id
        delegate_user_ids = retrieve_organisation_delegate_ids(cols_org_id)
        delegates_all = [retrieve_email_user(user_id) for user_id in delegate_user_ids]
        delegates_all_emails = [user.email for user in delegates_all if user]

        return self.email in delegates_all_emails


class OrganisationContactDeclinedDetails(models.Model):
    request = models.ForeignKey(OrganisationContact, on_delete=models.CASCADE)
    officer = models.ForeignKey(EmailUser, null=False, on_delete=models.CASCADE)

    class Meta:
        app_label = "commercialoperator"


class UserDelegation(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    user = models.ForeignKey(EmailUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("organisation", "user"),)
        app_label = "commercialoperator"

    def __str__(self):
        user = retrieve_email_user(self.user_id)
        return f"Org: {self.organisation}, User: {user}"


class OrganisationAction(UserAction):
    ACTION_REQUEST_APPROVED = "Organisation Request {} Approved"
    ACTION_LINK = "Linked {}"
    ACTION_UNLINK = "Unlinked {}"
    ACTION_CONTACT_ADDED = "Added new contact {}"
    ACTION_CONTACT_REMOVED = "Removed contact {}"
    ACTION_CONTACT_DECLINED = "Declined contact {}"
    ACTION_MAKE_CONTACT_ADMIN = "Made contact Organisation Admin {}"
    ACTION_MAKE_CONTACT_USER = "Made contact Organisation User {}"
    # ACTION_CONTACT_REMOVED = "Removed contact {}"
    ACTION_ORGANISATIONAL_DETAILS_SAVED_NOT_CHANGED = "Details saved without changes"
    ACTION_ORGANISATIONAL_DETAILS_SAVED_CHANGED = (
        "Details saved with the following changes: \n{}"
    )
    ACTION_ORGANISATIONAL_ADDRESS_DETAILS_SAVED_NOT_CHANGED = (
        "Address Details saved without changes"
    )
    ACTION_ORGANISATIONAL_ADDRESS_DETAILS_SAVED_CHANGED = (
        "Addres Details saved with folowing changes: \n{}"
    )
    ACTION_ORGANISATION_CONTACT_ACCEPT = "Accepted contact {}"
    # ACTION_CONTACT_DECLINE = "Declined contact {}"
    ACTION_MAKE_CONTACT_SUSPEND = "Suspended contact {}"
    ACTION_MAKE_CONTACT_REINSTATE = "REINSTATED contact {}"

    ACTION_ORGANISATIONAL_DETAILS_SAVED_NOT_CHANGED = "Details saved without changes"
    ACTION_ORGANISATIONAL_DETAILS_SAVED_CHANGED = (
        "Details saved with the following changes: \n{}"
    )
    ACTION_ORGANISATIONAL_ADDRESS_DETAILS_SAVED_NOT_CHANGED = (
        "Address Details saved without changes"
    )
    ACTION_ORGANISATIONAL_ADDRESS_DETAILS_SAVED_CHANGED = (
        "Addres Details saved with folowing changes: \n{}"
    )

    ACTION_UPDATE_ORGANISATION = "Updated organisation name"
    ACTION_UPDATE_ADDRESS = "Updated address"
    ACTION_UPDATE_CONTACTS = "Updated contacts"

    @classmethod
    def log_action(cls, organisation, action, user):
        return cls.objects.create(
            organisation=organisation, who_id=user.id, what=str(action)
        )

    organisation = models.ForeignKey(
        Organisation, related_name="action_logs", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "commercialoperator"


def update_organisation_comms_log_filename(instance, filename):
    return "organisations/{}/communications/{}/{}".format(
        instance.log_entry.organisation.id, instance.id, filename
    )


class OrganisationLogDocument(Document):
    log_entry = models.ForeignKey(
        "OrganisationLogEntry", related_name="documents", on_delete=models.CASCADE
    )
    _file = models.FileField(
        upload_to=update_organisation_comms_log_filename, max_length=512, storage=private_storage
    )

    class Meta:
        app_label = "commercialoperator"


class OrganisationLogEntry(CommunicationsLogEntry):
    organisation = models.ForeignKey(
        Organisation, related_name="comms_logs", on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        # save the request id if the reference not provided
        if not self.reference:
            self.reference = self.organisation.id
        super(OrganisationLogEntry, self).save(**kwargs)

    class Meta:
        app_label = "commercialoperator"


class OrganisationRequest(SanitiseFileMixin):

    STATUS_CHOICES = (
        ("with_assessor", "With Assessor"),
        ("approved", "Approved"),
        ("declined", "Declined"),
    )
    ROLE_CHOICES = (("employee", "Employee"), ("consultant", "Consultant"))
    name = models.CharField(max_length=128)
    abn = models.CharField(max_length=50, null=True, blank=True, verbose_name="ABN")
    requester = models.ForeignKey(EmailUser, on_delete=models.CASCADE)
    assigned_officer = models.ForeignKey(
        EmailUser,
        blank=True,
        null=True,
        related_name="org_request_assignee",
        on_delete=models.CASCADE,
    )
    identification = models.FileField(
        upload_to="organisation/requests",
        max_length=512,
        null=True,
        blank=True,
        storage=private_storage
    )
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default="with_assessor"
    )
    lodgement_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=100, choices=ROLE_CHOICES, default="employee")

    class Meta:
        app_label = "commercialoperator"
        ordering = ["name"]

    def accept(self, request):
        self.__accept(request)
        # Continue with remaining logic
        self.status = "approved"
        self.save()
        self.log_user_action(
            OrganisationRequestUserAction.ACTION_CONCLUDE_REQUEST.format(self.id),
            request.user,
        )

    @transaction.atomic
    def __accept(self, request):
        # Check if orgsanisation exists in ledger
        ledger_org = None
        organisation_response = get_search_organisation(self.name, self.abn)
        response_status = organisation_response.get("status", None)

        if response_status == status.HTTP_404_NOT_FOUND:
            # Create a new organisation in ledger
            create_organisation(self.name, self.abn)
            organisation_response = get_search_organisation(self.name, self.abn)
            ledger_org = None
            response_status = organisation_response.get("status", None)
            if response_status == status.HTTP_200_OK:
                for organisation in organisation_response.get("data", {}):
                    if organisation["organisation_abn"] == self.abn:
                        ledger_org = organisation
                        break

        elif response_status == status.HTTP_200_OK:
            ledger_org = None
            for organisation in organisation_response.get("data", {}):
                if organisation["organisation_abn"] == self.abn:
                    ledger_org = organisation
                    break

            if not ledger_org:
                create_organisation(self.name, self.abn)
                organisation_response = get_search_organisation(self.name, self.abn)
                response_status = organisation_response.get("status", None)
                if response_status == status.HTTP_200_OK:
                    for organisation in organisation_response.get("data", {}):
                        if organisation["organisation_abn"] == self.abn:
                            ledger_org = organisation
                            break

        if not ledger_org:
            raise ValidationError("Unable to create or retrieve organisation.")

        # Create Organisation in commercialoperator
        org, created = Organisation.objects.get_or_create(
            organisation_id=ledger_org["organisation_id"]
        )
        if created:
            logger.info(f"Organisation created in COLS: {org}")

        # Link requester to organisation
        delegate = UserDelegation.objects.create(user=self.requester, organisation=org)
        # log who approved the request
        org.log_user_action(
            OrganisationAction.ACTION_REQUEST_APPROVED.format(self.id), request.user
        )
        # log who created the link
        org.log_user_action(
            OrganisationAction.ACTION_LINK.format(
                "{} {}({})".format(
                    delegate.user.first_name,
                    delegate.user.last_name,
                    delegate.user.email,
                )
            ),
            request.user,
        )
        # Create contact person
        if self.role == "consultant":
            role = "consultant"
        else:
            role = "organisation_admin"
        # Create contact person

        OrganisationContact.objects.create(
            organisation=org,
            first_name=self.requester.first_name,
            last_name=self.requester.last_name,
            mobile_number=self.requester.mobile_number,
            phone_number=self.requester.phone_number,
            fax_number=self.requester.fax_number,
            email=self.requester.email,
            user_role=role,
            user_status="active",
            is_admin=True,
        )
        # send email to requester
        send_organisation_request_accept_email_notification(self, org, request)

    def send_org_access_group_request_notification(self, request):
        # user submits a new organisation request
        # send email to organisation access group
        org_access_recipients = [
            i.email for i in OrganisationAccessGroup.objects.last().all_members
        ]
        send_org_access_group_request_accept_email_notification(
            self, request, org_access_recipients
        )

    @transaction.atomic
    def assign_to(self, user, request):
        self.assigned_officer = user
        self.save()
        self.log_user_action(
            OrganisationRequestUserAction.ACTION_ASSIGN_TO.format(user.get_full_name()),
            request.user,
        )

    @transaction.atomic
    def unassign(self, request):
        self.assigned_officer = None
        self.save()
        self.log_user_action(OrganisationRequestUserAction.ACTION_UNASSIGN, request.user)

    @transaction.atomic
    def decline(self, reason, request):
        self.status = "declined"
        self.save()
        OrganisationRequestDeclinedDetails.objects.create(
            officer=request.user, reason=reason, request=self
        )
        self.log_user_action(
            OrganisationRequestUserAction.ACTION_DECLINE_REQUEST, request.user
        )
        send_organisation_request_decline_email_notification(self, request)

    def send_organisation_request_email_notification(self, request):
        # user submits a new organisation request
        # send email to organisation access group
        group = OrganisationAccessGroup.objects.first()
        if group and group.filtered_members:
            org_access_recipients = [m.email for m in group.filtered_members]
            send_organisation_request_email_notification(
                self, request, org_access_recipients
            )

    def log_user_action(self, action, user):
        return OrganisationRequestUserAction.log_action(self, action, user)


class OrganisationAccessGroup(models.Model, MembersPropertiesMixin):
    site = models.OneToOneField(Site, default="1", on_delete=models.CASCADE)
    members = models.ManyToManyField(EmailUser)

    def __str__(self):
        return "Organisation Access Group"

    class Meta:
        app_label = "commercialoperator"
        verbose_name_plural = "Organisation access group"


class OrganisationRequestUserAction(UserAction):
    ACTION_LODGE_REQUEST = "Lodge request {}"
    ACTION_ASSIGN_TO = "Assign to {}"
    ACTION_UNASSIGN = "Unassign"
    ACTION_DECLINE_REQUEST = "Decline request"
    # Assessors

    ACTION_CONCLUDE_REQUEST = "Conclude request {}"

    @classmethod
    def log_action(cls, request, action, user):
        return cls.objects.create(
            request_id=request.id, who_id=user.id, what=str(action)
        )

    request = models.ForeignKey(
        OrganisationRequest, related_name="action_logs", on_delete=models.CASCADE
    )

    class Meta:
        app_label = "commercialoperator"


class OrganisationRequestDeclinedDetails(SanitiseMixin):
    request = models.ForeignKey(OrganisationRequest, on_delete=models.CASCADE)
    officer = models.ForeignKey(EmailUser, null=False, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)

    class Meta:
        app_label = "commercialoperator"


def update_organisation_request_comms_log_filename(instance, filename):
    return "organisation_requests/{}/communications/{}/{}".format(
        instance.log_entry.request.id, instance.id, filename
    )


class OrganisationRequestLogDocument(Document):
    log_entry = models.ForeignKey(
        "OrganisationRequestLogEntry",
        related_name="documents",
        on_delete=models.CASCADE,
    )
    _file = models.FileField(
        upload_to=update_organisation_request_comms_log_filename, max_length=512, storage=private_storage
    )

    class Meta:
        app_label = "commercialoperator"


class OrganisationRequestLogEntry(CommunicationsLogEntry):
    request = models.ForeignKey(
        OrganisationRequest, related_name="comms_logs", on_delete=models.CASCADE
    )

    def save(self, **kwargs):
        # save the request id if the reference not provided
        if not self.reference:
            self.reference = self.request.id
        super(OrganisationRequestLogEntry, self).save(**kwargs)

    class Meta:
        app_label = "commercialoperator"


import reversion

# reversion.register(ledger_organisation, follow=["organisation_set"])
reversion.register(
    Organisation,
    follow=[
        "org_approvals",
        "contacts",
        "userdelegation_set",
        "action_logs",
        "comms_logs",
    ],
)
reversion.register(OrganisationContact)
reversion.register(OrganisationAction)
reversion.register(OrganisationLogEntry, follow=["documents"])
reversion.register(OrganisationLogDocument)
reversion.register(
    OrganisationRequest,
    follow=["action_logs", "organisationrequestdeclineddetails_set", "comms_logs"],
)
reversion.register(OrganisationAccessGroup, exclude=["members"])
reversion.register(OrganisationRequestUserAction)
reversion.register(OrganisationRequestDeclinedDetails)
reversion.register(OrganisationRequestLogDocument)
reversion.register(OrganisationRequestLogEntry, follow=["documents"])
reversion.register(UserDelegation)
