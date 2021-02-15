from rest_framework import serializers
from django.db.models import Sum, Max
from commercialoperator.components.main.models import CommunicationsLogEntry, Region, District, Tenure, ApplicationType, ActivityMatrix, AccessType, Park, Trail, Activity, ActivityCategory, Section, Zone, RequiredDocument, Question, GlobalSettings #, ParkPrice
from commercialoperator.components.proposals.models import  ProposalParkActivity
from commercialoperator.components.bookings.models import  ParkBooking
from ledger.accounts.models import EmailUser
from datetime import datetime, date
#from commercialoperator.components.proposals.serializers import ProposalTypeSerializer

class CommunicationLogEntrySerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=EmailUser.objects.all(),required=False)
    documents = serializers.SerializerMethodField()
    class Meta:
        model = CommunicationsLogEntry
        fields = (
            'id',
            'customer',
            'to',
            'fromm',
            'cc',
            'type',
            'reference',
            'subject'
            'text',
            'created',
            'staff',
            'proposal'
            'documents'
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'visible', 'doc_url')

class ActivitySerializer(serializers.ModelSerializer):
    #node_id = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    node_id = serializers.SerializerMethodField()
    class Meta:
        model = Activity
        fields = ('id', 'name', 'last_leaf', 'node_id')

    #def get_node_id(self, obj):
    #    return '{}_{}_id-{}'.format(obj.activity_category.name.replace(' ',''), obj.name.replace(' ',''), obj.id)

    def get_last_leaf(self, obj):
        return True

    def get_node_id(self, obj):
        """ Pulled from parent (out serializer) --> ZoneSerializer
        """
        first_level = self.context.get('park_id')
        second_level = self.context.get('zone_id')
        third_level = obj.id
        return '{}_{}_{}'.format(first_level, second_level, third_level)


class ZoneSerializer(serializers.ModelSerializer):
    label = serializers.SerializerMethodField()
    park_id = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    #allowed_zone_activities=ActivitySerializer(many=True, source='allowed_activities')
    allowed_zone_activities = serializers.SerializerMethodField()
    #children=ActivitySerializer(many=True, source='allowed_activities', context={'request': self.context.get('request'), 'customer_id': obj.id})
    #children=ActivitySerializer(many=True, source='allowed_activities')
    #children = serializers.SerializerMethodField()

    class Meta:
        model = Zone
        #fields = ('id', 'name', 'can_edit', 'last_leaf','visible', 'children')
        fields = ('id', 'name', 'label', 'park_id', 'can_edit', 'last_leaf','visible', 'allowed_zone_activities', 'allowed_activities_ids')

    def get_can_edit(self, obj):
        return True

    def get_last_leaf(self, obj):
        return True

    def get_label(self, obj):
        """ Pulled from parent (out serializer) --> ZoneSerializer
        """
        return '{} - {}'.format(self.context.get('parent_name'), obj.name) if self.context.get('parent_id') else obj.name

    def get_park_id(self, obj):
        """ Pulled from parent (out serializer) --> ZoneSerializer
        """
        return self.context.get('parent_id')

    def get_allowed_zone_activities(self, obj):
        """ The way ro push parent date to child level nested childen (ZoneSerializer --> ActivitySerializer)
        """
        children = obj.allowed_activities
        serializer_context = {'request': self.context.get('request'),
                              'zone_id': obj.id,
                              'park_id': self.context.get('parent_id')}
        serializer = ActivitySerializer(children, many=True, context=serializer_context)
        return serializer.data

class ParkFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Park
        fields=('id', 'name', 'park_type')

class MarineParkSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    #zones=ZoneSerializer(many=True)
    #children=ZoneSerializer(many=True, source='zones')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Park
        #fields=('id', 'name', 'can_edit', 'last_leaf', 'code', 'park_type', 'allowed_activities', 'zone_ids', 'adult_price', 'child_price', 'oracle_code', 'children' )
        fields=('id', 'name', 'can_edit', 'last_leaf', 'code', 'park_type', 'allowed_activities', 'zone_ids', 'adult_price', 'child_price', 'children' )

    def get_can_edit(self, obj):
        return False

    def get_last_leaf(self, obj):
        return False

    def get_children(self, obj):
        """ The way ro push parent date to child level nested childen (ZoneSerializer --> ActivitySerializer)
        """
        children = obj.zones
        serializer_context = {
            'request': self.context.get('request'),
            'parent_id': obj.id,
            'parent_name': obj.name
        }
        serializer = ZoneSerializer(children, many=True, context=serializer_context)
        return serializer.data



class ParkSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    zones=ZoneSerializer(many=True)
    district = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()
    max_group_arrival_by_date = serializers.SerializerMethodField()
    #children=ZoneSerializer(many=True, source='zones')

    class Meta:
        model = Park
        #fields=('id', 'name', 'can_edit', 'last_leaf', 'code', 'park_type', 'allowed_activities', 'zone_ids', 'adult_price', 'child_price', 'oracle_code', 'zones', 'district', 'region', 'max_group_arrival_by_date' )
        fields=('id', 'name', 'can_edit', 'last_leaf', 'code', 'park_type', 'allowed_activities', 'zone_ids', 'adult_price', 'child_price', 'zones', 'district', 'region', 'max_group_arrival_by_date','allowed_activities_ids')

    def get_can_edit(self, obj):
        #proposal = self.context['request'].GET.get('proposal')
        #activities = ProposalParkActivity.objects.filter(proposal_park__park=obj.id, proposal_park__proposal=proposal)
        #return True if activities else False
        return True

    def get_last_leaf(self, obj):
        return True

    def get_district(self, obj):
        return obj.district.id

    def get_region(self, obj):
        return {'name': obj.district.region.name, 'id': obj.district.region_id}

#    def get_max_group_arrival_by_date(self, obj):
#        """ Used in Admission Payments for parks to determine if park(s) have been paid for in previous sessions, for a given arrival date """
#        today = datetime.now().date()
#        group =  obj.bookings.filter(arrival__gte=today).values('arrival').annotate(total_adults=Max('no_adults'), total_children=Max('no_children'), total_free=Max('no_free_of_charge'))
#        if group:
#            groups_by_arrival = {}
#            for group_list in list(group):
#                arrival = group_list.pop('arrival')
#                arrival_str = arrival.strftime('%Y-%m-%d')
#                groups_by_arrival.update({arrival_str: group_list})
#            return groups_by_arrival
#        else:
#            return {}

    def get_max_group_arrival_by_date(self, obj):
        """ Used in Admission Payments for parks to determine if park(s) have been paid for in previous sessions, for a given arrival date 
            Now excluding parks booked in previous sessions, for payment calc'n
        """
        return {}

class DistrictSerializer(serializers.ModelSerializer):
    land_parks = ParkSerializer(many=True)
    marine_parks = ParkSerializer(many=True)
    class Meta:
        model = District
        fields = ('id', 'name', 'code', 'land_parks', 'marine_parks')

class RegionSerializer(serializers.ModelSerializer):
    districts = DistrictSerializer(many=True)
    class Meta:
        model = Region
        fields = ('id', 'name','forest_region', 'districts')

class DistrictSerializer2(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    is_disabled = serializers.SerializerMethodField()
    #children = ParkSerializer2(many=True, read_only=True, source='land_parks')
    children = ParkSerializer(many=True, read_only=True, source='land_parks')

    class Meta:
        model = District
        #fields = ('id', 'name', 'land_parks', 'marine_parks')
        fields = ('pk', 'id', 'name', 'last_leaf', 'is_disabled', 'children')

    def get_pk(self, obj):
        return obj.id

    def get_last_leaf(self, obj):
        return False

    def get_is_disabled(self, obj):
        return True if obj.parks.count()==0 else False


class RegionSerializer2(serializers.ModelSerializer):
    pk = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    children = DistrictSerializer2(many=True, read_only=True, source='districts')

    class Meta:
        model = Region
        fields = ('pk', 'id', 'name', 'last_leaf', 'children')

    def get_pk(self, obj):
        return obj.id

    def get_last_leaf(self, obj):
        return False


class AccessTypeSerializer(serializers.ModelSerializer):
    last_leaf = serializers.SerializerMethodField()
    class Meta:
        model = AccessType
        fields = ('id', 'name', 'last_leaf', 'visible')

    def get_last_leaf(self, obj):
        return True


class ActivityMatrixSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityMatrix
        fields = ('id', 'name', 'description', 'version', 'ordered', 'schema')


#class ActivitySerializer(serializers.ModelSerializer):
#    class Meta:
#        model = Activity
#        #ordering = ('order', 'name')
#        fields = ('id', 'name', 'application_type')


class TenureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenure
        fields = ('id', 'name', 'application_type')


class ApplicationTypeSerializer(serializers.ModelSerializer):
    #regions = RegionSerializer(many=True)
    #activity_app_types = ActivitySerializer(many=True)
    #tenure_app_types = TenureSerializer(many=True)
    class Meta:
        model = ApplicationType
        #fields = ('id', 'name', 'activity_app_types', 'tenure_app_types')
        #fields = ('id', 'name', 'tenure_app_types')
        fields = '__all__'
        #extra_fields = ['pizzas']


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ('key', 'value')



class RequiredDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequiredDocument
        fields = ('id', 'park','activity', 'question')


class ActivityCategorySerializer(serializers.ModelSerializer):
    #activities = ActivitySerializer(many=True)
    pk = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()
    #children = ActivitySerializer(many=True, source='activities')

    class Meta:
        model = ActivityCategory
        fields = ('pk', 'id', 'name','children')
        #fields = ('pk', 'id', 'name','activities')

    def get_pk(self, obj):
        return obj.id

    def get_children(self, obj):
        """ The way ro push parent date to child level nested childen (ActivityCategorySerializer --> ActivitySerializer)
        """
        children = obj.activities
        serializer_context = {'request': self.context.get('request'),
                              'parent_id': obj.id}
        serializer = ActivitySerializer(children, many=True, context=serializer_context)
        return serializer.data


class TrailSerializer(serializers.ModelSerializer):
    can_edit = serializers.SerializerMethodField()
    last_leaf = serializers.SerializerMethodField()
    sections=SectionSerializer(many=True)
    allowed_activities=ActivitySerializer(many=True)
    class Meta:
        model = Trail
        fields = ('id', 'name', 'can_edit', 'last_leaf', 'code', 'section_ids', 'sections', 'allowed_activities', 'allowed_activities_ids')

    def get_can_edit(self, obj):
        return True

    def get_last_leaf(self, obj):
        return True


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question_text', 'answer_one', 'answer_two', 'answer_three', 'answer_four','correct_answer', 'correct_answer_value')


class LandActivityTabSerializer(serializers.Serializer):
    land_parks = RegionSerializer2(many=True, read_only=True, source='regions')
    access_types = AccessTypeSerializer(many=True, read_only=True)
    land_activity_types = ActivitySerializer(many=True, read_only=True)
    trail_activity_types = ActivitySerializer(many=True, read_only=True)
    trails = TrailSerializer(many=True, read_only=True)
    land_required_documents = RequiredDocumentSerializer(many=True, read_only=True)
    #marine_activity_types = ActivitySerializer(many=True, read_only=True)
    #marine_activities = ActivityCategorySerializer(many=True, read_only=True)


class MarineActivityTabSerializer(serializers.Serializer):
    required_documents = RequiredDocumentSerializer(many=True, read_only=True)
    marine_activities = ActivityCategorySerializer(many=True, read_only=True)
    marine_parks = MarineParkSerializer(many=True, read_only=True)


class BookingSettlementReportSerializer(serializers.Serializer):
    date = serializers.DateTimeField(input_formats=['%d/%m/%Y'])


class OracleSerializer(serializers.Serializer):
    date = serializers.DateField(input_formats=['%d/%m/%Y','%Y-%m-%d'])
    override = serializers.BooleanField(default=False)



class ActivityFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name',)

class EventsParkSerializer(serializers.ModelSerializer):
    allowed_activities= serializers.SerializerMethodField()

    class Meta:
        model = Park
        fields=('id', 'name', 'allowed_activities', )

    def get_allowed_activities(self, obj):
        """ The way ro push parent date to child level nested childen (ZoneSerializer --> ActivitySerializer)
        """
        children=[]
        if obj.park_type=='land':
            children = obj.allowed_activities
        if obj.park_type=='marine':
            for zone in obj.zones.all():
                #children.append(zone.allowed_activities.all())
                zone_activities=[i for i in zone.allowed_activities.all()]
                children=children+zone_activities
        serializer_context = {'request': self.context.get('request'),
                              }
        serializer = ActivityFilterSerializer(children, many=True, context=serializer_context)
        return serializer.data

class FilmingParkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Park
        fields=('id', 'name',)


class TrailTabSerializer(serializers.Serializer):
    land_activity_types = ActivitySerializer(many=True, read_only=True)
    trails = TrailSerializer(many=True, read_only=True)
