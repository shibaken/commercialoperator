import traceback
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status, generics, views, mixins
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import PermissionDenied
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from ledger_api_client.ledger_models import EmailUserRO as EmailUser
from ledger_api_client.utils import get_all_organisation

from commercialoperator.components.approvals.serializers import EmailUserSerializer
from commercialoperator.components.permission.permission import organisation_permissions, InternalPermission, OrganisationRequestPermission
from commercialoperator.components.segregation.api import (
    LedgerOrganisationFilterBackend,
)
from commercialoperator.components.segregation.decorators import basic_exception_handler
from rest_framework_datatables.filters import DatatablesFilterBackend
from commercialoperator.components.segregation.utils import (
    filter_organisation_list,
    retrieve_delegate_organisation_ids,
    retrieve_email_user,
    retrieve_organisation_delegate_ids,
)
from commercialoperator.components.proposals.utils import (
    _get_params,
    search_in_emailuser_fields,
)
from commercialoperator.helpers import is_commercialoperator_admin, is_internal
from commercialoperator.components.organisations.models import (
    Organisation,
    OrganisationRequest,
    OrganisationRequestUserAction,
    OrganisationAccessGroup,
)

from commercialoperator.components.organisations.serializers import (
    OrganisationSerializer,
    OrganisationRequestSerializer,
    OrganisationRequestDTSerializer,
    OrganisationContactSerializer,
    OrganisationCheckSerializer,
    OrganisationPinCheckSerializer,
    OrganisationRequestActionSerializer,
    OrganisationActionSerializer,
    OrganisationRequestCommsSerializer,
    OrganisationCommsSerializer,
    OrgUserAcceptSerializer,
    OrganisationCheckExistSerializer,
    LedgerOrganisationFilterSerializer,
    OrganisationLogEntrySerializer,
    OrganisationRequestLogEntrySerializer,
)

class OrganisationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = Organisation.objects.none()
    serializer_class = OrganisationSerializer
    allow_external = False  # NOTE: Workaround for allowing organisations to be accessed when validating pins

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request) or self.allow_external:
            return Organisation.objects.all()
        else:
            user_orgs = retrieve_delegate_organisation_ids(user.id)
            return Organisation.objects.filter(organisation_id__in=user_orgs)

    def get_object(self):
        org_id = self.kwargs.get("pk", None)
        if not org_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "An Organisation PK is required"},
            )

        is_ledger_org_query = bool(self.request.POST.get("is_ledger_org_query", False))
        if is_ledger_org_query:
            try:
                return self.get_queryset().get(organisation_id=org_id)
            except Organisation.DoesNotExist:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={
                        "message": f"Organisation with ledger id {org_id} not found not found in COLS"
                    },
                )
        else:
            try:
                return super().get_object()
            except Organisation.DoesNotExist:
                raise serializers.ValidationError(
                    {
                        "message": f"Organisation does not exist in COLS.{"Did you attempt to query a ledger organisation in COLS?" if not is_ledger_org_query else ""}"
                    }
                )
            except serializers.ValidationError:
                raise serializers.ValidationError(
                    {"message": "Organisation does not exist"}
                )

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def contacts(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrganisationContactSerializer(
                instance.contacts.exclude(user_status="pending"), many=True
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

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    @basic_exception_handler
    def contacts_exclude(self, request, *args, **kwargs):
        ledger_organisation_id = kwargs.get("pk", None)
        if not ledger_organisation_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "An Organisation ID is required"},
            )

        try:
            cols_organisation = Organisation.objects.get(
                organisation_id=ledger_organisation_id
            )
        except Organisation.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "Organisation not found"},
            )

        contacts = cols_organisation.contacts.exclude(user_status="draft")
        serializer = OrganisationContactSerializer(contacts, many=True)

        return Response(serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @basic_exception_handler
    def validate_pins(self, request, *args, **kwargs):
        self.allow_external = True
        instance = self.get_object()
        serializer = OrganisationPinCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ret = instance.validate_pins(
            serializer.validated_data["pin1"],
            serializer.validated_data["pin2"],
            request,
        )

        if ret == None:
            # user has already been to this organisation - don't add again
            data = {"valid": ret}
            return Response({"valid": "User already exists"})

        data = {"valid": ret}
        if data["valid"]:
            # Notify each Admin member of request.
            instance.send_organisation_request_link_notification(request)
        return Response(data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def accept_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied

            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.accept_user(user_obj, request)
            serializer = self.get_serializer(instance)
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
    )
    def accept_declined_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.accept_declined_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def decline_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.decline_user(user_obj, request)
            serializer = self.get_serializer(instance)
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
    )
    @basic_exception_handler
    def unlink_user(self, request, *args, **kwargs):
        instance = self.get_object()
        if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
            raise PermissionDenied
        user_obj = self.request.user
        user_data = EmailUserSerializer(user_obj.id).data
        serializer = OrgUserAcceptSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)

        instance.unlink_user(user_obj, request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def make_admin_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.make_admin_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def make_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.make_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def make_consultant(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.make_consultant(user_obj, request)
            serializer = self.get_serializer(instance)
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
    )
    def suspend_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.suspend_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    def reinstate_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
                raise PermissionDenied
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data["email"].lower()
            )
            instance.reinstate_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @action(
        methods=[
            "POST",
        ],
        detail=True,
    )
    @basic_exception_handler
    def relink_user(self, request, *args, **kwargs):
        instance = self.get_object()
        if not organisation_permissions(request, instance.organisation_id) and not is_commercialoperator_admin(request):
            raise PermissionDenied
        serializer = OrgUserAcceptSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = EmailUser.objects.get(
            email=serializer.validated_data["email"].lower()
        )
        instance.relink_user(user_obj, request)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #TODO remove or refactor action and comms log funcs
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
            serializer = OrganisationActionSerializer(qs, many=True)
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
            serializer = OrganisationCommsSerializer(qs, many=True)
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
    @basic_exception_handler
    @transaction.atomic
    def add_comms_log(self, request, *args, **kwargs):
        instance = self.get_object()
        mutable = request.data._mutable
        request.data._mutable = True
        request.data["organisation"] = "{}".format(instance.id)
        request.data["staff_id"] = "{}".format(request.user.id)
        request.data._mutable = mutable
        serializer = OrganisationLogEntrySerializer(data=request.data)
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

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    @basic_exception_handler
    def existence(self, request, *args, **kwargs):
        serializer = OrganisationCheckSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get("name", None)
        abn = serializer.validated_data.get("abn", None)
        data = Organisation.existence(name, abn)
        # Check request user cannot be relinked to org.
        data.update([("user", request.user.id)])
        data.update([("abn", request.data["abn"])])
        serializer = OrganisationCheckExistSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def organisation_lookup(self, request, *args, **kwargs):
        self.allow_external = True
        filtered_organisations = filter_organisation_list(
            self, request, *args, **kwargs
        )
        organisation_ids = [o.organisation_id for o in filtered_organisations]
        organisations = self.get_queryset().filter(organisation_id__in=organisation_ids)

        data_transform = [
            {
                "id": organisation.id,
                "text": f"{organisation.name} (ABN: {organisation.abn})",
                "first_five": organisation.first_five,
            }
            for organisation in organisations
        ]
        return Response({"results": data_transform})

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    @basic_exception_handler
    def linked_organisation(self, request, *args, **kwargs):
        org_id = request.GET.get("org_id", None)
        if not org_id:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "An Organisation ID is required"},
            )
        try:
            org = self.get_queryset().get(organisation_id=org_id)
        except Organisation.DoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": f"Organisation with ledger id {org_id} not found"},
            )
        else:
            if not organisation_permissions(request, org_id) and not is_commercialoperator_admin(request):
                return Response(
                    status=status.HTTP_403_FORBIDDEN,
                    data={
                        "message": "You do not have permission to view this organisation."
                    },
                )

        serializer = OrganisationSerializer(org, context={"request": request})

        return Response(serializer.data)


class OrganisationListFilterView(generics.ListAPIView):
    queryset = Organisation.objects.none()
    serializer_class = LedgerOrganisationFilterSerializer
    filter_backends = (LedgerOrganisationFilterBackend,)
    search_fields = (
        "organisation_name",
        "organisation_trading_name",
        "organisation_abn",
    )
    permission_classes=[InternalPermission]

    def get_queryset(self):
        org_list = Organisation.objects.all().values_list("organisation_id", flat=True)
        return Organisation.objects.filter(id__in=org_list)

    def list(self, request, *args, **kwargs):
        from commercialoperator.components.segregation.serializers import (
            OrganisationListSerializer,
        )

        organisations = filter_organisation_list(self, request, *args, **kwargs)
        serializer = OrganisationListSerializer(
            organisations, many=True, context={"request": request}
        )

        return Response(serializer.data)


class OrganisationRequestDatatableFilterBackend(DatatablesFilterBackend):
    def filter_queryset(self, request, queryset, view):
        total_count = queryset.count()
        params = _get_params(request)

        search_value = (params.get("search[value]") or "").strip()

        if search_value:
            matching_ids = search_in_emailuser_fields(search_value)

            if matching_ids:
                if is_internal(request):
                    queryset = queryset.filter(
                        Q(requester__in=matching_ids) | Q(assigned_officer_id__in=matching_ids) | Q(name__icontains=search_value)
                )
                else:
                    queryset = queryset.filter(
                        Q(requester__in=matching_ids) | Q(name__icontains=search_value)
                    )
            else:
                queryset = queryset.filter(
                    Q(name__icontains=search_value)
                )

        role = (params.get("datatable_filter_role")).strip() if params.get("datatable_filter_role") else None
        status = (params.get("datatable_filter_status")).strip() if params.get("datatable_filter_status") else None

        if role and role.lower() != "all":
            queryset = queryset.filter(role=role)
        if status and status.lower() != "all":
            queryset = queryset.filter(status=status)

        setattr(view, "_datatables_total_count", total_count)

        return queryset


class OrganisationRequestsViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = OrganisationRequest.objects.none()
    serializer_class = OrganisationRequestSerializer
    filter_backends = (OrganisationRequestDatatableFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    page_size = 10
    ordering = ("lodgement_date",)
    

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return OrganisationRequest.objects.all()
        else:
            user_org_ids = retrieve_delegate_organisation_ids(user.id)
            user_organisations = Organisation.objects.filter(
                organisation_id__in=user_org_ids
            )
            user_organisation_abns = [org.abn for org in user_organisations]

            # NOTE: Adding organisation requests where the user is a delegate here, on top of being a requester
            return OrganisationRequest.objects.filter(
                Q(abn__in=user_organisation_abns) | Q(requester_id=user)
            )

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    def filter_list(self, request, *args, **kwargs):

        statuses = [
            dict(search_term=i[0], value=i[1])
            for i in OrganisationRequest.STATUS_CHOICES
        ]
        roles = [i[1] for i in OrganisationRequest.ROLE_CHOICES]

        data = dict(
            status_choices=statuses,
            role_choices=roles,
        )
        return Response(data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    @basic_exception_handler
    def linked_organisations(self, request, *args, **kwargs):
        user_id = request.user.id
        qs = self.get_queryset()

        # Ledger organisation ids
        ledger_org_ids = []
        # Get all organisations from ledger in advance to not otherwise query ledger in each loop
        all_organisations_response = get_all_organisation()
        if all_organisations_response.get("status") != status.HTTP_200_OK:
            raise serializers.ValidationError(
                "Error fetching organisations from ledger"
            )
        ledger_organisation_data = all_organisations_response.get("data", [])
        # Retrieve ledger organisation ids by ABN for which there is an organisation request
        organisation_request_abns = [org_req.abn for org_req in qs]
        ledger_org_ids = [
            d["organisation_id"]
            for d in ledger_organisation_data
            if d["organisation_abn"] in organisation_request_abns
        ]
        ledger_org_ids = list(set(ledger_org_ids))
        # Get COLS organisation ids for the ledger organisation ids (there is no abn field in organisation model, so have to take a little detour)
        organisation_ids = Organisation.objects.filter(
            organisation_id__in=ledger_org_ids
        ).values_list("id", flat=True)
        # Of those, get the COLS organisation ids where the user is a delegate
        user_delegate_organisation_ids = [
            oid
            for oid in organisation_ids
            if user_id in retrieve_organisation_delegate_ids(oid)
        ]
        # Get the organisation ABNs for the user delegate organisations
        organisation_abns = [
            org.abn
            for org in Organisation.objects.filter(
                id__in=user_delegate_organisation_ids
            )
        ]

        serializer = OrganisationRequestSerializer(
            qs.filter(abn__in=organisation_abns),
            context={"request": request},
            many=True,
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
        permission_classes=[InternalPermission]
    )
    @basic_exception_handler
    def datatable_list(self, request, *args, **kwargs):

        qs = self.get_queryset()
        qs = self.filter_queryset(qs)
        
        result_page = self.paginator.paginate_queryset(qs, request)
        
        serializer = OrganisationRequestDTSerializer(result_page, context={"request": request}, many=True)

        return self.paginator.get_paginated_response(serializer.data)

    
    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[OrganisationRequestPermission]
    )
    @basic_exception_handler
    def assign_request_user(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.assign_to(request.user, request)
        serializer = OrganisationRequestSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[OrganisationRequestPermission]
    )
    @basic_exception_handler
    def unassign(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.unassign(request)
        serializer = OrganisationRequestSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[OrganisationRequestPermission]
    )
    @basic_exception_handler
    def accept(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.accept(request)
        serializer = OrganisationRequestSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
        permission_classes=[OrganisationRequestPermission]
    )
    def decline(self, request, *args, **kwargs):
        instance = self.get_object()
        reason = ""
        instance.decline(reason, request)
        serializer = OrganisationRequestSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

    @action(
        methods=[
            "POST",
        ],
        detail=True,
        permission_classes=[OrganisationRequestPermission]
    )
    @basic_exception_handler
    def assign_to(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = request.data.get("user_id", None)
        user = None
        if not user_id:
            raise serializers.ValiationError("A user id is required")
        try:
            user = EmailUser.objects.get(id=user_id)
        except EmailUser.DoesNotExist:
            raise serializers.ValidationError(
                "A user with the id passed in does not exist"
            )
        instance.assign_to(user, request)
        serializer = OrganisationRequestSerializer(
            instance, context={"request": request}
        )
        return Response(serializer.data)

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
            serializer = OrganisationRequestActionSerializer(qs, many=True)
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
            serializer = OrganisationRequestCommsSerializer(qs, many=True)
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
    @basic_exception_handler
    @transaction.atomic
    def add_comms_log(self, request, *args, **kwargs):
        instance = self.get_object()
        mutable = request.data._mutable
        request.data._mutable = True
        request.data["organisation"] = "{}".format(instance.id)
        request.data["request"] = "{}".format(instance.id)
        request.data["staff_id"] = "{}".format(request.user.id)
        request.data._mutable = mutable
        serializer = OrganisationRequestLogEntrySerializer(data=request.data)
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

    @basic_exception_handler
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["requester"] = request.user
        if request.data["role"] == "consultant":
            # Check if consultant can be relinked to org.
            data = Organisation.existence(request.data["abn"])
            data.update([("user", request.user.id)])
            data.update([("abn", request.data["abn"])])
            existing_org = OrganisationCheckExistSerializer(data=data)
            existing_org.is_valid(raise_exception=True)
        with transaction.atomic():
            instance = serializer.save()
            instance.log_user_action(
                OrganisationRequestUserAction.ACTION_LODGE_REQUEST.format(instance.id),
                request.user,
            )
            instance.send_organisation_request_email_notification(request)
        return Response(serializer.data)


class OrganisationAccessGroupMembersView(views.APIView):

    renderer_classes = [
        JSONRenderer,
    ]
    permission_classes=[InternalPermission]

    def get(self, request, format=None):
        members = []
        if is_internal(request):
            group = OrganisationAccessGroup.objects.first()
            if group:
                for m in group.all_members:
                    emailuser = retrieve_email_user(m)
                    if emailuser:
                        full_name = f"{emailuser.first_name} {emailuser.last_name}"
                        members.append(
                            {
                                "name": full_name,
                                "id": m,
                            }
                        )
            else:
                for m in EmailUser.objects.filter(
                    is_superuser=True, is_staff=True, is_active=True
                ):
                    emailuser = retrieve_email_user(m)
                    if emailuser:
                        full_name = f"{emailuser.first_name} {emailuser.last_name}"
                        members.append({"name": full_name, "id": m.id})
        return Response(members)