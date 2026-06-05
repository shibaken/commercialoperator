import traceback
import json
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, views, mixins
from rest_framework.decorators import renderer_classes, action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from commercialoperator.components.proposals.models import ProposalUserAction

from commercialoperator.components.proposals.models import (
    ProposalFilmingActivity,
    ProposalFilmingParks,
    Proposal,
    FilmingParkDocument,
)
from commercialoperator.components.proposals.serializers_filming import (
    ProposalFilmingParksSerializer,
    SaveProposalFilmingParksSerializer,
)

from commercialoperator.helpers import is_internal
from django.core.exceptions import PermissionDenied

import logging
logger = logging.getLogger(__name__)

from commercialoperator.components.proposals.api import user_can_edit

class ProposalFilmingParksViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = ProposalFilmingParks.objects.none()
    serializer_class = ProposalFilmingParksSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return ProposalFilmingParks.objects.all().order_by("id")
        else:
            user_orgs = [org.id for org in user.commercialoperator_organisations.all()]
            return ProposalFilmingParks.objects.filter(
                Q(proposal_id__org_applicant_id__in=user_orgs)
                | Q(proposal_id__submitter=user)
            ).order_by("id")

    @action(methods=["post"], detail=True)
    def edit_park(self, request, *args, **kwargs):
        try:
            instance = self.get_object()

            if not instance.proposal or not user_can_edit(request, instance.proposal):
                raise PermissionDenied

            serializer = SaveProposalFilmingParksSerializer(
                instance, data=json.loads(request.data.get("data"))
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            instance.add_documents(request)
            instance.proposal.log_user_action(
                ProposalUserAction.ACTION_EDIT_FILMING_PARK.format(instance.id), request.user
            )
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, "error_dict"):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                if hasattr(e, "message"):
                    raise serializers.ValidationError(e.message)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance.proposal or not user_can_edit(request, instance.proposal):
            raise PermissionDenied
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        try:
            proposal = Proposal.objects.get(id=json.loads(request.data.get("data"))["proposal"])
            if not proposal or not user_can_edit(request, proposal):
                raise PermissionDenied
            
            serializer = SaveProposalFilmingParksSerializer(
                data=json.loads(request.data.get("data"))
            )
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            instance.add_documents(request)
            instance.proposal.log_user_action(
                ProposalUserAction.ACTION_CREATE_FILMING_PARK.format(instance.id),
                request.user,
            )
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
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
    @renderer_classes((JSONRenderer,))
    def delete_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if not instance.proposal or not user_can_edit(request, instance.proposal):
                raise PermissionDenied
            FilmingParkDocument.objects.get(id=request.data.get("id")).delete()
            return Response(
                [
                    dict(id=i.id, name=i.name, _file=i._file.url)
                    for i in instance.filming_park_documents.all()
                ]
            )
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class FilmingActivityTabView(views.APIView):

    def get(self, request, format=None):
        container = {}
        film_type_choices = []
        purpose_choices = []
        sponsorship_choices = []
        film_usage_choices = []

        film_types = ProposalFilmingActivity.FILM_TYPE_CHOICES
        purpose = ProposalFilmingActivity.PURPOSE_CHOICES
        sponsorships = ProposalFilmingActivity.SPONSORSHIP_CHOICES
        film_usage = ProposalFilmingActivity.FILM_USE_CHOICES

        if film_types:
            for c in film_types:
                film_type_choices.append({"key": c[0], "value": c[1]})
        if purpose:
            for p in purpose:
                purpose_choices.append({"key": p[0], "value": p[1]})

        if sponsorships:
            for s in sponsorships:
                sponsorship_choices.append({"key": s[0], "value": s[1]})

        if film_usage:
            for f in film_usage:
                film_usage_choices.append({"key": f[0], "value": f[1]})

        container.update({"film_type_choices": film_type_choices})
        container.update({"purpose_choices": purpose_choices})
        container.update({"sponsorship_choices": sponsorship_choices})
        container.update({"film_usage_choices": film_usage_choices})

        return Response(container)
