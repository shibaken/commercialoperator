import traceback
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q, Value
from django.db.models.functions import Concat
from django.db import transaction
from django.core.exceptions import ValidationError
from django_countries import countries
from rest_framework import viewsets, serializers, generics, views, mixins, filters
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.api import get_account_details
from commercialoperator.components.organisations.models import OrganisationRequest
from commercialoperator.components.segregation.decorators import basic_exception_handler

from commercialoperator.components.users.serializers import (
    UserSerializer,
    UserFilterSerializer,
    EmailUserActionSerializer,
    EmailUserCommsSerializer,
    EmailUserLogEntrySerializer,
    UserSystemSettingsSerializer,
)
from commercialoperator.components.organisations.serializers import (
    OrganisationRequestDTSerializer,
)
from commercialoperator.components.main.models import UserSystemSettings
from commercialoperator.helpers import is_internal

from commercialoperator.components.permission.permission import InternalPermission

import logging

logger = logging.getLogger(__name__)

class GetCountries(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        country_list = cache.get(settings.CACHE_KEY_COUNTRY_LIST)
        if not country_list:
            country_list = []
            for country in list(countries):
                country_list.append({"name": country.name, "code": country.code})
            cache.set(
                settings.CACHE_KEY_COUNTRY_LIST,
                country_list,
                settings.CACHE_TIMEOUT_2_HOURS,
            )

        return Response(country_list)


class GetProfile(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class UserListFilterBackend(filters.SearchFilter):
    def filter_queryset(self, request, queryset, view):
        search_fields = view.search_fields
        search_term = request.GET.get("search", "")
        if search_term is None:
            logger.debug("No user search term provided")
            return queryset
        if len(search_term) <= 1:
            logger.debug("User search term too short")
            return []

        search_dict = {f"{field}__icontains": search_term for field in search_fields}

        if all(f in search_fields for f in ["first_name", "last_name"]):
            queryset = queryset.annotate(
                full_name=Concat("first_name", Value(" "), "last_name")
            )
            search_dict["full_name__icontains"] = search_term

        return queryset.filter(Q(**search_dict, _connector=Q.OR))[:10]


class UserListFilterView(generics.ListAPIView):

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return EmailUser.objects.all()
        else:
            qs = EmailUser.objects.filter(Q(id=user.id))
            return qs

    @basic_exception_handler
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        if not is_internal(request):
            serializer = self.serializer_class(queryset, many=True)
        else:
            serializer = self.serializer_class(queryset, many=True)

        return Response(serializer.data)

    queryset = get_queryset
    serializer_class = UserFilterSerializer
    filter_backends = (UserListFilterBackend,)
    search_fields = ("email", "first_name", "last_name")
    permission_classes = [InternalPermission]


class UserViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = EmailUser.objects.none()
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return EmailUser.objects.all()
        else:
            qs = EmailUser.objects.filter(Q(id=user.id))
            return qs

    #TODO is this supposed to be internal only? (current template appears to indicate that)
    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @basic_exception_handler
    def update_system_settings(self, request, *args, **kwargs):
        instance = self.get_object()
        user_setting, created = UserSystemSettings.objects.get_or_create(user=instance)
        serializer = UserSystemSettingsSerializer(user_setting, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        instance = self.get_object()
        serializer = UserSerializer(instance, context={"request": request})
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def pending_org_requests(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            requester_id = instance.id
            serializer = OrganisationRequestDTSerializer(
                OrganisationRequest.objects.filter(
                    status="with_assessor", requester_id=requester_id
                ),
                many=True,
                context={"request": request},
            )
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    #TODO remove or replace comms/action log for user
    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = EmailUserActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = EmailUserCommsSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[InternalPermission]
    )
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                mutable = request.data._mutable
                request.data._mutable = True
                request.data["emailuser"] = "{}".format(instance.id)
                request.data["staff"] = "{}".format(request.user.id)
                request.data._mutable = mutable
                serializer = EmailUserLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    comms.documents.create(
                        name = str(request.FILES[f]),
                        _file = request.FILES[f]
                    )
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    def get_department_users(self, request, *args, **kwargs):
        try:
            search_term = request.GET.get("term", "")
            data = (
                self.get_queryset()
                .filter(is_staff=True)
                .filter(
                    Q(first_name__icontains=search_term)
                    | Q(last_name__icontains=search_term)
                )
                .values("email", "first_name", "last_name")[:10]
            )
            data_transform = [
                {
                    "id": person["email"],
                    "text": person["first_name"] + " " + person["last_name"],
                }
                for person in data
            ]
            return Response({"results": data_transform})
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

#TODO determine if the below are needed (or at least if they can be refactored)
class GetLedgerAccount(views.APIView):
    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({"error": "User is not logged in."})
        response = get_account_details(request, str(request.user.id))
        return response

class GetRequestUserID(views.APIView):
    """Yes, this is a bit silly but for now the get_account_details from ledger_api_client doesn't return the
    request user id"""

    renderer_classes = [
        JSONRenderer,
    ]

    def get(self, request, format=None):
        if request.user.is_anonymous:
            return Response({"id": None, "is_internal": False})
        return Response({"id": request.user.id, "is_internal": is_internal(request)})
