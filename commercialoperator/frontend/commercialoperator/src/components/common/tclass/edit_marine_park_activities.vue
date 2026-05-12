<template lang="html">
    <div id="editMarinePark">
        <modal
            transition="modal fade"
            :title="title(localZoneLabel)"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="marineActivitiesForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
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
                                                v-model="new_activities"
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
                                <div class="form-group">
                                    <div class="row">
                                        <div class="form-horizontal col-sm-9">
                                            <label
                                                class="control-label pull-left"
                                                for="Name"
                                                >Point of access</label
                                            >
                                        </div>
                                        <div class="form-horizontal col-sm-9">
                                            <input
                                                ref="access_point"
                                                v-model="access_point"
                                                class="form-control"
                                                name="access_point"
                                                type="text"
                                                :disabled="!canEditActivities"
                                            />
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
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Edit-marine-park-activities',
    components: {
        modal,
        alert,
    },
    props: {
        canEditActivities: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        zone_label: {
            type: String,
            default: '',
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            park: Object,
            park_id: null,
            zone_id: null,
            park_name: '',
            access_types: null,
            allowed_activities: [],
            park_access: [],
            park_activities: [],
            selected_zone: '',
            issuingVehicle: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            // Adding this prop here because it was missing in the original code
            access_point: '',
            localZoneLabel: this.zone_label, // Local copy to avoid mutating zone_label
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        isClickable: function () {
            var vm = this;
            return vm.canEditActivities;
        },
    },
    watch: {
        zone_label: {
            handler: function (value) {
                this.localZoneLabel = value;
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.marineActivitiesForm;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        title: function (label) {
            return 'Edit Access and Activities for ' + label;
        },
        ok: function () {
            let vm = this;
            var new_activities = [];

            var data = {
                zone: vm.zone_id,
                activities: vm.new_activities,
                access_point: vm.access_point,
            };
            new_activities.push(data);
            vm.$emit(
                'refreshSelectionFromResponse',
                vm.park_id,
                vm.zone_id,
                data
            );
            vm.close();
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.park_id = null;
            this.selected_zone = '';
            this.park_activities = [];
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
        },
        addFormValidations: function () {},
        eventListeners: function () {},
    },
};
</script>

<style lang="css"></style>
