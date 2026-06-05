from django.core.management.base import BaseCommand
from django.conf import settings

from ledger_api_client.managed_models import SystemGroup, SystemGroupPermission
from ledger_api_client.ledger_models import UsersInGroup
from django.contrib.auth.models import Group

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Migrate ledger auth groups to localised system groups"

    def handle(self, *args, **options):

        auth_groups = [settings.ADMIN_GROUP]

        for group_name in auth_groups:
            logger.info("Transferring membership of auth group {} from ledger to local system groups... ".format(group_name))

            #first check if the system group exists
            system_group_qs = SystemGroup.objects.filter(name=group_name)
            if not SystemGroup.objects.filter(name=group_name).exists():
                system_group = SystemGroup.objects.create(name=group_name)
            else:
                system_group = system_group_qs.first()
            
            #get ledger group member ids
            group = Group.objects.filter(name=group_name)
            if group.exists():
                user_ids = UsersInGroup.objects.filter(group_id=group.first().id).values_list('emailuser_id', flat=True)

                #add member ids to system group    
                for user_id in user_ids:
                    SystemGroupPermission.objects.create(system_group=system_group, emailuser_id=user_id)