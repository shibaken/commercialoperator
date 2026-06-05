from django.conf import settings
from commercialoperator import helpers

def commercialoperator_url(request):
    template_group = 'commercialoperator'
    TERMS = "/know/online-commercialoperator-booking-terms-and-conditions"

    is_admin = False

    if request.user.is_authenticated:
        is_admin = helpers.is_commercialoperator_admin(request)

    return {
        'EXPLORE_PARKS_SEARCH': '/external/payment',
        'EXPLORE_PARKS_CONTACT': '/contact-us',
        'EXPLORE_PARKS_ENTRY_FEES': '/know/entry-fees',
        'EXPLORE_PARKS_TERMS': TERMS,
        'DEV_STATIC': settings.DEV_STATIC,
        'DEV_STATIC_URL': settings.DEV_STATIC_URL,
        'TEMPLATE_GROUP' : template_group,
        'SYSTEM_NAME' : settings.SYSTEM_NAME,
        'IS_ADMIN' : is_admin,
        'PUBLIC_URL' : settings.PUBLIC_URL,
        }


def template_context(request):
    """Pass extra context variables to every template.
    """
    context = commercialoperator_url(request)
    return context



