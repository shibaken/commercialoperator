from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from datetime import datetime, timedelta, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from commercialoperator.components.main.models import Park, ApplicationType
from commercialoperator.components.proposals.models import Proposal, ProposalUserAction
from commercialoperator.components.organisations.models import Organisation
from commercialoperator.components.bookings.models import (
    Booking,
    ParkBooking,
    BookingInvoice,
    ApplicationFee,
    ComplianceFee,
    FilmingFee,
    FilmingFeeInvoice,
)

from commercialoperator.components.bookings.email import (
    send_invoice_tclass_email_notification,
    send_monthly_confirmation_tclass_email_notification,
    send_confirmation_tclass_email_notification,
    send_monthly_invoice_tclass_email_notification,
)
from ledger.checkout.utils import create_basket_session, create_checkout_session, calculate_excl_gst, createCustomBasket
from ledger.payments.invoice.utils import CreateInvoiceBasket
from ledger.accounts.models import EmailUser
from ledger.payments.models import Invoice
from ledger.payments.utils import oracle_parser
import json
import ast
from decimal import Decimal



import logging
logger = logging.getLogger('payment_checkout')


def create_filming_fee_invoice(proposal, user, offset_months=-1):

    products = [{
        u'ledger_description': u'Helena and Aurora Range Conservation Park - 2020-07-02 - Adult',
        u'oracle_code': u'NNP487 GST',
        u'price_excl_tax': Decimal('9.090909090909'),
        u'price_incl_tax': Decimal('10.00'),
        u'quantity': 2
    }]

    invoice = None
    with transaction.atomic():
        #if is_invoicing_period(booking) and is_monthly_invoicing_allowed(booking):
        if True:
            try:
                logger.info('Creating standalone invoice')

                #import ipdb; ipdb.set_trace()
                payment_method = 'other'
                invoice_text = 'Payment Invoice'
                basket  = createCustomBasket(products, user, settings.PAYMENT_SYSTEM_ID)
                order = CreateInvoiceBasket(
                    payment_method=payment_method, system=settings.PAYMENT_SYSTEM_PREFIX
                ).create_invoice_and_order(basket, 0, None, None, user=user, invoice_text=invoice_text)

                invoice = Invoice.objects.get(order_number=order.number)

                deferred_payment_date = invoice.created + relativedelta(months=1)
                filming_fee = FilmingFee.objects.create(proposal=proposal, created_by=user, payment_type=FilmingFee.PAYMENT_TYPE_BLACK, deferred_payment_date=deferred_payment_date)
                filming_fee_inv = FilmingFeeInvoice.objects.create(filming_fee=filming_fee, invoice_reference=invoice.reference)
#                deferred_payment_date = calc_payment_due_date(booking, invoice.created + relativedelta(months=1))
#                book_inv = BookingInvoice.objects.create(booking=booking, invoice_reference=invoice.reference, payment_method=invoice.payment_method, deferred_payment_date=deferred_payment_date)
#
#                recipients = list(set([booking.proposal.applicant_email, user.email])) # unique list
#                send_monthly_invoice_tclass_email_notification(user, booking, invoice, recipients=recipients)
#                ProposalUserAction.log_action(booking.proposal,ProposalUserAction.ACTION_SEND_MONTHLY_INVOICE.format(invoice.reference, booking.proposal.id, ', '.join(recipients)), user)
            except Exception, e:
                logger.error('Failed to create standalone invoice')
                logger.error('{}'.format(e))

    return invoice


