from django.conf import settings
from ledger.accounts.models import EmailUser,Address
from commercialoperator.components.proposals.models import (
#                                    ProposalType,
#                                    Proposal,
#                                    ProposalUserAction,
#                                    ProposalLogEntry,
#                                    Referral,
#                                    ProposalRequirement,
#                                    ProposalStandardRequirement,
#                                    ProposalDeclinedDetails,
#                                    AmendmentRequest,
#                                    AmendmentReason,
#                                    ProposalApplicantDetails,
#                                    ProposalActivitiesLand,
#                                    ProposalActivitiesMarine,
#                                    ProposalPark,
#                                    ProposalParkActivity,
#                                    Vehicle,
#                                    Vessel,
#                                    ProposalTrail,
#                                    QAOfficerReferral,
#                                    ProposalParkAccess,
#                                    ProposalTrailSection,
#                                    ProposalTrailSectionActivity,
#                                    ProposalParkZoneActivity,
#                                    ProposalParkZone,
#                                    ProposalAccreditation,
#                                    ChecklistQuestion,
#                                    ProposalAssessmentAnswer,
#                                    ProposalAssessment,
#                                    RequirementDocument,
#                                    ProposalOtherDetails,
                                    ProposalEventActivities,
                                    ProposalEventManagement,
                                    ProposalEventVehiclesVessels,
                                    ProposalEventOtherDetails,
                                    ProposalEventsParks,
                                    EventsParkDocument,
                                    AbseilingClimbingActivity,
                                    PreEventsParkDocument,
                                    ProposalPreEventsParks
                                    #ProposalEventOnlineTraining,
                                )
from commercialoperator.components.main.serializers import CommunicationLogEntrySerializer, ParkFilterSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version


class ProposalEventActivitiesSerializer(serializers.ModelSerializer):
    commencement_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    completion_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    class Meta:
        model = ProposalEventActivities
        fields = '__all__'


class ProposalEventManagementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalEventManagement
        fields = '__all__'


class ProposalEventVehiclesVesselsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalEventVehiclesVessels
        fields = '__all__'


class ProposalEventOtherDetailsSerializer(serializers.ModelSerializer):
    insurance_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    training_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    class Meta:
        model = ProposalEventOtherDetails
        #fields = '__all__'
        fields=(
                'id',
                'insurance_expiry',
                'training_date',
                'participants_number',
                'officials_number',
                'support_vehicle_number',
                'proposal',
                )

class EventsParkDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsParkDocument
        fields = ('id', 'name', '_file')

class ProposalEventsParksSerializer(serializers.ModelSerializer):
    park=ParkFilterSerializer()
    #activities=serializers.CharField(source='activities.name', many=True)
    events_park_documents = EventsParkDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ProposalEventsParks
        fields = ('id', 'park', 'activities','activities_names', 'proposal', 'events_park_documents')

class SaveProposalEventsParksSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    class Meta:
        model = ProposalEventsParks
        fields = ('id', 'park','proposal', 'activities')

class AbseilingClimbingActivitySerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    class Meta:
        model = AbseilingClimbingActivity
        fields = '__all__'


class PreEventsParkDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreEventsParkDocument
        fields = ('id', 'name', '_file')

class ProposalPreEventsParksSerializer(serializers.ModelSerializer):
    park=ParkFilterSerializer()
    #activities=serializers.CharField(source='activities.name', many=True)
    pre_event_park_documents = PreEventsParkDocumentSerializer(many=True, read_only=True)
    class Meta:
        model = ProposalPreEventsParks
        fields = ('id', 'park', 'activities', 'pre_event_park_documents', 'proposal')

class SaveProposalPreEventsParksSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    class Meta:
        model = ProposalPreEventsParks
        fields = ('id', 'park','proposal', 'activities')
