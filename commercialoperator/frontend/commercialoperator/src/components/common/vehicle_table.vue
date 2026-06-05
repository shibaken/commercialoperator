<template id="vehicle_table">
    <div class="row">
        <div class="col-sm-12">
            <div class="row">
                <div v-if="!proposal.readonly" class="col-md-3">
                    <input
                        type="button"
                        style="margin-top: 25px"
                        class="btn btn-primary"
                        value="Add new vehicle"
                        @click.prevent="newVehicle"
                    />
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12">
                    <datatable
                        :id="datatable_id"
                        ref="vehicle_datatable"
                        :dt-options="vehicle_options"
                        :dt-headers="vehicle_headers"
                    />
                </div>
            </div>
        </div>
        <editVehicle
            ref="edit_vehicle"
            :access_types="access_types"
            @refreshFromResponse="refreshFromResponse"
        ></editVehicle>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue';
import editVehicle from './edit_vehicle.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'VehicleTableDash',
    components: {
        datatable,
        editVehicle,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        url: {
            type: String,
            required: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        access_types: {
            type: Array,
            required: true,
        },
    },
    data() {
        let vm = this;
        return {
            new_vehicle: {
                access_type: null,
                capacity: '',
                rego: '',
                rego_expiry: null,
                license: '',
                proposal: vm.proposal.id,
            },
            pBody: 'pBody' + uuid(),
            datatable_id: 'vehicle-datatable-' + uuid(),
            // Filters for Vehicles
            external_status: ['Due', 'Future', 'Under Review', 'Approved'],
            internal_status: ['Due', 'Future', 'With Assessor', 'Approved'],
            vehicle_headers: [
                'Vehicle Type',
                'Seating capacity',
                'Registration no.',
                'Registration Expiry',
                'Transport license no.',
                'Action',
            ],
            vehicle_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    {
                        responsivePriority: 2,
                        targets: -1,
                    },
                ],
                responsive: true,
                ajax: {
                    url: vm.url,
                    dataSrc: '',
                },
                dom: constants.DATATABLE_DOM_HTML,
                buttons: [
                    {
                        extend: 'excelHtml5',
                        text: 'Excel',
                        className: 'btn btn-primary me-2 rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                    {
                        extend: 'csvHtml5',
                        text: 'CSV',
                        className: 'btn btn-primary rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                ],
                columns: [
                    {
                        data: 'access_type',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data.name;
                        },
                    },
                    {
                        data: 'capacity',
                    },
                    {
                        data: 'rego',
                    },
                    {
                        data: 'rego_expiry',
                    },
                    {
                        data: 'license',
                    },
                    {
                        data: 'id',
                        orderable: false,
                        searchable: false,
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.proposal.readonly) {
                                links += `<a href='#${full.id}' data-edit-vehicle='${full.id}'>Edit Vehicle</a><br/>`;
                                links += `<a href='#${full.id}' data-discard-vehicle='${full.id}'>Discard</a><br/>`;
                            }
                            return links;
                        },
                    },
                ],
                processing: true,
            },
        };
    },
    computed: {
        is_external: function () {
            return this.level == 'external';
        },
    },
    watch: {},
    mounted: function () {
        let vm = this;
        vm.fetchFilterLists();
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
        });
        if (vm.is_external) {
            var column = vm.$refs.vehicle_datatable.vmDataTable.columns(8); //Hide 'Assigned To column for external'
            column.visible(false);
        }
    },
    methods: {
        fetchFilterLists: function () {},
        newVehicle: function () {
            let vm = this;
            this.$refs.edit_vehicle.vehicle_id = null;
            var new_vehicle_another = {
                access_type: null,
                capacity: '',
                rego: '',
                rego_expiry: null,
                license: '',
                proposal: vm.proposal.id,
            };
            this.$refs.edit_vehicle.vehicle = new_vehicle_another;
            this.$refs.edit_vehicle.localVehicleAction = 'add';
            this.$refs.edit_vehicle.isModalOpen = true;
        },
        editVehicle: function (id) {
            this.$refs.edit_vehicle.vehicle_id = id;
            this.$refs.edit_vehicle.fetchVehicle(id);
            this.$refs.edit_vehicle.isModalOpen = true;
        },
        discardVehicle: function (vehicle_id) {
            let vm = this;
            swal.fire({
                title: 'Discard Vehicle',
                text: 'Are you sure you want to discard this vehicle?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Discard Vehicle',
                confirmButtonColor: '#d9534f',
            }).then(
                (result) => {
                    if (!result.isConfirmed) {
                        return;
                    }
                    helpers
                        .fetchUrl(api_endpoints.discard_vehicle(vehicle_id), {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        })
                        .then(
                            () => {
                                swal.fire({
                                    title: 'Discarded',
                                    text: 'Your vehicle has been discarded',
                                    icon: 'success',
                                });
                                vm.$refs.vehicle_datatable.vmDataTable.ajax.reload();
                            },
                            (error) => {
                                console.log(error);
                            }
                        );
                },
                () => {}
            );
        },
        addEventListeners: function () {
            let vm = this;
            vm.$refs.vehicle_datatable.vmDataTable.on(
                'click',
                'a[data-edit-vehicle]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-edit-vehicle');
                    vm.editVehicle(id);
                }
            );
            // External Discard listener
            vm.$refs.vehicle_datatable.vmDataTable.on(
                'click',
                'a[data-discard-vehicle]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-discard-vehicle');
                    vm.discardVehicle(id);
                }
            );
        },
        refreshFromResponse: function () {
            this.$refs.vehicle_datatable.vmDataTable.ajax.reload();
        },
        initialiseSearch: function () {},
    },
};
</script>
<style scoped></style>
