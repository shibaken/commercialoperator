<template lang="html">
    <div id="internal-proposal-onhold">
        <modal
            transition="modal fade"
            title="Application With QA Officer"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form
                        class="needs-validation form-horizontal"
                        name="withqaForm"
                    >
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <div
                                            class="input-group"
                                            style="width: 70%"
                                        >
                                            <TextArea
                                                id="id-qaofficer-comments"
                                                ref="comments"
                                                :proposal_id="proposal_id"
                                                :readonly="readonly"
                                                name="_comments"
                                                class="form-control"
                                                label="Comments"
                                                :is-required="true"
                                            />
                                            <div v-if="is_qaofficer_status">
                                                <FileField
                                                    id="id_file"
                                                    :document_url="document_url"
                                                    :proposal_id="proposal_id"
                                                    :is-repeatable="true"
                                                    name="qaofficer_file"
                                                    label="Add Document"
                                                    @refreshFromResponse="
                                                        refreshFromResponse
                                                    "
                                                />
                                            </div>
                                            <div v-else>
                                                <FileField
                                                    id="id_file"
                                                    :document_url="document_url"
                                                    :proposal_id="proposal_id"
                                                    :is-repeatable="true"
                                                    name="assessor_qa_file"
                                                    label="Add Document"
                                                    @refreshFromResponse="
                                                        refreshFromResponse
                                                    "
                                                />
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

import TextArea from '@/components/forms/text-area.vue';
import FileField from '@/components/forms/file.vue';

import { helpers, api_endpoints } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'proposal-qaofficer',
    components: {
        TextArea,
        FileField,
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
        readonly: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            hasErrors: false,
            errorString: '',
            validation_form: null,
            // eslint-disable-next-line vue/no-reserved-keys
            _file: '_file',
            // eslint-disable-next-line vue/no-reserved-keys
            _comments: '_comments',
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        document_url: function () {
            // location on media folder for the docs - to be passed to FileField
            return this.proposal_id
                ? `/api/proposal/${this.proposal_id}/process_qaofficer_document/`
                : '';
        },
        is_qaofficer_status: function () {
            return this.processing_status == 'With QA Officer' ? true : false;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.withqaForm;
        this.$nextTick(() => {
            vm.eventListerners();
        });
    },
    methods: {
        refreshFromResponse: function (document_list) {
            let vm = this;
            vm.document_list = helpers.copyObject(document_list);
        },
        _refreshFromResponse: function (response) {
            let vm = this;
            vm.document_list = helpers.copyObject(response);
        },
        save: function () {
            let vm = this;
            var is_with_qaofficer =
                vm.processing_status == 'With QA Officer' ? true : false;
            var data = {
                with_qaofficer: is_with_qaofficer ? 'False' : 'True', // since wee need to do the reverse
                file_input_name: 'qaofficer_file',
                proposal: vm.proposal_id,
                text: vm.$refs.comments.localValue, // getting the value from the text-area.vue field
            };
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        vm.proposal_id + '/with_qaofficer'
                    ),
                    {
                        method: 'POST',
                        body: JSON.stringify(data),
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                )
                .then(
                    (res) => {
                        if (!is_with_qaofficer) {
                            swal.fire({
                                title: 'Send Application to QA Officer',
                                text: 'Send Application to QA Officer',
                                icon: 'success',
                            });
                        } else {
                            swal.fire({
                                title: 'Application QA Officer Assessment Completed',
                                text: 'Application QA Officer Assessment Completed',
                                icon: 'success',
                            });
                        }

                        vm.proposal = res;
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
        ok: function () {
            let vm = this;
            if (vm.$refs.comments.isValid() && helpers.validateForm(vm.form)) {
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
        },
        addFormValidations: function () {},
        eventListerners: function () {},
    },
};
</script>

<style lang="css"></style>
