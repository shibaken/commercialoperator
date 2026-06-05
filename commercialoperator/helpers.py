from ledger_api_client.managed_models import SystemGroup
from ledger_api_client.ledger_models import UsersInGroup
from django.contrib.auth.models import Group
from django.conf import settings

import logging

from commercialoperator.components.segregation.utils import (
    retrieve_email_user,
    retrieve_organisation_delegate_ids,
    retrieve_user_groups
)

logger = logging.getLogger(__name__)

def is_payment_admin(user):
    print ("is_payment_admin")
    if user.is_superuser:
        return True
    group = Group.objects.filter(name=settings.PAYMENT_OFFICERS_GROUP)
    if group.exists():
        return user.id in list(UsersInGroup.objects.filter(group_id=group.first().id).values_list('emailuser_id', flat=True))
    else:
        return False

def belongs_to_by_user_id(user_id, group_name):
    system_group = SystemGroup.objects.filter(name=group_name).first()
    return system_group and user_id in system_group.get_system_group_member_ids()

#NOTE: all belongs_to groups have been altered to require 1) settings env vars 2) system group models to be implemented
#This will require a migration plan to transition from ledger-based groups to local groups
def belongs_to(user, group_name):
    """
    Check if the user belongs to the given group.
    :param user:
    :param group_name:
    :return:
    """

    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    return belongs_to_by_user_id(user.id, group_name)


def is_commercialoperator_admin(request):
    return (
        request.user.is_authenticated
        and belongs_to(request.user, settings.ADMIN_GROUP)
    )

def is_finance_officer(request):
    return belongs_to(request.user, settings.GROUP_FINANCE)


#NOTE: this is now used only in the UserSerializer for information - it should not be used to determine internal group membership
def in_dbca_domain(request):
    user = request.user
    try:
        domain = user.email.split("@")[1]
        return domain in settings.DEPT_DOMAINS
    except:
        return False

def is_in_organisation_contacts(request, organisation):
    """Takes a cols Organisation object and checks if the request.user is in the organisation's contacts."""

    delegate_ids = retrieve_organisation_delegate_ids(organisation.id)
    delegates = [retrieve_email_user(user_id) for user_id in delegate_ids]
    delegate_emails = [delegate.email for delegate in delegates]

    return request.user.email in delegate_emails

def is_approver(request):
    return request.user.is_superuser or retrieve_user_groups("proposalapprovergroup", request.user.id).exists() if request.user else False

def is_assessor(request):
    return request.user.is_superuser or retrieve_user_groups("proposalassessorgroup", request.user.id).exists() if request.user else False

def is_district_approver(request):
    return request.user.is_superuser or retrieve_user_groups("districtproposalapprovergroup", request.user.id).exists() if request.user else False

def is_district_assessor(request):
    return request.user.is_superuser or retrieve_user_groups("districtproposalassessorgroup", request.user.id).exists() if request.user else False

def is_organisation_access_approver(request):
    return request.user.is_superuser or retrieve_user_groups("organisationaccessgroup", request.user.id).exists() if request.user else False

def is_referrer(request):
    return request.user.is_superuser or retrieve_user_groups("referralrecipientgroup", request.user.id).exists() if request.user else False

def is_qa_officer(request):
    return request.user.is_superuser or retrieve_user_groups("qaofficergroup", request.user.id).exists() if request.user else False

def is_internal(request):
    """Any users in an internal user group"""
    return (
        request.user.is_superuser or
        is_commercialoperator_admin(request) or
        is_payment_admin(request.user) or
        is_commercialoperator_admin(request) or
        is_finance_officer(request) or 
        is_organisation_access_approver(request) or
        is_qa_officer(request)
    )


