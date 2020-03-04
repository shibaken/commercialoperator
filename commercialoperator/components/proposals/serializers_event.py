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
                                    #ProposalEventOnlineTraining,
                                )

from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version


class ProposalEventActivitiesSerializer(serializers.ModelSerializer):

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

    class Meta:
        model = ProposalEventOtherDetails
        #fields = '__all__'
        fields=(
                'id',
                'insurance_expiry',
                'proposal',
                )



#class ProposalEventOnlineTrainingSerializer(serializers.ModelSerializer):
#    insurance_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
#
#    class Meta:
#        model = ProposalEventOnlineTraining
#        fields = '__all__'


