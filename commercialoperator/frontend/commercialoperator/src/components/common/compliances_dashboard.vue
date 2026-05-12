<template id="proposal_dashboard">
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div class="row mb-1">
                    <div class="col-md-3">
                        <div
                            id="select_compliance_status_parent"
                            class="form-group"
                        >
                            <label for="select_compliance_status">Status</label>
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_compliance_status"
                                    ref="select_compliance_status"
                                    v-model="filterComplianceStatus"
                                    class="form-control"
                                >
                                    <option value="All">All</option>
                                    <option
                                        v-for="s in status"
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
                        <div
                            id="select_compliance_application_type_parent"
                            class="form-group"
                        >
                            <label for="select_compliance_application_type"
                                >Licence Type</label
                            >
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_compliance_application_type"
                                    ref="select_compliance_application_type"
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

                    <div class="col-md-3">
                        <label for="input_compliance_due_date_from"
                            >Due date From</label
                        >
                        <div
                            ref="complianceDateFromPicker"
                            class="input-group date"
                        >
                            <input
                                id="input_compliance_due_date_from"
                                v-model="filterComplianceDueFrom"
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
                        <label for="input_compliance_due_date_to"
                            >Due date To</label
                        >
                        <div
                            ref="complianceDateToPicker"
                            class="input-group date"
                        >
                            <input
                                id="input_compliance_due_date_to"
                                v-model="filterComplianceDueTo"
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
            is_payment_admin: false,
            datatable_id: 'proposal-datatable-' + uuid(),
            // Filters for Proposals
            filterApplicationType: 'All',
            filterProposalRegion: 'All',
            filterProposalActivity: 'All',
            filterComplianceStatus: 'All',
            filterComplianceDueFrom: '',
            filterComplianceDueTo: '',
            filterProposalSubmitter: 'All',
            dateFormat: 'DD/MM/YYYY',
            external_status: [
                { value: 'due', name: 'Due' },
                // { value: 'future', name: 'Future' },
                { value: 'with_assessor', name: 'Under Review' },
                { value: 'approved', name: 'Approved' },
            ],
            internal_status: [
                { value: 'due', name: 'Due' },
                { value: 'future', name: 'Future' },
                { value: 'with_assessor', name: 'With Assessor' },
                { value: 'approved', name: 'Approved' },
            ],
            status: [],
            application_types: [],
            proposal_submitters: [],
            proposal_headers: [
                'Number',
                'Licence',
                'Licence Type',
                'Holder',
                'Status',
                'Due Date',
                'Assigned To',
                'Event Name',
                'Action',
            ],
            proposal_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    {
                        responsivePriority: 2,
                        targets: 8, // Action column
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
                            vm.filterComplianceDueFrom != '' &&
                            vm.filterComplianceDueFrom != null
                                ? moment(vm.filterComplianceDueFrom).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.date_to =
                            vm.filterComplianceDueTo != '' &&
                            vm.filterComplianceDueTo != null
                                ? moment(vm.filterComplianceDueTo).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.datatable_filter_processing_status =
                            vm.filterComplianceStatus.toLowerCase();
                        d.datatable_filter_proposal__application_type__name =
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
                            return full.reference;
                        },
                        name: 'id, lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'approval_lodgement_number',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data;
                        },
                        name: 'approval__lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'application_type',
                        name: 'proposal__application_type__name',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'holder',
                        name: 'approval__org_applicant__organisation__organisation_name, approval__proxy_applicant__email, approval__proxy_applicant__first_name, approval__proxy_applicant__last_name',
                        orderable: false,
                        searchable: false,
                        mRender: function (data, type, full) {
                            return vm.level == 'external' ? full.holder : data;
                        },
                    },
                    {
                        data: 'processing_status',
                        mRender: function (data, type, full) {
                            return vm.level == 'external'
                                ? full.customer_status
                                : data;
                        },
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'due_date',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data != '' && data != null
                                ? moment(data).format(vm.dateFormat)
                                : '';
                        },
                        orderable: true,
                        searchable: false,
                    },
                    {
                        data: 'assigned_to',
                        name: 'assigned_to__first_name, assigned_to__last_name, assigned_to__email',
                        searchable: false,
                        orderable: false,
                    },
                    {
                        data: 'compliance_licence_name',
                        searchable: false,
                        orderable: false,
                        name: '',
                    },
                    {
                        data: 'id',
                        searchable: false,
                        orderable: false,
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.is_external) {
                                if (full.can_process) {
                                    links += `<a href='/internal/compliance/${full.id}'>Process</a><br/>`;
                                } else {
                                    links += `<a href='/internal/compliance/${full.id}'>View</a><br/>`;
                                }
                                if (full.fee_paid) {
                                    if (vm.is_payment_admin) {
                                        links += `<a href='/cols/payments/invoice-payment-view/${full.fee_invoice_reference}' target='_blank'>View Payment</a><br/>`;
                                    }
                                }
                            } else {
                                if (full.can_user_view) {
                                    links += `<a href='/external/compliance/${full.id}'>View</a><br/>`;
                                } else {
                                    links += `<a href='/external/compliance/${full.id}'>Submit</a><br/>`;
                                }
                            }

                            if (full.fee_invoice_reference) {
                                links += `<a href='/cols/payments/invoice-compliance-pdf/${full.fee_invoice_reference}' target='_blank'><i style='color:red;' class='fas fa-file-pdf'>&nbsp</i>#${full.fee_invoice_reference}</a><br/>`;
                            }

                            return links;
                        },
                        name: '',
                    },
                    {
                        data: 'reference',
                        visible: false,
                        name: 'lodgement_number',
                    },
                ],
                processing: true,
            },
            isLoading: false,
        };
    },
    computed: {
        is_external: function () {
            return this.level === 'external';
        },
        is_internal: function () {
            return this.level === 'internal';
        },
    },
    watch: {
        filterComplianceStatus: function () {
            let vm = this;
            if (vm.filterComplianceStatus != 'All') {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(4)
                    .search(vm.filterComplianceStatus)
                    .draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(4)
                    .search('')
                    .draw();
            }
        },
        filterProposalSubmitter: function () {
            this.$refs.proposal_datatable.vmDataTable.draw();
        },
        filterComplianceDueFrom: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterComplianceDueTo: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterApplicationType: function () {
            let vm = this;
            if (vm.filterApplicationType != 'All') {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(2)
                    .search(vm.filterApplicationType)
                    .draw();
            } else {
                vm.$refs.proposal_datatable.vmDataTable
                    .columns(2)
                    .search('')
                    .draw();
            }
        },
    },
    mounted: function () {
        let vm = this;
        this.fetchProfile();
        vm.fetchFilterLists();
        $('a[data-bs-toggle="collapse"]').on('click', function () {
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
        if (vm.is_external) {
            var column = vm.$refs.proposal_datatable.vmDataTable.columns(6); //Hide 'Assigned To column for external'
            column.visible(false);
        }
    },
    methods: {
        fetchFilterLists: function () {
            let vm = this;
            vm.isLoading = true;

            vm.status =
                vm.level == 'external'
                    ? vm.external_status
                    : vm.internal_status;

            helpers
                .fetchUrl(api_endpoints.filter_list_compliances)
                .then(
                    (response) => {
                        vm.application_types = response.application_types;
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
            helpers.initialiseSelect2.bind(this)(
                'select_compliance_status',
                'select_compliance_status_parent',
                'filterComplianceStatus',
                'Select Compliance Status',
                false
            );
            helpers.initialiseSelect2.bind(this)(
                'select_compliance_application_type',
                'select_compliance_application_type_parent',
                'filterApplicationType',
                'Select Application Type',
                false
            );
        },
        initialiseSearch: function () {
            this.dateSearch();
        },
        submitterSearch: function () {
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function (settings, data, dataIndex, original) {
                    let filtered_submitter = vm.filterProposalSubmitter;
                    if (filtered_submitter == 'All') {
                        return true;
                    }
                    return filtered_submitter == original.submitter.email;
                }
            );
        },
        dateSearch: function () {
            let vm = this;
            vm.$refs.proposal_datatable.table.dataTableExt.afnFiltering.push(
                function (settings, data, dataIndex, original) {
                    let from = vm.filterComplianceDueFrom;
                    let to = vm.filterComplianceDueTo;
                    let val = original.due_date;

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
                () => {}
            );
        },
    },
};
</script>
<style scoped></style>
