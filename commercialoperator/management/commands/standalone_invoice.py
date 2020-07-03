from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from ledger.accounts.models import EmailUser
from commercialoperator.components.bookings.utils import create_filming_fee_invoice
from commercialoperator.components.bookings.email import send_monthly_invoices_failed_tclass
from commercialoperator.components.proposals.models import Proposal
import datetime

import logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the Standalone Invoices Script - generates invoices'

    def handle(self, *args, **options):
        proposal = Proposal.objects.get(id=537)
        try:
            user = EmailUser.objects.get(email=settings.CRON_EMAIL)
        except:
            user = EmailUser.objects.create(email=settings.CRON_EMAIL, password='')

        logger.info('Running command {}'.format(__name__))
        invoice = create_filming_fee_invoice(proposal, user, offset_months=-1)

        if not invoice:
            # some invoices failed
            logger.info('Command {} failed. Invoice failed to generate for')
            #send_monthly_invoices_failed_tclass(failed_bookings)
        logger.info('Command {} completed'.format(__name__))
