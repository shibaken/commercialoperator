<template lang="html">
    <div id="editVehicle">
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
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="access_type"
                                            >Vehicle Type</label
                                        >
                                    </div>
                                    <div
                                        id="access_type_parent"
                                        class="col-sm-9"
                                    >
                                        <select
                                            id="access_type"
                                            ref="access_type"
                                            v-model="vehicle_access_id"
                                            class="form-control"
                                            name="access_type"
                                            required
                                        >
                                            <option
                                                v-for="a in access_types"
                                                :key="a.id"
                                                :value="a.id"
                                            >
                                                {{ a.name }}
                                            </option>
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
                                            >Seating Capacity</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="capacity"
                                            v-model="vehicle.capacity"
                                            class="form-control"
                                            name="capacity"
                                            type="number"
                                            required
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
                                            >Registration No.</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="rego"
                                            v-model="vehicle.rego"
                                            class="form-control"
                                            name="rego"
                                            type="text"
                                            required
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
                                            >Registration Expiry</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="rego_expiry"
                                            class="input-group date"
                                            style="width: 40%"
                                        >
                                            <input
                                                v-model="vehicle.rego_expiry"
                                                type="date"
                                                class="form-control"
                                                name="rego_expiry"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                            />
                                            <span class="input-group-addon">
                                                <span
                                                    class="glyphicon glyphicon-calendar"
                                                ></span>
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
                                            >Transport licence no.</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="license"
                                            v-model="vehicle.license"
                                            class="form-control"
                                            name="license"
                                            type="text"
                                            required
                                        />
                                    </div>
                                </div>
                            </div>
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
    name: 'Edit-Vehicle',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        vehicle_action: {
            type: String,
            default: 'edit',
        },
        // eslint-disable-next-line vue/prop-name-casing
        access_types: {
            type: Array,
            required: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            vehicle: Object,
            vehicle_id: Number,
            vehicle_access_id: null,
            state: 'proposed_vehicle',
            issuingVehicle: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            localVehicleAction: JSON.parse(JSON.stringify(this.vehicle_action)),
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.localVehicleAction == 'add'
                ? 'Add a new Vehicle record'
                : 'Edit a vehicle record';
        },
    },
    watch: {
        vehicle_action: {
            handler(newVal) {
                this.localVehicleAction = JSON.parse(JSON.stringify(newVal));
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;

        vm.form = document.forms.vehicleForm;
        this.$nextTick(() => {
            vm.addEventListeners();
        });
    },
    methods: {
        ok: function () {
            let vm = this;
            // Check form validity
            if (helpers.validateForm(vm.form)) {
                console.log('Form is valid');
                vm.sendData();
            } else {
                console.warn('Form is not valid');
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.vehicle = {};
            this.hasErrors = false;
            $(this.$refs.rego_expiry).val('');
            this.$refs.capacity = '';
            this.$refs.license = '';
            this.$refs.rego = '';
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
        fetchVehicle: function (vid) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(api_endpoints.vehicles, vid)
                )
                .then(
                    (res) => {
                        vm.vehicle = res;
                        if (vm.vehicle.access_type) {
                            vm.vehicle_access_id = vm.vehicle.access_type.id;
                        }
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },

        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            if (vm.vehicle_access_id != null) {
                vm.vehicle.access_type = vm.vehicle_access_id;
            }
            let vehicle = JSON.parse(JSON.stringify(vm.vehicle));
            vm.issuingVehicle = true;
            if (vm.localVehicleAction == 'add' && vm.vehicle_id == null) {
                helpers
                    .fetchUrl(api_endpoints.vehicles, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(vehicle),
                    })
                    .then(
                        (response) => {
                            vm.issuingVehicle = false;
                            vm.vehicle = {};
                            vm.close();
                            swal.fire({
                                title: 'Created',
                                text: 'New vehicle record has been created.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingVehicle = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.vehicles,
                            vm.vehicle_id + '/edit_vehicle'
                        ),
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(vehicle),
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingVehicle = false;
                            vm.vehicle = {};
                            vm.close();
                            swal.fire({
                                title: 'Saved',
                                text: 'Vehicle details has been saved.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingVehicle = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        addEventListeners: function () {
            helpers.initialiseSelect2.bind(this)(
                'access_type',
                'access_type_parent',
                'vehicle_access_id',
                'Select a type'
            );
        },
    },
};
</script>

<style lang="css">
input[type='date'],
input[type='text'],
input[type='number'] {
    width: 40%;
    box-sizing: border-box;
    margin-bottom: 0.25rem;
}
</style>
