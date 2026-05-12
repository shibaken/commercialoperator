<template lang="html">
    <div id="proposalRequirementDetail">
        <modal
            transition="modal fade"
            title="Requirement"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="requirementForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <label class="radio-inline control-label"
                                    ><input
                                        v-model="requirement.standard"
                                        type="radio"
                                        name="requirementType"
                                        :value="true"
                                    />Standard Requirement</label
                                >
                                <label class="radio-inline"
                                    ><input
                                        v-model="requirement.standard"
                                        type="radio"
                                        name="requirementType"
                                        :value="false"
                                    />Free Text Requirement</label
                                >
                            </div>
                        </div>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Requirement</label
                                        >
                                    </div>
                                    <div
                                        v-if="requirement.standard"
                                        class="col-sm-9"
                                    >
                                        <div
                                            v-show="requirements.length > 0"
                                            style="width: 70% !important"
                                        >
                                            <div
                                                id="standard_req_parent"
                                                class="form-group"
                                            >
                                                <select
                                                    id="standard_req"
                                                    ref="standard_req"
                                                    v-model="
                                                        requirement.standard_requirement
                                                    "
                                                    class="form-control"
                                                    name="standard_requirement"
                                                >
                                                    <option
                                                        v-for="r in requirements"
                                                        :key="r.id"
                                                        :value="r.id"
                                                    >
                                                        {{ r.code }}
                                                        {{ r.text }}
                                                    </option>
                                                </select>
                                            </div>
                                        </div>
                                    </div>
                                    <div v-else class="col-sm-9">
                                        <textarea
                                            v-model="
                                                requirement.free_requirement
                                            "
                                            style="width: 70%"
                                            class="form-control"
                                            name="free_requirement"
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
                                            >Due Date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="due_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-model="requirement.due_date"
                                                type="date"
                                                class="form-control"
                                                name="due_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-9">
                                        <div
                                            ref="add_attachments"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <FileField2
                                                ref="filefield"
                                                :uploaded_documents="
                                                    requirement.requirement_documents
                                                "
                                                :delete_url="delete_url"
                                                :proposal_id="proposal_id"
                                                :is-repeatable="true"
                                                name="requirements_file"
                                                @refreshFromResponse="
                                                    refreshFromResponse
                                                "
                                            />
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <template v-if="validDate">
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-3">
                                            <label
                                                class="control-label pull-left"
                                                for="Name"
                                                >Notification only</label
                                            >
                                        </div>
                                        <div class="col-sm-9">
                                            <label class="checkbox-inline"
                                                ><input
                                                    v-model="
                                                        requirement.notification_only
                                                    "
                                                    type="checkbox"
                                            /></label>
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-3">
                                            <label
                                                class="control-label pull-left"
                                                for="Name"
                                                >Recurrence</label
                                            >
                                        </div>
                                        <div class="col-sm-9">
                                            <label class="checkbox-inline"
                                                ><input
                                                    v-model="
                                                        requirement.recurrence
                                                    "
                                                    type="checkbox"
                                            /></label>
                                        </div>
                                    </div>
                                </div>
                                <template v-if="requirement.recurrence">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label
                                                    class="control-label pull-left"
                                                    for="Name"
                                                    >Recurrence pattern</label
                                                >
                                            </div>
                                            <div class="col-sm-9">
                                                <label
                                                    class="radio-inline control-label"
                                                    ><input
                                                        v-model="
                                                            requirement.recurrence_pattern
                                                        "
                                                        type="radio"
                                                        name="recurrenceSchedule"
                                                        value="1"
                                                    />Weekly</label
                                                >
                                                <label
                                                    class="radio-inline control-label"
                                                    ><input
                                                        v-model="
                                                            requirement.recurrence_pattern
                                                        "
                                                        type="radio"
                                                        name="recurrenceSchedule"
                                                        value="2"
                                                    />Monthly</label
                                                >
                                                <label
                                                    class="radio-inline control-label"
                                                    ><input
                                                        v-model="
                                                            requirement.recurrence_pattern
                                                        "
                                                        type="radio"
                                                        name="recurrenceSchedule"
                                                        value="3"
                                                    />Yearly</label
                                                >
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <label
                                                    class="control-label"
                                                    for="Name"
                                                >
                                                    <strong class="pull-left"
                                                        >Recur every</strong
                                                    >
                                                    <input
                                                        v-model="
                                                            requirement.recurrence_schedule
                                                        "
                                                        class="form-control w-50 pull-left"
                                                        style="
                                                            width: 10%;
                                                            margin-left: 10px;
                                                        "
                                                        type="number"
                                                        name="schedule"
                                                    />
                                                    <strong
                                                        v-if="
                                                            requirement.recurrence_pattern ==
                                                            '1'
                                                        "
                                                        class="pull-left"
                                                        style="
                                                            margin-left: 10px;
                                                        "
                                                        >week(s)</strong
                                                    >
                                                    <strong
                                                        v-else-if="
                                                            requirement.recurrence_pattern ==
                                                            '2'
                                                        "
                                                        class="pull-left"
                                                        style="
                                                            margin-left: 10px;
                                                        "
                                                        >month(s)</strong
                                                    >
                                                    <strong
                                                        v-else-if="
                                                            requirement.recurrence_pattern ==
                                                            '3'
                                                        "
                                                        class="pull-left"
                                                        style="
                                                            margin-left: 10px;
                                                        "
                                                        >year(s)</strong
                                                    >
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </template>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <template v-if="requirement.id">
                    <button
                        v-if="updatingRequirement"
                        type="button"
                        disabled
                        class="btn btn-secondary"
                        @click="ok"
                    >
                        <i class="fas fa-spinnner fa-spin"></i> Updating
                    </button>
                    <button
                        v-else
                        type="button"
                        class="btn btn-secondary"
                        @click="ok"
                    >
                        Update
                    </button>
                </template>
                <template v-else>
                    <button
                        v-if="addingRequirement"
                        type="button"
                        disabled
                        class="btn btn-secondary"
                        @click="ok"
                    >
                        <i class="fas fa-spinner fa-spin"></i> Adding
                    </button>
                    <button
                        v-else
                        type="button"
                        class="btn btn-secondary"
                        @click="ok"
                    >
                        Add
                    </button>
                </template>
                <button type="button" class="btn btn-secondary" @click="cancel">
                    Cancel
                </button>
            </template>
        </modal>
    </div>
</template>

<script>
import FileField2 from '@/components/forms/filefield2.vue';
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Requirement-Detail',
    components: {
        FileField2,
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        proposal_id: {
            type: Number,
            required: true,
        },
        requirements: {
            type: Array,
            required: true,
        },
        hasReferralMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        referral_group: {
            type: Number,
            default: null,
        },
        hasDistrictAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        district_proposal: {
            type: Number,
            default: null,
        },
        district: {
            type: Number,
            default: null,
        },
    },
    data: function () {
        let vm = this;
        return {
            isModalOpen: false,
            form: null,
            requirement: {
                id: '',
                due_date: '',
                standard: true,
                recurrence: false,
                recurrence_pattern: '1',
                proposal: vm.proposal_id,
                referral_group: vm.referral_group,
                num_files: 0,
                input_name: 'requirement_doc',
                requirement_documents: [],
                district_proposal: vm.district_proposal,
                district: vm.district,
            },
            addingRequirement: false,
            updatingRequirement: false,
            validation_form: null,
            type: '1',
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            validDate: false,
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        due_date: {
            cache: false,
            get() {
                if (
                    this.requirement.due_date == undefined ||
                    this.requirement.due_date == '' ||
                    this.requirement.due_date == null
                ) {
                    return '';
                } else {
                    return this.requirement.due_date;
                }
            },
        },
        delete_url: function () {
            return this.requirement.id
                ? '/api/proposal_requirements/' +
                      this.requirement.id +
                      '/delete_document/'
                : '';
        },
    },
    watch: {
        due_date: function () {
            this.validDate = moment(this.requirement.due_date).isValid();
        },
        'requirement.standard': {
            handler: function (val) {
                if (val == true) {
                    const vm = this;
                    this.$nextTick(() => {
                        vm.eventListeners();
                    });
                }
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.requirementForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
        });
        vm.requirement.requirement_documents =
            vm.$refs.filefield.uploaded_documents;
    },
    methods: {
        refreshFromResponse: function (updated_docs) {
            this.requirement.requirement_documents = updated_docs;
        },
        initialiseRequirement: function () {
            this.requirement = {
                due_date: '',
                standard: true,
                recurrence: false,
                recurrence_pattern: '1',
                proposal: this.proposal_id,
                referral_group: this.referral_group,
            };
        },
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
                vm.$refs.filefield.reset_files();
            }
        },
        cancel: function () {
            this.close();
            this.$refs.filefield.reset_files();
        },
        close: function () {
            this.isModalOpen = false;
            $(this.$refs.standard_req).val(null).trigger('change');
            this.requirement = {
                standard: true,
                recurrence: false,
                due_date: '',
                recurrence_pattern: '1',
                proposal: this.proposal_id,
            };
            this.$refs.filefield.reset_files();
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            // $(this.$refs.due_date).data('DateTimePicker').clear();
            this.validation_form.resetForm();
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
            let requirement = JSON.parse(JSON.stringify(vm.requirement));
            if (requirement.standard) {
                requirement.free_requirement = '';
            } else {
                requirement.standard_requirement = '';
                $(this.$refs.standard_req).val(null).trigger('change');
            }
            if (!requirement.due_date) {
                requirement.due_date = null;
                requirement.recurrence = false;
                delete requirement.recurrence_pattern;
                requirement.recurrence_schedule
                    ? delete requirement.recurrence_schedule
                    : '';
            }

            let formData = new FormData();

            // Add files to formData
            var files = vm.$refs.filefield.files;
            $.each(files, function (idx, v) {
                var file = v['file'];
                var filename = v['name'];
                var name = 'file-' + idx;
                formData.append(name, file, filename);
            });
            requirement.num_files = files.length;
            requirement.input_name = 'requirement_doc';
            requirement.proposal = vm.proposal_id;

            if (vm.requirement.id) {
                vm.updatingRequirement = true;
                requirement.update = true;
                formData.append('data', JSON.stringify(requirement));
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposal_requirements,
                            requirement.id
                        ),
                        {
                            method: 'PUT',
                            body: formData,
                        }
                    )
                    .then(
                        () => {
                            vm.updatingRequirement = false;
                            vm.$parent.updatedRequirements();
                            vm.close();
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.errorString = helpers.apiVueResourceError(error);
                            vm.updatingRequirement = false;
                        }
                    );
            } else {
                vm.addingRequirement = true;
                requirement.update = false;
                formData.append('data', JSON.stringify(requirement));
                helpers
                    .fetchUrl(api_endpoints.proposal_requirements, {
                        method: 'POST',
                        body: formData,
                    })
                    .then(
                        () => {
                            vm.addingRequirement = false;
                            vm.close();
                            vm.$parent.updatedRequirements();
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.addingRequirement = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    standard_requirement: {
                        required: {
                            depends: function () {
                                return vm.requirement.standard;
                            },
                        },
                    },
                    free_requirement: {
                        required: {
                            depends: function () {
                                return !vm.requirement.standard;
                            },
                        },
                    },
                    schedule: {
                        required: {
                            depends: function () {
                                return vm.requirement.recurrence;
                            },
                        },
                    },
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
        eventListeners: function () {
            let vm = this;
            // Intialise select2
            $(vm.$refs.standard_req)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    minimumInputLength: 0,
                    placeholder: 'Select Requirement',
                    dropdownParent: '#standard_req_parent',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.requirement.standard_requirement = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.requirement.standard_requirement = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
