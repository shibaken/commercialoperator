<template lang="html">
    <div class="container">
        <PrivacyNotice />

        <form
            :action="proposal_form_url"
            method="post"
            name="new_proposal"
            enctype="multipart/form-data"
        >
            <div v-if="!proposal_readonly">
                <div v-if="hasAmendmentRequest" class="row" style="color: red">
                    <div class="col-lg-12 pull-right">
                            <FormSection
                                :form-collapse="false"
                                label="An amendment has been requested for this Application"
                                index="amendment_request"
                                subtitle=""
                            >
                                <div
                                    v-for="a in amendment_request"
                                    :key="a.reason"
                                >
                                    <p>Reason: {{ a.reason }}</p>
                                    <p>Details:</p>
                                    <p v-for="t in splitText(a.text)" :key="t">
                                        {{ t }}
                                    </p>
                                </div>
                            </FormSection>
                    </div>
                </div>
            </div>

            <div
                v-if="missing_fields.length > 0"
                id="error"
                style="
                    margin: 10px;
                    padding: 5px;
                    color: red;
                    border: 1px solid red;
                "
            >
                <b>Please answer the following mandatory question(s):</b>
                <ul>
                    <li v-for="error in missing_fields" :key="error">
                        {{ error.label }}
                    </li>
                </ul>
            </div>

            <div v-if="proposal" id="scrollspy-heading" class="col-lg-12">
                <h4>
                    Commercial Operator -
                    {{ proposal.application_type }} application:
                    {{ proposal.lodgement_number }}
                </h4>
            </div>

            <ProposalTClass
                v-if="
                    proposal &&
                    proposal_parks &&
                    proposal.application_type == application_type_tclass
                "
                id="proposalStart"
                ref="proposal_tclass"
                :proposal="proposal"
                :can-edit-activities="canEditActivities"
                :is_external="true"
                :proposal_parks="proposal_parks"
            ></ProposalTClass>
            <ProposalFilming
                v-else-if="
                    proposal &&
                    proposal.application_type == application_type_filming
                "
                id="proposalStart"
                ref="proposal_filming"
                :proposal="proposal"
                :can-edit-activities="canEditActivities"
                :can-edit-period="canEditPeriod"
                :is_external="true"
                :proposal_parks="proposal_parks"
            ></ProposalFilming>
            <ProposalEvent
                v-else-if="
                    proposal &&
                    proposal.application_type == application_type_event
                "
                id="proposalStart"
                ref="proposal_event"
                :proposal="proposal"
                :can-edit-activities="canEditActivities"
                :can-edit-period="canEditPeriod"
                :is_external="true"
                :proposal_parks="proposal_parks"
            ></ProposalEvent>

            <div>
                <input
                    type="hidden"
                    name="csrfmiddlewaretoken"
                    :value="csrf_token"
                />
                <input
                    type="hidden"
                    name="schema"
                    :value="JSON.stringify(proposal)"
                />
                <input type="hidden" name="proposal_id" :value="1" />

                <div class="row" style="margin-bottom: 50px">
                    <div
                        class="navbar navbar-nav navbar-fixed-bottom ms-auto align-items-end"
                        style="background-color: #f5f5f5"
                    >
                        <div>
                            <div
                                v-if="proposal && !proposal.readonly"
                                class="container-fluid"
                            >
                                <p class="pull-right" style="margin-top: 5px">
                                    <button
                                        v-if="saveExitProposal"
                                        type="button"
                                        class="btn btn-primary"
                                        disabled
                                    >
                                        Save and Exit&nbsp;
                                        <i
                                            class="fas fa-circle-notch fa-spin fa-fw"
                                        ></i>
                                    </button>
                                    <input
                                        v-else
                                        type="button"
                                        class="btn btn-primary me-2"
                                        value="Save and Exit"
                                        :disabled="
                                            savingProposal || paySubmitting
                                        "
                                        @click.prevent="save_exit"
                                    />
                                    <button
                                        v-if="savingProposal"
                                        type="button"
                                        class="btn btn-primary me-2"
                                        disabled
                                    >
                                        Save and Continue&nbsp;
                                        <i
                                            class="fas fa-circle-notch fa-spin fa-fw"
                                        ></i>
                                    </button>
                                    <input
                                        v-else
                                        type="button"
                                        class="btn btn-primary me-2"
                                        value="Save and Continue"
                                        :disabled="
                                            saveExitProposal || paySubmitting
                                        "
                                        @click.prevent="save"
                                    />

                                    <button
                                        v-if="paySubmitting"
                                        type="button"
                                        class="btn btn-primary me-2"
                                        disabled
                                    >
                                        {{ submit_text() }}&nbsp;
                                        <i
                                            class="fas fa-circle-notch fa-spin fa-fw"
                                        ></i>
                                    </button>
                                    <input
                                        v-else
                                        type="button"
                                        class="btn btn-primary me-2"
                                        :value="submit_text()"
                                        :disabled="
                                            !trainingCompleted ||
                                            saveExitProposal ||
                                            savingProposal
                                        "
                                        :title="completed_online_training"
                                        @click.prevent="submit"
                                    />
                                    <input
                                        id="save_and_continue_btn"
                                        type="hidden"
                                        class="btn btn-primary me-2"
                                        value="Save Without Confirmation"
                                        @click.prevent="save_wo_confirm"
                                    />
                                </p>
                            </div>
                            <div v-else class="container-fluid">
                                <p class="float-end" style="margin-top: 5px">
                                    <router-link
                                        class="btn btn-primary me-2"
                                        :to="{
                                            name: 'external-proposals-dash',
                                        }"
                                        >Back to Dashboard</router-link
                                    >
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
import ProposalTClass from '../form_tclass.vue';
import ProposalFilming from '../form_filming.vue';
import ProposalEvent from '../form_event.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import PrivacyNotice from '@/components/common/privacy_notice.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import $ from 'jquery'
export default {
    name: 'ExternalProposal',
    components: {
        FormSection,
        ProposalTClass,
        ProposalFilming,
        ProposalEvent,
        PrivacyNotice,
    },

    beforeRouteEnter: function (to, from, next) {
        if (to.params.proposal_id) {
            helpers
                .fetchUrl(`/api/proposal/${to.params.proposal_id}.json`)
                .then(
                    (res) => {
                        next((vm) => {
                            vm.loading.push('fetching proposal');
                            vm.proposal = res;
                            //used in activities_land for T Class licence
                            vm.proposal.selected_trails_activities = [];
                            vm.proposal.selected_parks_activities = [];
                            vm.proposal.marine_parks_activities = [];
                            vm.loading.splice('fetching proposal', 1);
                            vm.setdata(vm.proposal.readonly);
                            vm.fetchProposalParks(to.params.proposal_id);

                            helpers
                                .fetchUrl(
                                    helpers.add_endpoint_json(
                                        api_endpoints.proposals,
                                        to.params.proposal_id +
                                            '/amendment_request'
                                    )
                                )
                                .then(
                                    (res) => {
                                        vm.setAmendmentData(res);
                                    },
                                    (err) => {
                                        console.log(err);
                                    }
                                );
                        });
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        } else {
            helpers
                .fetchUrl('/api/proposal.json', {
                    method: 'POST',
                })
                .then(
                    (res) => {
                        next((vm) => {
                            vm.loading.push('fetching proposal');
                            vm.proposal = res;
                            vm.loading.splice('fetching proposal', 1);
                        });
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        }
    },
    data: function () {
        return {
            proposal: null,
            loading: [],
            form: null,
            amendment_request: [],
            saveError: false,
            proposal_readonly: true,
            hasAmendmentRequest: false,
            submitting: false,
            saveExitProposal: false,
            savingProposal: false,
            paySubmitting: false,
            newText: '',
            pBody: 'pBody',
            missing_fields: [],
            proposal_parks: null,
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        proposal_form_url: function () {
            return this.proposal
                ? `/api/proposal/${this.proposal.id}/draft.json`
                : '';
        },
        application_fee_url: function () {
            return this.proposal ? `/application_fee/${this.proposal.id}/` : '';
        },
        proposal_submit_url: function () {
            return this.proposal
                ? `/api/proposal/${this.proposal.id}/submit.json`
                : '';
        },
        canEditActivities: function () {
            return this.proposal ? this.proposal.can_user_edit : 'false';
        },
        canEditPeriod: function () {
            return this.proposal ? this.proposal.can_user_edit : 'false';
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
        trainingCompleted: function () {
            if (this.proposal.application_type == 'Event') {
                return this.proposal.applicant_training_completed;
            }
            return this.proposal.training_completed;
        },
        completed_online_training: function () {
            return !this.trainingCompleted
                ? "Please complete 'Online Training'"
                : '';
        },
    },

    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_proposal;
        window.addEventListener('beforeunload', vm.leaving);
        window.addEventListener('onblur', vm.leaving);
    },
    methods: {
        proposal_refs: function () {
            let vm = this;
            if (vm.proposal.application_type == vm.application_type_tclass) {
                return vm.$refs.proposal_tclass;
            } else if (
                vm.proposal.application_type == vm.application_type_filming
            ) {
                return vm.$refs.proposal_filming;
            } else if (
                vm.proposal.application_type == vm.application_type_event
            ) {
                return vm.$refs.proposal_event;
            }
        },

        submit_text: function () {
            let vm = this;
            if (vm.proposal.application_type == vm.application_type_filming) {
                // Filming has deferred payment once assessor decides whether 'Licence' (has a fee) or 'Lawful Authority' (has no fee) is to be issued
                return 'Submit';
            } else if (vm.proposal.fee_paid) {
                return 'Resubmit';
            } else if (vm.proposal.allow_full_discount) {
                return 'Submit';
            } else {
                return 'Pay and Submit';
            }
        },
        set_formData: function (validate_form = false) {
            let vm = this;
            if (validate_form && !helpers.validateForm(vm.form)) {
                throw new Error('Please fix the form errors before saving');
            }
            let formData = new FormData(vm.form);

            formData.append(
                'selected_parks_activities',
                JSON.stringify(vm.proposal.selected_parks_activities)
            );
            formData.append(
                'selected_trails_activities',
                JSON.stringify(vm.proposal.selected_trails_activities)
            );
            formData.append(
                'marine_parks_activities',
                JSON.stringify(vm.proposal.marine_parks_activities)
            );

            return formData;
        },
        save: async function () {
            let vm = this;
            vm.savingProposal = true;

            let formData;
            try {
                formData = vm.set_formData();
            } catch (e) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: e.message,
                    icon: 'error',
                });
                return;
            }

            const result = helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        vm.savingProposal = false;
                        return swal.fire({
                            title: 'Saved',
                            text: 'Your application has been saved',
                            icon: 'success',
                        });
                    },
                    (error) => {
                        vm.savingProposal = false;
                        return swal.fire({
                            title: 'Save Error',
                            text: error,
                            icon: 'error',
                        });
                    }
                );
            return result;
        },
        save_exit: async function (e) {
            let vm = this;
            this.submitting = true;
            this.saveExitProposal = true;
            await this.save(e)
                .then(
                    () => {
                        // After saving, redirect to the dashboard
                        vm.$router.push({
                            name: 'external-proposals-dash',
                        });
                    },
                    (err) => {
                        console.log(err);
                        vm.submitting = false;
                        vm.saveExitProposal = false;
                    }
                )
                .finally(() => {
                    // Reset the saveExitProposal flag
                    vm.saveExitProposal = false;
                });
        },

        save_wo_confirm: function () {
            let vm = this;
            let formData;
            try {
                formData = vm.set_formData();
            } catch (e) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: e.message,
                    icon: 'error',
                });
                return;
            }

            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        swal.fire({
                            title: 'Saved',
                            text: 'Your application has been saved',
                            icon: 'success',
                        });
                    },
                    (err) => {
                        var errorText = helpers.apiVueResourceError(err);
                        swal.fire({
                            title: 'Save Error',
                            text: errorText,
                            icon: 'error',
                        });
                    }
                );
        },
        save_before_submit: async function () {
            let vm = this;
            let formData;
            try {
                // Validate the form before saving
                formData = vm.set_formData(true);
            } catch (e) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: e.message,
                    icon: 'error',
                });
                return;
            }
            vm.saveError = false;

            const result = await helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        //
                    },
                    (err) => {
                        var errorText = helpers.apiVueResourceError(err);
                        swal.fire({
                            title: 'Save Error',
                            text: errorText,
                            icon: 'error',
                        });
                        vm.paySubmitting = false;
                        vm.saveError = true;
                    }
                );
            return result;
        },

        save_and_redirect: function () {
            let vm = this;
            let formData;
            try {
                formData = vm.set_formData();
            } catch (e) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: e.message,
                    icon: 'error',
                });
                return;
            }

            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        /* after the above save, redirect to the Django post() method in ApplicationFeeView */
                        vm.post_and_redirect(vm.application_fee_url, {
                            csrfmiddlewaretoken: vm.csrf_token,
                        });
                    },
                    (err) => {
                        var errorText = helpers.apiVueResourceError(err);
                        swal.fire({
                            title: 'Save Error',
                            text: errorText,
                            icon: 'error',
                        });
                        vm.paySubmitting = false;
                    }
                );
        },

        setdata: function (readonly) {
            this.proposal_readonly = readonly;
        },

        setAmendmentData: function (amendment_request) {
            this.amendment_request = amendment_request;

            if (amendment_request.length > 0) this.hasAmendmentRequest = true;
        },

        splitText: function (aText) {
            let newText = '';
            newText = aText.split('\n');
            return newText;
        },

        leaving: function (e) {
            let vm = this;
            var dialogText = 'You have some unsaved changes.';
            if (!vm.proposal_readonly && !vm.submitting) {
                e.returnValue = dialogText;
                return dialogText;
            } else {
                return null;
            }
        },

        highlight_missing_fields: function () {
            let vm = this;
            for (var missing_field of vm.missing_fields) {
                $('#' + missing_field.id).css('color', 'red');
            }
        },

        validate: function () {
            let vm = this;

            // reset default colour
            for (var field of vm.missing_fields) {
                $('#' + field.id).css('color', '#515151');
            }
            vm.missing_fields = [];

            // get all required fields, that are not hidden in the DOM
            var required_fields = $(
                'input[type=text]:required, textarea:required, input[type=checkbox]:required, input[type=radio]:required, input[type=file]:required, select:required'
            ).not(':hidden');

            // loop through all (non-hidden) required fields, and check data has been entered
            required_fields.each(function () {
                let id = 'id_' + this.name;
                if (this.type == 'radio') {
                    if (!$('input[name=' + this.name + ']').is(':checked')) {
                        let text = $('#' + id).text();
                        console.log(
                            'radio not checked: ' + this.type + ' ' + text
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'checkbox') {
                    id = 'id_' + this.classList['value'];
                    if (
                        $('[class=' + this.classList['value'] + ']:checked')
                            .length == 0
                    ) {
                        text = $('#' + id).text();
                        console.log(
                            'checkbox not checked: ' + this.type + ' ' + text
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'select-one') {
                    if ($(this).val() == '') {
                        text = $('#' + id).text(); // this is the (question) label
                        id = 'id_' + $(this).prop('name'); // the label id
                        console.log(
                            'selector not selected: ' + this.type + ' ' + text
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'file') {
                    var num_files = $('#' + id).attr('num_files');
                    if (num_files == '0') {
                        var text = $('#' + id).text();
                        console.log(
                            'file not uploaded: ' + this.type + ' ' + this.name
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'text') {
                    if (this.value == '') {
                        text = $('#' + id).text();
                        console.log(
                            'text not provided: ' + this.type + ' ' + this.name
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }

                if (this.type == 'textarea') {
                    if (this.value == '') {
                        text = $('#' + id).text();
                        console.log(
                            'textarea not provided: ' +
                                this.type +
                                ' ' +
                                this.name
                        );
                        vm.missing_fields.push({ id: id, label: text });
                    }
                }
            });

            return vm.missing_fields.length;
        },

        can_submit: function () {
            let vm = this;
            let blank_fields = [];

            if (vm.proposal.application_type == vm.application_type_tclass) {
                if (
                    vm.$refs.proposal_tclass.$refs.other_details
                        .selected_accreditations.length == 0
                ) {
                    blank_fields.push(' Level of Accreditation is required');
                } else {
                    for (
                        var i = 0;
                        i < vm.proposal.other_details.accreditations.length;
                        i++
                    ) {
                        if (
                            !vm.proposal.other_details.accreditations[i]
                                .is_deleted &&
                            vm.proposal.other_details.accreditations[i]
                                .accreditation_type != 'no' && 
                            vm.proposal.other_details.accreditations[i].accreditation_type!='narta'
                        ) {
                            if (
                                vm.proposal.other_details.accreditations[i]
                                    .accreditation_expiry == null ||
                                vm.proposal.other_details.accreditations[i]
                                    .accreditation_expiry == ''
                            ) {
                                blank_fields.push(
                                    'Expiry date for accreditation type ' +
                                        vm.proposal.other_details
                                            .accreditations[i]
                                            .accreditation_type_value +
                                        ' is required'
                                );
                            }
                            var acc_ref =
                                vm.proposal.other_details.accreditations[i]
                                    .accreditation_type;
                            if (
                                vm.$refs.proposal_tclass.$refs.other_details
                                    .$refs[acc_ref][0].$refs.accreditation_file
                                    .documents.length == 0
                            ) {
                                blank_fields.push(
                                    'Accreditation Certificate for accreditation type ' +
                                        vm.proposal.other_details
                                            .accreditations[i]
                                            .accreditation_type_value +
                                        ' is required'
                                );
                            }
                        }
                    }
                }
        if (vm.$refs.proposal_tclass.$refs.other_details.selected_information_standards.length==0 ){
            blank_fields.push(' Accessible Tourism Information is required')
          }
          else{
            for(var j=0; j<vm.proposal.other_details.information_standards.length; j++){
              if(!vm.proposal.other_details.information_standards[j].is_deleted && vm.proposal.other_details.information_standards[j].information_standard_type!='no'){
                if(vm.proposal.other_details.information_standards[j].information_comments==null || vm.proposal.other_details.information_standards[j].information_comments==''){
                  blank_fields.push('Details for accessible tourism information type '+vm.proposal.other_details.information_standards[j].information_standard_type_value+' are required')
                }
              }
            }
          }
          if (vm.$refs.proposal_tclass.$refs.other_details.selected_emission_standards.length==0 ){
            blank_fields.push(' Tourism Emission Reduction Standards is required')
          }
          else{
            for(var k=0; k<vm.proposal.other_details.emission_standards.length; k++){
              if(!vm.proposal.other_details.emission_standards[k].is_deleted && vm.proposal.other_details.emission_standards[k].emission_standard_type!='no'){
                if(vm.proposal.other_details.emission_standards[k].emission_comments==null || vm.proposal.other_details.emission_standards[k].emission_comments==''){
                  blank_fields.push('Details for tourism emission reduction standard type '+vm.proposal.other_details.emission_standards[k].emission_standard_type_value+' are required')
                }
              }
            }
          }

                if (
                    vm.proposal.other_details.preferred_licence_period == '' ||
                    vm.proposal.other_details.preferred_licence_period == null
                ) {
                    blank_fields.push(' Preferred Licence Period is required');
                }
                if (
                    vm.proposal.other_details.nominated_start_date == '' ||
                    vm.proposal.other_details.nominated_start_date == null
                ) {
                    blank_fields.push(
                        ' Licence Nominated Start Date is required'
                    );
                }

                if (
                    vm.$refs.proposal_tclass.$refs.other_details.$refs
                        .deed_poll_doc.documents.length == 0
                ) {
                    blank_fields.push(' Deed poll document is missing');
                }

                if (
                    vm.$refs.proposal_tclass.$refs.other_details.$refs
                        .currency_doc.documents.length == 0
                ) {
                    blank_fields.push(
                        ' Certificate of currency document is missing'
                    );
                }
                if (
                    vm.proposal.other_details.insurance_expiry == '' ||
                    vm.proposal.other_details.insurance_expiry == null
                ) {
                    blank_fields.push(
                        ' Certificate of currency expiry date is missing'
                    );
                }
            } else if (
                vm.proposal.application_type == vm.application_type_filming
            ) {
                blank_fields = vm.can_submit_filming();
            } else if (
                vm.proposal.application_type == vm.application_type_event
            ) {
                blank_fields = vm.can_submit_event();
            }

            if (blank_fields.length == 0) {
                return true;
            } else {
                return blank_fields;
            }
        },
        can_submit_event: function () {
            let vm = this;
            let blank_fields = [];

            if (
                vm.proposal.event_activity.event_name == '' ||
                vm.proposal.event_activity.event_name == null
            ) {
                blank_fields.push(' Name of the event is missing');
            }
            if (
                vm.proposal.event_activity.commencement_date == '' ||
                vm.proposal.event_activity.commencement_date == null ||
                vm.proposal.event_activity.completion_date == '' ||
                vm.proposal.event_activity.completion_date == ''
            ) {
                blank_fields.push(' Period of proposed event is required');
            }
            if (
                vm.proposal.event_activity.completion_date != '' &&
                vm.proposal.event_activity.max_num_months_ahead != 0
            ) {
                let completion_date = moment(
                    vm.proposal.event_activity.completion_date,
                    'DD/MM/YYYY'
                );
                let max_future_date = moment().add(
                    vm.proposal.event_activity.max_num_months_ahead,
                    'months'
                );
                if (completion_date > max_future_date) {
                    blank_fields.push(
                        ' Event Completion Date cannot be beyond ' +
                            max_future_date.format('DD-MM-YYYY')
                    );
                }
            }
            if (
                vm.$refs.proposal_event.$refs.event_activities.$refs.parks_table.$refs.park_datatable.vmDataTable
                    .rows()
                    .data().length < 1
            ) {
                blank_fields.push(
                    ' List of parks where the event is proposed to occur is missing'
                );
            }
            if (
                vm.$refs.proposal_event.$refs.event_activities.$refs.parks_table
                    .$refs.event_park_maps.documents.length == 0
            ) {
                blank_fields.push(
                    ' A detailed itinerary and map of the event route document is missing'
                );
            }
            if (vm.proposal.event_activity.pdswa_location) {
                if (
                    vm.$refs.proposal_event.$refs.event_activities.$refs
                        .event_activity_pdswa_file.documents.length == 0
                ) {
                    blank_fields.push(
                        ' Department of Water and Environmental Regulation application form document is missing'
                    );
                }
            }
            if (
                vm.proposal.event_management.num_participants == null ||
                vm.proposal.event_management.num_participants === '' ||
                vm.proposal.event_management.num_participants < 0
            ) {
                blank_fields.push(
                    ' Valid number of participants expected is missing'
                );
            }
            if (
                vm.proposal.event_management.num_spectators == null ||
                vm.proposal.event_management.num_spectators === '' ||
                vm.proposal.event_management.num_spectators < 0
            ) {
                blank_fields.push(
                    ' Valid number of spectators expected is missing'
                );
            }
            if (
                vm.proposal.event_management.num_officials == null ||
                vm.proposal.event_management.num_officials === '' ||
                vm.proposal.event_management.num_officials < 0
            ) {
                blank_fields.push(
                    ' Valid number of officials expected is missing'
                );
            }
            if (
                vm.proposal.event_management.num_vehicles == null ||
                vm.proposal.event_management.num_vehicles === '' ||
                vm.proposal.event_management.num_vehicles < 0
            ) {
                blank_fields.push(
                    ' Valid number of vehicles/ vessels is missing'
                );
            }
            if (vm.proposal.event_management.media_involved) {
                if (
                    vm.proposal.event_management.media_details == null ||
                    vm.proposal.event_management.media_details == ''
                ) {
                    blank_fields.push(' Media involved details are missing');
                }
            }
            if (vm.proposal.event_management.structure_change) {
                if (
                    vm.proposal.event_management.structure_change_details ==
                        null ||
                    vm.proposal.event_management.structure_change_details == ''
                ) {
                    blank_fields.push(' Structure change details are missing');
                }
            }
            if (vm.proposal.event_management.vendor_hired) {
                if (
                    vm.proposal.event_management.vendor_hired_details == null ||
                    vm.proposal.event_management.vendor_hired_details == ''
                ) {
                    blank_fields.push(' Vendors hired details are missing');
                }
            }
            if (vm.proposal.event_management.toilets_provided) {
                if (
                    vm.proposal.event_management.toilets_provided_details ==
                        null ||
                    vm.proposal.event_management.toilets_provided_details == ''
                ) {
                    blank_fields.push(
                        ' Portable toilets and/ or showers details are missing'
                    );
                }
            }
            if (
                vm.proposal.event_management.rubbish_removal_details == null ||
                vm.proposal.event_management.rubbish_removal_details == ''
            ) {
                blank_fields.push(' Remove waste details are missing');
            }
            if (vm.proposal.event_management.approvals_gained) {
                if (
                    vm.proposal.event_management.approvals_gained_details ==
                        null ||
                    vm.proposal.event_management.approvals_gained_details == ''
                ) {
                    blank_fields.push(
                        ' Necessary approvals gained details are missing'
                    );
                }
            }
            if (
                vm.$refs.proposal_event.$refs.event_management.$refs
                    .event_risk_management_plan.documents.length == 0
            ) {
                blank_fields.push(
                    ' Attached copies of your management plans are missing'
                );
            }
            if (vm.proposal.event_management.traffic_management_plan) {
                if (
                    vm.$refs.proposal_event.$refs.event_management.$refs
                        .event_management_traffic_management_plan.documents
                        .length == 0
                ) {
                    blank_fields.push(
                        ' Traffic management plan document missing'
                    );
                }
            }
            if (
                vm.$refs.proposal_event.$refs.event_other_details.$refs
                    .deed_poll_doc.documents.length == 0
            ) {
                blank_fields.push(' Deed poll document is missing');
            }

            if (
                vm.$refs.proposal_event.$refs.event_other_details.$refs
                    .currency_doc.documents.length == 0
            ) {
                blank_fields.push(
                    ' Certificate of currency document is missing'
                );
            }
            if (
                vm.proposal.event_other_details.insurance_expiry == '' ||
                vm.proposal.event_other_details.insurance_expiry == null
            ) {
                blank_fields.push(
                    ' Certificate of currency expiry date is missing'
                );
            }
            return blank_fields;
        },
        can_submit_filming: function () {
            let vm = this;
            let blank_fields = [];
            if (
                vm.proposal.filming_activity.commencement_date == '' ||
                vm.proposal.filming_activity.commencement_date == null ||
                vm.proposal.filming_activity.completion_date == '' ||
                vm.proposal.filming_activity.completion_date == ''
            ) {
                blank_fields.push(
                    ' Period of proposed filming/ photography is required'
                );
            }
            if (
                vm.proposal.filming_activity.film_type == '' ||
                vm.proposal.filming_activity.film_type == null
            ) {
                blank_fields.push(' Type of film to be undertaken is missing');
            }
            if (
                vm.proposal.filming_activity.activity_title == '' ||
                vm.proposal.filming_activity.activity_title == null
            ) {
                blank_fields.push(' Title of film is missing');
            }
            if (
                vm.proposal.filming_activity.sponsorship == '' ||
                vm.proposal.filming_activity.sponsorship == null
            ) {
                blank_fields.push(' Tourism WA sponsorship is missing');
            }
            if (
                vm.proposal.filming_activity.production_description == '' ||
                vm.proposal.filming_activity.production_description == null
            ) {
                blank_fields.push(' Description of production is missing');
            }
            if (
                vm.proposal.filming_activity.film_purpose == '' ||
                vm.proposal.filming_activity.film_purpose == null
            ) {
                blank_fields.push(' Film purpose is missing');
            }
            if (
                vm.proposal.filming_activity.film_usage == '' ||
                vm.proposal.filming_activity.film_usage == null
            ) {
                blank_fields.push(' Usage of film is missing');
            }
            if (vm.proposal.filming_access.track_use) {
                if (
                    vm.proposal.filming_access.track_use_details == '' ||
                    vm.proposal.filming_access.track_use_details == null
                ) {
                    blank_fields.push(' Track use details are missing');
                }
            }
            if (vm.proposal.filming_access.off_road) {
                if (
                    vm.proposal.filming_access.off_road_details == '' ||
                    vm.proposal.filming_access.off_road_details == null
                ) {
                    blank_fields.push(' Off road details are missing');
                }
            }
            if (vm.proposal.filming_access.road_closure) {
                if (
                    vm.proposal.filming_access.road_closure_details == '' ||
                    vm.proposal.filming_access.road_closure_details == null
                ) {
                    blank_fields.push(
                        ' Roads or car park to be closed details are missing'
                    );
                }
            }
            if (vm.proposal.filming_access.camp_on_land) {
                if (
                    vm.proposal.filming_access.camp_location == '' ||
                    vm.proposal.filming_access.camp_location == null
                ) {
                    blank_fields.push(' Camping location details are missing');
                }
            }
            if (vm.proposal.filming_access.staff_assistance) {
                if (
                    vm.proposal.filming_access.assistance_staff_capacity ==
                        '' ||
                    vm.proposal.filming_access.assistance_staff_capacity == null
                ) {
                    blank_fields.push(
                        ' Staff assistance capacity details are missing'
                    );
                }
            }
            if (vm.proposal.filming_access.staff_to_film) {
                if (
                    vm.proposal.filming_access.film_staff_capacity == '' ||
                    vm.proposal.filming_access.film_staff_capacity == null
                ) {
                    blank_fields.push(
                        ' Department staff to film capacity details are missing'
                    );
                }
            }
            if (vm.proposal.filming_access.cultural_significance) {
                if (
                    vm.proposal.filming_access.cultural_significance_details ==
                        '' ||
                    vm.proposal.filming_access.cultural_significance_details ==
                        null
                ) {
                    blank_fields.push(
                        ' Items/ areas of cultural significance details are missing'
                    );
                }
            }
            if (
                vm.proposal.filming_access.no_of_people == '' ||
                vm.proposal.filming_access.no_of_people == null
            ) {
                blank_fields.push(
                    ' Number of people in filming party is missing'
                );
            }
            if (vm.proposal.filming_equipment.rps_used) {
                if (
                    vm.proposal.filming_equipment.rps_used_details == '' ||
                    vm.proposal.filming_equipment.rps_used_details == null
                ) {
                    blank_fields.push(' RPA details are missing');
                }
                if (
                    vm.$refs.proposal_filming.$refs.filming_equipment.$refs
                        .rps_certificate.documents.length == 0
                ) {
                    blank_fields.push(' RePL/ ReOC document missing');
                }
            }
            if (vm.proposal.filming_equipment.alteration_required) {
                if (
                    vm.proposal.filming_equipment.alteration_required_details ==
                        '' ||
                    vm.proposal.filming_equipment.alteration_required_details ==
                        null
                ) {
                    blank_fields.push(
                        ' Any alteration to occur details are missing'
                    );
                }
            }
            if (
                vm.proposal.filming_equipment.num_cameras == '' ||
                vm.proposal.filming_equipment.num_cameras == null
            ) {
                blank_fields.push(' Number and type of cameras is missing');
            }
            if (
                vm.proposal.filming_equipment.other_equipments == '' ||
                vm.proposal.filming_equipment.other_equipments == null
            ) {
                blank_fields.push(
                    ' Other significant equipment details are missing'
                );
            }
            if (
                vm.proposal.filming_other_details.safety_details == '' ||
                vm.proposal.filming_other_details.safety_details == null
            ) {
                blank_fields.push(' Safety details are missing');
            }
            if (
                vm.$refs.proposal_filming.$refs.filming_other_details.$refs
                    .currency_doc.documents.length == 0
            ) {
                blank_fields.push(
                    ' Certificate of currency document is missing'
                );
            }
            if (
                vm.proposal.filming_other_details.insurance_expiry == '' ||
                vm.proposal.filming_other_details.insurance_expiry == null
            ) {
                blank_fields.push(
                    ' Certificate of currency expiry date is missing'
                );
            }
            if (
                vm.$refs.proposal_filming.$refs.filming_other_details.$refs
                    .deed_poll_doc.documents.length == 0
            ) {
                blank_fields.push(' Deed poll document is missing');
            }
            return blank_fields;
        },
        submit: function () {
            let vm = this;
            let formData;
            try {
                formData = vm.set_formData(true);
            } catch (e) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: e.message,
                    icon: 'error',
                });
                return;
            }

            var missing_data = vm.can_submit();
            if (missing_data != true) {
                swal.fire({
                    title: 'Please fix following errors before submitting',
                    text: missing_data,
                    icon: 'error',
                });
                return false;
            }

            // remove the confirm prompt when navigating away from window (on button 'Submit' click)
            vm.submitting = true;
            vm.paySubmitting = true;

            swal.fire({
                title: vm.submit_text() + ' Application',
                text:
                    'Are you sure you want to ' +
                    vm.submit_text().toLowerCase() +
                    ' this application?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: vm.submit_text(),
            }).then(
                async (result) => {
                    if (!result.isConfirmed) {
                        vm.submitting = false;
                        vm.paySubmitting = false;
                        return;
                    }
                    // Filming has deferred payment once assessor decides whether 'Licence' (fee) or 'Lawful Authority' (no fee) is to be issued
                    if (
                        !vm.proposal.fee_paid &&
                        vm.proposal.application_type !=
                            vm.application_type_filming
                    ) {
                        vm.save_and_redirect();
                    } else {
                        /* just save and submit - no payment required (probably application was pushed back by assessor for amendment */
                        await vm.save_before_submit();
                        if (!vm.saveError) {
                            helpers
                                .fetchUrl(
                                    helpers.add_endpoint_json(
                                        api_endpoints.proposals,
                                        vm.proposal.id + '/submit'
                                    ),
                                    {
                                        method: 'POST',
                                        body: formData,
                                    }
                                )
                                .then(
                                    (res) => {
                                        vm.proposal = res;
                                        vm.$router.push({
                                            name: 'submit_proposal',
                                            params: {
                                                proposal_id: vm.proposal.id,
                                            },
                                        });
                                    },
                                    (err) => {
                                        swal.fire({
                                            title: 'Submit Error',
                                            text: helpers.apiVueResourceError(
                                                err
                                            ),
                                            icon: 'error',
                                        });
                                    }
                                );
                        }
                    }
                },
                () => {
                    vm.paySubmitting = false;
                }
            );
        },

        post_and_redirect: function (url, postData) {
            /* http.post and ajax do not allow redirect from Django View (post method),
           this function allows redirect by mimicking a form submit.

           usage:  vm.post_and_redirect(vm.application_fee_url, {'csrfmiddlewaretoken' : vm.csrf_token});
        */
            var postFormStr = "<form method='POST' action='" + url + "'>";

            for (var key in postData) {
                // eslint-disable-next-line no-prototype-builtins
                if (postData.hasOwnProperty(key)) {
                    postFormStr +=
                        "<input type='hidden' name='" +
                        key +
                        "' value='" +
                        postData[key] +
                        "'>";
                }
            }
            postFormStr += '</form>';
            var formElement = $(postFormStr);
            $('body').append(formElement);
            $(formElement).submit();
        },
        fetchProposalParks: function (proposal_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        proposal_id + '/parks_and_trails'
                    )
                )
                .then(
                    (response) => {
                        vm.proposal_parks = helpers.copyObject(response);
                        console.log(vm.proposal_parks);
                    },
                    () => {}
                );
        },
    },
};
</script>

<style lang="css" scoped></style>
