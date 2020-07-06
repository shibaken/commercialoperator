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
                                    Proposal,
                                    FilmingParkDocument,
                                    DistrictProposal,

                                )

#from commercialoperator.components.organisations.models import (
#                                Organisation
#                            )
from commercialoperator.components.main.serializers import CommunicationLogEntrySerializer, ParkFilterSerializer
#from commercialoperator.components.organisations.serializers import OrganisationSerializer
#from commercialoperator.components.users.serializers import UserAddressSerializer, DocumentSerializer
from rest_framework import serializers
from django.db.models import Q
from reversion.models import Version



class ProposalFilmingActivitySerializer(serializers.ModelSerializer):
    film_type=serializers.MultipleChoiceField(choices=ProposalFilmingActivity.FILM_TYPE_CHOICES, allow_blank=True, allow_null=True, required=False)
    film_purpose=serializers.MultipleChoiceField(choices=ProposalFilmingActivity.PURPOSE_CHOICES, allow_blank=True, allow_null=True, required=False)
    #sponsorship=serializers.MultipleChoiceField(choices=ProposalFilmingActivity.SPONSORSHIP_CHOICES, allow_blank=True, allow_null=True, required=False)
    film_usage=serializers.MultipleChoiceField(choices=ProposalFilmingActivity.FILM_USE_CHOICES, allow_blank=True, allow_null=True, required=False)
    commencement_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)
    completion_date = serializers.DateField(format="%d/%m/%Y",input_formats=['%d/%m/%Y'],required=False,allow_null=True)

    
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
class FilmingParkDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilmingParkDocument
        fields = ('id', 'name', '_file')

class ProposalFilmingParksSerializer(serializers.ModelSerializer):
    park=ParkFilterSerializer()
    from_date=serializers.DateField(format="%d/%m/%Y")
    to_date=serializers.DateField(format="%d/%m/%Y")
    filming_park_documents = FilmingParkDocumentSerializer(many=True, read_only=True)
    can_assessor_edit= serializers.SerializerMethodField()

    class Meta:
        model = ProposalFilmingParks
        fields = ('id', 'park', 'feature_of_interest', 'from_date', 'to_date', 'proposal', 'filming_park_documents', 'can_assessor_edit')

    def get_can_assessor_edit(self,obj):
        request = self.context['request']
        user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
        return obj.can_assessor_edit(user)    

class SaveProposalFilmingParksSerializer(serializers.ModelSerializer):
    #park=ParkFilterSerializer()
    from_date=serializers.DateField(input_formats=['%d/%m/%Y'], allow_null=True)
    to_date=serializers.DateField(input_formats=['%d/%m/%Y'], allow_null=True)
    class Meta:
        model = ProposalFilmingParks
        fields = ('id', 'park', 'feature_of_interest', 'from_date', 'to_date', 'proposal')


class ProposalFilmingSerializer(serializers.ModelSerializer):
    readonly = serializers.SerializerMethodField(read_only=True)
    documents_url = serializers.SerializerMethodField()
    proposal_type = serializers.SerializerMethodField()
    get_history = serializers.ReadOnlyField()
    is_qa_officer = serializers.SerializerMethodField()
    fee_invoice_url = serializers.SerializerMethodField()
    
    submitter = serializers.CharField(source='submitter.get_full_name')
    processing_status = serializers.SerializerMethodField(read_only=True)
    review_status = serializers.SerializerMethodField(read_only=True)
    customer_status = serializers.SerializerMethodField(read_only=True)

    application_type = serializers.CharField(source='application_type.name', read_only=True)
    region = serializers.CharField(source='region.name', read_only=True)
    district = serializers.CharField(source='district.name', read_only=True)

    class Meta:
        model = Proposal
        fields = (
                'id',
                'application_type',
                'proposal_type',
                'activity',
                'approval_level',
                'title',
                'region',
                'district',
                'tenure',
                'customer_status',
                'processing_status',
                'review_status',
                #'hard_copy',
                'applicant_type',
                'applicant',
                'org_applicant',
                'proxy_applicant',
                'submitter',
                'assigned_officer',
                'previous_application',
                'get_history',
                'lodgement_date',
                'modified_date',
                'documents',
                'requirements',
                'readonly',
                'can_user_edit',
                'can_user_view',
                'documents_url',
                'reference',
                'lodgement_number',
                'lodgement_sequence',
                'can_officer_process',
                'proposal_type',
                'is_qa_officer',
                'pending_amendment_request',
                'is_amendment_proposal',

                # tab field models
                'applicant_details',
                'training_completed',
                'fee_invoice_url',
                'fee_paid',

                )
        read_only_fields=('documents',)

   

    def get_documents_url(self,obj):
        return '/media/{}/proposals/{}/documents/'.format(settings.MEDIA_APP_DIR, obj.id)

    def get_readonly(self,obj):
        return False

    def get_processing_status(self,obj):
        return obj.get_processing_status_display()

    def get_review_status(self,obj):
        return obj.get_review_status_display()

    def get_customer_status(self,obj):
        return obj.get_customer_status_display()

    def get_proposal_type(self,obj):
        return obj.get_proposal_type_display()

    def get_is_qa_officer(self,obj):
        request = self.context['request']
        return request.user.email in obj.qa_officers()

    def get_fee_invoice_url(self,obj):
        return '/cols/payments/invoice-pdf/{}'.format(obj.fee_invoice_reference) if obj.fee_paid else None

 


class DistrictProposalSerializer(serializers.ModelSerializer):
    processing_status = serializers.CharField(source='get_processing_status_display')
    #customer_status = serializers.CharField(source='get_customer_status_display')
    # latest_referrals = ProposalReferralSerializer(many=True)
    # can_be_completed = serializers.BooleanField()
    # can_process=serializers.SerializerMethodField()
    # referral_assessment=ProposalAssessmentSerializer(read_only=True)


    class Meta:
        model = DistrictProposal
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super(DistrictProposalSerializer, self).__init__(*args, **kwargs)
        self.fields['proposal'] = InternalFilmingProposalSerializer(context={'request':self.context['request']})

    # def get_can_process(self,obj):
    #     request = self.context['request']
    #     user = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
    #     return obj.can_process(user)