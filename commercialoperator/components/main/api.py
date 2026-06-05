from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from commercialoperator.components.main.models import (
    Region,
    District,
    ApplicationType,
    ActivityMatrix,
    AccessType,
    Park,
    Trail,
    ActivityCategory,
    Activity,
    RequiredDocument,
    Question,
    GlobalSettings,
)
from commercialoperator.components.main.serializers import (
    RegionSerializer,
    DistrictSerializer,
    ApplicationTypeSerializer,
    ActivityMatrixSerializer,
    AccessTypeSerializer,
    ParkSerializer,
    TrailSerializer,
    ActivitySerializer,
    ActivityCategorySerializer,
    RequiredDocumentSerializer,
    QuestionSerializer,
    GlobalSettingsSerializer,
    LandActivityTabSerializer,
    MarineActivityTabSerializer,
    EventsParkSerializer,
    TrailTabSerializer,
    FilmingParkSerializer,
    EventsTabSerializer,
)
from django.db.models import Q
from collections import namedtuple

import logging

logger = logging.getLogger("payment_checkout")


class DistrictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = District.objects.none()

    serializer_class = DistrictSerializer 
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = District.objects.all().order_by("id")
            return queryset
        return District.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def land_parks(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.land_parks
        qs.order_by("id")
        serializer = ParkSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def parks(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.parks
        qs.order_by("id")
        serializer = ParkSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all().order_by("id")
    serializer_class = RegionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Region.objects.all().order_by("id")
            return queryset
        return Region.objects.none()


class ActivityMatrixViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityMatrix.objects.none()
    serializer_class = ActivityMatrixSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            activity_matrix = ActivityMatrix.objects.filter(
                name="Commercial Operator"
            ).order_by("-version")
            if not activity_matrix.exists():
                return ActivityMatrix.objects.none()
            return [
                ActivityMatrix.objects.filter(name="Commercial Operator")
                .order_by("-version")
                .first()
            ]
        return ActivityMatrix.objects.none()


class ApplicationTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ApplicationType.objects.none()
    serializer_class = ApplicationTypeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return ApplicationType.objects.order_by("order").filter(visible=True)
        return ApplicationType.objects.none()


class AccessTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AccessType.objects.none()
    serializer_class = AccessTypeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return AccessType.objects.all().order_by("id")
        return AccessType.objects.none()


class GlobalSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalSettings.objects.none
    serializer_class = GlobalSettingsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = GlobalSettings.objects.all().order_by("id")
            return queryset
        return GlobalSettings.objects.none()


class LandActivityTabViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing the various serialized viewsets in a single container
    """

    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            # Container = namedtuple('ActivityLandTab', ('access_types', 'activity_types', 'regions'))
            trails_allowed_activities_id = (
                Trail.objects.all()
                .order_by("allowed_activities")
                .values_list("allowed_activities", flat=True)
                .distinct()
            )
            trail_activity_types = Activity.objects.filter(
                id__in=trails_allowed_activities_id
            )
            Container = namedtuple(
                "ActivityLandTab",
                (
                    "access_types",
                    "land_activity_types",
                    "trail_activity_types",
                    "marine_activity_types",
                    "trails",
                    "marine_activities",
                    "land_required_documents",
                    "regions",
                ),
            )
            container = Container(
                access_types=AccessType.objects.all().order_by("id"),
                land_activity_types=Activity.objects.filter(
                    activity_category__activity_type="land"
                ).order_by("id"),
                trail_activity_types=trail_activity_types,
                marine_activity_types=Activity.objects.filter(
                    activity_category__activity_type="marine"
                ).order_by("id"),
                trails=Trail.objects.all().order_by("id"),
                marine_activities=ActivityCategory.objects.filter(
                    activity_type="marine"
                ).order_by("id"),
                land_required_documents=RequiredDocument.objects.filter().order_by(
                    "id"
                ),
                regions=Region.objects.all().order_by("id"),
            )
            # print(container)
            serializer = LandActivityTabSerializer(container)
            return Response(serializer.data)
        else:
            Container = namedtuple("ActivityLandTab", ())
            container = Container()
            serializer = LandActivityTabSerializer(container)
            return Response(serializer.data)


class MarineActivityTabViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing the various serialized viewsets in a single container
    """

    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            # Container = namedtuple('ActivityLandTab', ('access_types', 'activity_types', 'regions'))
            Container = namedtuple(
                "ActivityMarineTab",
                (
                    "marine_activities",
                    "marine_parks",
                    "required_documents",
                    "marine_parks_external",
                ),
            )
            container = Container(
                # marine_activity_types=Activity.objects.filter(activity_category__activity_type='marine').order_by('id'),
                marine_activities=ActivityCategory.objects.filter(
                    activity_type="marine"
                ).order_by("id"),
                # marine_parks=ActivityCategory.objects.filter(activity_type='marine').order_by('id'),
                marine_parks=Park.objects.filter(park_type="marine").order_by("id"),
                required_documents=RequiredDocument.objects.filter().order_by("id"),
                marine_parks_external=Park.objects.filter(park_type="marine")
                .exclude(visible_to_external=False)
                .order_by("id"),
            )
            serializer = MarineActivityTabSerializer(container)
            return Response(serializer.data)
        else:
            Container = namedtuple("ActivityMarineTab", ())
            container = Container()
            serializer = MarineActivityTabSerializer(container)
            return Response(serializer.data)


class ParkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Park.objects.none()
    serializer_class = ParkSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Park.objects.all().order_by("id")
            return queryset
        return Park.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def events_parks_list(self, request, *args, **kwargs):
        serializer = EventsParkSerializer(
            self.get_queryset(), context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def filming_parks_list(self, request, *args, **kwargs):
        serializer = FilmingParkSerializer(
            self.get_queryset(), context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def filming_parks_external_list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        new_qs = qs.exclude(visible_to_external=False)
        serializer = FilmingParkSerializer(
            new_qs, context={"request": request}, many=True
        )
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def marine_parks(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(park_type="marine")
        serializer = ParkSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def land_parks(self, request, *args, **kwargs):
        qs = self.get_queryset().filter(park_type="land")
        serializer = ParkSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def allowed_activities(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.allowed_activities.all()
        serializer = ActivitySerializer(qs, context={"request": request}, many=True)
        # serializer = ActivitySerializer(qs)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def allowed_access(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.allowed_access.all()
        serializer = AccessTypeSerializer(qs, context={"request": request}, many=True)
        # serializer = ActivitySerializer(qs)
        return Response(serializer.data)


class TrailViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trail.objects.none()
    serializer_class = TrailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            queryset = Trail.objects.all().order_by("id")
            return queryset
        return Trail.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=True,
    )
    def allowed_activities(self, request, *args, **kwargs):
        instance = self.get_object()
        qs = instance.allowed_activities.all()
        serializer = ActivitySerializer(qs, context={"request": request}, many=True)
        # serializer = ActivitySerializer(qs)
        return Response(serializer.data)


class LandActivitiesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.none()
    serializer_class = ActivitySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            categories = ActivityCategory.objects.filter(activity_type="land")
            activities = Activity.objects.filter(
                Q(activity_category__in=categories) & Q(visible=True)
            )
            return activities
        return Activity.objects.none()


class MarineActivitiesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ActivityCategory.objects.none()
    serializer_class = ActivityCategorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            categories = ActivityCategory.objects.filter(activity_type="marine")
            return categories
        return ActivityCategory.objects.none()


class RequiredDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RequiredDocument.objects.none()
    serializer_class = RequiredDocumentSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return RequiredDocument.objects.all()
        return RequiredDocument.objects.none()


class QuestionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Question.objects.none()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Question.objects.all()
        return Question.objects.none()

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def tclass_questions_list(self, request, *args, **kwargs):
        qs = Question.objects.filter(application_type__name=ApplicationType.TCLASS)
        serializer = QuestionSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)

    @action(
        methods=[
            "GET",
        ],
        detail=False,
    )
    def events_questions_list(self, request, *args, **kwargs):
        qs = Question.objects.filter(application_type__name=ApplicationType.EVENT)
        serializer = QuestionSerializer(qs, context={"request": request}, many=True)
        return Response(serializer.data)


# To display only trails and activity types on Event activity tab
class TrailTabViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing the various serialized viewsets in a single container
    """

    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            Container = namedtuple(
                "TrailTab",
                (
                    "land_activity_types",
                    "trails",
                    "event_activity_types",
                ),
            )
            container = Container(
                land_activity_types=Activity.objects.filter(
                    activity_category__activity_type="land"
                ).order_by("id"),
                trails=Trail.objects.all().order_by("id"),
                event_activity_types=Activity.objects.filter(
                    activity_category__activity_type="event"
                ).order_by("id"),
            )
            serializer = TrailTabSerializer(container)
            return Response(serializer.data)
        else:
            Container = namedtuple("TrailTab", ())
            container = Container()
            serializer = TrailTabSerializer(container)
            return Response(serializer.data)


# To display only trails and activity types on Event activity tab
class EventsParkTabViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for listing the various serialized viewsets in a single container
    """

    def list(self, request):
        user = self.request.user
        if user.is_authenticated:
            Container = namedtuple(
                "EventTab", ("parks", "event_activity_types", "parks_external")
            )
            container = Container(
                parks=Park.objects.all().order_by("id"),
                parks_external=Park.objects.all()
                .exclude(visible_to_external=False)
                .order_by("id"),
                event_activity_types=Activity.objects.filter(
                    activity_category__activity_type="event"
                ).order_by("id"),
            )
            serializer = EventsTabSerializer(container)
            return Response(serializer.data)
        else:
            Container = namedtuple("EventTab", ())
            container = Container()
            serializer = EventsTabSerializer(container)
            return Response(serializer.data)
