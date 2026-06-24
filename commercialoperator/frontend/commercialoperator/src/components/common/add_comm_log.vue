<template lang="html">
    <div id="AddComms">
        <modal
            transition="modal fade"
            title="Communication log - Add entry"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="commsForm">
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
                                            >To</label
                                        >
                                    </div>
                                    <div class="col-sm-4">
                                        <input
                                            v-model="comms.to"
                                            type="text"
                                            class="form-control"
                                            name="to"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >From</label
                                        >
                                    </div>
                                    <div class="col-sm-4">
                                        <input
                                            v-model="comms.fromm"
                                            type="text"
                                            class="form-control"
                                            name="fromm"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Type</label
                                        >
                                    </div>
                                    <div
                                        id="select_add_comm_log_type_parent"
                                        class="col-sm-4"
                                    >
                                        <select
                                            id="select_add_comm_log_type"
                                            ref="select_add_comm_log_type"
                                            v-model="comms.type"
                                            class="form-control"
                                            name="type"
                                        >
                                            <option value="">
                                                Select Type
                                            </option>
                                            <option value="email">Email</option>
                                            <option value="mail">Mail</option>
                                            <option value="phone">Phone</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Subject/Description</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            v-model="comms.subject"
                                            type="text"
                                            class="form-control"
                                            name="subject"
                                            style="width: 70%"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Text</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <textarea
                                            v-model="comms.text"
                                            name="text"
                                            class="form-control"
                                            style="width: 70%"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
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
                                        <template v-for="(f, i) in files" :key="i">
                                            <div
                                                :class="
                                                    'row top-buffer file-row-' +
                                                    i
                                                "
                                            >
                                                <div class="col-sm-4">
                                                    <span
                                                        v-if="f.file == null"
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
                                                <div class="col-sm-4">
                                                    <span>{{ f.name }}</span>
                                                </div>
                                                <div class="col-sm-4">
                                                    <button
                                                        class="btn btn-danger"
                                                        @click="removeFile(i)"
                                                    >
                                                        Remove
                                                    </button>
                                                </div>
                                            </div>
                                        </template>
                                        <a
                                            href=""
                                            @click.prevent="attachAnother"
                                            ><i
                                                class="fas fa-lg fa-plus top-buffer-2x"
                                            ></i
                                        ></a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="addingComms"
                    type="button"
                    disabled
                    class="btn btn-primary"
                    @click="ok"
                >
                    <i class="fas fa-spinner fa-spin"></i> Adding
                </button>
                <button
                    v-else
                    type="button"
                    class="btn btn-primary"
                    @click="ok"
                >
                    Add
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
import { helpers } from '@/utils/hooks.js';
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Add-Comms',
    components: {
        modal,
        alert,
    },
    props: {
        url: {
            type: String,
            required: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            comms: {
                to: '',
                fromm: '',
                type: '',
                subject: '',
                text: '',
                cc: '',
            },
            state: 'proposed_approval',
            addingComms: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            to: "",
            from: "",
            log_type: "",
            subject: "",
            text: "",
            files: [],
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.processing_status == 'With Approver'
                ? 'Issue Comms'
                : 'Propose to issue licence';
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.commsForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            helpers.initialiseSelect2.bind(this)(
                'select_add_comm_log_type',
                'select_add_comm_log_type_parent',
                'comms.type',
                'Select a Type',
                false
            );
            vm.syncTypeSelect('');
        });
    },
    methods: {
        syncTypeSelect: function (value = '') {
            this.comms.type = value;
            if (this.$refs.select_add_comm_log_type) {
                $(this.$refs.select_add_comm_log_type).val(value).trigger('change');
            }
        },
        ok: function () {
            let vm = this;
            vm.hasErrors = false;
            vm.errorString = '';

            if (vm.addingComms) {
                return;
            }

            const formIsValid = vm.validation_form
                ? vm.validation_form.form()
                : $(vm.form).valid();

            if (!formIsValid) {
                vm.hasErrors = true;
                if (vm.validation_form && vm.validation_form.errorList.length > 0) {
                    const firstError = vm.validation_form.errorList[0];
                    const fieldName = firstError.element.name
                        ? firstError.element.name.replace('fromm', 'from')
                        : 'required field';
                    vm.errorString = `Please complete the '${fieldName}' field.`;
                } else {
                    vm.errorString = 'Please complete all required fields before adding this entry.';
                }
                return;
            }

            vm.sendData();
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
            file_obj.name = _file ? _file.name : '';
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
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.addingComms = false;
            this.comms = {
                to: '',
                fromm: '',
                type: '',
                subject: '',
                text: '',
                cc: '',
            };
            this.hasErrors = false;
            this.errorString = '';
            $('.has-error').removeClass('has-error');
            if (this.validation_form) {
                this.validation_form.resetForm();
            }
            if (this.form) {
                this.form.reset();
            }
            this.syncTypeSelect('');
            this.files = [];
            this.attachAnother();
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            let comms = new FormData(); 
            comms.append('to', vm.comms.to || '');
            comms.append('fromm', vm.comms.fromm || '');
            comms.append('cc', vm.comms.cc || '');
            comms.append('type', vm.comms.type || '');
            comms.append('subject', vm.comms.subject || '');
            comms.append('text', vm.comms.text || '');
            for (let i = 0; i < vm.files.length; i++) {
                if (vm.files[i] && vm.files[i].file) {
                    comms.append('files', vm.files[i].file);
                }
            }
            vm.addingComms = true;
            helpers
                .fetchUrl(vm.url, {
                    method: 'POST',
                    body: comms,
                })
                .then(
                    () => {
                        vm.addingComms = false;
                        vm.close();
                    },
                    (error) => {
                        vm.hasErrors = true;
                        vm.addingComms = false;
                        try {
                            vm.errorString = helpers.apiVueResourceError(error);
                        } catch (e) {
                            vm.errorString = 'The file type is not supported.';
                        }

                        if (!vm.errorString) {
                            vm.errorString = 'The file type is not supported.';
                        }
                    }
                );
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    to: 'required',
                    fromm: 'required',
                    type: 'required',
                    subject: 'required',
                    text: 'required',
                },
                messages: {},
                showErrors: function (errorMap, errorList) {
                    const hasTooltip = $.fn && typeof $.fn.tooltip === 'function';
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
                        var $errorElement = $(error.element);

                        if (hasTooltip) {
                            $errorElement.tooltip({
                                trigger: 'focus',
                            });
                        }

                        $errorElement
                            .attr('data-original-title', error.message)
                            .parents('.form-group')
                            .addClass('has-error');
                    }
                },
            });
        },
    },
};
</script>

<style lang="css">
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
    margin-top: 5px;
}
.top-buffer-2x {
    margin-top: 10px;
}
</style>
