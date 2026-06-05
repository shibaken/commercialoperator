<template lang="html">
    <div>
        <div class="col-md-12">
            <ul id="pills-tab" class="nav nav-pills mb-3" role="tablist">
                <li class="nav-item">
                    <a
                        id="pills-applicant-tab"
                        class="nav-link"
                        :class="{
                            active: isSelectedTabById('pills-applicant-tab'),
                        }"
                        data-bs-toggle="pill"
                        href="#pills-applicant"
                        role="tab"
                        aria-controls="pills-applicant"
                        :aria-selected="
                            isSelectedTabById('pills-applicant-tab') || null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        1. Applicant
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-activities-land-tab"
                        class="nav-link"
                        :class="{
                            active: isSelectedTabById(
                                'pills-activities-land-tab'
                            ),
                        }"
                        data-bs-toggle="pill"
                        href="#pills-activities-land"
                        role="tab"
                        aria-controls="pills-activities-land"
                        :aria-selected="
                            isSelectedTabById('pills-activities-land-tab') ||
                            null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        2. Activities (land)
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-activities-marine-tab"
                        class="nav-link"
                        :class="{
                            active: isSelectedTabById(
                                'pills-activities-marine-tab'
                            ),
                        }"
                        data-bs-toggle="pill"
                        href="#pills-activities-marine"
                        role="tab"
                        aria-controls="pills-activities-marine"
                        :aria-selected="
                            isSelectedTabById('pills-activities-marine-tab') ||
                            null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        3. Activities (marine)
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-other-details-tab"
                        class="nav-link"
                        :class="{
                            active: isSelectedTabById(
                                'pills-other-details-tab'
                            ),
                        }"
                        data-bs-toggle="pill"
                        href="#pills-other-details"
                        role="tab"
                        aria-controls="pills-other-details"
                        :aria-selected="
                            isSelectedTabById('pills-other-details-tab') || null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        4. Other Details
                    </a>
                </li>
                <li v-if="is_external" id="li-training" class="nav-item">
                    <a
                        id="pills-online-training-tab"
                        class="nav-link"
                        :class="{
                            active: isSelectedTabById(
                                'pills-online-training-tab'
                            ),
                        }"
                        data-bs-toggle="pill"
                        href="#pills-online-training"
                        role="tab"
                        aria-controls="pills-online-training"
                        :aria-selected="
                            isSelectedTabById('pills-online-training-tab') ||
                            null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        5. Questionnaire
                    </a>
                </li>
                <li v-if="is_external" id="li-payment" class="nav-item">
                    <a
                        id="pills-payment-tab"
                        class="nav-link disabled"
                        :class="{
                            active: isSelectedTabById('pills-payment-tab'),
                        }"
                        data-bs-toggle="pill"
                        href=""
                        role="tab"
                        aria-controls="pills-payment"
                        :aria-selected="
                            isSelectedTabById('pills-payment-tab') || null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        6. Payment
                    </a>
                </li>
                <li v-if="is_external" id="li-confirm" class="nav-item">
                    <a
                        id="pills-confirm-tab"
                        class="nav-link disabled"
                        :class="{
                            active: isSelectedTabById('pills-confirm-tab'),
                        }"
                        data-bs-toggle="pill"
                        href=""
                        role="tab"
                        aria-controls="pills-confirm"
                        :aria-selected="
                            isSelectedTabById('pills-confirm-tab') || null
                        "
                        @click.prevent="tabClicked($event.target.id)"
                    >
                        7. Confirmation
                    </a>
                </li>
            </ul>
            <div id="pills-tabContent" class="tab-content">
                <div
                    id="pills-applicant"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-applicant-tab'),
                        active: isSelectedTabById('pills-applicant-tab'),
                    }"
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
                        <div v-if="is_referral"></div>
                    </div>
                </div>
                <div
                    id="pills-activities-land"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-activities-land-tab'),
                        active: isSelectedTabById('pills-activities-land-tab'),
                    }"
                    role="tabpanel"
                    aria-labelledby="pills-activities-land-tab"
                >
                    <!-- NOTE: Does the v-bind (it used to be v-on="$listeners" in vue2) do anything for the functionality of this component or can we axe it? -->
                    <ActivitiesLand
                        v-if="
                            proposal_parks &&
                            Object.keys(proposal_parks).length > 0
                        "
                        v-bind="$attrs"
                        id="proposalStartActivitiesLand"
                        ref="activities_land"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                        :proposal_parks="proposal_parks"
                        :is_external="is_external"
                    ></ActivitiesLand>
                </div>
                <div
                    id="pills-activities-marine"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-activities-marine-tab'),
                        active: isSelectedTabById(
                            'pills-activities-marine-tab'
                        ),
                    }"
                    role="tabpanel"
                    aria-labelledby="pills-activities-marine-tab"
                >
                    <!-- NOTE: Does the v-bind (it used to be v-on="$listeners" in vue2) do anything for the functionality of this component or can we axe it? -->
                    <ActivitiesMarine
                        v-if="
                            proposal_parks &&
                            Object.keys(proposal_parks).length > 0
                        "
                        v-bind="$attrs"
                        id="proposalStartActivitiesMarine"
                        ref="activities_marine"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                        :proposal_parks="proposal_parks"
                        :is_external="is_external"
                    ></ActivitiesMarine>
                </div>
                <div
                    id="pills-other-details"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-other-details-tab'),
                        active: isSelectedTabById('pills-other-details-tab'),
                    }"
                    role="tabpanel"
                    aria-labelledby="pills-other-details-tab"
                >
                    <OtherDetails
                        id="proposalStartOtherDetails"
                        ref="other_details"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                    ></OtherDetails>
                </div>
                <div
                    id="pills-online-training"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-online-training-tab'),
                        active: isSelectedTabById('pills-online-training-tab'),
                    }"
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
                    :class="{
                        show: isSelectedTabById('pills-payment-tab'),
                        active: isSelectedTabById('pills-payment-tab'),
                    }"
                    role="tabpanel"
                    aria-labelledby="pills-payment-tab"
                >
                    <!-- This is a Dummy Tab -->
                </div>
                <div
                    id="pills-confirm"
                    class="tab-pane fade"
                    :class="{
                        show: isSelectedTabById('pills-confirm-tab'),
                        active: isSelectedTabById('pills-confirm-tab'),
                    }"
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
import ActivitiesLand from '@/components/common/tclass/activities_land.vue';
import ActivitiesMarine from '@/components/common/tclass/activities_marine.vue';
import OtherDetails from '@/components/common/tclass/other_details.vue';
import OnlineTraining from '@/components/common/tclass/online_training.vue';
import Confirmation from '@/components/common/tclass/confirmation.vue';
import $ from 'jquery';
export default {
    components: {
        Account,
        Applicant,
        ActivitiesLand,
        ActivitiesMarine,
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
        // Session storage values
        sessionStorageActiveTabCache: {
            type: String,
            required: false,
            default: function () {
                return (
                    sessionStorage.getItem('sessionStorageActiveTabCache') ||
                    'pills-applicant-tab'
                );
            },
        },
    },
    data: function () {
        return {
            values: null,
            sessionStorageActiveTab:
                sessionStorage.getItem('sessionStorageActiveTabCache') ||
                'pills-applicant-tab',
        };
    },
    computed: {
        applicantType: function () {
            return this.proposal.applicant_type;
        },
    },
    mounted: function () {
        let vm = this;
        vm.set_tabs();
        vm.form = document.forms.new_proposal;
        vm.eventListener();
    },
    methods: {
        set_tabs: function () {
            let vm = this;

            if (vm.proposal.fee_paid) {
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
        eventListener: function () {
            let vm = this;
            $('a[href="#pills-activities-land"]').on(
                'shown.bs.tab',
                function () {
                    vm.$refs.activities_land.$refs.vehicles_table.$refs.vehicle_datatable.vmDataTable.columns
                        .adjust()
                        .responsive.recalc();
                }
            );
            $('a[href="#pills-activities-marine"]').on(
                'shown.bs.tab',
                function () {
                    vm.$refs.activities_marine.$refs.vessel_table.$refs.vessel_datatable.vmDataTable.columns
                        .adjust()
                        .responsive.recalc();
                }
            );
        },
        /**
         * This function is called when a tab is clicked.
         * It updates the sessionStorageActiveTab and stores it in sessionStorage.
         * @param {string} tab - The ID of the clicked tab.
         */
        tabClicked: function (tab) {
            console.log('Tab clicked:', tab);
            this.sessionStorageActiveTab = tab;
            sessionStorage.setItem('sessionStorageActiveTabCache', tab);
        },
        /**
         * This function checks if the given tabId is the currently selected tab.
         * @param {string} tabId - The ID of the tab to check.
         * @returns {boolean} - Returns true if the tabId matches the sessionStorageActiveTab, otherwise false.
         */
        isSelectedTabById: function (tabId) {
            return this.sessionStorageActiveTab === tabId;
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
    margin-bottom: 2px;
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

.admin > div {
    display: inline-block;
    vertical-align: top;
    margin-right: 1em;
}
</style>
