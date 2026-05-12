<template lang="html">
    <div id="approvalCancellation">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form
                        class="needs-validation form-horizontal"
                        name="suspendApprovalForm"
                    >
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >From Date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="from_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-model="approval.from_date"
                                                type="date"
                                                class="form-control"
                                                name="from_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                            />
                                            <div class="invalid-feedback">
                                                Please enter a valid date
                                            </div>
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >To Date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="to_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-model="approval.to_date"
                                                type="date"
                                                class="form-control"
                                                name="to_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                            />
                                            <div class="invalid-feedback">
                                                Please enter a valid date
                                            </div>
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Suspension Details</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            v-model="
                                                approval.suspension_details
                                            "
                                            name="suspension_details"
                                            class="form-control"
                                            style="width: 70%"
                                            required
                                        ></textarea>
                                        <div class="invalid-feedback">
                                            Please provide suspension details
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="issuingApproval"
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
import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
export default {
    name: 'SuspendApproval',
    components: {
        modal,
        alert,
    },
    props: {},
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            approval: {},
            approval_id: Number,
            state: 'proposed_approval',
            issuingApproval: false,
            validation_form: null,
            hasErrors: false,
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
            return 'Suspend Licence';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.suspendApprovalForm;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        ok: function () {
            let vm = this;
            vm.validateForm();
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.approval = {};
            //this.approval.from_date = ""
            //this.approval.to_date = ""
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            // $(this.$refs.from_date).data('DateTimePicker').clear();
            // $(this.$refs.to_date).data('DateTimePicker').clear();
            // this.validation_form.resetForm();
            this.form.reset();
            this.form.classList.remove('was-validated');
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

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.approvals,
                        vm.approval_id + '/approval_suspension'
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
                        vm.approval = {};
                        vm.close();
                        swal.fire({
                            title: 'Suspend',
                            text: 'An email has been sent to applicant about suspension of this licence',
                            icon: 'success',
                        });
                        vm.$emit('refreshFromResponse', response);
                    },
                    (error) => {
                        vm.hasErrors = true;
                        vm.issuingApproval = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    }
                );
        },
        validateForm: function () {
            const vm = this;

            if (vm.form.checkValidity()) {
                console.log('suspendApprovalForm is valid');
                vm.sendData();
            } else {
                console.log('suspendApprovalForm is invalid');
                vm.form.classList.add('was-validated');
                $(vm.form).find(':invalid').first().focus();
            }

            return false;
        },
        eventListeners: function () {
            let vm = this;

            $(vm.$refs.to_date).on('dp.change', function (e) {
                if ($(vm.$refs.to_date).data('DateTimePicker').date()) {
                    vm.approval.to_date = e.date.format('DD/MM/YYYY');
                } else if ($(vm.$refs.to_date).data('date') === '') {
                    vm.approval.to_date = null;
                }
            });
        },
    },
};
</script>

<style lang="css"></style>
