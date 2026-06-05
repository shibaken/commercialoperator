from commercialoperator.components.organisations.models import Organisation
from commercialoperator.components.proposals.views import InternalHistoryCompareDetailView

class OrganisationHistoryCompareView(InternalHistoryCompareDetailView):
    """
    View for reversion_compare
    """
    model = Organisation
    template_name = 'commercialoperator/reversion_history.html'
