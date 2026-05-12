<template lang="html">
    <div id="approvalExtend">
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
                        name="extendApprovalForm"
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
                                            >Extend Details</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            v-model="approval.extend_details"
                                            name="extend_details"
                                            class="form-control"
                                            style="width: 70%"
                                            required
                                        ></textarea>
                                        <div class="invalid-feedback">
                                            Please provide extend details
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
    name: 'Extend-Approval',
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
            return 'Extend Licence';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.extendApprovalForm;
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
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            this.form.reset();
            this.form.classList.remove('was-validated');
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
                        vm.approval_id + '/approval_extend'
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
                        swal.fire({
                            title: 'Extended',
                            text: 'Licence has been extended',
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
                console.log('extendApprovalForm is valid');
                vm.sendData();
            } else {
                console.log('extendApprovalForm is invalid');
                vm.form.classList.add('was-validated');
                $(vm.form).find(':invalid').first().focus();
            }

            return false;
        },
        eventListeners: function () {},
    },
};
</script>

<style lang="css"></style>
