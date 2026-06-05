import string
import random

from commercialoperator.components.segregation.utils import retrieve_group_members

from ledger_api_client.ledger_models import EmailUserRO as EmailUser


def can_manage_org(organisation, user):
    from commercialoperator.components.organisations.models import (
        OrganisationAccessGroup,
        UserDelegation,
    )

    try:
        UserDelegation.objects.get(organisation=organisation, user=user)
        return can_admin_org(organisation, user.id)
    except UserDelegation.DoesNotExist:
        pass
    try:
        group = OrganisationAccessGroup.objects.first()
        if group:
            # group.members.get(id=user.id)
            if not user.id in retrieve_group_members(group):
                raise EmailUser.DoesNotExist
        return True
    except EmailUser.DoesNotExist:
        pass
    if user.is_superuser:
        return True
    return False


def is_last_admin(organisation, user):
    from commercialoperator.components.organisations.models import OrganisationContact

    """ A check for whether the user contact is the only administrator for the Organisation. """
    _last_admin = False
    try:
        _admin_contacts = OrganisationContact.objects.filter(
            organisation_id=organisation,
            user_status="active",
            user_role="organisation_admin",
        )
        _is_admin = _admin_contacts.filter(email=user.email).exists()
        if _is_admin and _admin_contacts.count() < 2:
            _last_admin = True
    except OrganisationContact.DoesNotExist:
        _last_admin = False
    return _last_admin


def can_admin_org(organisation, user_id):
    from commercialoperator.components.organisations.models import (
        OrganisationContact,
    )

    try:
        emailuser = EmailUser.objects.get(id=user_id)
    except EmailUser.DoesNotExist:
        print("email user does not exist")
        return False

    if emailuser.is_superuser:
        return True

    organisation_id = getattr(organisation, "id", None) if not isinstance(organisation,dict) else organisation["id"] if "id" in organisation else None
    if not organisation_id:
        print("no organisation_id")
        return False

    try:
        org_contact = OrganisationContact.objects.filter(
            organisation_id=organisation_id, email=emailuser.email, is_admin=True, user_status='active'
        )

        return org_contact.exists()
    except Exception as e:
        print(e)
    return False


def can_relink(organisation, user):
    from commercialoperator.components.organisations.models import OrganisationContact

    """ Check user contact can be relinked to the Organisation. """
    _can_relink = False
    try:
        _can_relink = OrganisationContact.objects.filter(
            organisation_id=organisation.id, email=user.email, user_status="unlinked"
        ).exists()
    except OrganisationContact.DoesNotExist:
        _can_relink = False
    return _can_relink


def can_approve(organisation, user):
    from commercialoperator.components.organisations.models import OrganisationContact

    """ Check user contact linkage to the Organisation can be approved. """
    _can_approve = False
    try:
        _can_approve = OrganisationContact.objects.filter(
            organisation_id=organisation.id,
            email=user.email,
            user_status__in=("declined", "pending"),
        ).exists()
    except OrganisationContact.DoesNotExist:
        _can_approve = False
    return _can_approve


def is_consultant(organisation, user):
    from commercialoperator.components.organisations.models import OrganisationContact

    organisation_id = getattr(organisation, "id", None)
    if not organisation_id:
        return False

    try:
        org_contact = OrganisationContact.objects.get(
            organisation_id=organisation_id, email=user.email
        )

        return org_contact.check_consultant
    except OrganisationContact.DoesNotExist:
        pass
    return False


def random_generator(size=12, chars=string.digits):
    return "".join(random.choice(chars) for _ in range(size))


def has_atleast_one_admin(organisation):
    """A check for whether Organisation has atlease one admin user"""

    from commercialoperator.components.organisations.models import OrganisationContact

    _atleast_one_admin = False
    try:
        _admin_contacts = OrganisationContact.objects.filter(
            organisation_id=organisation.id,
            user_status="active",
            user_role="organisation_admin",
            is_admin=True,
        )
        if _admin_contacts.count() > 0:
            _atleast_one_admin = True
    except OrganisationContact.DoesNotExist:
        _atleast_one_admin = False
    return _atleast_one_admin


def is_org_access_member(user):
    from commercialoperator.components.organisations.models import (
        OrganisationAccessGroup,
        OrganisationContact,
    )

    try:
        group = OrganisationAccessGroup.objects.first()
        if group and group.filtered_members:
            return user in group.filtered_members
        return False
    except OrganisationContact.DoesNotExist:
        pass
    return False
