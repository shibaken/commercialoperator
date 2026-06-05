<template lang="html">
    <div id="internal-compliance-amend">
        <modal
            transition="modal fade"
            title="Amendment Request"
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
                            <div class="row mb-3">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label
                                                    class="control-label pull-left"
                                                    for="Name"
                                                    >Reason</label
                                                >
                                            </div>
                                            <div
                                                id="amendment_reason_modal"
                                                class="col-sm-9"
                                            >
                                                <select
                                                    ref="reason"
                                                    v-model="amendment.reason"
                                                    class="form-control"
                                                    name="reason"
                                                    required
                                                >
                                                    <option
                                                        v-for="r in reason_choices"
                                                        :key="r.key"
                                                        :value="r.key"
                                                    >
                                                        {{ r.value }}
                                                    </option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label
                                                    class="control-label pull-left"
                                                    for="Name"
                                                    >Details</label
                                                >
                                            </div>
                                            <div class="col-sm-9">
                                                <textarea
                                                    v-model="amendment.text"
                                                    class="form-control"
                                                    name="name"
                                                    required
                                                ></textarea>
                                            </div>
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

import { helpers } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'compliance-amendment-request',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        compliance_id: {
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
                amendingcompliance: false,
                compliance: vm.compliance_id,
            },
            reason_choices: {},
            hasErrors: false,
            errorString: '',
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
        this.$nextTick(() => {
            vm.eventListerners();
        });
    },
    methods: {
        ok: function () {
            let vm = this;
            if (helpers.validateForm(vm.form)) {
                vm.sendData();
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
                compliance: this.compliance_id,
            };
            this.hasErrors = false;
            $(this.$refs.reason).val(null).trigger('change');
            $('.has-error').removeClass('has-error');
        },
        fetchAmendmentChoices: function () {
            let vm = this;
            helpers
                .fetchUrl('/api/compliance_amendment_reason_choices.json')
                .then(
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
                .fetchUrl('/api/compliance_amendment_request.json', {
                    method: 'POST',
                    body: JSON.stringify(amendment),
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(
                    (response) => {
                        swal.fire({
                            title: 'Sent',
                            text: 'An email has been sent to applicant with the request to amend this compliance',
                            icon: 'success',
                        });
                        vm.amendingcompliance = true;
                        console.log(response);
                        vm.close();

                        vm.$router.push({ path: '/internal' }); //Navigate to dashboard after creating Amendment request
                    },
                    (error) => {
                        console.log(error);
                        vm.hasErrors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.amendingcompliance = true;
                    }
                );
        },
        eventListerners: function () {
            let vm = this;

            // Intialise select2
            $(vm.$refs.reason)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Reason',
                    dropdownParent: $('#amendment_reason_modal'),
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.amendment.reason = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.amendment.reason = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
