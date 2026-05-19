from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.db.models import Q
from commercialoperator.components.proposals.models import (
    Proposal,
    Referral,
    ProposalType,
    DistrictProposal,
)
from commercialoperator.components.approvals.models import Approval
from commercialoperator.components.compliances.models import Compliance
import json
from reversion_compare.views import HistoryCompareDetailView
from reversion.models import Version
from django.contrib.auth.mixins import UserPassesTestMixin
from commercialoperator.helpers import is_internal

class InternalHistoryCompareDetailView(UserPassesTestMixin, HistoryCompareDetailView):

    def _get_action_list(self):
        action_list = [
            {"version": version, "revision": version.revision}
            for version in self._order_version_queryset(
                Version.objects.get_for_object(self.get_object()).select_related("revision")
            )
        ]
        return action_list

    def test_func(self):
        return is_internal(self.request)

class ProposalHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """

    model = Proposal
    template_name = "commercialoperator/reversion_history.html"


class ProposalFilteredHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare - with 'status' in the comment field only'
    """

    model = Proposal
    template_name = "commercialoperator/reversion_history.html"

    def _get_action_list(
        self,
    ):
        """Get only versions when processing_status changed, and add the most recent (current) version"""
        current_revision_id = (
            Version.objects.get_for_object(self.get_object()).first().revision_id
        )
        action_list = [
            {"version": version, "revision": version.revision}
            for version in self._order_version_queryset(
                Version.objects.get_for_object(self.get_object())
                .select_related("revision")
                .filter(
                    Q(revision__comment__icontains="status")
                    | Q(revision_id=current_revision_id)
                )
            )
        ]
        return action_list


class ReferralHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """

    model = Referral
    template_name = "commercialoperator/reversion_history.html"


class ApprovalHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """

    model = Approval
    template_name = "commercialoperator/reversion_history.html"


class ComplianceHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """

    model = Compliance
    template_name = "commercialoperator/reversion_history.html"


class ProposalTypeHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """

    model = ProposalType
    template_name = "commercialoperator/reversion_history.html"


class PreviewLicencePDFView(UserPassesTestMixin, View):

    def test_func(self):
        return is_internal(self.request)
    
    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type="application/pdf")

        proposal = self.get_object()
        details = json.loads(request.POST.get("formData"))

        response.write(proposal.preview_approval(request, details))
        return response

    def get_object(self):
        return get_object_or_404(Proposal, id=self.kwargs["proposal_pk"])


class PreviewDistrictLicencePDFView(UserPassesTestMixin, View):

    def test_func(self):
        return is_internal(self.request)
    
    def post(self, request, *args, **kwargs):
        response = HttpResponse(content_type="application/pdf")

        district_proposal = self.get_object()
        details = json.loads(request.POST.get("formData"))

        response.write(district_proposal.preview_approval(request, details))
        return response

    def get_object(self):
        return get_object_or_404(
            DistrictProposal, id=self.kwargs["district_proposal_pk"]
        )


from commercialoperator.components.proposals.utils import test_proposal_emails

class TestEmailView(UserPassesTestMixin, View):

    def test_func(self):
        return is_internal(self.request)
    
    def get(self, request, *args, **kwargs):
        test_proposal_emails(request)
        return HttpResponse("Test Email Script Completed")
