<template lang="html">
    <div>
        <div class="col-md-12">
            <ul id="pills-tab" class="nav nav-pills mb-3" role="tablist">
                <li class="nav-item">
                    <a
                        id="pills-applicant-tab"
                        class="nav-link active"
                        data-bs-toggle="pill"
                        href="#pills-applicant"
                        role="tab"
                        aria-controls="pills-applicant"
                        aria-selected="true"
                    >
                        1. Applicant
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-activities-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-activities"
                        role="tab"
                        aria-controls="pills-activities"
                        aria-selected="false"
                    >
                        2. Activities
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-event-management-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-event-management"
                        role="tab"
                        aria-controls="pills-event-management"
                        aria-selected="false"
                    >
                        3. Event Management
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-vehicles-vessels-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-vehicles-vessels"
                        role="tab"
                        aria-controls="pills-vehicles-vessels"
                        aria-selected="false"
                    >
                        4. Vehicles/Vessels
                    </a>
                </li>

                <li class="nav-item">
                    <a
                        id="pills-other-details-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-other-details"
                        role="tab"
                        aria-controls="pills-other-details"
                        aria-selected="false"
                    >
                        5. Other Details
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-online-training-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-online-training"
                        role="tab"
                        aria-controls="pills-online-training"
                        aria-selected="false"
                    >
                        6. Online Training
                    </a>
                </li>
                <li v-if="is_external" id="li-payment" class="nav-item">
                    <a
                        id="pills-payment-tab"
                        class="nav-link disabled"
                        data-bs-toggle="pill"
                        href=""
                        role="tab"
                        aria-controls="pills-payment"
                        aria-selected="false"
                    >
                        7. Payment
                    </a>
                </li>
                <li v-if="is_external" id="li-confirm" class="nav-item">
                    <a
                        id="pills-confirm-tab"
                        class="nav-link disabled"
                        data-bs-toggle="pill"
                        href=""
                        role="tab"
                        aria-controls="pills-confirm"
                        aria-selected="false"
                    >
                        8. Confirmation
                    </a>
                </li>
            </ul>
            <div id="pills-tabContent" class="tab-content">
                <div
                    id="pills-applicant"
                    class="tab-pane fade active show"
                    role="tabpanel"
                    aria-labelledby="pills-applicant-tab"
                >
                    <div v-if="is_external">
                        <Account
                            v-if="applicantType == 'SUB'"
                            ref="profile"
                        ></Account>

                        <Organisation
                            v-if="applicantType == 'ORG'"
                            ref="organisation"
                            :org_id="proposal.org_applicant"
                            :is-application="true"
                        ></Organisation>
                    </div>
                    <div v-else>
                        <Applicant
                            id="proposalStartApplicant"
                            :proposal="proposal"
                        ></Applicant>
                        <div v-if="is_internal">
                            <Assessment
                                :proposal="proposal"
                                :assessment="proposal.assessor_assessment"
                                :has-assessor-mode="hasAssessorMode"
                                :is_internal="is_internal"
                                :is_referral="is_referral"
                            ></Assessment>
                            <div
                                v-for="assess in proposal.referral_assessments"
                                :key="assess.id"
                            >
                                <Assessment
                                    :proposal="proposal"
                                    :assessment="assess"
                                ></Assessment>
                            </div>
                        </div>
                    </div>
                </div>

                <div
                    id="pills-activities"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-activities-tab"
                >
                    <Activities
                        id="proposalStartActivities"
                        ref="event_activities"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                        :can-edit-period="canEditPeriod"
                        :is_external="is_external"
                        :has-assessor-mode="hasAssessorMode"
                        :is_internal="is_internal"
                        :has-referral-mode="hasReferralMode"
                    ></Activities>
                </div>
                <div
                    id="pills-event-management"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-event-management-tab"
                >
                    <EventManagement
                        id="proposalStartEventManagement"
                        ref="event_management"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                    ></EventManagement>
                </div>
                <div
                    id="pills-vehicles-vessels"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-vehicles-vessels-tab"
                >
                    <VehiclesVessels
                        id="proposalStartVehiclesVessels"
                        :proposal="proposal"
                    ></VehiclesVessels>
                </div>
                <div
                    id="pills-other-details"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-other-details-tab"
                >
                    <OtherDetails
                        id="proposalStartOtherDetails"
                        ref="event_other_details"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                    ></OtherDetails>
                </div>
                <div
                    id="pills-online-training"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-online-training-tab"
                >
                    <OnlineTraining
                        id="proposalStartOnlineTraining"
                        :proposal="proposal"
                    ></OnlineTraining>
                </div>
                <div
                    id="pills-payment"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-payment-tab"
                ></div>
                <div
                    id="pills-confirm"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-confirm-tab"
                >
                    <Confirmation
                        id="proposalStartConfirmation"
                        :proposal="proposal"
                    ></Confirmation>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Account from '@/components/user/account.vue';
import Organisation from '@/components/external/organisations/organisation_details.vue';
import Applicant from '@/components/common/tclass/applicant.vue';
import Assessment from '@/components/common/tclass/assessment.vue';
import Activities from '@/components/common/event/activities.vue';
import EventManagement from '@/components/common/event/event_management.vue';
import VehiclesVessels from '@/components/common/event/vehicles_vessels.vue';
import OtherDetails from '@/components/common/event/other_details.vue';
import OnlineTraining from '@/components/common/event/online_training.vue';
import Confirmation from '@/components/common/event/confirmation.vue';
import $ from 'jquery';
export default {
    components: {
        Account,
        Applicant,
        Activities,
        EventManagement,
        VehiclesVessels,
        OtherDetails,
        OnlineTraining,
        Confirmation,
        Organisation,
        Assessment,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        canEditActivities: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_internal: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_referral: {
            type: Boolean,
            default: false,
        },
        hasReferralMode: {
            type: Boolean,
            default: false,
        },
        hasAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/require-default-prop
        referral: {
            type: Object,
            required: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        proposal_parks: {
            type: Object,
            default: null,
        },
        canEditPeriod: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            values: null,
        };
    },
    computed: {
        applicantType: function () {
            return this.proposal.applicant_type;
        },
    },
    mounted: function () {
        let vm = this;
        $('#pills-activities-tab').on('shown.bs.tab', function () {
            // fixes column width collapse on datatables within the tabs
            vm.$refs.event_activities.$refs.trails_table.$refs.park_datatable.vmDataTable.columns
                .adjust()
                .responsive.recalc();
            vm.$refs.event_activities.$refs.parks_table.$refs.park_datatable.vmDataTable.columns
                .adjust()
                .responsive.recalc();
        });
        vm.set_tabs();
        vm.form = document.forms.new_proposal;
    },
    methods: {
        set_tabs: function () {
            let vm = this;

            if (vm.proposal.fee_paid && vm.training_completed) {
                /* Online Training tab */
                $('#pills-online-training-tab').attr(
                    'style',
                    'background-color:#E5E8E8 !important; color: #99A3A4;'
                );
                $('#li-training').attr('class', 'nav-item disabled');
                $('#pills-online-training-tab').attr('href', '');
            }

            if (!vm.proposal.training_completed) {
                /* Payment tab  (this is enabled after online_training is completed - in online_training.vue)*/
                $('#pills-payment-tab').attr(
                    'style',
                    'background-color:#E5E8E8 !important; color: #99A3A4;'
                );
                $('#li-payment').attr('class', 'nav-item disabled');
            }

            /* Confirmation tab - Always Disabled */
            $('#pills-confirm-tab').attr(
                'style',
                'background-color:#E5E8E8 !important; color: #99A3A4;'
            );
            $('#li-confirm').attr('class', 'nav-item disabled');
        },
    },
};
</script>

<style lang="css" scoped>
.section {
    text-transform: capitalize;
}
.list-group {
    margin-bottom: 0;
}
.fixed-top {
    position: fixed;
    top: 56px;
}

.nav-item {
    background-color: rgb(200, 200, 200, 0.8) !important;
}

.nav-item > li > a {
    background-color: yellow !important;
    color: #fff;
}

.nav-item > li.active > a,
.nav-item > li.active > a:hover,
.nav-item > li.active > a:focus {
    color: white;
    background-color: blue;
    border: 1px solid #888888;
}
</style>
