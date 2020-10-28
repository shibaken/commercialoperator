import traceback
import os
import base64
import geojson
import json
from six.moves.urllib.parse import urlparse
from wsgiref.util import FileWrapper
from django.db.models import Q, Min
from django.db import transaction, connection
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework import viewsets, serializers, status, generics, views
from rest_framework.decorators import detail_route, list_route, renderer_classes, parser_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from django.core.cache import cache
from ledger.accounts.models import EmailUser, Address
from ledger.address.models import Country
from datetime import datetime, timedelta, date
from commercialoperator.components.proposals.utils import save_proponent_data,save_assessor_data, proposal_submit
from commercialoperator.components.proposals.models import searchKeyWords, search_reference, ProposalUserAction
from commercialoperator.utils import missing_required_fields
from commercialoperator.components.main.utils import check_db_connection

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from commercialoperator.components.main.models import Document, Region, District, Tenure, ApplicationType, RequiredDocument
from commercialoperator.components.proposals.models import (
	ProposalEventsParks,
    Proposal,
    AbseilingClimbingActivity,
    PreEventsParkDocument,
    ProposalPreEventsParks,
    ProposalEventsTrails,
)
from commercialoperator.components.proposals.serializers_event import (
    ProposalEventsParksSerializer,
    SaveProposalEventsParksSerializer,
    AbseilingClimbingActivitySerializer,
    ProposalPreEventsParksSerializer,
    SaveProposalPreEventsParksSerializer,
    ProposalEventsTrailsSerializer,
    SaveProposalEventsTrailsSerializer,
    
)

from commercialoperator.helpers import is_customer, is_internal
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from rest_framework.filters import BaseFilterBackend
import reversion
from reversion.models import Version
from collections import namedtuple

import logging
logger = logging.getLogger(__name__)




class ProposalEventsParksViewSet(viewsets.ModelViewSet):
    queryset = ProposalEventsParks.objects.all().order_by('id')
    serializer_class = ProposalEventsParksSerializer

    @detail_route(methods=['post'])
    def edit_park(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveProposalEventsParksSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            #instance = self.get_object()
            serializer = SaveProposalEventsParksSerializer(data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            instance=serializer.save()
            #instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_CREATE_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    @renderer_classes((JSONRenderer,))
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            EventsParkDocument.objects.get(id=request.data.get('id')).delete()
            return Response([dict(id=i.id, name=i.name,_file=i._file.url) for i in instance.filming_park_documents.all()])
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

class AbseilingClimbingActivityViewSet(viewsets.ModelViewSet):
    queryset = AbseilingClimbingActivity.objects.all().order_by('id')
    serializer_class = AbseilingClimbingActivitySerializer

    @detail_route(methods=['post'])
    def edit_abseiling_climbing(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = AbseilingClimbingActivitySerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_ABSEILING_CLIMBING_ACTIVITY.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

class ProposalPreEventsParksViewSet(viewsets.ModelViewSet):
    queryset = ProposalPreEventsParks.objects.all().order_by('id')
    serializer_class = ProposalPreEventsParksSerializer

    @detail_route(methods=['post'])
    def edit_park(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveProposalPreEventsParksSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_PRE_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            #instance = self.get_object()
            serializer = SaveProposalPreEventsParksSerializer(data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            instance=serializer.save()
            instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_CREATE_PRE_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    @renderer_classes((JSONRenderer,))
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            PreEventsParkDocument.objects.get(id=request.data.get('id')).delete()
            return Response([dict(id=i.id, name=i.name,_file=i._file.url) for i in instance.pre_event_park_documents.all()])
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

class ProposalEventsTrailsViewSet(viewsets.ModelViewSet):
    queryset = ProposalEventsTrails.objects.all().order_by('id')
    serializer_class = ProposalEventsTrailsSerializer

    @detail_route(methods=['post'])
    def edit_trail(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = SaveProposalEventsTrailsSerializer(instance, data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            #instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_EDIT_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            #instance = self.get_object()
            serializer = SaveProposalEventsTrailsSerializer(data=json.loads(request.data.get('data')))
            serializer.is_valid(raise_exception=True)
            instance=serializer.save()
            #instance.add_documents(request)
            instance.proposal.log_user_action(ProposalUserAction.ACTION_CREATE_EVENT_PARK.format(instance.id),request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))
