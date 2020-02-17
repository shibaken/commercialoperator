from django.conf import settings
from ledger.accounts.models import EmailUser,Address
from commercialoperator.components.proposals.models import (
                                    ProposalType,
                                    Proposal,
                                    ProposalUserAction,
                                    ProposalLogEntry,
                                    Referral,
                                    ProposalRequirement,
                                    ProposalStandardRequirement,
                                    ProposalDeclinedDetails,
                                    AmendmentRequest,
                                    AmendmentReason,
                                    ProposalApplicantDetails,
                                    ProposalActivitiesLand,
                                    ProposalActivitiesMarine,
                                    ProposalPark,
                                    ProposalParkActivity,
                                    Vehicle,
                                    Vessel,
                                    ProposalTrail,
                                    QAOfficerReferral,
                                    ProposalParkAccess,
                                    ProposalTrailSection,
                                    ProposalTrailSectionActivity,
                                    ProposalParkZoneActivity,
                                    ProposalParkZone,
                                    ProposalAccreditation,
                                    ChecklistQuestion,
                                    ProposalAssessmentAnswer,
                                    ProposalAssessment,
                                    RequirementDocument,
                                    ProposalOtherDetails,

                                )
from commercialoperator.components.organisations.models import (
                                Organisation
                            )
from commercialoperator.components.main.serializers import CommunicationLogEntrySerializer, ParkSerializer, ActivitySerializer, AccessTypeSerializer, TrailSerializer
from commercialoperator.components.organisations.serializers import OrganisationSerializer
from commercialoperator.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version


class ProposalOtherDetailsFilmingSerializer(serializers.ModelSerializer):
    nominated_start_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    insurance_expiry = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    accreditations = ProposalAccreditationSerializer(many=True, read_only=True)
    preferred_licence_period = serializers.CharField(allow_blank=True, allow_null=True)
    proposed_end_date = serializers.DateField(format="%d/%m/%Y",read_only=True)

    class Meta:
        model = ProposalOtherDetails
        fields=(
                'id',
                'accreditations',
                'preferred_licence_period',
                'nominated_start_date',
                'insurance_expiry',
                'other_comments',
                'credit_fees',
                'credit_docket_books',
                'docket_books_number',
                'mooring',
                'proposed_end_date',
                )


class SaveProposalOtherDetailsFilmingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalOtherDetails
        fields=(
                'preferred_licence_period',
                'nominated_start_date',
                'insurance_expiry',
                'other_comments',
                'credit_fees',
                'credit_docket_books',
                'proposal',
                )



