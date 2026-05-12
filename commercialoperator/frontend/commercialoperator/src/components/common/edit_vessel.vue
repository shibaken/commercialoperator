<template lang="html">
    <div id="editVessel">
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
                        id="vessel-form"
                        class="form-horizontal"
                        name="vesselForm"
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
                                            >Nominated Vessel</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="capacity"
                                            v-model="vessel.nominated_vessel"
                                            class="form-control"
                                            name="capacity"
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
                                            >SPV No./ Reg. No.</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="spv_no"
                                            v-model="vessel.spv_no"
                                            class="form-control"
                                            name="spv_no"
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
                                            >Hire and Drive reg.</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="hire_rego"
                                            v-model="vessel.hire_rego"
                                            class="form-control"
                                            name="hire_rego"
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
                                            >No. of craft</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="craft_no"
                                            v-model="vessel.craft_no"
                                            class="form-control"
                                            name="craft_no"
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
                                            >Vessel Size</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            ref="size"
                                            v-model="vessel.size"
                                            class="form-control"
                                            name="size"
                                            type="number"
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
                    v-if="issuingVessel"
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
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Edit-Vessel',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        vessel_action: {
            type: String,
            default: 'edit',
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            vessel: Object,
            vessel_id: Number,
            access_types: null,
            vessel_access_id: null,
            state: 'proposed_vessel',
            issuingVessel: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            localVesselAction: JSON.parse(JSON.stringify(this.vessel_action)),
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.localVesselAction == 'add'
                ? 'Add a new Vessel record'
                : 'Edit a vessel record';
        },
    },
    watch: {
        vessel_action: {
            handler(newVal) {
                this.localVesselAction = JSON.parse(JSON.stringify(newVal));
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;

        vm.form = document.forms.vesselForm;
        this.$nextTick(() => {
            vm.eventListeners();
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
            this.vessel = {};
            this.hasErrors = false;
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
        fetchVessel: function (vid) {
            let vm = this;
            helpers
                .fetchUrl(helpers.add_endpoint_json(api_endpoints.vessels, vid))
                .then(
                    (res) => {
                        vm.vessel = res;
                        if (vm.vessel.access_type) {
                            vm.vessel_access_id = vm.vessel.access_type.id;
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
            let vessel = JSON.parse(JSON.stringify(vm.vessel));
            vm.issuingVessel = true;
            if (vm.localVesselAction == 'add' && vm.vessel_id == null) {
                helpers
                    .fetchUrl(api_endpoints.vessels, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(vessel),
                    })
                    .then(
                        (response) => {
                            vm.issuingVessel = false;
                            vm.close();
                            swal.fire({
                                title: 'Created',
                                text: 'New vessel record has been created.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingVessel = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.vessels,
                            vm.vessel_id + '/edit_vessel'
                        ),
                        {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(vessel),
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingVessel = false;
                            vm.close();
                            swal.fire({
                                title: 'Saved',
                                text: 'Vessel details has been saved.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingVessel = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        eventListeners: function () {},
    },
};
</script>

<style lang="css">
input[type='text'],
input[type='number'] {
    width: 40%;
    box-sizing: border-box;
    margin-bottom: 0.25rem;
}
</style>
