<template lang="html">
    <div id="internal-proposal-onhold">
        <modal
            transition="modal fade"
            title="Put Application On-hold"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="onholdForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <TextArea
                                            id="id-onhold-comments"
                                            ref="on_hold_comments"
                                            :proposal_id="proposal_id"
                                            :readonly="readonly"
                                            name="on_hold_comments"
                                            label="Comments"
                                        />
                                        <FileField
                                            id="id_file"
                                            :document_url="document_url"
                                            :proposal_id="proposal_id"
                                            :is-repeatable="true"
                                            name="on_hold_file"
                                            label="Add Document"
                                            @refreshFromResponse="
                                                refreshFromResponse
                                            "
                                        />
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
    name: 'proposal-onhold',
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
            on_hold_file: 'on_hold_file',
            on_hold_comments: 'on_hold_comments',
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        document_url: function () {
            return this.proposal_id
                ? `/api/proposal/${this.proposal_id}/process_onhold_document/`
                : '';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.onholdForm;
        vm.addFormValidations();
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
            var is_onhold = vm.processing_status == 'On Hold' ? true : false;
            var data = {
                onhold: is_onhold ? 'False' : 'True', // since wee need to do the reverse
                file_input_name: 'on_hold_file',
                proposal: vm.proposal_id,
                text: vm.$refs.on_hold_comments.localValue, // getting the value from the text-area.vue field
            };
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        vm.proposal_id + '/on_hold'
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
                        if (!is_onhold) {
                            swal.fire({
                                title: 'Put Application On-hold',
                                text: 'Application On-hold',
                                icon: 'success',
                            });
                        } else {
                            swal.fire({
                                title: 'Application On-hold Remove',
                                text: 'Application On-hold Removed',
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

            // this.validation_form.resetForm();
        },
        addFormValidations: function () {},
        eventListerners: function () {},
    },
};
</script>

<style lang="css"></style>
