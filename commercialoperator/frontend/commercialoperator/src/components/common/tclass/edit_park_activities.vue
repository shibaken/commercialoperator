<template lang="html">
    <div id="editParkActivities">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="vehicleForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <form>
                                <div class="form-horizontal col-sm-6">
                                    <label class="control-label">Access</label>
                                    <div
                                        v-for="a in allowed_access_types"
                                        :key="a.id"
                                        class=""
                                    >
                                        <div class="form-check">
                                            <input
                                                ref="Checkbox"
                                                v-model="park_access"
                                                :onclick="isClickable"
                                                class="form-check-input"
                                                type="checkbox"
                                                :value="a.id"
                                                data-parsley-required
                                                :disabled="!canEditActivities"
                                            />
                                            {{ a.name }}
                                        </div>
                                    </div>
                                </div>
                            </form>

                            <form>
                                <div class="form-horizontal col-sm-6">
                                    <label class="control-label"
                                        >Activities</label
                                    >
                                    <div
                                        v-for="a in allowed_activities"
                                        :key="a.id"
                                        class=""
                                    >
                                        <div class="form-check">
                                            <input
                                                ref="Checkbox"
                                                v-model="park_activities"
                                                :onclick="isClickable"
                                                class="form-check-input"
                                                :value="a.id"
                                                type="checkbox"
                                                data-parsley-required
                                                :disabled="!canEditActivities"
                                            />
                                            {{ a.name }}
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="issuingVehicle"
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
                    :disabled="!canEditActivities"
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
    name: 'Edit-Park-Activities',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        vehicle_id: {
            type: Number,
            required: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        vehicle_action: {
            type: String,
            default: 'edit',
        },
        canEditActivities: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            park: Object,
            park_id: null,
            park_name: '',
            access_types: null,
            allowed_activities: [],
            allowed_access_types: [],
            park_access: [],
            park_activities: [],
            vehicle_access_id: null,
            issuingVehicle: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.park_name
                ? 'Edit Access and Activities for ' + this.park_name
                : 'Edit Access and Activities';
        },
        isClickable: function () {
            var vm = this;
            return vm.canEditActivities;
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchAccessTypes();
        vm.form = document.forms.vehicleForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                var allowed_activities_id = [];
                for (var i = 0; i < vm.allowed_activities.length; i++) {
                    allowed_activities_id.push(vm.allowed_activities[i].id);
                }
                for (var j = 0; j < vm.park_activities.length; j++) {
                    if (
                        allowed_activities_id.indexOf(vm.park_activities[j]) ==
                        -1
                    ) {
                        vm.park_activities.splice(j, 1);
                    }
                }
                vm.$emit(
                    'refreshSelectionFromResponse',
                    vm.park_id,
                    vm.park_activities,
                    vm.park_access
                );
            }
            vm.close();
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.park_id = null;
            this.park_access = [];
            this.park_activities = [];
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            this.validation_form.resetForm();
        },
        fetchAccessTypes: function () {
            let vm = this;
            helpers.fetchUrl('/api/access_types.json').then(
                (res) => {
                    vm.access_types = res;
                },
                (err) => {
                    console.log(err);
                }
            );
        },
        fetchAllowedActivities: function (park_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.parks,
                        park_id + '/allowed_activities'
                    )
                )
                .then(
                    (res) => {
                        vm.allowed_activities = res;
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        fetchAllowedAccessTypes: function (park_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.parks,
                        park_id + '/allowed_access'
                    )
                )
                .then(
                    (res) => {
                        vm.allowed_access_types = res;
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },

        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    access_type: 'required',
                },
                messages: {},
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
        eventListeners: function () {},
    },
};
</script>

<style lang="css"></style>
