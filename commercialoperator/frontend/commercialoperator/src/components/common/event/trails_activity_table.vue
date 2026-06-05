<template id="event_trails_activity_table">
    <div class="">
        <div class="col-sm-12">
            <div class="row">
                <div v-if="canEditActivities" class="col-md-3">
                    <input
                        type="button"
                        style="margin-top: 25px"
                        class="btn btn-primary"
                        value="Add"
                        @click.prevent="newTrail"
                    />
                </div>
            </div>
            <div class="row">&nbsp;</div>

            <div class="row">
                <div class="col-lg-12" style="margin-top: 25px">
                    <datatable
                        :id="datatable_id"
                        ref="park_datatable"
                        :dt-options="park_options"
                        :dt-headers="park_headers"
                    />
                </div>
            </div>
        </div>
        <editTrail
            ref="edit_trail"
            :is_internal="is_internal"
            @refreshFromResponse="refreshFromResponse"
        ></editTrail>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue';
import editTrail from './edit_trail_activity.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'EventTrailTableDash',
    components: {
        datatable,
        editTrail,
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
        canEditActivities: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_internal: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        let vm = this;
        return {
            new_park: {
                park: null,
                activities: [],
                proposal: vm.proposal.id,
            },
            pBody: 'pBody' + uuid(),
            datatable_id: 'trail-datatable-' + uuid(),
            uuid: 0,
            // Filters for Parks
            park_headers: [
                'Trail',
                'Section',
                'Activities (application)',
                'Activities (assessor)',
                'Action',
            ],
            park_options: {
                autoWidth: false,
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
                        data: 'trail',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data ? data.name : '';
                        },
                    },
                    {
                        data: 'section',

                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            if (data) {
                                return data.name;
                            } else {
                                return '';
                            }
                        },
                    },
                    {
                        data: 'event_trail_activities',
                    },
                    {
                        data: 'activities_assessor_names',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            if (!data) {
                                data = [];
                            }
                            return data.join(',');
                        },
                    },
                    {
                        data: 'id',
                        orderable: false,
                        searchable: false,
                        mRender: function (data, type, full) {
                            let links = '';
                            if (vm.canEditActivities) {
                                links += `<a href='#${full.id}' data-edit-park='${full.id}'>Edit</a><br/>`;
                                links += `<a href='#${full.id}' data-discard-trail='${full.id}'>Discard</a><br/>`;
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
        editParkBindId: function () {
            let edit_trail_bind_id = '';
            edit_trail_bind_id = 'editPark' + parseInt(this.uuid);
            return edit_trail_bind_id;
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
            var column = vm.$refs.park_datatable.vmDataTable.columns(3); //Hide 'Assigned To column for external'
            column.visible(false);
        }
    },
    methods: {
        fetchFilterLists: function () {},
        newTrail: function () {
            let vm = this;
            this.uuid += 1;

            this.$nextTick(() => {
                this.$refs.edit_trail.trail_id = null;
                var new_trail_another = {
                    trail: null,
                    section: null,
                    event_trail_activities: '',
                    proposal: vm.proposal.id,
                };
                this.$refs.edit_trail.trail = new_trail_another;
                this.$refs.edit_trail.localTrailAction = 'add';

                this.$refs.edit_trail.isModalOpen = true;
            });
        },
        editTrail: function (id) {
            this.uuid += 1;
            this.$nextTick(() => {
                this.$refs.edit_trail.trail_id = id;
                this.$refs.edit_trail.fetchTrail(id);
                this.$refs.edit_trail.isModalOpen = true;
            });
        },
        discardTrail: function (trail_id) {
            let vm = this;
            swal.fire({
                title: 'Discard Trail',
                text: 'Are you sure you want to discard this trail?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Discard Trail',
                confirmButtonColor: '#d9534f',
            }).then(
                (result) => {
                    if (!result.isConfirmed) {
                        return;
                    }
                    helpers
                        .fetchUrl(api_endpoints.discard_event_trail(trail_id), {
                            method: 'DELETE',
                        })
                        .then(
                            () => {
                                swal.fire({
                                    title: 'Discarded',
                                    text: 'Your trail has been discarded',
                                    icon: 'success',
                                });
                                vm.$refs.park_datatable.vmDataTable.ajax.reload();
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
            vm.$refs.park_datatable.vmDataTable.on(
                'click',
                'a[data-edit-park]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-edit-park');
                    vm.editTrail(id);
                }
            );
            // External Discard listener
            vm.$refs.park_datatable.vmDataTable.on(
                'click',
                'a[data-discard-trail]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-discard-trail');
                    vm.discardTrail(id);
                }
            );
        },
        refreshFromResponse: function () {
            this.$refs.park_datatable.vmDataTable.ajax.reload();
        },
        initialiseSearch: function () {},
    },
};
</script>
<style scoped></style>
