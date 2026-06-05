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
                        id="pills-activity-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-activity"
                        role="tab"
                        aria-controls="pills-activity"
                        aria-selected="false"
                    >
                        2. Activity
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-access-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-access"
                        role="tab"
                        aria-controls="pills-access"
                        aria-selected="false"
                    >
                        3. Access
                    </a>
                </li>
                <li class="nav-item">
                    <a
                        id="pills-equipment-tab"
                        class="nav-link"
                        data-bs-toggle="pill"
                        href="#pills-equipment"
                        role="tab"
                        aria-controls="pills-equipment"
                        aria-selected="false"
                    >
                        4. Equipment
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
                        6. Confirmation
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
                        <div v-if="is_internal || is_referral">
                            <ApprovalType
                                :proposal="proposal"
                                :has-assessor-mode="hasAssessorMode"
                            ></ApprovalType>
                        </div>
                        <div v-if="is_internal">
                            <Assessment
                                v-if="proposal.assessor_assessment"
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
                    id="pills-activity"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-activity-tab"
                >
                    <Activity
                        id="proposalStartActivity"
                        :proposal="proposal"
                        :has-district-assessor-mode="hasDistrictAssessorMode"
                        :district_proposal="district_proposal"
                        :can-edit-activities="canEditActivities"
                        :can-edit-period="canEditPeriod"
                        :is_external="is_external"
                    ></Activity>
                </div>
                <div
                    id="pills-access"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-access-tab"
                >
                    <Access
                        id="proposalStartAccess"
                        ref="filming_access"
                        :proposal="proposal"
                        :has-district-assessor-mode="hasDistrictAssessorMode"
                        :district_proposal="district_proposal"
                        :can-edit-activities="canEditActivities"
                        :can-edit-period="canEditPeriod"
                        :is_external="is_external"
                    ></Access>
                </div>
                <div
                    id="pills-equipment"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-equipment-tab"
                >
                    <Equipment
                        id="proposalStartEquipment"
                        ref="filming_equipment"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                    ></Equipment>
                </div>
                <div
                    id="pills-other-details"
                    class="tab-pane fade"
                    role="tabpanel"
                    aria-labelledby="pills-other-details-tab"
                >
                    <OtherDetails
                        id="proposalStartOtherDetails"
                        ref="filming_other_details"
                        :proposal="proposal"
                        :can-edit-activities="canEditActivities"
                    ></OtherDetails>
                </div>
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
import Organisation from '@/components/external/organisations//organisation_details.vue';
import Applicant from '@/components/common/tclass/applicant.vue';
import Assessment from '@/components/common/tclass/assessment.vue';
import ApprovalType from '@/components/common/filming/approval_type.vue';
import Activity from '@/components/common/filming/activity.vue';
import Access from '@/components/common/filming/access.vue';
import Equipment from '@/components/common/filming/equipment.vue';
import OtherDetails from '@/components/common/filming/other_details.vue';
import Confirmation from '@/components/common/filming/confirmation.vue';
import $ from 'jquery';
export default {
    components: {
        Account,
        Applicant,
        Activity,
        Access,
        Equipment,
        OtherDetails,
        Confirmation,
        Organisation,
        Assessment,
        ApprovalType,
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
        canEditPeriod: {
            type: Boolean,
            default: false,
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
        hasDistrictAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        district_proposal: {
            type: Object,
            default: null,
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
        vm.set_tabs();
        vm.eventListener();
        vm.form = document.forms.new_proposal;
    },
    methods: {
        set_tabs: function () {
            /* Confirmation tab - Always Disabled */
            $('#pills-confirm-tab').attr(
                'style',
                'background-color:#E5E8E8 !important; color: #99A3A4;'
            );
            $('#li-confirm').attr('class', 'nav-item disabled');
        },
        eventListener: function () {
            let vm = this;
            $('a[href="#pills-access"]').on('shown.bs.tab', function () {
                vm.$refs.filming_access.$refs.parks_table.$refs.park_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            });
            $('a[href="#pills-equipment"]').on('shown.bs.tab', function () {
                vm.$refs.filming_equipment.$refs.vessel_table.$refs.vessel_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            });
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
