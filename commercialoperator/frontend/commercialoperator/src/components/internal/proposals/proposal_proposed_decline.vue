<template lang="html">
    <div id="change-contact">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="declineForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            v-if="check_status()"
                                            class="control-label"
                                            for="Name"
                                            >Details</label
                                        >
                                        <label
                                            v-else
                                            class="control-label"
                                            for="Name"
                                            >Provide Reason for the proposed
                                            decline
                                        </label>
                                        <textarea
                                            v-model="decline.reason"
                                            style="width: 70%"
                                            class="form-control"
                                            name="reason"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            v-if="check_status()"
                                            class="control-label"
                                            for="Name"
                                            >CC email</label
                                        >
                                        <label
                                            v-else
                                            class="control-label"
                                            for="Name"
                                            >Proposed CC email</label
                                        >
                                        <input
                                            v-model="decline.cc_email"
                                            type="text"
                                            style="width: 70%"
                                            class="form-control"
                                            name="cc_email"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="decliningProposal"
                    type="button"
                    disabled
                    class="btn btn-secondary"
                    @click="ok"
                >
                    <i class="fa fa-spinner fa-spin"></i> Processing
                </button>
                <button
                    v-else
                    type="button"
                    class="btn btn-secondary"
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
    name: 'Decline-Proposal',
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
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            decline: {},
            decliningProposal: false,
            hasErrors: false,
            validation_form: null,
            errorString: '',
            successString: '',
            success: false,
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.processing_status == 'With Approver'
                ? 'Decline'
                : 'Proposed Decline';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.declineForm;
        vm.addFormValidations();
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.decline = {};
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            this.validation_form.resetForm();
        },

        check_status: function () {
            let vm = this;
            if (vm.processing_status == 'With Approver') return true;
            else return false;
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            let decline = JSON.parse(JSON.stringify(vm.decline));
            vm.decliningProposal = true;
            if (vm.processing_status != 'With Approver') {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal_id + '/proposed_decline'
                        ),
                        {
                            method: 'POST',
                            body: JSON.stringify(decline),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    )
                    .then(
                        (response) => {
                            vm.decliningProposal = false;
                            vm.close();
                            vm.$emit('refreshFromResponse', response);
                            vm.$router.push({ path: '/internal' }); //Navigate to dashboard after propose decline.
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.decliningProposal = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal_id + '/final_decline'
                        ),
                        {
                            method: 'POST',
                            body: JSON.stringify(decline),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        }
                    )
                    .then(
                        (response) => {
                            vm.decliningProposal = false;
                            vm.close();
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.decliningProposal = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    reason: 'required',
                },
                messages: {
                    arrival: 'field is required',
                    departure: 'field is required',
                    campground: 'field is required',
                    campsite: 'field is required',
                },
                showErrors: function (errorMap, errorList) {
                    $.each(this.validElements(), function (index, element) {
                        var $element = $(element);
                        $element
                            .attr('data-original-title', '')
                            .parents('.form-group')
                            .removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    // $('.' + this.settings.validClass).tooltip('destroy');
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: 'focus',
                            })
                            .attr('data-original-title', error.message)
                            .parents('.form-group')
                            .addClass('has-error');
                    }
                },
            });
        },
        eventListerners: function () {},
    },
};
</script>

<style lang="css"></style>
