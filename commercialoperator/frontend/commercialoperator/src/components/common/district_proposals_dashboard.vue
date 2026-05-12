<template id="district_proposal_dashboard">
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div class="row mb-1">
                    <div class="col-md-3">
                        <div
                            id="select_district_proposal_status_parent"
                            class="form-group"
                        >
                            <label for="select_district_proposal_status"
                                >Status</label
                            >
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_district_proposal_status"
                                    ref="select_district_proposal_status"
                                    v-model="filterProposalStatus"
                                    class="form-control"
                                >
                                    <option value="All">All</option>
                                    <option
                                        v-for="s in proposal_status"
                                        :key="s.value"
                                        :value="s.value"
                                    >
                                        {{ s.name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label for="input_proposal_date_from"
                            >Lodged From</label
                        >
                        <div
                            ref="proposalDateFromPicker"
                            class="input-group date"
                        >
                            <input
                                id="input_proposal_date_from"
                                v-model="filterProposalLodgedFrom"
                                type="date"
                                class="form-control"
                                max="2999-12-31"
                                placeholder="DD/MM/YYYY"
                            />
                            <span class="input-group-text">
                                <i class="fas fa-calendar-days"></i>
                            </span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <label for="input_proposal_date_to">Lodged To</label>
                        <div
                            ref="proposalDateToPicker"
                            class="input-group date"
                        >
                            <input
                                id="input_proposal_date_to"
                                v-model="filterProposalLodgedTo"
                                type="date"
                                class="form-control"
                                max="2999-12-31"
                                placeholder="DD/MM/YYYY"
                            />
                            <span class="input-group-text">
                                <i class="fas fa-calendar-days"></i>
                            </span>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-lg-12">
                        <datatable
                            :id="datatable_id"
                            ref="proposal_datatable"
                            :dt-options="proposal_options"
                            :dt-headers="proposal_headers"
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import datatable from '@/utils/vue/datatable.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'DistrictProposalTableDash',
    components: {
        datatable,
    },
    props: {
        url: {
            type: String,
            required: true,
        },
    },

    data() {
        let vm = this;
        return {
            pBody: 'pBody' + uuid(),
            datatable_id: 'district-proposal-datatable-' + uuid(),
            // Filters for Proposals
            filterProposalRegion: [],
            filterProposalActivity: 'All',
            filterProposalStatus: 'All',
            filterProposalLodgedFrom: '',
            filterProposalLodgedTo: '',
            dateFormat: 'DD/MM/YYYY',
            proposal_status: [],
            proposal_headers: [
                'Number',
                'Submitter',
                'Applicant',
                'Status',
                'Lodged on',
                'Action',
            ],
            proposal_options: {
                customProposalSearch: true,
                tableID: 'proposal-datatable-' + uuid(),
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    {
                        responsivePriority: 2,
                        targets: 5, // Action column
                    },
                ],
                responsive: true,
                serverSide: true,
                order: [[0, 'desc']],
                lengthMenu: [
                    [10, 25, 50, 100, -1],
                    [10, 25, 50, 100, 'All'],
                ],
                ajax: {
                    url: vm.url,
                    dataSrc: 'data',

                    // adding extra GET params for Custom filtering
                    data: function (d) {
                        d.date_from =
                            vm.filterProposalLodgedFrom != '' &&
                            vm.filterProposalLodgedFrom != null
                                ? moment(vm.filterProposalLodgedFrom).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.date_to =
                            vm.filterProposalLodgedTo != '' &&
                            vm.filterProposalLodgedTo != null
                                ? moment(vm.filterProposalLodgedTo).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.datatable_filter_processing_status =
                            vm.filterProposalStatus;
                    },
                },
                columns: [
                    {
                        data: 'proposal',
                        mRender: function (data, type, full) {
                            return full.proposal_lodgement_number;
                        },
                        name: 'proposal__id, proposal__lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'submitter',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            if (data && data.full_name) {
                                return `${data.full_name}`;
                            }
                            return '';
                        },
                        name: 'proposal__submitter__first_name, proposal__submitter__last_name, proposal__submitter__email',
                        orderable: false,
                        searchable: false, //overridden by filterbackend
                    },
                    {
                        data: 'applicant',
                        name: 'proposal__org_applicant__organisation__organisation_name, proposal__proxy_applicant__email, proposal__proxy_applicant__first_name, proposal__proxy_applicant__last_name',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'processing_status',
                        name: 'processing_status',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'proposal_lodgement_date',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data != '' && data != null
                                ? moment(data).format(vm.dateFormat)
                                : '';
                        },
                        name: 'proposal__lodgement_date',
                        orderable: true,
                        searchable: false,
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            links += full.district_assessor_can_assess
                                ? `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>Process</a><br/>`
                                : `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>View</a><br/>`;
                            return links;
                        },
                        searchable: false,
                        orderable: false,
                        name: '',
                    },
                    { data: 'proposal', visible: false, searchable: false },
                    { data: 'id', visible: false, searchable: false },
                ],
                processing: true,
            },
            isLoading: false,
        };
    },
    computed: {},
    watch: {
        filterProposalStatus: function () {
            let vm = this;
            if (vm.filterProposalStatus != 'All') {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(3)
                    .search(vm.filterProposalStatus)
                    .draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(3)
                    .search('')
                    .draw();
            }
        },
        filterProposalRegion: {
            handler: function () {
                this.$refs.proposal_datatable.vmDataTable.draw();
            },
            deep: true,
        },
        filterProposalLodgedFrom: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterProposalLodgedTo: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchFilterLists();
        $('a[data-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
        });
    },
    methods: {
        fetchFilterLists: function () {
            let vm = this;
            vm.isLoading = true;

            helpers
                .fetchUrl(api_endpoints.filter_list_district_proposals)
                .then(
                    (response) => {
                        vm.proposal_status = response.processing_status_choices;
                    },
                    (error) => {
                        console.log(error);
                    }
                )
                .finally(() => {
                    vm.isLoading = false;
                });
        },

        addEventListeners: function () {
            let vm = this;
            // End Proposal Date Filters
            // External Discard listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-discard-proposal]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-discard-proposal');
                    vm.discardProposal(id);
                }
            );

            helpers.initialiseSelect2.bind(this)(
                'select_district_proposal_status',
                'select_district_proposal_status_parent',
                'filterProposalStatus',
                'Select Status',
                false
            );
        },
        initialiseSearch: function () {
            this.dateSearch();
        },
        dateSearch: function () {
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function (settings, data, dataIndex, original) {
                    let from = vm.filterProposalLodgedFrom;
                    let to = vm.filterProposalLodgedTo;
                    let val = original.lodgement_date;

                    if (from == '' && to == '') {
                        return true;
                    } else if (from != '' && to != '') {
                        return val != null && val != ''
                            ? moment()
                                  .range(
                                      moment(from, vm.dateFormat),
                                      moment(to, vm.dateFormat)
                                  )
                                  .contains(moment(val))
                            : false;
                    } else if (from == '' && to != '') {
                        if (val != null && val != '') {
                            return moment(to, vm.dateFormat).diff(
                                moment(val)
                            ) >= 0
                                ? true
                                : false;
                        } else {
                            return false;
                        }
                    } else if (to == '' && from != '') {
                        if (val != null && val != '') {
                            return moment(val).diff(
                                moment(from, vm.dateFormat)
                            ) >= 0
                                ? true
                                : false;
                        } else {
                            return false;
                        }
                    } else {
                        return false;
                    }
                }
            );
        },
    },
};
</script>
<style scoped></style>
