<template lang="html">
    <div id="internal-proposal-eclass">
        <modal
            transition="modal fade"
            title="Add new Commercial Operator E Class licence"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form
                        class="form-horizontal"
                        name="eclassForm"
                        enctype="multipart/form-data"
                    >
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="row">
                                <div class="col-sm-offset-2 col-sm-8">
                                    <div class="form-group">
                                        <div class="radio">
                                            <input
                                                v-model="applicant_type"
                                                type="radio"
                                                value="user"
                                                name="applicant_type"
                                                @change="set_url"
                                            />
                                            Individual <br />
                                            <input
                                                v-model="applicant_type"
                                                type="radio"
                                                value="org"
                                                name="applicant_type"
                                                @change="set_url"
                                            />
                                            Organisation <br />
                                        </div>

                                        <TextFilteredField
                                            id="id_holder"
                                            :url="filtered_url"
                                            :readonly="readonly"
                                            name="holder"
                                            label="Holder"
                                            :is-required="isRequired"
                                        />
                                        <DateField
                                            id="id_issue_date"
                                            :proposal_id="proposal_id"
                                            :readonly="readonly"
                                            name="issue_date"
                                            label="Issue Date"
                                            :is-required="isRequired"
                                        />
                                        <DateField
                                            id="id_start_date"
                                            :proposal_id="proposal_id"
                                            :readonly="readonly"
                                            name="start_date"
                                            label="Start Date"
                                            :is-required="isRequired"
                                        />
                                        <DateField
                                            id="id_expiry_date"
                                            :proposal_id="proposal_id"
                                            :readonly="readonly"
                                            name="expiry_date"
                                            label="Expiry Date"
                                            :is-required="isRequired"
                                        />
                                        <TextField
                                            id="id_reserved_licence"
                                            :proposal_id="proposal_id"
                                            name="reserved_licence"
                                            label="Reserved Licence Lodgement Number"
                                            :is-required="false"
                                        />
                                        <div class="form-group">
                                            <div class="row">
                                                <div class="col-sm-3">
                                                    <label
                                                        class="control-label pull-left"
                                                        for="Name"
                                                        >Attachments</label
                                                    >
                                                </div>
                                                <div class="col-sm-9">
                                                    <template
                                                        v-for="(f, i) in files"
                                                    >
                                                        <!-- eslint-disable-next-line vue/require-v-for-key -->
                                                        <div
                                                            :class="
                                                                'row top-buffer file-row-' +
                                                                i
                                                            "
                                                        >
                                                            <div
                                                                class="col-sm-4"
                                                            >
                                                                <span
                                                                    v-if="
                                                                        f.file ==
                                                                        null
                                                                    "
                                                                    class="btn btn-info btn-file pull-left"
                                                                >
                                                                    Attach File
                                                                    <input
                                                                        type="file"
                                                                        :name="
                                                                            'file-upload-' +
                                                                            i
                                                                        "
                                                                        :class="
                                                                            'file-upload-' +
                                                                            i
                                                                        "
                                                                        :required="
                                                                            isRequired
                                                                        "
                                                                        @change="
                                                                            uploadFile(
                                                                                'file-upload-' +
                                                                                    i,
                                                                                f
                                                                            )
                                                                        "
                                                                    />
                                                                </span>
                                                                <span
                                                                    v-else
                                                                    class="btn btn-info btn-file pull-left"
                                                                >
                                                                    Update File
                                                                    <input
                                                                        type="file"
                                                                        :name="
                                                                            'file-upload-' +
                                                                            i
                                                                        "
                                                                        :class="
                                                                            'file-upload-' +
                                                                            i
                                                                        "
                                                                        @change="
                                                                            uploadFile(
                                                                                'file-upload-' +
                                                                                    i,
                                                                                f
                                                                            )
                                                                        "
                                                                    />
                                                                </span>
                                                            </div>
                                                            <div
                                                                class="col-sm-4"
                                                            >
                                                                <span>{{
                                                                    f.name
                                                                }}</span>
                                                            </div>
                                                            <div
                                                                class="col-sm-4"
                                                            >
                                                                <button
                                                                    class="btn btn-danger"
                                                                    @click="
                                                                        removeFile(
                                                                            i
                                                                        )
                                                                    "
                                                                >
                                                                    Remove
                                                                </button>
                                                            </div>
                                                        </div>
                                                    </template>
                                                </div>
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

import TextField from '@/components/forms/text.vue';
import DateField from '@/components/forms/date-field.vue';
import TextFilteredField from '@/components/forms/text-filtered.vue';

import { helpers, api_endpoints } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'proposal-onhold',
    components: {
        TextField,
        DateField,
        TextFilteredField,
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        proposal_id: {
            type: Number,
            required: false,
        },
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        processing_status: {
            type: String,
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
            _comments: '_comments',
            isRequired: true,
            files: [
                {
                    file: null,
                    name: '',
                },
            ],
            applicant_type: 'user',
            filtered_url: api_endpoints.filtered_users + '?search=',
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        document_url: function () {
            // location on media folder for the docs - to be passed to FileField
            return `/api/approvals/0/add_eclass_licence/`;
        },
        filtered_users_url: function () {
            return api_endpoints.filtered_users + '?search=';
        },
        filtered_organisations_url: function () {
            return api_endpoints.filtered_organisations + '?search=';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.eclassForm;
        this.$nextTick(() => {
            vm.eventListerners();
        });
    },
    methods: {
        set_url: function () {
            let vm = this;
            if (this.applicant_type == 'user') {
                vm.filtered_url = this.filtered_users_url;
            } else {
                vm.filtered_url = this.filtered_organisations_url;
            }
        },

        uploadFile(target, file_obj) {
            let _file = null;
            var input = $('.' + target)[0];
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(input.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            file_obj.file = _file;
            file_obj.name = _file.name;
        },
        removeFile(index) {
            let length = this.files.length;
            $('.file-row-' + index).remove();
            this.files.splice(index, 1);
            this.$nextTick(() => {
                length == 1 ? this.attachAnother() : '';
            });
        },
        attachAnother() {
            this.files.push({
                file: null,
                name: '',
            });
        },

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
            let form = new FormData(vm.form);
            // I manually added the file to the form data
            if (vm.files.length > 0) {
                form.append('file', vm.files[0].file);
            }
            // NOTE: The api endpoint here used to be '/api/approvals/0/add_eclass_licence/'. What?
            helpers
                .fetchUrl('/api/approvals/0/add_eclass_licence/', {
                    method: 'POST',
                    body: form,
                })
                .then(
                    (res) => {
                        vm.proposal = res;
                        swal.fire({
                            title: 'New E Class Licence Created',
                            text:
                                'New E Class Licence Created: ' +
                                res['approval'],
                            icon: 'success',
                        });
                        vm.$router.push({ path: '/internal/approvals' }); //Navigate to dashboard after completing the referral
                    },
                    (err) => {
                        swal.fire({
                            title: 'Submit Error',
                            text: err,
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

        eventListerners: function () {},
    },
};
</script>

<style lang="css">
#id_reserved_licence {
    font-weight: normal;
}
</style>
