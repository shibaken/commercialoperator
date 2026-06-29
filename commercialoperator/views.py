from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponse

from commercialoperator.helpers import is_internal, is_commercialoperator_admin
from commercialoperator.forms import *
from commercialoperator.components.proposals.models import (
    Referral,
    Proposal,
    DistrictProposal,
)

from commercialoperator.components.proposals.models import Proposal
from commercialoperator.components.organisations.models import Organisation, OrganisationContact
from commercialoperator.components.approvals.models import Approval
from django.db.models import Q

from commercialoperator.components.compliances.models import Compliance
from commercialoperator.components.proposals.mixins import ReferralOwnerMixin

from django.core.management import call_command
from django.conf import settings

import logging
logger = logging.getLogger("payment_checkout")

import os
import mimetypes

class InternalView(UserPassesTestMixin, TemplateView):
    template_name = "commercialoperator/dash/index.html"

    def test_func(self):
        return is_internal(self.request)

    def get_context_data(self, **kwargs):
        context = super(InternalView, self).get_context_data(**kwargs)
        return context


class ExternalView(LoginRequiredMixin, TemplateView):
    template_name = "commercialoperator/dash/index.html"

    def get_context_data(self, **kwargs):
        context = super(ExternalView, self).get_context_data(**kwargs)
        return context


class ReferralView(ReferralOwnerMixin, DetailView):
    model = Referral
    template_name = "commercialoperator/dash/index.html"


class ExternalProposalView(DetailView):
    model = Proposal
    template_name = "commercialoperator/dash/index.html"


class ExternalComplianceView(DetailView):
    model = Compliance
    template_name = "commercialoperator/dash/index.html"


class InternalComplianceView(DetailView):
    model = Compliance
    template_name = "commercialoperator/dash/index.html"


class DistrictProposalView(DetailView):
    model = DistrictProposal
    template_name = "commercialoperator/dash/index.html"


class CommercialOperatorRoutingView(TemplateView):
    template_name = "commercialoperator/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            # if is_internal(self.request):
            #     return redirect("internal")
            return redirect("external")
        kwargs["form"] = LoginForm
        return super(CommercialOperatorRoutingView, self).get(*args, **kwargs)


class CommercialOperatorContactView(TemplateView):
    template_name = "commercialoperator/contact.html"


class CommercialOperatorFurtherInformationView(TemplateView):
    template_name = "commercialoperator/further_info.html"


class InternalProposalView(DetailView):
    model = Proposal
    template_name = "commercialoperator/dash/index.html"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if is_internal(self.request):
                return super(InternalProposalView, self).get(*args, **kwargs)


#TODO we may need to lock this behind an env var so this is not accessible on prod
class ManagementCommandsView(UserPassesTestMixin, LoginRequiredMixin, TemplateView):
    template_name = "commercialoperator/mgt-commands.html"

    def test_func(self):
        return is_commercialoperator_admin(self.request) #TODO check if admin appropriate auth (sys admin may be needed)

    def post(self, request):
        data = {}
        command_script = request.POST.get("script", None)
        if command_script:
            print("running {}".format(command_script))
            call_command(command_script)
            data.update({command_script: "true"})

        return render(request, self.template_name, data)


def is_authorised_to_access_proposal_document(request,document_id):
    if is_internal(request):
        return True
    elif request.user and request.user.is_authenticated:
        user = request.user
        user_orgs = [org.id for org in user.commericaloperator_organisations.all()]
        return Proposal.objects.filter(id=document_id).filter(
                Q(applicant_id__in=user_orgs) |
                Q(submitter=user)).exists()

def is_authorised_to_access_approval_document(request,document_id):
    if is_internal(request):
        return True
    elif request.user and request.user.is_authenticated:
        user = request.user
        user_orgs = [org.id for org in user.commericaloperator_organisations.all()]
        return Approval.objects.filter(id=document_id).filter(
                Q(applicant_id__in = user_orgs) |
                Q(proxy_applicant_id=user.id)).exists()

def is_authorised_to_access_organisation_document(request,document_id):
    if is_internal(request):
        return True
    elif request.user and request.user.is_authenticated:
        user = request.user
        org_contacts = OrganisationContact.objects.filter(is_admin=True).filter(email=user.email)
        user_admin_orgs = [org.organisation.id for org in org_contacts]
        return Organisation.objects.filter(id=document_id).filter(id__in=user_admin_orgs).exists()

def get_file_path_id(check_str,file_path):
    file_name_path_split = file_path.split("/")
    #if the check_str is in the file path, the next value should be the id
    if check_str in file_name_path_split:
        id_index = file_name_path_split.index(check_str)+1
        if len(file_name_path_split) > id_index and file_name_path_split[id_index].isnumeric():
            return int(file_name_path_split[id_index])
        else:
            return False
    else:
        return False

def is_authorised_to_access_document(request):
    
    if is_internal(request):
        return True
    elif request.user.is_authenticated:
        p_document_id = get_file_path_id("proposals",request.path)
        if p_document_id:
            return is_authorised_to_access_proposal_document(request,p_document_id)
        
        a_document_id = get_file_path_id("approvals",request.path)
        if a_document_id:
            return is_authorised_to_access_approval_document(request,a_document_id)
        
        #for organisation requests, this will fail and they are stored in a request subdir and by date (which is fine for current use cases)
        o_document_id = get_file_path_id("organisations",request.path)
        if o_document_id:
            return is_authorised_to_access_organisation_document(request,o_document_id)
        return False
    else:
        return False

def getPrivateFile(request):

    if is_authorised_to_access_document(request):
        file_name_path =  request.path
        #norm path will convert any traversal or repeat / in to its normalised form
        full_file_path= os.path.normpath(settings.BASE_DIR+file_name_path) 
        #we then ensure the normalised path is within the BASE_DIR (and the file exists)
        if full_file_path.startswith(settings.BASE_DIR) and os.path.isfile(full_file_path):
            extension = file_name_path.split(".")[-1]
            the_file = open(full_file_path, 'rb')
            the_data = the_file.read()
            the_file.close()
            if extension == 'msg':
                return HttpResponse(the_data, content_type="application/vnd.ms-outlook")
            if extension == 'eml':
                return HttpResponse(the_data, content_type="application/vnd.ms-outlook")

            try:
                return HttpResponse(the_data, content_type=mimetypes.types_map['.'+str(extension.lower())])
            except:
                return HttpResponse(status=500)
       
    return HttpResponse(status=403)