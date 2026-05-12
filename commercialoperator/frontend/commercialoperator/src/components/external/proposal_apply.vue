<template lang="html">
    <div class="container">
        <div class="row">
            <div class="col-sm-12">
                <form
                    class="form-horizontal"
                    name="personal_form"
                    method="post"
                >
                    <div class="card">
                        <FormSection
                            :form-collapse="false"
                            label="Applicant"
                            index="license_applicant"
                            subtitle="The applicant will be the licensee"
                        >
                            <template #header-extra>
                                <span
                                    >&nbsp;<i
                                        class="fa fa-question-circle"
                                        data-toggle="tooltip"
                                        data-placement="bottom"
                                        style="color: blue"
                                        title="Please ensure the applicant is the same as the insured party on your public liability on your public liability insurance certificate."
                                    ></i
                                ></span>
                            </template>
                            <div class="col-sm-12">
                                <div v-if="!isLoading" class="form-group">
                                    <div
                                        v-if="
                                            profile
                                                .commercialoperator_organisations
                                                .length > 0
                                        "
                                    >
                                        <label>Do you apply </label>
                                        <br />
                                        <div
                                            v-for="orga in profile.commercialoperator_organisations"
                                            :key="orga.id"
                                            class="radio"
                                        >
                                            <label v-if="!orga.is_consultant">
                                                <input
                                                    v-model="org_applicant"
                                                    type="radio"
                                                    name="behalf_of_org"
                                                    :value="orga.id"
                                                />
                                                On behalf of {{ orga.name }}
                                            </label>
                                            <label v-if="orga.is_consultant">
                                                <input
                                                    v-model="org_applicant"
                                                    type="radio"
                                                    name="behalf_of_org"
                                                    :value="orga.id"
                                                />
                                                On behalf of {{ orga.name }} (as
                                                a Consultant)
                                            </label>
                                        </div>
                                    </div>
                                    <div v-else>
                                        <p style="color: red">
                                            You cannot start a new application
                                            as you have not linked yourself to
                                            any organisation yet. Please go to
                                            your account page in the Options
                                            menu to link your self to an
                                            organisation.
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </FormSection>
                    </div>

                    <div
                        v-show="org_applicant != '' || yourself != ''"
                        class="card"
                    >
                        <FormSection
                            :form-collapse="false"
                            label="Apply for"
                            index="license_apply_for"
                            subtitle=""
                        >
                            <div>
                                <label
                                    for="select_proposal_apply_license_type"
                                    class="control-label"
                                    >Licence Type *
                                    <a
                                        :href="proposal_type_help_url"
                                        target="_blank"
                                        ><i
                                            class="fa fa-question-circle"
                                            style="color: blue"
                                            >&nbsp;</i
                                        ></a
                                    ></label
                                >
                                <div class="col-sm-12">
                                    <div
                                        id="select_proposal_apply_license_type_parent"
                                        class="form-group"
                                    >
                                        <select
                                            id="select_proposal_apply_license_type"
                                            ref="select_proposal_apply_license_type"
                                            v-model="selected_application_id"
                                            class="form-control"
                                            style="width: 40%"
                                            @change="
                                                chainedSelectAppType(
                                                    selected_application_id
                                                )
                                            "
                                        >
                                            <option value="" selected disabled>
                                                Select Licence type*
                                            </option>
                                            <option
                                                v-for="application_type in application_types"
                                                :key="application_type.value"
                                                :value="application_type.value"
                                            >
                                                {{ application_type.text }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div v-show="has_event_proposals()" class="">
                                <div>
                                    <label
                                        for="select_proposal_apply_copy_license"
                                        class="control-label"
                                        >Prefill application with details from
                                        previously approved event
                                    </label>
                                    <div class="col-sm-12">
                                        <div
                                            id="select_proposal_apply_copy_license_parent"
                                            class="form-group"
                                        >
                                            <select
                                                id="select_proposal_apply_copy_license"
                                                ref="select_proposal_apply_copy_license"
                                                v-model="selected_copy_from"
                                                class="form-control"
                                                style="width: 40%"
                                            >
                                                <option
                                                    value=""
                                                    selected
                                                    disabled
                                                >
                                                    Select Event Licence to copy
                                                    from*
                                                </option>
                                                <option
                                                    v-for="event_proposal in event_proposals()"
                                                    :key="event_proposal.id"
                                                    :value="
                                                        event_proposal.current_proposal
                                                    "
                                                >
                                                    {{
                                                        event_proposal.current_proposal__event_activity__event_name
                                                    }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-if="display_region_selectbox">
                                <label
                                    for="select_proposal_apply_region"
                                    class="control-label"
                                    >Region *
                                    <a :href="region_help_url" target="_blank"
                                        ><i
                                            class="fa fa-question-circle"
                                            style="color: blue"
                                            >&nbsp;</i
                                        ></a
                                    >
                                </label>
                                <div class="col-sm-12">
                                    <div
                                        id="select_proposal_apply_region_parent"
                                        class="form-group"
                                    >
                                        <select
                                            id="select_proposal_apply_region"
                                            ref="select_proposal_apply_region"
                                            v-model="selected_region"
                                            class="form-control"
                                            style="width: 40%"
                                            @change="
                                                chainedSelectDistricts(
                                                    selected_region
                                                )
                                            "
                                        >
                                            <option value="" selected disabled>
                                                Select region
                                            </option>
                                            <option
                                                v-for="region in regions"
                                                :key="region.value"
                                                :value="region.value"
                                            >
                                                {{ region.text }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div
                                v-if="
                                    display_region_selectbox && selected_region
                                "
                            >
                                <label
                                    for="select_proposal_apply_district"
                                    class="control-label"
                                    style="font-weight: normal"
                                    >District
                                    <a :href="district_help_url" target="_blank"
                                        ><i
                                            class="fa fa-question-circle"
                                            style="color: blue"
                                            >&nbsp;</i
                                        ></a
                                    ></label
                                >
                                <div class="col-sm-12">
                                    <div
                                        id="select_proposal_apply_district_parent"
                                        class="form-group"
                                    >
                                        <select
                                            id="select_proposal_apply_district"
                                            ref="select_proposal_apply_district"
                                            v-model="selected_district"
                                            class="form-control"
                                            style="width: 40%"
                                        >
                                            <option value="" selected disabled>
                                                Select district
                                            </option>
                                            <option
                                                v-for="district in districts"
                                                :key="district.value"
                                                :value="district.value"
                                            >
                                                {{ district.text }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div v-if="display_activity_matrix_selectbox">
                                <div v-if="activities.length > 0">
                                    <label
                                        for="select_proposal_apply_activity"
                                        class="control-label"
                                        >Activity Type *
                                        <a
                                            :href="activity_type_help_url"
                                            target="_blank"
                                            ><i
                                                class="fa fa-question-circle"
                                                style="color: blue"
                                                >&nbsp;</i
                                            ></a
                                        ></label
                                    >
                                    <div class="col-sm-12">
                                        <div
                                            id="select_proposal_apply_activity_parent"
                                            class="form-group"
                                        >
                                            <select
                                                id="select_proposal_apply_activity"
                                                ref="select_proposal_apply_activity"
                                                v-model="selected_activity"
                                                class="form-control"
                                                style="width: 40%"
                                                @change="
                                                    chainedSelectSubActivities1(
                                                        selected_activity
                                                    )
                                                "
                                            >
                                                <option
                                                    value=""
                                                    selected
                                                    disabled
                                                >
                                                    Select activity
                                                </option>
                                                <option
                                                    v-for="activity in activities"
                                                    :key="activity.value"
                                                    :value="activity.value"
                                                >
                                                    {{ activity.text }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="sub_activities1.length > 0">
                                    <label
                                        for="select_proposal_apply_sub_activity1"
                                        class="control-label"
                                        >Sub Activity 1 *
                                        <a
                                            :href="sub_activity_1_help_url"
                                            target="_blank"
                                            ><i
                                                class="fa fa-question-circle"
                                                style="color: blue"
                                                >&nbsp;</i
                                            ></a
                                        ></label
                                    >
                                    <div class="col-sm-12">
                                        <div
                                            id="select_proposal_apply_sub_activity1_parent"
                                            class="form-group"
                                        >
                                            <select
                                                id="select_proposal_apply_sub_activity1"
                                                ref="select_proposal_apply_sub_activity1"
                                                v-model="selected_sub_activity1"
                                                class="form-control"
                                                style="width: 40%"
                                                @change="
                                                    chainedSelectSubActivities2(
                                                        selected_sub_activity1
                                                    )
                                                "
                                            >
                                                <option
                                                    value=""
                                                    selected
                                                    disabled
                                                >
                                                    Select sub_activity 1
                                                </option>
                                                <option
                                                    v-for="sub_activity1 in sub_activities1"
                                                    :key="sub_activity1.value"
                                                    :value="sub_activity1.value"
                                                >
                                                    {{ sub_activity1.text }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="sub_activities2.length > 0">
                                    <label
                                        for="select_proposal_apply_sub_activity2"
                                        class="control-label"
                                        >Sub Activity 2 *
                                        <a
                                            :href="sub_activity_2_help_url"
                                            target="_blank"
                                            ><i
                                                class="fa fa-question-circle"
                                                style="color: blue"
                                                >&nbsp;</i
                                            ></a
                                        ></label
                                    >
                                    <div class="col-sm-12">
                                        <div
                                            id="select_proposal_apply_sub_activity2_parent"
                                            class="form-group"
                                        >
                                            <select
                                                id="select_proposal_apply_sub_activity2"
                                                ref="select_proposal_apply_sub_activity2"
                                                v-model="selected_sub_activity2"
                                                class="form-control"
                                                style="width: 40%"
                                                @change="
                                                    chainedSelectCategories(
                                                        selected_sub_activity2
                                                    )
                                                "
                                            >
                                                <option
                                                    value=""
                                                    selected
                                                    disabled
                                                >
                                                    Select sub_activity 2
                                                </option>
                                                <option
                                                    v-for="sub_activity2 in sub_activities2"
                                                    :key="sub_activity2.value"
                                                    :value="sub_activity2.value"
                                                >
                                                    {{ sub_activity2.text }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>

                                <div v-if="categories.length > 0">
                                    <label
                                        for="select_proposal_apply_category"
                                        class="control-label"
                                        >Category *
                                        <a
                                            :href="category_help_url"
                                            target="_blank"
                                            ><i
                                                class="fa fa-question-circle"
                                                style="color: blue"
                                                >&nbsp;</i
                                            ></a
                                        ></label
                                    >
                                    <div class="col-sm-12">
                                        <div
                                            id="select_proposal_apply_category_parent"
                                            class="form-group"
                                        >
                                            <select
                                                id="select_proposal_apply_category"
                                                ref="select_proposal_apply_category"
                                                v-model="selected_category"
                                                class="form-control"
                                                style="width: 40%"
                                                @change="
                                                    get_approval_level(
                                                        selected_category
                                                    )
                                                "
                                            >
                                                <option
                                                    value=""
                                                    selected
                                                    disabled
                                                >
                                                    Select category
                                                </option>
                                                <option
                                                    v-for="category in categories"
                                                    :key="category.value"
                                                    :value="category.value"
                                                    :name="category.approval"
                                                >
                                                    {{ category.text }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </FormSection>
                    </div>

                    <div v-show="has_active_proposals()" class="col-sm-12">
                        <p style="color: red">
                            This organisation has a current commercial
                            operations application or licence: You can apply to
                            amend a licence from the licences table on the home
                            dashboard.
                        </p>
                        <p style="color: red">{{ active_proposals() }}</p>
                    </div>
                    <div class="col-sm-12">
                        <button
                            v-if="!creatingProposal"
                            :disabled="isDisabled() || has_active_proposals()"
                            class="btn btn-primary pull-right"
                            @click.prevent="submit()"
                        >
                            Continue
                        </button>
                        <button
                            v-else
                            disabled
                            class="pull-right btn btn-primary"
                        >
                            <i class="fa fa-spin fa-spinner"></i>&nbsp;Creating
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import { api_endpoints, helpers } from '@/utils/hooks';
import utils from './utils';
import FormSection from '@/components/forms/section_toggle.vue';
import { v4 as uuid } from 'uuid';

export default {
    components: {
        FormSection,
    },
    beforeRouteEnter: function (to, from, next) {
        let initialisers = [utils.fetchProfile()];
        next((vm) => {
            vm.loading.push('fetching profile');
            Promise.all(initialisers).then((data) => {
                vm.profile = data[0];
                vm.loading.splice('fetching profile', 1);
            });
        });
    },
    data: function () {
        return {
            proposal: null,
            agent: {},
            behalf_of: '',
            org_applicant: '',
            yourself: '',
            profile: {
                commercialoperator_organisations: [],
            },
            loading: [],
            form: null,
            pBody: 'pBody' + uuid(),
            pBody2: 'pBody2' + uuid(),

            selected_application_id: '',
            selected_application_name: '',
            selected_region: '',
            selected_district: '',
            application_types: [],
            selected_activity: '',
            selected_sub_activity1: '',
            selected_sub_activity2: '',
            selected_category: '',
            regions: [],
            districts: [],
            activity_matrix: [],
            activities: [],
            sub_activities1: [],
            sub_activities2: [],
            categories: [],
            approval_level: '',
            creatingProposal: false,
            selected_copy_from: null,
            display_region_selectbox: false,
            display_activity_matrix_selectbox: false,
            site_url: api_endpoints.site_url.endsWith('/')
                ? api_endpoints.site_url
                : api_endpoints.site_url + '/',
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0;
        },
        org: function () {
            let vm = this;
            if (vm.org_applicant != '' && vm.org_applicant != 'yourself') {
                return vm.profile.commercialoperator_organisations.find(
                    (org) => parseInt(org.id) === parseInt(vm.org_applicant)
                ).name;
            }
            return vm.org_applicant;
        },
        manyDistricts: function () {
            return this.districts.length > 1;
        },
        proposal_type_help_url: function () {
            return api_endpoints.proposal_type_help_url;
        },
        region_help_url: function () {
            return this.site_url + 'help/commercialoperator/user/#apply_region';
        },
        district_help_url: function () {
            return (
                this.site_url + 'help/commercialoperator/user/#apply_district'
            );
        },
        activity_type_help_url: function () {
            return (
                this.site_url +
                'help/commercialoperator/user/#apply_activity_type'
            );
        },
        sub_activity_1_help_url: function () {
            return (
                this.site_url +
                'help/commercialoperator/user/#apply_sub_activity_1'
            );
        },
        sub_activity_2_help_url: function () {
            return (
                this.site_url +
                'help/commercialoperator/user/#apply_sub_activity_2'
            );
        },
        category_help_url: function () {
            return (
                this.site_url + 'help/commercialoperator/user/#apply_category'
            );
        },
        application_type_tclass: function () {
            return api_endpoints.t_class;
        },
        application_type_filming: function () {
            return api_endpoints.filming;
        },
        application_type_event: function () {
            return api_endpoints.event;
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchRegions();
        vm.fetchApplicationTypes();
        vm.form = document.forms.new_proposal;

        vm.$nextTick(() => {
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_license_type',
                    'select_proposal_apply_license_type_parent',
                    'selected_application_id',
                    'Select a License Type *',
                    false
                )
                .on('select2:select', function () {
                    vm.chainedSelectAppType(vm.selected_application_id);
                });
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_region',
                    'select_proposal_apply_region_parent',
                    'selected_region',
                    'Select a Region',
                    false
                )
                .on('select2:select', function () {
                    vm.chainedSelectDistricts(vm.selected_region);
                });
            helpers.initialiseSelect2.bind(this)(
                'select_proposal_apply_district',
                'select_proposal_apply_district_parent',
                'selected_district',
                'Select a District',
                false
            );
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_activity',
                    'select_proposal_apply_activity_parent',
                    'selected_activity',
                    'Select an Activity Type',
                    false
                )
                .on('select2:select', function () {
                    vm.chainedSelectSubActivities1(vm.selected_activity);
                });
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_sub_activity1',
                    'select_proposal_apply_sub_activity1_parent',
                    'selected_sub_activity1',
                    'Select Sub Activity 1',
                    false
                )
                .on('select2:select', function () {
                    vm.chainedSelectSubActivities2(vm.selected_sub_activity1);
                });
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_sub_activity2',
                    'select_proposal_apply_sub_activity2_parent',
                    'selected_sub_activity2',
                    'Select Sub Activity 2',
                    false
                )
                .on('select2:select', function () {
                    vm.chainedSelectCategories(vm.selected_sub_activity2);
                });
            helpers.initialiseSelect2
                .bind(this)(
                    'select_proposal_apply_category',
                    'select_proposal_apply_category_parent',
                    'selected_category',
                    'Select a Category',
                    false
                )
                .on('select2:select', function () {
                    vm.get_approval_level(vm.selected_category);
                });
            helpers.initialiseSelect2.bind(this)(
                'select_proposal_apply_copy_license',
                'select_proposal_apply_copy_license_parent',
                'selected_copy_from',
                'Select an Event License to copy from *',
                false
            );
        });
    },
    methods: {
        has_active_proposals: function () {
            return this.active_proposals().length > 0;
        },
        active_proposals: function () {
            // returns active 'T Class' proposals - cannot have more than 1 active 'T Class' application at a time
            let vm = this;
            var proposals = [];
            var org = vm.profile.commercialoperator_organisations.find(
                (el) => el.name === vm.org
            );
            if (
                org &&
                vm.selected_application_name == vm.application_type_tclass
            ) {
                proposals = org.active_proposals.find(
                    (el) => el.application_type === vm.application_type_tclass
                ).proposals;
            }
            return proposals;
        },
        has_event_proposals: function () {
            return this.event_proposals().length > 0;
        },
        event_proposals: function () {
            // returns active 'T Class' proposals - cannot have more than 1 active 'T Class' application at a time
            let vm = this;
            var proposals = [];
            var org = vm.profile.commercialoperator_organisations.find(
                (el) => el.name === vm.org
            );
            if (
                org &&
                vm.selected_application_name == vm.application_type_event
            ) {
                proposals = org.current_event_proposals.find(
                    (el) => el.application_type === vm.application_type_event
                ).proposals;
            }
            return proposals;
        },
        submit: function () {
            let vm = this;
            console.log(vm.org_applicant);
            swal.fire({
                title: 'Create ' + vm.selected_application_name,
                text:
                    'Are you sure you want to create ' +
                    this.alertText() +
                    ' application on behalf of ' +
                    vm.org +
                    ' ?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Accept',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed && !vm.has_active_proposals()) {
                        vm.createProposal();
                    }
                }
            );
        },
        alertText: function () {
            let vm = this;
            if (vm.selected_application_name == vm.application_type_tclass) {
                return 'a ' + vm.application_type_tclass;
            } else if (
                vm.selected_application_name == vm.application_type_filming
            ) {
                return 'a ' + vm.application_type_filming;
            } else if (
                vm.selected_application_name == vm.application_type_event
            ) {
                return 'an ' + vm.application_type_event;
            }
        },
        createProposal: function () {
            let vm = this;
            vm.creatingProposal = true;
            if (vm.org_applicant == 'yourself') {
                vm.org_applicant = '';
            }
            const data = {
                org_applicant: vm.org_applicant,
                application: vm.selected_application_id,
                region: vm.selected_region,
                district: vm.selected_district,
                activity: vm.selected_activity,
                sub_activity1: vm.selected_sub_activity1,
                sub_activity2: vm.selected_sub_activity2,
                category: vm.selected_category,
                approval_level: vm.approval_level,
                selected_copy_from: vm.selected_copy_from,
            };
            helpers
                .fetchUrl('/api/proposal.json', {
                    method: 'POST',
                    body: JSON.stringify(data),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(
                    (res) => {
                        vm.proposal = res;
                        vm.$router.push({
                            name: 'draft_proposal',
                            params: { proposal_id: vm.proposal.id },
                        });
                        vm.creatingProposal = false;
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        isDisabled: function () {
            let vm = this;
            if (
                (vm.org_applicant == '' && vm.yourself == '') ||
                vm.selected_application_id == ''
            ) {
                return true;
            }
            return false;
        },
        fetchRegions: function () {
            let vm = this;

            helpers.fetchUrl(api_endpoints.regions).then(
                (response) => {
                    vm.api_regions = response;

                    for (var i = 0; i < vm.api_regions.length; i++) {
                        this.regions.push({
                            text: vm.api_regions[i].name,
                            value: vm.api_regions[i].id,
                            districts: vm.api_regions[i].districts,
                        });
                    }
                },
                (error) => {
                    console.log(error);
                }
            );
        },

        searchList: function (id, search_list) {
            /* Searches for dictionary in list */
            for (var i = 0; i < search_list.length; i++) {
                if (search_list[i].value == id) {
                    return search_list[i];
                }
            }
            return [];
        },
        chainedSelectDistricts: function (region_id) {
            let vm = this;
            vm.districts = [];

            var api_districts = this.searchList(
                region_id,
                vm.regions
            ).districts;
            if (api_districts.length > 0) {
                for (var i = 0; i < api_districts.length; i++) {
                    this.districts.push({
                        text: api_districts[i].name,
                        value: api_districts[i].id,
                    });
                }
            }
        },
        fetchApplicationTypes: function () {
            let vm = this;

            helpers.fetchUrl(api_endpoints.application_types).then(
                (response) => {
                    vm.api_app_types = response.results;
                    for (var i = 0; i < vm.api_app_types.length; i++) {
                        this.application_types.push({
                            text: vm.api_app_types[i].name,
                            value: vm.api_app_types[i].id,
                        });
                    }
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        chainedSelectAppType: function (application_id) {
            /* reset */
            let vm = this;
            vm.selected_region = '';
            vm.selected_district = '';
            vm.selected_activity = '';
            vm.display_region_selectbox = false;
            vm.display_activity_matrix_selectbox = false;
            vm.selected_copy_from = null;

            vm.selected_application_name = this.searchList(
                application_id,
                vm.application_types
            ).text;

            if (vm.selected_application_name == 'Western Power Maintenance') {
                vm.display_region_selectbox = true;
                vm.display_activity_matrix_selectbox = true;
            }
        },

        fetchActivityMatrix: function () {
            let vm = this;
            vm.sub_activities1 = [];
            vm.sub_activities2 = [];
            vm.categories = [];
            vm.approval_level = '';

            helpers.fetchUrl(api_endpoints.activity_matrix).then(
                (response) => {
                    this.activity_matrix = response[0].schema[0];
                    this.keys_ordered = response[0].ordered;

                    var keys = this.keys_ordered
                        ? Object.keys(this.activity_matrix).sort()
                        : Object.keys(this.activity_matrix);
                    for (var i = 0; i < keys.length; i++) {
                        this.activities.push({ text: keys[i], value: keys[i] });
                    }
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        chainedSelectSubActivities1: function (activity_name) {
            let vm = this;
            vm.sub_activities1 = [];
            vm.sub_activities2 = [];
            vm.categories = [];
            vm.selected_sub_activity1 = '';
            vm.selected_sub_activity2 = '';
            vm.selected_category = '';
            vm.approval_level = '';

            vm.sub_activities1 = [];
            var [api_activities, res] = this.get_sub_matrix(
                activity_name,
                vm.activity_matrix
            );
            if (res == 'null' || res == null) {
                vm.approval_level = api_activities;
                return;
            } else if (res == 'pass') {
                var api_sub_activities = this.get_sub_matrix(
                    'pass',
                    api_activities[0]
                )[0];
                if ('pass' in api_sub_activities[0]) {
                    // go straight to categories widget
                    var categories = api_sub_activities[0]['pass'];
                    for (let i = 0; i < categories.length; i++) {
                        this.categories.push({
                            text: categories[i][0],
                            value: categories[i][0],
                            approval: categories[i][1],
                        });
                    }
                } else {
                    // go to sub_activity2 widget
                    for (let i = 0; i < api_sub_activities.length; i++) {
                        var key = Object.keys(api_activities[i])[0];
                        this.sub_activities1.push({
                            text: key,
                            value: key,
                            sub_matrix: api_activities[i][key],
                        });
                    }
                }
            } else {
                for (let i = 0; i < api_activities.length; i++) {
                    const key = Object.keys(api_activities[i])[0];
                    this.sub_activities1.push({
                        text: key,
                        value: key,
                        sub_matrix: api_activities[i][key],
                    });
                }
            }
        },

        chainedSelectSubActivities2: function (activity_name) {
            let vm = this;
            vm.sub_activities2 = [];
            vm.categories = [];
            vm.selected_sub_activity2 = '';
            vm.selected_category = '';
            vm.approval_level = '';

            var [api_activities, res] = this.get_sub_matrix(
                activity_name,
                vm.sub_activities1
            );
            if (res == 'null' || res == null) {
                vm.approval_level = api_activities;
                return;
            } else if (res == 'pass') {
                for (var i = 0; i < api_activities.length; i++) {
                    this.categories.push({
                        text: api_activities[i][0],
                        value: api_activities[i][0],
                        approval: api_activities[i][1],
                    });
                }
            } else {
                for (let i = 0; i < vm.sub_activities1.length; i++) {
                    if (activity_name == vm.sub_activities1[i]['text']) {
                        var api_activities2 =
                            vm.sub_activities1[i]['sub_matrix'];
                        for (var j = 0; j < api_activities2.length; j++) {
                            var key = Object.keys(api_activities2[j])[0];
                            this.sub_activities2.push({
                                text: key,
                                value: key,
                                sub_matrix: api_activities2[j][key],
                            });
                        }
                    }
                }
            }
        },
        chainedSelectCategories: function (activity_name) {
            let vm = this;
            vm.categories = [];
            vm.selected_category = '';
            vm.approval_level = '';

            for (var i = 0; i < vm.sub_activities2.length; i++) {
                if (activity_name == vm.sub_activities2[i]['text']) {
                    var api_categories = vm.sub_activities2[i]['sub_matrix'];
                    for (var j = 0; j < api_categories.length; j++) {
                        this.categories.push({
                            text: api_categories[j][0],
                            value: api_categories[j][0],
                            approval: api_categories[j][1],
                        });
                    }
                }
            }
        },

        get_sub_matrix: function (activity_name, sub_activities) {
            if (activity_name in sub_activities) {
                if (sub_activities[activity_name].length > 0) {
                    if ('pass' in sub_activities[activity_name][0]) {
                        return [sub_activities[activity_name], 'pass'];
                    } else if ('null' in sub_activities[activity_name][0]) {
                        let approval_level;
                        if (
                            sub_activities[activity_name]['sub_matrix'] == null
                        ) {
                            approval_level =
                                sub_activities[activity_name][0]['null'][0][0];
                        } else {
                            approval_level =
                                sub_activities[activity_name]['sub_matrix'][0][
                                    'null'
                                ][0];
                        }
                        return [approval_level, 'null'];
                    }
                }

                // not a sub_matrix --> this is the main activity_matrix data (as provided by the REST API)
                return [sub_activities[activity_name], true];
            }
            for (var i = 0; i < sub_activities.length; i++) {
                if (activity_name == sub_activities[i]['text']) {
                    var key_sub_matrix = Object.keys(
                        sub_activities[i]['sub_matrix'][0]
                    )[0];
                    if (key_sub_matrix == 'null') {
                        var approval_level =
                            sub_activities[i]['sub_matrix'][0]['null'][0];
                        return [approval_level, null];
                    } else if (key_sub_matrix == 'pass') {
                        return [
                            sub_activities[i]['sub_matrix'][0]['pass'],
                            'pass',
                        ];
                    } else {
                        return [sub_activities[i]['sub_matrix'][0], true];
                    }
                }
            }
        },
        get_approval_level: function (category_name) {
            let vm = this;
            for (var i = 0; i < vm.categories.length; i++) {
                if (category_name == vm.categories[i]['text']) {
                    vm.approval_level = vm.categories[i]['approval'];
                }
            }
        },
    },
};
</script>

<style lang="css">
input[type='text'],
select {
    width: 40%;
    box-sizing: border-box;

    min-height: 34px;
    padding: 0;
    height: auto;
}

.group-box {
    border-style: solid;
    border-width: thin;
    border-color: #ffffff;
}
</style>
