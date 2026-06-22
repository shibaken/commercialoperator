<template>
    <div id="externalCompliance" class="container">
        <PrivacyNotice />

        <div v-if="isDiscarded" class="row" style="color: red">
            <h3>
                You cannot access this Compliance with requirements as this has
                been discarded.
            </h3>
        </div>
        <div v-else class="row">
            <div v-if="!isFinalised">
                <div v-if="hasAmendmentRequest" class="row" style="color: red">
                    <div class="col-lg-12 pull-right">
                            <FormSection
                                :form-collapse="false"
                                label="An amendment has been requested for this Compliance with Requirements"
                                index="amendment_request"
                                subtitle=""
                            >
                                <div
                                    v-for="a in amendment_request"
                                    :key="a.text"
                                >
                                    <p>Reason: {{ a.reason }}</p>
                                    <p>Details: {{ a.text }}</p>
                                </div>
                            </FormSection>
                    </div>
                </div>
            </div>

            <h3>
                <strong
                    >Compliance with Requirements:
                    {{ compliance.reference }}</strong
                >
            </h3>

            <div class="col-md-12">
                <div class="row">
                        <FormSection
                            :form-collapse="false"
                            label="Compliance with Requirements"
                            index="compliance"
                            subtitle=""
                        >
                            <div class="row">
                                <div class="col-md-12">
                                    <form
                                        class="form-horizontal"
                                        name="complianceForm"
                                        method="post"
                                    >
                                        <alert v-if="showError" type="danger"
                                            ><strong>{{
                                                errorString
                                            }}</strong></alert
                                        >

                                        <div class="row mb-2">
                                            <div class="form-group">
                                                <label
                                                    class="col-sm-3 control-label pull-left"
                                                    for="text_requirement"
                                                    >Requirement:</label
                                                >
                                                <div class="col-sm-6">
                                                    <textarea
                                                        id="text_requirement"
                                                        v-model="
                                                            compliance.requirement
                                                        "
                                                        type="text"
                                                        class="form-control w-100"
                                                        name="requirement"
                                                        disabled
                                                        readonly
                                                    ></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div class="form-group">
                                                <label
                                                    class="col-sm-3 control-label pull-left"
                                                    for="text_details"
                                                    >Details:</label
                                                >
                                                <div class="col-sm-6">
                                                    <textarea
                                                        id="text_details"
                                                        v-model="
                                                            compliance.text
                                                        "
                                                        :disabled="isFinalised"
                                                        class="form-control"
                                                        name="detail"
                                                        placeholder=""
                                                        required
                                                    ></textarea>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div
                                                v-if="hasDocuments"
                                                class="form-group"
                                            >
                                                <div
                                                    class="col-sm-3 control-label pull-left"
                                                >
                                                    <label
                                                        for="compliance-document-0"
                                                        >Documents:</label
                                                    >
                                                </div>
                                                <div class="col-sm-6">
                                                    <div
                                                        v-for="(
                                                            d, idx
                                                        ) in compliance.documents"
                                                        :key="d.id"
                                                        class="row"
                                                    >
                                                        <a
                                                            :id="`compliance-document-${idx}`"
                                                            :href="d[1]"
                                                            target="_blank"
                                                            class="control-label pull-left"
                                                            >{{ d[0] }}</a
                                                        >
                                                        <span
                                                            v-if="
                                                                !isFinalised &&
                                                                d.can_delete
                                                            "
                                                        >
                                                            <a
                                                                class="fas fa-trash control-label"
                                                                title="Remove file"
                                                                style="
                                                                    cursor: pointer;
                                                                    color: red;
                                                                "
                                                                @click="
                                                                    delete_document(
                                                                        d
                                                                    )
                                                                "
                                                            ></a>
                                                        </span>
                                                        <span v-else>
                                                            <i
                                                                class="fas fa-circle-info"
                                                                aria-hidden="true"
                                                                title="Previously submitted documents cannot be deleted"
                                                                style="
                                                                    cursor: pointer;
                                                                "
                                                            ></i
                                                        ></span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="row mb-2">
                                            <div
                                                v-if="!isFinalised"
                                                class="form-group"
                                            >
                                                <label
                                                    class="col-sm-3 control-label pull-left"
                                                    :for="`file-upload-form-${files.findIndex((f) => f.file === null)}`"
                                                    >Attachments:</label
                                                >
                                                <div class="col-sm-6">
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
                                                                    style="
                                                                        margin-bottom: 5px;
                                                                    "
                                                                >
                                                                    Attach File
                                                                    <input
                                                                        :id="`file-upload-form-${i}`"
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
                                                                <span
                                                                    v-else
                                                                    class="btn btn-info btn-file pull-left"
                                                                    style="
                                                                        margin-bottom: 5px;
                                                                    "
                                                                >
                                                                    Update File
                                                                    <input
                                                                        :id="`file-upload-form-${i}`"
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
                                                    <a
                                                        href=""
                                                        @click.prevent="
                                                            attachAnother
                                                        "
                                                        ><i
                                                            class="fas fa-lg fa-plus top-buffer-2x"
                                                        ></i
                                                    ></a>
                                                </div>
                                            </div>
                                        </div>

                                        <div
                                            v-if="
                                                compliance.participant_number_required &&
                                                !isFinalised &&
                                                !compliance.fee_paid
                                            "
                                        >
                                            <div class="row">
                                                <div class="form-group">
                                                    <label
                                                        class="col-sm-3 control-label pull-left"
                                                        for="Name"
                                                        >Number of event
                                                        participants (aged 17
                                                        years or over):</label
                                                    >
                                                    <div class="col-sm-6">
                                                        <input
                                                            type="text"
                                                            :disabled="
                                                                isFinalised
                                                            "
                                                            class="form-control"
                                                            name="num_participants"
                                                            placeholder=""
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                            <div class="row">
                                                <div class="form-group">
                                                    <label
                                                        class="col-sm-3 control-label pull-left"
                                                        for="Name"
                                                        >Number of child
                                                        participants (aged 16
                                                        years or below):</label
                                                    >
                                                    <div class="col-sm-6">
                                                        <input
                                                            type="text"
                                                            :disabled="
                                                                isFinalised
                                                            "
                                                            class="form-control"
                                                            name="num_child_participants"
                                                            placeholder=""
                                                        />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>

                                        <div class="row">
                                            <div class="col-sm-9">
                                                <div class="pull-right">
                                                    <button
                                                        v-if="
                                                            compliance.participant_number_required &&
                                                            !isFinalised &&
                                                            !compliance.fee_paid
                                                        "
                                                        type="button"
                                                        class="btn btn-primary me-2"
                                                        @click.prevent="
                                                            pay_and_submit()
                                                        "
                                                    >
                                                        Pay and Submit
                                                    </button>
                                                    <button
                                                        v-else-if="!isFinalised"
                                                        type="button"
                                                        class="btn btn-primary me-2"
                                                        @click.prevent="
                                                            submit()
                                                        "
                                                    >
                                                        Submit
                                                    </button>
                                                    <button
                                                        v-if="!isFinalised"
                                                        type="button"
                                                        class="btn btn-primary"
                                                        @click.prevent="close()"
                                                    >
                                                        Close
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </FormSection>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import $ from 'jquery';
import { api_endpoints, helpers } from '@/utils/hooks';
import alert from '@vue-utils/alert.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import PrivacyNotice from '@/components/common/privacy_notice.vue';
import { v4 as uuid } from 'uuid';

export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'externalCompliance',
    filters: {
        formatDate: function (data) {
            return moment(data).format('DD/MM/YYYY HH:mm:ss');
        },
    },
    components: {
        alert,
        FormSection,
        PrivacyNotice,
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                helpers.add_endpoint_json(
                    api_endpoints.compliances,
                    to.params.compliance_id
                )
            )
            .then(
                (response) => {
                    next((vm) => {
                        vm.compliance = response;
                        if (
                            vm.compliance.customer_status == 'Under Review' ||
                            vm.compliance.customer_status == 'Approved'
                        ) {
                            vm.isFinalised = true;
                        }
                        if (vm.compliance && vm.compliance.documents) {
                            vm.hasDocuments = true;
                        }

                        helpers
                            .fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.compliances,
                                    to.params.compliance_id +
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
                (error) => {
                    console.log(error);
                }
            );
    },
    data() {
        return {
            form: null,
            loading: [],
            compliance: {},
            original_compliance: {},
            amendment_request: [],
            hasAmendmentRequest: false,
            isFinalised: false,
            hasErrors: false,
            errorString: '',
            pdBody: 'pdBody' + uuid(),
            oBody: 'oBody' + uuid(),
            hasDocuments: false,
            validation_form: null,
            files: [
                {
                    file: null,
                    name: '',
                },
            ],
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        isLoading: function () {
            return this.loading.length > 0;
        },
        isDiscarded: function () {
            return (
                this.compliance &&
                this.compliance.customer_status == 'Discarded'
            );
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        compliance_fee_url: function () {
            return this.compliance
                ? `/compliance_fee/${this.compliance.id}/`
                : '';
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
    },
    watch: {
        isFinalised: function () {
            return (
                this.compliance &&
                (this.compliance.customer_status == 'Under Review' ||
                    this.compliance.customer_status == 'Approved')
            );
        },
        hasDocuments: function () {
            return this.compliance && this.compliance.documents;
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.complianceForm;
    },
    methods: {
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
        submit: function () {
            let vm = this;
            if (helpers.validateForm(vm.form)) {
                vm.sendData();
            }
        },

        close: function () {
            let vm = this;
            this.compliance = {};
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            // this.validation_form.resetForm();
            let file_length = vm.files.length;
            this.files = [];
            for (var i = 0; i < file_length; i++) {
                vm.$nextTick(() => {
                    $('.file-row-' + i).remove();
                });
            }
            this.attachAnother();
            vm.$router.push({ name: 'external-proposals-dash' }); //Navigate to dashboard
        },
        setAmendmentData: function (amendment_request) {
            this.amendment_request = amendment_request;

            if (amendment_request.length > 0) this.hasAmendmentRequest = true;
        },

        delete_document: function (doc) {
            let vm = this;
            let data = { document: doc };
            if (doc) {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.compliances,
                            vm.compliance.id + '/delete_document'
                        ),
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data),
                        }
                    )
                    .then(
                        (response) => {
                            vm.refreshFromResponse(response);
                            vm.compliance = response;
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },

        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            let data = new FormData(vm.form);
            vm.addingComms = true;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.compliances,
                        vm.compliance.id + '/submit'
                    ),
                    {
                        method: 'POST',
                        body: data,
                    }
                )
                .then(
                    (response) => {
                        vm.addingCompliance = false;
                        vm.refreshFromResponse(response);

                        vm.compliance = response;
                        vm.$router.push({
                            name: 'submit_compliance',
                            params: { compliance_id: vm.compliance.id },
                        });
                    },
                    (error) => {
                        vm.hasErrors = true;
                        vm.addingCompliance = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    }
                );
        },

        pay_and_submit: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.hasErrors = false;
                vm.errorString = '';
                let data = new FormData(vm.form);
                vm.addingComms = true;
                if (
                    vm.compliance &&
                    !vm.compliance.documents.length > 0 &&
                    vm.files.length > 0 &&
                    vm.files[0].file == null
                ) {
                    vm.hasErrors = true;
                    vm.errorString =
                        'Please upload at least one document prior to submitting.';
                } else {
                    swal.fire({
                        title: vm.submit_text() + ' Compliance',
                        text:
                            'Are you sure you want to ' +
                            vm.submit_text().toLowerCase() +
                            ' this requirement?',
                        icon: 'question',
                        showCancelButton: true,
                        confirmButtonText: vm.submit_text(),
                    }).then((swalresult) => {
                        if (swalresult.isConfirmed) {
                            helpers.fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.compliances,
                                    vm.compliance.id + '/submit'
                                ),
                                {
                                    method: 'POST',
                                    body: data,
                                }
                            )
                            .then(
                                (response) => {
                                    vm.addingCompliance = false;
                                    vm.refreshFromResponse(response);
                                    vm.compliance = response;

                                    /* after the above save, redirect to the Django post() method in ApplicationFeeView */
                                    vm.post_and_redirect(
                                        vm.compliance_fee_url,
                                        { csrfmiddlewaretoken: vm.csrf_token }
                                    );
                                },
                                (error) => {
                                    vm.hasErrors = true;
                                    vm.addingCompliance = false;
                                    vm.errorString =
                                        helpers.apiVueResourceError(error);
                                }
                            );
                        }
                    });
                }
            }
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

        _sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            // Note: this variable was called `data` before. It was never used and the post method took `formData` which was never declared. I renamed data to formData
            let formData = new FormData(vm.form);
            vm.addingComms = true;

            // remove the confirm prompt when navigating away from window (on button 'Submit' click)
            vm.submitting = true;
            vm.paySubmitting = true;

            swal.fire({
                title: vm.submit_text() + ' Compliance',
                text:
                    'Are you sure you want to ' +
                    vm.submit_text().toLowerCase() +
                    ' this application?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: vm.submit_text(),
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(vm.proposal_form_url, {
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
                            () => {}
                        );

                    // Filming has deferred payment once assessor decides whether 'Licence' (fee) or 'Lawful Authority' (no fee) is to be issued
                    if (
                        !vm.proposal.fee_paid &&
                        vm.proposal.application_type !=
                            vm.application_type_filming
                    ) {
                        vm.save_and_redirect();
                    } else {
                        /* just save and submit - no payment required (probably application was pushed back by assessor for amendment */
                        vm.save_wo_confirm();
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
                                        params: { proposal_id: vm.proposal.id },
                                    });
                                },
                                (err) => {
                                    swal.fire({
                                        title: 'Submit Error',
                                        text: helpers.apiVueResourceError(err),
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

        submit_text: function () {
            return 'Pay and Submit';
        },

        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_compliance = helpers.copyObject(response);
            vm.compliance = helpers.copyObject(response);
            if (
                vm.compliance.customer_status == 'Under Review' ||
                vm.compliance.customer_status == 'Approved'
            ) {
                vm.isFinalised = true;
            }
            if (vm.compliance && vm.compliance.documents) {
                vm.hasDocuments = true;
            }
        },
    },
};
</script>
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}
.actionBtn {
    cursor: pointer;
}
.hidePopover {
    display: none;
}
.btn-file {
    position: relative;
    overflow: hidden;
}
.btn-file input[type='file'] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;
}
.top-buffer {
    margin-top: 0px;
}
.top-buffer-2x {
    margin-top: 0px;
}
</style>
