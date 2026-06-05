<template id="proposal_dashboard">
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div class="row" mb-1>
                    <div class="col-md-3">
                        <div
                            id="select_qaofficer_proposal_status_parent"
                            class="form-group"
                        >
                            <label for="select_qaofficer_proposal_status"
                                >Status</label
                            >
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_qaofficer_proposal_status"
                                    ref="select_qaofficer_proposal_status"
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
                    <div v-if="is_external" class="col-md-3">
                        <router-link
                            style="margin-top: 25px"
                            class="btn btn-primary pull-right"
                            :to="{ name: 'apply_proposal' }"
                            >New Application</router-link
                        >
                    </div>
                    <div class="col-md-3">
                        <label for="select_qaofficer_proposal_date_from"
                            >Lodged From</label
                        >
                        <div
                            ref="proposalDateFromPicker"
                            class="input-group date"
                        >
                            <input
                                id="select_qaofficer_proposal_date_from"
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
                        <label for="select_qaofficer_proposal_date_to"
                            >Lodged To</label
                        >
                        <div
                            ref="proposalDateToPicker"
                            class="input-group date"
                        >
                            <input
                                id="select_qaofficer_proposal_date_to"
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
    name: 'ProposalTableDash',
    components: {
        datatable,
    },
    props: {
        level: {
            type: String,
            required: true,
            validator: function (val) {
                let options = ['internal', 'referral', 'external'];
                return options.indexOf(val) != -1 ? true : false;
            },
        },
        url: {
            type: String,
            required: true,
        },
    },
    data() {
        let vm = this;
        return {
            pBody: 'pBody' + uuid(),
            datatable_id: 'proposal-datatable-' + uuid(),
            //Profile to check if user has access to process Proposal
            profile: {},
            // Filters for Proposals
            filterProposalStatus: 'All',
            filterProposalLodgedFrom: '',
            filterProposalLodgedTo: '',
            dateFormat: 'DD/MM/YYYY',
            internal_status: [
                { value: 'draft', name: 'Draft' },
                { value: 'with_assessor', name: 'With Assessor' },
                { value: 'on_hold', name: 'On Hold' },
                { value: 'with_qa_officer', name: 'With QA Officer' },
                { value: 'with_referral', name: 'With Referral' },
                {
                    value: 'with_assessor_requirements',
                    name: 'With Assessor (Requirements)',
                },
                { value: 'with_approver', name: 'With Approver' },
                { value: 'approved', name: 'Approved' },
                { value: 'declined', name: 'Declined' },
                { value: 'discarded', name: 'Discarded' },
            ],
            proposal_activityTitles: [],
            proposal_regions: [],
            proposal_status: [],
            proposal_headers: [
                'Number',
                'Submitter',
                'Applicant',
                'Status',
                'Lodged on',
                'Assigned Officer',
                'Action',
            ],
            proposal_options: {
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
                        data: 'id',
                        mRender: function (data, type, full) {
                            return full.lodgement_number;
                        },
                        name: 'lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'submitter',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            if (data) {
                                return `${data.first_name} ${data.last_name}`;
                            }
                            return '';
                        },
                        orderable: false,
                        searchable: false, //overridden by filterbackend
                        name: 'submitter__first_name, submitter__last_name, submitter__email',
                    },
                    {
                        data: 'applicant',
                        name: 'org_applicant__organisation__organisation_name, proxy_applicant__email, proxy_applicant__first_name, proxy_applicant__last_name',
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
                        data: 'lodgement_date',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data != '' && data != null
                                ? moment(data).format(vm.dateFormat)
                                : '';
                        },
                        searchable: false,
                        orderable: true,
                    },
                    {
                        data: 'assigned_officer',
                        name: 'assigned_officer__first_name, assigned_officer__last_name',
                        orderable: false,
                        searchable: false, //overridden by filterbackend
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.is_external) {
                                if (
                                    full.processing_status == 'With QA Officer'
                                ) {
                                    links += `<a href='/internal/proposal/${full.id}'>Process</a><br/>`;
                                } else {
                                    links += `<a href='/internal/proposal/${full.id}'>View</a><br/>`;
                                }
                            } else {
                                if (full.can_user_edit) {
                                    links += `<a href='/external/proposal/${full.id}'>Continue</a><br/>`;
                                    links += `<a href='#${full.id}' data-discard-proposal='${full.id}'>Discard</a><br/>`;
                                } else if (full.can_user_view) {
                                    links += `<a href='/external/proposal/${full.id}'>View</a><br/>`;
                                }
                            }
                            return links;
                        },
                        name: '',
                        searchable: false,
                        orderable: false,
                    },
                ],
                processing: true,
            },
            isLoading: false,
        };
    },
    computed: {
        is_external: function () {
            return this.level == 'external';
        },
        is_referral: function () {
            return this.level == 'referral';
        },
    },
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
        this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        $('a[data-bs-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
        this.$nextTick(() => {
            vm.initialiseSearch();
            vm.addEventListeners();
        });
    },
    methods: {
        fetchFilterLists: function () {
            let vm = this;
            vm.isLoading = true;

            helpers
                .fetchUrl(api_endpoints.filter_list)
                .then(
                    (response) => {
                        vm.proposal_status =
                            vm.level == 'internal'
                                ? vm.internal_status
                                : vm.external_status;
                    },
                    (error) => {
                        console.log(error);
                    }
                )
                .finally(() => {
                    vm.isLoading = false;
                });
        },

        discardProposal: function (proposal_id) {
            let vm = this;
            swal.fire({
                title: 'Discard Application',
                text: 'Are you sure you want to discard this application?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(api_endpoints.discard_proposal(proposal_id), {
                            method: 'DELETE',
                        })
                        .then(
                            () => {
                                swal.fire({
                                    title: 'Discarded',
                                    text: 'Your application has been discarded',
                                    icon: 'success',
                                });
                                vm.$refs.proposal_datatable.vmDataTable.ajax.reload();
                            },
                            (error) => {
                                console.log(error);
                            }
                        );
                    }
                },
                () => {}
            );
        },
        addEventListeners: function () {
            let vm = this;
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
                'select_qaofficer_proposal_status',
                'select_qaofficer_proposal_status_parent',
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

        fetchProfile: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.profile).then(
                (response) => {
                    vm.profile = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },

        check_assessor: function (proposal) {
            let vm = this;
            if (proposal.assigned_officer) {
                {
                    if (proposal.assigned_officer == vm.profile.full_name)
                        return true;
                    else return false;
                }
            } else {
                var assessor = proposal.allowed_assessors.filter(
                    function (elem) {
                        return (elem.id = vm.profile.id);
                    }
                );
                if (assessor.length > 0) return true;
                else return false;
            }
        },
    },
};
</script>
<style scoped>
.dt-buttons {
    float: right;
}
</style>
