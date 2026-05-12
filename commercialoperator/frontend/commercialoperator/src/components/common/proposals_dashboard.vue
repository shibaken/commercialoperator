<template id="proposal_dashboard">
    <div class="row">
        <div class="col-sm-12">
            <div class="row mb-1">
                <div class="col-md-3">
                    <div
                        id="select_proposal_status_parent"
                        class="form-group"
                    >
                        <label for="select_proposal_status">Status</label>
                        <div v-show="isLoading">
                            <select class="form-control">
                                <option value="">Loading...</option>
                            </select>
                        </div>
                        <div v-show="!isLoading">
                            <select
                                id="select_proposal_status"
                                ref="select_proposal_status"
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
                <div class="col-md-3 mb-3">
                    <label for="input_lodged_from_date">Lodged From</label>
                    <div
                        ref="proposalDateFromPicker"
                        class="input-group date"
                    >
                        <input
                            id="input_lodged_from_date"
                            v-model="filterProposalLodgedFrom"
                            type="date"
                            class="form-control"
                            max="2999-12-31"
                            placeholder="DD/MM/YYYY"
                        />
                        <span class="input-group-addon">
                            <i class="fas fa-calendar-days"></i>
                        </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <label for="input_lodged_to_date">Lodged To</label>
                    <div
                        ref="proposalDateToPicker"
                        class="input-group date"
                    >
                        <input
                            id="input_lodged_to_date"
                            v-model="filterProposalLodgedTo"
                            type="date"
                            class="form-control"
                            max="2999-12-31"
                            placeholder="DD/MM/YYYY"
                        />
                        <span class="input-group-addon">
                            <i class="fas fa-calendar-days"></i>
                        </span>
                    </div>
                </div>
                <div class="col-md-3">
                    <div
                        id="select_proposal_application_type_parent"
                        class="form-group"
                    >
                        <label for="select_proposal_application_type"
                            >Licence Type</label
                        >
                        <div v-show="isLoading">
                            <select class="form-control">
                                <option value="">Loading...</option>
                            </select>
                        </div>
                        <div v-show="!isLoading">
                            <select
                                id="select_proposal_application_type"
                                ref="select_proposal_application_type"
                                v-model="filterApplicationType"
                                class="form-control"
                            >
                                <option value="All">All</option>
                                <option
                                    v-for="s in application_types"
                                    :key="s"
                                    :value="s"
                                >
                                    {{ s }}
                                </option>
                            </select>
                        </div>
                    </div>
                </div>
            </div>          
            
            <div class="row mb-3 justify-content-end">
                <div
                    v-if="is_external"
                    class="col-md-3"
                >
                    <div class="form-group mt-auto mb-0 align-self-end">
                        <router-link
                            type="button"
                            class="btn btn-primary float-end"
                            :to="{ name: 'apply_proposal' }"
                            >New Application</router-link
                        >
                    </div>
                </div>  
            </div>
            
            <div class="row">
                <div class="col-lg-12">
                    <datatable
                        v-if="level == 'external'"
                        :id="datatable_id"
                        ref="proposal_datatable"
                        :dt-options="proposal_ex_options"
                        :dt-headers="proposal_ex_headers"
                    />
                    <datatable
                        v-else
                        :id="datatable_id"
                        ref="proposal_datatable"
                        :dt-options="proposal_options"
                        :dt-headers="proposal_headers"
                    />
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
            is_payment_admin: false,
            // Filters for Proposals
            filterApplicationType: 'All',
            filterProposalStatus: 'All',
            filterProposalLodgedFrom: '',
            filterProposalLodgedTo: '',
            dateFormat: 'DD/MM/YYYY',
            application_types: [],
            external_status: [
                { value: 'draft', name: 'Draft' },
                { value: 'with_assessor', name: 'Under Review' },
                { value: 'approved', name: 'Approved' },
                { value: 'declined', name: 'Declined' },
                { value: 'discarded', name: 'Discarded' },
                { value: 'awaiting_payment', name: 'Awaiting Payment' },
            ],
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
                { value: 'awaiting_payment', name: 'Awaiting Payment' },
            ],
            proposal_status: [],
            proposal_ex_headers: [
                'Number',
                'Licence Type',
                'Submitter',
                'Applicant',
                'Status',
                'Lodged on',
                'Event Name',
                'Action',
            ],
            proposal_ex_options: {
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
                searching: true,
                responsive: true,
                serverSide: true,
                pageLength:10,
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
                        d.datatable_filter_application_type__name =
                            vm.filterApplicationType;
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
                        name: 'id, lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'application_type',
                        name: 'application_type__name',
                        orderable: false,
                        searchable: false,
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
                        name: 'submitter__first_name, submitter__last_name, submitter__email',
                        orderable: false,
                        searchable: false, //overridden
                    },
                    {
                        data: 'applicant',
                        name: 'org_applicant__organisation__organisation_name, proxy_applicant__email, proxy_applicant__first_name, proxy_applicant__last_name',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'customer_status',
                        name: 'customer_status',
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
                        data: 'event_name',
                        searchable: false,
                        orderable: false,
                        name: 'event_name',
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.is_external) {
                                if (full.assessor_process) {
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
                                if (
                                    full.customer_status ==
                                        'Awaiting Payment' &&
                                    !full.fee_paid
                                ) {
                                    links += `<a href='/filming_fee/${full.id}'>Make Payment</a><br/>`;
                                    links += `<a href='/cols/payments/awaiting-payment-pdf/${full.id}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>Pending Invoice</a><br/>`;
                                }
                            }
                            if (
                                full.fee_invoice_reference &&
                                full.proposal_type != 'Amendment'
                            ) {
                                if (full.application_type == 'Filming') {
                                    links += `<a href='/cols/payments/invoice-filmingfee-pdf/${full.fee_invoice_reference}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>#${full.fee_invoice_reference}</a><br/>`;
                                } else {
                                    links += `<a href='/cols/payments/invoice-pdf/${full.fee_invoice_reference}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>#${full.fee_invoice_reference}</a><br/>`;
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
            proposal_headers: [
                'Number',
                'Licence Type',
                'Submitter',
                'Applicant',
                'Status',
                'Lodged on',
                'Assigned Officer',
                'Event Name',
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
                searching: true,
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
                        d.datatable_filter_application_type__name =
                            vm.filterApplicationType;
                        return d
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
                        data: 'application_type',
                        name: 'application_type__name',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'submitter',
                        mRender: function (data, type, full) {
                            if (data && data.full_name) {
                                return `${data.full_name}`;
                            }
                            return '';
                        },
                        name: 'submitter__first_name, submitter__last_name, submitter__email',
                        orderable: false,
                        searchable: false, //override in filter backend
                    },
                    {
                        data: 'applicant',
                        name: 'org_applicant__organisation__organisation_name',
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
                        searchable: false, // handles by filter_queryset override method - class ProposalFilterBackend
                        orderable: true,
                    },
                    {
                        data: 'assigned_officer',
                        name: 'assigned_officer__first_name, assigned_officer__last_name',
                        orderable: false,
                        searchable: false, //override in filter backend
                    },
                    {
                        data: 'event_name',
                        orderable: false,
                        searchable: false,
                        name: 'event_name',
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.is_external) {
                                if (full.assessor_process) {
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

                            if (
                                !full.fee_paid &&
                                full.processing_status == 'Awaiting Payment'
                            ) {
                                if (vm.is_payment_admin) {
                                    links += `<a href='/filming_fee/${full.id}'>Record Payment</a><br/>`;
                                }
                                links += `<a href='/cols/payments/awaiting-payment-pdf/${full.id}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>Pending Invoice</a><br/>`;
                            }

                            if (
                                full.fee_invoice_reference &&
                                full.proposal_type != 'Amendment'
                            ) {
                                if (vm.is_payment_admin) {
                                    links += `<a href='/cols/payments/invoice-payment-view/${full.fee_invoice_reference}' target='_blank'>View Payment</a><br/>`;
                                }

                                if (full.application_type == 'Filming') {
                                    links += `<a href='/cols/payments/invoice-filmingfee-pdf/${full.fee_invoice_reference}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>#${full.fee_invoice_reference}</a><br/>`;
                                } else {
                                    links += `<a href='/cols/payments/invoice-pdf/${full.fee_invoice_reference}' target='_blank'><i style='color:red;' class='fa fa-file-pdf'>&nbsp</i>#${full.fee_invoice_reference}</a><br/>`;
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
                    .columns(4)
                    .search(vm.filterProposalStatus)
                    .draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(4)
                    .search('')
                    .draw();
            }
        },
        filterApplicationType: function () {
            let vm = this;
            if (vm.filterApplicationType != 'All') {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(1)
                    .search(vm.filterApplicationType)
                    .draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(1)
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
        $('a[data-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
        this.$nextTick(() => {
            this.dateSearch();
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
                        vm.application_types = response.application_types;
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
                text: 'Are you sure you want to discard this proposal?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Discard Application',
                confirmButtonColor: '#d9534f',
            }).then(
                (result) => {
                    if (!result.isConfirmed) {
                        return;
                    }
                    helpers
                        .fetchUrl(api_endpoints.discard_proposal(proposal_id), {
                            method: 'DELETE',
                        })
                        .then(
                            () => {
                                swal.fire({
                                    title: 'Discarded',
                                    text: 'Your proposal has been discarded',
                                    icon: 'success',
                                });
                                vm.$refs.proposal_datatable.vmDataTable.ajax.reload();
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
                'select_proposal_status',
                'select_proposal_status_parent',
                'filterProposalStatus',
                'Select Status',
                false
            );
            helpers.initialiseSelect2.bind(this)(
                'select_proposal_application_type',
                'select_proposal_application_type_parent',
                'filterApplicationType',
                'Select Application Type',
                false
            );
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
                    vm.is_payment_admin = response.is_payment_admin;
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
