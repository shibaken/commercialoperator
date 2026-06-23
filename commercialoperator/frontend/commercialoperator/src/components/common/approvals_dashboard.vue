<template id="proposal_dashboard">
    <div class="row">
        <div class="col-sm-12">
            <div class="card">
                <div class="row">
                    <div class="col-md-3">
                        <div
                            id="select_approval_proposal_status_parent"
                            class="form-group"
                        >
                            <label for="select_approval_proposal_status"
                                >Status</label
                            >
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_approval_proposal_status"
                                    ref="select_approval_proposal_status"
                                    v-model="filterProposalStatus"
                                    class="form-control"
                                >
                                    <option value="All">All</option>
                                    <option
                                        v-for="s in approval_status"
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
                        <div
                            id="select_approval_licence_type_parent"
                            class="form-group"
                        >
                            <label for="select_approval_licence_type"
                                >Licence Type</label
                            >
                            <div v-show="isLoading">
                                <select class="form-control">
                                    <option value="">Loading...</option>
                                </select>
                            </div>
                            <div v-show="!isLoading">
                                <select
                                    id="select_approval_licence_type"
                                    ref="select_approval_licence_type"
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
                <div class="row">
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="input_start_from_date"
                                >Start From</label
                            >
                            <div
                                ref="startDateFromPicker"
                                class="input-group date"
                            >
                                <input
                                    id="input_start_from_date"
                                    v-model="filterStartFrom"
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
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="input_start_to_date">Start To</label>
                            <div
                                ref="startDateToPicker"
                                class="input-group date"
                            >
                                <input
                                    id="input_start_to_date"
                                    v-model="filterStartTo"
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
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="input_expiry_from_date"
                                >Expiry From</label
                            >
                            <div
                                ref="expiryDateFromPicker"
                                class="input-group date"
                            >
                                <input
                                    id="input_expiry_from_date"
                                    v-model="filterExpiryFrom"
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
                    <div class="col-md-3">
                        <div class="form-group">
                            <label for="input_expiry_to_date">Expiry To</label>
                            <div
                                ref="expiryDateToPicker"
                                class="input-group date"
                            >
                                <input
                                    id="input_expiry_to_date"
                                    v-model="filterExpiryTo"
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

                    <div v-if="is_internal" class="col-md-3 ms-md-auto">
                        <div class="form-group">
                            <label />
                            <div>
                                <button
                                    class="btn btn-primary top-buffer-s float-end"
                                    :disabled="disabled"
                                    @click.prevent="createEClassLicence()"
                                >
                                    New E Class licence
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <div class="col-lg-12" style="margin-top: 25px">
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
        <ApprovalExtend
            ref="approval_extend"
            @refreshFromResponse="refreshFromResponse"
        ></ApprovalExtend>
        <ApprovalCancellation
            ref="approval_cancellation"
            @refreshFromResponse="refreshFromResponse"
        ></ApprovalCancellation>
        <ApprovalSuspension
            ref="approval_suspension"
            @refreshFromResponse="refreshFromResponse"
        ></ApprovalSuspension>
        <ApprovalSurrender
            ref="approval_surrender"
            @refreshFromResponse="refreshFromResponse"
        ></ApprovalSurrender>
        <EClassLicence ref="eclass_licence"></EClassLicence>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue';
import ApprovalExtend from '../internal/approvals/approval_extend.vue';
import ApprovalCancellation from '../internal/approvals/approval_cancellation.vue';
import ApprovalSuspension from '../internal/approvals/approval_suspension.vue';
import ApprovalSurrender from '../internal/approvals/approval_surrender.vue';
import EClassLicence from '../internal/approvals/approval_eclass.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import _ from 'lodash';
import $ from 'jquery'
export default {
    name: 'ProposalTableDash',
    components: {
        datatable,
        ApprovalExtend,
        ApprovalCancellation,
        ApprovalSuspension,
        ApprovalSurrender,
        EClassLicence,
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
        disabled: {
            type: Boolean,
            default: false,
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
            filterApplicationType: 'All',
            filterProposalStatus: 'All',
            filterStartFrom: '',
            filterStartTo: '',
            filterExpiryFrom: '',
            filterExpiryTo: '',
            dateFormat: 'DD/MM/YYYY',
            application_types: [],
            approval_status: [],
            proposal_headers: [
                'Number',
                'Application',
                'Licence Type',
                'Holder',
                'Status',
                'Start Date',
                'Expiry Date',
                'Licence',
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
                        targets: 9, // Action column
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
                        d.start_date_from =
                            vm.filterStartFrom != '' &&
                            vm.filterStartFrom != null
                                ? moment(vm.filterStartFrom).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.start_date_to =
                            vm.filterStartTo != '' && vm.filterStartTo != null
                                ? moment(vm.filterStartTo).format('YYYY-MM-DD')
                                : '';
                        d.expiry_date_from =
                            vm.filterExpiryFrom != '' &&
                            vm.filterExpiryFrom != null
                                ? moment(vm.filterExpiryFrom).format(
                                      'YYYY-MM-DD'
                                  )
                                : '';
                        d.expiry_date_to =
                            vm.filterExpiryTo != '' && vm.filterExpiryTo != null
                                ? moment(vm.filterExpiryTo).format('YYYY-MM-DD')
                                : '';
                        d.datatable_filter_status =
                            vm.filterProposalStatus.toLowerCase();
                        d.datatable_filter_current_proposal__application_type__name =
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
                        render: function (data, type, full) {
                            if (!vm.is_external) {
                                var result = '';
                                var popTemplate = '';
                                var message = '';
                                let icon = '';
                                icon =
                                    "<i class='fas fa-exclamation-triangle' style='color:red'></i>";
                                result = full.reserved_licence
                                    ? '<span>' +
                                      full.lodgement_number +
                                      ' (R) </span>'
                                    : '<span>' +
                                      full.lodgement_number +
                                      '</span>';
                                if (full.can_reissue) {
                                    if (!full.can_action) {
                                        if (full.set_to_cancel) {
                                            message =
                                                'This Licence is marked for cancellation to future date';
                                        }
                                        if (full.set_to_suspend) {
                                            message =
                                                'This Licence is marked for suspension to future date';
                                        }
                                        if (full.set_to_surrender) {
                                            message =
                                                'This Licence is marked for surrendering to future date';
                                        }
                                        const title = full.lodgement_number;
                                        popTemplate =
                                            helpers.initialisePopoverTemplate(
                                                title,
                                                ''
                                            );
                                        result += popTemplate({
                                            text: message,
                                            icon: icon,
                                        });
                                    }
                                }
                                return result;
                            } else {
                                return full.lodgement_number;
                            }
                        },
                        name: 'lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'linked_applications',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            let applications = '';
                            _.forEach(data, function (item) {
                                applications += item + '<br>';
                            });
                            return applications;
                        },
                        name: 'current_proposal__lodgement_number',
                        orderable: true,
                        searchable: true,
                    },
                    {
                        data: 'application_type',
                        name: 'current_proposal__application_type__name',
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'applicant',
                        name: 'org_applicant__organisation__organisation_name, proxy_applicant__first_name, proxy_applicant__last_name, proxy_applicant__email',
                        // Note: Set to non-searchable because for now we can't search in ledger fields (emailuser, organisation)
                        orderable: false,
                        searchable: false,
                    },
                    { 
                        data: 'status', 
                        orderable: false,
                        searchable: false,
                    },
                    {
                        data: 'start_date',
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
                        data: 'expiry_date',
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
                        data: 'licence_document',
                        mRender: function (data, type, full) {
                            var result = '';
                            var popTemplate = '';
                            if (!full.migrated) {
                                result = `<a href="${data}" target="_blank"><i style="color:red" class="fas fa-file-pdf"></i></a>`;
                            } else if (full.migrated) {
                                var icon =
                                    "<i class='fas fa-file-pdf' style='color:red'></i>";
                                var message = 'This is a migrated licence';

                                const title = `License ${full.lodgement_number}`;
                                popTemplate = helpers.initialisePopoverTemplate(
                                    title,
                                    ''
                                );

                                result += popTemplate({
                                    text: message,
                                    icon: icon,
                                });
                            }
                            if (full.requirement_docs) {
                                _.forEach(
                                    full.requirement_docs,
                                    function (item) {
                                        result += `<br><a href="${item[1]}" target="_blank">${item[0]}</a>`;
                                    }
                                );
                            }
                            return result;
                        },
                        name: 'licence_document__name',
                        searchable: false,
                        orderable: false,
                    },
                    {
                        data: 'licence_name',
                        searchable: false,
                        orderable: false,
                        name: '',
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (!vm.is_external) {
                                if (full.is_approver) {
                                    if (!full.is_lawful_authority) {
                                        if (full.can_reissue) {
                                            links += `<a href='#${full.id}' data-reissue-approval='${full.current_proposal}'>Reissue</a><br/>`;
                                        }
                                    }
                                }
                                if (full.is_assessor) {
                                    if (full.is_lawful_authority) {
                                        if (full.can_reissue_lawful_authority) {
                                            links += `<a href='#${full.id}' data-reissue-approval='${full.current_proposal}'>Reissue</a><br/>`;
                                        }
                                    }
                                    if (
                                        full.application_type == 'E Class' &&
                                        (full.status == 'Current' ||
                                            full.status == 'Suspended')
                                    ) {
                                        if (full.can_extend) {
                                            links += `<a href='#${full.id}' data-extend-approval='${full.id}'>Extend</a><br/>`;
                                        } else {
                                            links += `<a class='disabled' title='Licence has already been extended' style="color: grey;text-decoration: none;">Extend</a><br/>`;
                                        }
                                    }
                                    if (full.can_reissue && full.can_action) {
                                        if (full.is_lawful_authority) {
                                            if (
                                                full.can_reissue_lawful_authority
                                            ) {
                                                links += `<a href='#${full.id}' data-cancel-approval='${full.id}'>Cancel</a><br/>`;
                                                links += `<a href='#${full.id}' data-surrender-approval='${full.id}'>Surrender</a><br/>`;
                                            }
                                        } else {
                                            links += `<a href='#${full.id}' data-cancel-approval='${full.id}'>Cancel</a><br/>`;
                                            links += `<a href='#${full.id}' data-surrender-approval='${full.id}'>Surrender</a><br/>`;
                                        }
                                    }
                                    if (
                                        full.status == 'Current' &&
                                        full.can_action
                                    ) {
                                        if (full.is_lawful_authority) {
                                            if (
                                                full.is_lawful_authority_finalised
                                            ) {
                                                links += `<a href='#${full.id}' data-suspend-approval='${full.id}'>Suspend</a><br/>`;
                                            }
                                        } else {
                                            links += `<a href='#${full.id}' data-suspend-approval='${full.id}'>Suspend</a><br/>`;
                                        }
                                    }
                                    if (full.can_reinstate) {
                                        links += `<a href='#${full.id}' data-reinstate-approval='${full.id}'>Reinstate</a><br/>`;
                                    }
                                    links += `<a href='/internal/approval/${full.id}'>View</a><br/>`;
                                } else {
                                    links += `<a href='/internal/approval/${full.id}'>View</a><br/>`;
                                }
                                if (
                                    full.renewal_document &&
                                    full.renewal_sent &&
                                    full.status != 'Expired'
                                ) {
                                    links += `<a href='${full.renewal_document}' target='_blank'>Renewal Notice</a><br/>`;
                                }
                            } else {
                                //External Dashboard actions.
                                if (full.can_reissue) {
                                    links += `<a href='/external/approval/${full.id}'>View</a><br/>`;
                                    if (full.can_action) {
                                        if (full.is_lawful_authority) {
                                            if (
                                                full.can_reissue_lawful_authority
                                            ) {
                                                links += `<a href='#${full.id}' data-surrender-approval='${full.id}'>Surrender</a><br/>`;
                                            }
                                        } else {
                                            links += `<a href='#${full.id}' data-surrender-approval='${full.id}'>Surrender</a><br/>`;
                                        }

                                        if (full.can_amend) {
                                            links += `<a href='#${full.id}' data-amend-approval='${full.current_proposal}'>Amend</a><br/>`;
                                        }
                                    }
                                    if (
                                        full.renewal_document &&
                                        full.renewal_sent &&
                                        full.can_renew
                                    ) {
                                        links += `<a href='#${full.id}' data-renew-approval='${full.current_proposal}'>Renew</a><br/>`;
                                    }
                                } else {
                                    links += `<a href='/external/approval/${full.id}'>View</a><br/>`;
                                }
                            }
                            return links;
                        },
                        searchable: false,
                        orderable: false,
                        name: '',
                    },
                    { data: 'migrated', visible: false },
                ],
                processing: true,
            },
            isLoading: false,
        };
    },
    computed: {
        status: function () {
            return [];
        },
        is_external: function () {
            return this.level == 'external';
        },
        is_internal: function () {
            return this.level == 'internal';
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
        filterStartFrom: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterStartTo: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterExpiryFrom: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload(
                helpers.enablePopovers,
                false
            );
        },
        filterExpiryTo: function () {
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
        this.fetchFilterLists();
        this.fetchProfile();
        let vm = this;
        // $('a[data-bs-toggle="collapse"]').on('click', function () {
        //     var chev = $(this).children()[0];
        //     window.setTimeout(function () {
        //         $(chev).toggleClass(
        //             'fa-chevron-down fa-chevron-up'
        //         );
        //     }, 100);
        // });
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
            // const table = this.$refs.proposal_datatable.vmDataTable;
            // helpers.addEllipsisEventListeners(table);
            // helpers.enablePopovers();
        });
    },
    methods: {
        createEClassLicence: function () {
            this.$refs.eclass_licence.isModalOpen = true;
        },

        fetchFilterLists: function () {
            let vm = this;
            vm.isLoading = true;

            helpers
                .fetchUrl(api_endpoints.filter_list_approvals)
                .then(
                    (response) => {
                        vm.approval_status = response.approval_status_choices;
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
            let vm = this;
            // End Proposal Date Filters
            // Internal Reissue listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-reissue-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-reissue-approval');
                    vm.reissueApproval(id);
                }
            );

            // Internal Extend listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-extend-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-extend-approval');
                    vm.extendApproval(id);
                }
            );

            //Internal Cancel listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-cancel-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-cancel-approval');
                    vm.cancelApproval(id);
                }
            );

            //Internal Suspend listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-suspend-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-suspend-approval');
                    vm.suspendApproval(id);
                }
            );

            // Internal Reinstate listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-reinstate-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-reinstate-approval');
                    vm.reinstateApproval(id);
                }
            );

            //Internal/ External Surrender listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-surrender-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-surrender-approval');
                    vm.surrenderApproval(id);
                }
            );

            // External renewal listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-renew-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-renew-approval');
                    vm.renewApproval(id);
                }
            );

            // External amend listener
            vm.$refs.proposal_datatable.vmDataTable.on(
                'click',
                'a[data-amend-approval]',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-amend-approval');
                    vm.amendApproval(id);
                }
            );

            vm.$refs.proposal_datatable.vmDataTable.on('draw.dt', function () {
                var popoverTriggerList = [].slice.call(
                    document.querySelectorAll('a[data-bs-toggle="popover"]')
                );
                popoverTriggerList.map(function (popoverTriggerEl) {
                    let popover = new bootstrap.Popover(popoverTriggerEl);
                    // Listeners to hide popovers on 'x'-click
                    vm.$refs.proposal_datatable.vmDataTable.on(
                        'click',
                        'a[data-bs-toggle="popover"]',
                        function (e) {
                            e.preventDefault();
                            let attributes = e.currentTarget.attributes;
                            let popoverId;
                            if (attributes && attributes.length > 0) {
                                popoverId = attributes['10'].value;
                            }

                            if (popover.tip && popover.tip.id == popoverId) {
                                // Ideally the listener would only be shown on popover show, but that does work okay for now
                                $(`#${popoverId}`)
                                    .find('.popover-close')
                                    .off('click')
                                    .on('click', () => popover.hide());
                            }
                        }
                    );

                    return popover;
                });
            });

            helpers.initialiseSelect2.bind(this)(
                'select_approval_proposal_status',
                'select_approval_proposal_status_parent',
                'filterProposalStatus',
                'Select Status',
                false
            );
            helpers.initialiseSelect2.bind(this)(
                'select_approval_licence_type',
                'select_approval_licence_type_parent',
                'filterApplicationType',
                'Select Application Type',
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
                    let from = vm.filterExpiryFrom;
                    let to = vm.filterExpiryTo;
                    let val = original.expiry_date;

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

            var assessor = proposal.allowed_assessors.filter(function (elem) {
                return (elem.id = vm.profile.id);
            });
            if (assessor.length > 0) return true;
            else return false;
        },

        reissueApproval: function (proposal_id) {
            let vm = this;
            let status = 'with_approver';
            let data = { status: status };
            swal.fire({
                title: 'Reissue Licence',
                text: 'Are you sure you want to reissue this licence?',
                icon: 'warning',
                confirmButtonText: 'Reissue licence',
            }).then(
                () => {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.proposals,
                                proposal_id + '/reissue_approval'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(data),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                vm.$router.push({
                                    name: 'internal-proposal',
                                    params: { proposal_id: proposal_id },
                                });
                            },
                            (error) => {
                                console.log(error);
                                swal.fire({
                                    title: 'Reissue Licence',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                },
                () => {}
            );
        },

        _extendApproval: function (approval_id) {
            let vm = this;
            let status = 'with_approver';
            let data = { status: status };
            swal.fire({
                title: 'Renew Licence',
                text: "<input type='email' class='form-control' name='email' id='email'/>",
                icon: 'input',
                showCancelButton: true,
                confirmButtonText: 'Extend licence',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.approvals,
                                approval_id + '/approval_extend'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(data),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        ).then(
                            () => {
                                vm.$router.push({
                                    name: 'internal-proposal',
                                    params: { approval_id: approval_id },
                                });
                            },
                            (error) => {
                                console.log(error);
                                swal.fire({
                                    title: 'Extend Licence',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                    }
                },
            );
        },

        extendApproval: function (approval_id) {
            this.$refs.approval_extend.approval_id = approval_id;
            this.$refs.approval_extend.isModalOpen = true;
        },

        reinstateApproval: function (approval_id) {
            let vm = this;
            swal.fire({
                title: 'Reinstate Licence',
                text: 'Are you sure you want to reinstate this licence?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Reinstate licence',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.approvals,
                                approval_id + '/approval_reinstate'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify({}),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                swal.fire({
                                    title: 'Reinstate',
                                    text: 'Your licence has been reinstated',
                                    icon: 'success',
                                });
                                vm.$refs.proposal_datatable.vmDataTable.ajax.reload();
                            },
                            (error) => {
                                console.log(error);
                                swal.fire({
                                    title: 'Reinstate Licence',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                    }
                },
                () => {}
            );
        },

        renewApproval: function (proposal_id) {
            let vm = this;
            swal.fire({
                title: 'Renew Licence',
                text: 'Are you sure you want to renew this licence?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Renew licence',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        swal.fire({
                            title: 'Loading...',
                            allowOutsideClick: false,
                            allowEscapeKey: false,
                            didOpen: () => {
                                swal.showLoading();
                            },
                            customClass: {
                                container: 'swal2-popover',
                            },
                        });
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.proposals,
                                proposal_id + '/renew_approval'
                            )
                        )
                        .then(
                            (response) => {
                                swal.hideLoading();
                                swal.close();
                                let proposal = {};
                                proposal = response;
                                vm.$router.push({
                                    name: 'draft_proposal',
                                    params: { proposal_id: proposal.id },
                                });
                            },
                            (error) => {
                                console.log(error);
                                swal.fire({
                                    title: 'Renew Licence',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                    }
                },
                () => {}
            );
        },

        amendApproval: function (proposal_id) {
            let vm = this;
            swal.fire({
                title: 'Amend Licence',
                text: 'Are you sure you want to amend this licence?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Amend licence',
            }).then(
                (result) => {
                    if (!result || !result.isConfirmed) {
                        return;
                    }
                    swal.fire({
                        title: 'Loading...',
                        icon: 'info',
                        allowOutsideClick: false,
                        allowEscapeKey: false,
                        showConfirmButton: false,
                        didOpen: () => {
                            swal.showLoading();
                        },
                        customClass: {
                            container: 'swal2-popover',
                        },
                    });
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.proposals,
                                proposal_id + '/amend_approval'
                            )
                        )
                        .then(
                            (response) => {
                                swal.hideLoading();
                                swal.close();
                                let proposal = {};
                                proposal = response;
                                vm.$router.push({
                                    name: 'draft_proposal',
                                    params: { proposal_id: proposal.id },
                                });
                            },
                            (error) => {
                                console.log(error);
                                swal.fire({
                                    title: 'Amend Licence',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                },
                () => {}
            );
        },

        cancelApproval: function (approval_id) {
            this.$refs.approval_cancellation.approval_id = approval_id;
            this.$refs.approval_cancellation.isModalOpen = true;
        },

        suspendApproval: function (approval_id) {
            this.$refs.approval_suspension.approval = {};
            this.$refs.approval_suspension.approval_id = approval_id;
            this.$refs.approval_suspension.isModalOpen = true;
        },

        surrenderApproval: function (approval_id) {
            this.$refs.approval_surrender.approval_id = approval_id;
            this.$refs.approval_surrender.isModalOpen = true;
        },

        refreshFromResponse: function () {
            this.$refs.proposal_datatable.vmDataTable.ajax.reload();
        },
    },
};
</script>

<style scoped>
.swal2-popover {
    z-index: 1090 !important;
}
</style>
