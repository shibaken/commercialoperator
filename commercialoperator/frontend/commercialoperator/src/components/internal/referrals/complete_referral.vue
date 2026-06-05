<template lang="html">
    <div id="internal-proposal-amend">
        <modal
            transition="modal fade"
            title="Complete Referral"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="amendForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <label
                                            class="control-label pull-left"
                                            for="referral_comment"
                                            >Comment</label
                                        >
                                        <textarea
                                            v-model="referral_comment"
                                            class="form-control"
                                            name="referral_comment"
                                            required="true"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <!-- templated from from proposal_approval.vue -->
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Attach Document
                                        </label>
                                        <div>
                                            <span
                                                v-if="!uploadedFile"
                                                class="btn btn-info btn-file pull-left"
                                            >
                                                Attach File<input
                                                    ref="uploadedFile"
                                                    type="file"
                                                    @change="readFile()"
                                                />
                                            </span>
                                            <span
                                                v-else
                                                class="pull-left"
                                                style="
                                                    margin-left: 10px;
                                                    margin-top: 10px;
                                                "
                                            >
                                                {{ uploadedFileName() }}
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
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
    name: 'referral-complete',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        proposal_id: {
            type: Number,
        },
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        referral_id: {
            type: Number,
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            amendment: {
                reason: '',
                reason_id: null,
                amendingProposal: false,
                proposal: vm.proposal_id,
            },
            reason_choices: {},
            hasErrors: false,
            errorString: '',
            validation_form: null,
            uploadedFile: null,
            referral_comment: '',
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.amendForm;
        vm.fetchAmendmentChoices();
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListerners();
        });
    },
    methods: {
        readFile: function () {
            let vm = this;
            let _file = null;
            var input = $(vm.$refs.uploadedFile)[0];
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(input.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            vm.uploadedFile = _file;
        },
        removeFile: function () {
            let vm = this;
            vm.uploadedFile = null;
            vm.save();
        },
        save: function () {
            let vm = this;
            let data = new FormData(vm.form);
            data.append('referral_document', vm.uploadedFile);
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        vm.referral_id + '/complete'
                    ),
                    {
                        method: 'POST',
                        body: data,
                    }
                )
                .then(
                    (res) => {
                        swal.fire({
                            title: 'Referral Complete',
                            text: 'The referral has been completed successfully.',
                            icon: 'success',
                        });

                        vm.proposal = res;
                        vm.$emit('refreshFromResponse', res);
                        vm.$router.push({ path: '/internal' }); //Navigate to dashboard after completing the referral
                    },
                    (err) => {
                        swal.fire({
                            title: 'Submit Error',
                            text: helpers.apiVueResourceError(err),
                            icon: 'error',
                        });
                    }
                );
        },
        uploadedFileName: function () {
            return this.uploadedFile != null ? this.uploadedFile.name : '';
        },

        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.save();
            }
        },
        cancel: function () {
            let vm = this;
            vm.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.amendment = {
                reason: '',
                reason_id: null,
                proposal: this.proposal_id,
            };
            this.hasErrors = false;
            $(this.$refs.reason).val(null).trigger('change');
            $('.has-error').removeClass('has-error');

            this.validation_form.resetForm();
        },
        fetchAmendmentChoices: function () {
            let vm = this;
            helpers.fetchUrl('/api/amendment_request_reason_choices.json').then(
                (response) => {
                    vm.reason_choices = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            let amendment = JSON.parse(JSON.stringify(vm.amendment));
            helpers
                .fetchUrl('/api/amendment_request.json', {
                    method: 'POST',
                    body: JSON.stringify(amendment),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(
                    () => {
                        swal(
                            'Sent',
                            'An email has been sent to applicant with the request to amend this Application',
                            'success'
                        );
                        swal.fire({
                            title: 'Amendment Request Sent',
                            text: 'An email has been sent to applicant with the request to amend this Application',
                            icon: 'success',
                        });
                        vm.amendingProposal = true;
                        vm.close();
                        helpers
                            .fetchUrl(
                                `/api/proposal/${vm.proposal_id}/internal_proposal.json`
                            )
                            .then(
                                (response) => {
                                    vm.$emit('refreshFromResponse', response);
                                },
                                (error) => {
                                    console.log(error);
                                }
                            );
                        vm.$router.push({ path: '/internal' }); //Navigate to dashboard after creating Amendment request
                    },
                    (error) => {
                        console.log(error);
                        vm.hasErrors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.amendingProposal = true;
                    }
                );
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    reason: 'required',
                },
                messages: {
                    reason: 'field is required',
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
        eventListerners: function () {
            let vm = this;

            // Intialise select2
            $(vm.$refs.reason)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Reason',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.amendment.reason = selected.val();
                    vm.amendment.reason_id = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.amendment.reason = selected.val();
                    vm.amendment.reason_id = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
