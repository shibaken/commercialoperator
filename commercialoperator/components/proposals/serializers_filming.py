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
                                    ProposalFilmingActivity,
                                    ProposalFilmingAccess,
                                    ProposalFilmingEquipment,
                                    ProposalFilmingOtherDetails,
                                    ProposalFilmingParks,
                                )

#from commercialoperator.components.organisations.models import (
#                                Organisation
#                            )
#from commercialoperator.components.main.serializers import CommunicationLogEntrySerializer, ParkSerializer, ActivitySerializer, AccessTypeSerializer, TrailSerializer
#from commercialoperator.components.organisations.serializers import OrganisationSerializer
#from commercialoperator.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version


class ProposalFilmingActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalFilmingActivity
        fields = '__all__'


class ProposalFilmingAccessSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalFilmingAccess
        fields = '__all__'


class ProposalFilmingEquipmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProposalFilmingEquipment
        fields = '__all__'


class ProposalFilmingOtherDetailsSerializer(serializers.ModelSerializer):
    insurance_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    class Meta:
        model = ProposalFilmingOtherDetails
        fields=(
                'id',
                'safety_details',
                'camping_fee_waived',
                'fee_waived_num_people',
                'insurance_expiry',
                'proposal',
                )


#class SaveProposalFilmingOtherDetailsSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = ProposalOtherDetails
#        fields=(
#                'preferred_licence_period',
#                'nominated_start_date',
#                'insurance_expiry',
#                'other_comments',
#                'credit_fees',
#                'credit_docket_books',
#                'proposal',
#                )

class ProposalFilmingParksSerializer(serializers.ModelSerializer):
    from_date=serializers.DateField(format="%d/%m/%Y")
    to_date=serializers.DateField(format="%d/%m/%Y")
    class Meta:
        model = ProposalFilmingParks
        fields = ('id', 'park', 'feature_of_interest', 'from_date', 'to_date', 'proposal')

