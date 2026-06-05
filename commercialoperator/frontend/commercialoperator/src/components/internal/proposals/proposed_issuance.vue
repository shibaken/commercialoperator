<template lang="html">
    <div id="proposedIssuanceApproval">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="approvalForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            v-if="
                                                processing_status ==
                                                'With Approver'
                                            "
                                            class="control-label pull-left"
                                            for="Name"
                                            >Start Date</label
                                        >
                                        <label
                                            v-else
                                            class="control-label pull-left"
                                            for="Name"
                                            >Proposed Start Date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="start_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-model="approval.start_date"
                                                type="date"
                                                class="form-control"
                                                name="start_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div v-show="showstartDateError" class="row">
                                    <alert class="col-sm-12" type="danger"
                                        ><strong>{{
                                            startDateErrorString
                                        }}</strong></alert
                                    >
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            v-if="
                                                processing_status ==
                                                'With Approver'
                                            "
                                            class="control-label pull-left"
                                            for="Name"
                                            >Expiry Date</label
                                        >
                                        <label
                                            v-else
                                            class="control-label pull-left"
                                            for="Name"
                                            >Proposed Expiry Date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="due_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                ref="expiry_date"
                                                v-model="approval.expiry_date"
                                                type="date"
                                                class="form-control"
                                                name="due_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div v-show="showtoDateError" class="row">
                                    <alert class="col-sm-12" type="danger"
                                        ><strong>{{
                                            toDateErrorString
                                        }}</strong></alert
                                    >
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            v-if="
                                                processing_status ==
                                                'With Approver'
                                            "
                                            class="control-label pull-left"
                                            for="Name"
                                            >Details</label
                                        >
                                        <label
                                            v-else
                                            class="control-label pull-left"
                                            for="Name"
                                            >Proposed Details</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            v-model="approval.details"
                                            name="approval_details"
                                            class="form-control"
                                            style="width: 70%"
                                            required
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            v-if="
                                                processing_status ==
                                                'With Approver'
                                            "
                                            class="control-label pull-left"
                                            for="Name"
                                            >CC email</label
                                        >
                                        <label
                                            v-else
                                            class="control-label pull-left"
                                            for="Name"
                                            >Proposed CC email</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            v-model="approval.cc_email"
                                            type="text"
                                            class="form-control"
                                            name="approval_cc"
                                            style="width: 70%"
                                        />
                                    </div>
                                </div>
                                <div v-show="showApprovalCCError" class="row">
                                    <alert class="col-sm-12" type="danger"
                                        ><strong>{{
                                            approvalCCErrorString
                                        }}</strong></alert
                                    >
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>

            <p v-if="can_preview">
                Click <a href="#" @click.prevent="preview">here</a> to preview
                the licence document.
            </p>

            <template #footer>
                <button
                    v-if="issuingApproval"
                    type="button"
                    disabled
                    class="btn btn-primary"
                    @click="ok"
                >
                    <i class="fas fa-spinner fa-spin"></i> Processing
                </button>
                <button
                    v-else
                    type="button"
                    class="btn btn-primary"
                    @click="ok"
                >
                    Ok
                </button>
                <button type="button" class="btn btn-secondary" @click="cancel">
                    Cancel
                </button>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Proposed-Approval',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        proposal_id: {
            type: Number,
            required: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        processing_status: {
            type: String,
            required: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        proposal_type: {
            type: String,
            required: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            approval: {},
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            hasErrors: false,
            toDateError: false,
            startDateError: false,
            errorString: '',
            toDateErrorString: '',
            startDateErrorString: '',
            successString: '',
            success: false,
            approvalCCError: false,
            approvalCCErrorString: '',
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        showtoDateError: function () {
            var vm = this;
            return vm.toDateError;
        },
        showstartDateError: function () {
            var vm = this;
            return vm.startDateError;
        },
        showApprovalCCError: function () {
            var vm = this;
            return vm.approvalCCError;
        },
        title: function () {
            return this.processing_status == 'With Approver'
                ? 'Issue Licence'
                : 'Propose to issue licence';
        },
        is_amendment: function () {
            return this.proposal_type == 'Amendment' ? true : false;
        },
        can_preview: function () {
            return (this.processing_status == 'With Approver' ||
                this.processing_status == 'With Assessor (Requirements)') &&
                this.approval.start_date &&
                this.approval.expiry_date
                ? true
                : false;
        },
        preview_licence_url: function () {
            return this.proposal_id
                ? `/preview/licence-pdf/${this.proposal_id}`
                : '';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.approvalForm;
        // NOTE: `vm.addFormValidations();` replaced with form required attribute and call to `helpers.validateForm(vm.form)` in ok() method
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        preview: function () {
            let vm = this;

            let formData = new FormData(vm.form);

            // convert formData to json
            let jsonObject = {};
            for (const [key, value] of formData.entries()) {
                jsonObject[key] = value;
            }

            vm.post_and_redirect(vm.preview_licence_url, {
                csrfmiddlewaretoken: vm.csrf_token,
                formData: JSON.stringify(jsonObject),
            });
        },

        post_and_redirect: function (url, postData) {
            /* http.post and ajax do not allow redirect from Django View (post method),
               this function allows redirect by mimicking a form submit.

               usage:  vm.post_and_redirect(vm.application_fee_url, {'csrfmiddlewaretoken' : vm.csrf_token});
            */
            var postFormStr =
                "<form method='POST' target='_blank' name='Preview Licence' action='" +
                url +
                "'>";

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
        ok: function () {
            let vm = this;

            // Check form validity
            if (helpers.validateForm(vm.form) && vm.validateApprovalCC()) {
                console.log('Form is valid');
                vm.sendData();
            } else {
                console.warn('Form is not valid');
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            // this.approval = {};
            this.hasErrors = false;
            this.toDateError = false;
            this.startDateError = false;
            $('.has-error').removeClass('has-error');
            // $(this.$refs.due_date).val('');
            // $(this.$refs.start_date).val('');
            // this.validation_form.resetForm();
        },
        fetchContact: function (id) {
            let vm = this;
            helpers.fetchUrl(api_endpoints.contact(id)).then(
                (response) => {
                    vm.contact = response;
                    vm.isModalOpen = true;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            let approval = JSON.parse(JSON.stringify(vm.approval));
            vm.issuingApproval = true;
            if (vm.state == 'proposed_approval') {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal_id + '/proposed_approval'
                        ),
                        {
                            method: 'POST',
                            body: JSON.stringify(approval),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingApproval = false;
                            vm.close();
                            vm.$emit('refreshFromResponse', response);
                            vm.$router.push({ path: '/internal' }); //Navigate to dashboard page after Propose issue.
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingApproval = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            } else if (vm.state == 'final_approval') {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal_id + '/final_approval'
                        ),
                        {
                            method: 'POST',
                            body: JSON.stringify(approval),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingApproval = false;
                            vm.close();
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingApproval = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        validateApprovalCC: function () {
            let vm = this;
            const ccRegex = new RegExp(
                // eslint-disable-next-line no-useless-escape
                /^(([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5}){1,25})+([,.](([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5}){1,25})+)*$/
            );
            if (!vm.approval.cc_email || ccRegex.test(vm.approval.cc_email)) {
                vm.approvalCCError = false;
                vm.approvalCCErrorString = '';
                return true;
            } else {
                vm.approvalCCError = true;
                vm.approvalCCErrorString =
                    'Please ensure each CC email is valid and separated with a ,';
                return false;
            }
        },
        eventListeners: function () {},
    },
};
</script>

<style lang="css"></style>
