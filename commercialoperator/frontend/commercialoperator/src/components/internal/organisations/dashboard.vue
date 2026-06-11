<template>
    <div id="internalOrgAccessDash" class="container">
        <div class="row">
            <div class="col-sm-12">
                <FormSection
                    :form-collapse="false"
                    label="Organisation Access Requests"
                    index="organisation_access_requests"
                >
                    <div class="card">
                        <div class="row mb-1">
                            <div class="col-md-3">
                                <div
                                    id="select_organisation_access_role_parent"
                                    class="form-group"
                                >
                                    <label for="select_organisation_access_role"
                                        >Role</label
                                    >
                                    <div v-show="isLoading">
                                        <select class="form-control">
                                            <option value="">Loading...</option>
                                        </select>
                                    </div>
                                    <div v-show="!isLoading">
                                        <select
                                            id="select_organisation_access_role"
                                            ref="select_organisation_access_role"
                                            v-model="filterRole"
                                            class="form-control"
                                        >
                                            <option value="All">All</option>
                                            <option
                                                v-for="r in roleChoices"
                                                :key="r"
                                                :value="r"
                                            >
                                                {{ r }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-3">
                                <div
                                    id="select_organisation_access_status_parent"
                                    class="form-group"
                                >
                                    <label
                                        for="select_organisation_access_status"
                                        >Status</label
                                    >
                                    <div v-show="isLoading">
                                        <select class="form-control">
                                            <option value="">Loading...</option>
                                        </select>
                                    </div>
                                    <div v-show="!isLoading">
                                        <select
                                            id="select_organisation_access_status"
                                            ref="select_organisation_access_status"
                                            v-model="filterStatus"
                                            class="form-control"
                                        >
                                            <option value="All">All</option>
                                            <option
                                                v-for="s in statusChoices"
                                                :key="s.search_term"
                                                :value="s.search_term"
                                            >
                                                {{ s.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-12">
                                <datatable
                                    id="org-access-table"
                                    ref="org_access_table"
                                    :dt-options="dtOptions"
                                    :dt-headers="dtHeaders"
                                ></datatable>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import FormSection from '@/components/forms/section_toggle.vue';
import datatable from '@vue-utils/datatable.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';

export default {
    name: 'OrganisationAccessDashboard',
    components: {
        FormSection,
        datatable,
    },
    data() {
        let vm = this;
        return {
            // Filters
            pBody: 'pBody' + uuid(),
            filterRole: 'All',
            filterStatus: 'All',
            statusChoices: [],
            roleChoices: [],
            members: [],
            profile: {},
            dtOptions: {
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
                processing: true,
                order: [[0, 'desc']],
                ajax: {
                    url: api_endpoints.organisation_requests_datatable,
                    dataSrc: 'data',
                    data: function (d) {
                        d.datatable_filter_role = vm.filterRole.toLowerCase();
                        d.datatable_filter_status = vm.filterStatus;
                        return d;
                    },
                },
                columns: [
                    {
                        data: 'id',
                        name: 'id',
                        searchable: false,
                        orderable: true,
                    },
                    {
                        data: 'name',
                        name: 'name',
                        searchable: true,
                        orderable: true,
                    },
                    {
                        data: 'requester',
                        name: 'requester__first_name, requester__last_name',
                        orderable: false,
                        searchable: true,
                    },
                    {
                        data: 'role',
                        name: 'role',
                        searchable: false,
                        orderable: true,
                    },
                    {
                        data: 'status',
                        name: 'status',
                        searchable: false,
                        orderable: true,
                    },
                    {
                        data: 'lodgement_date',
                        name: 'lodgement_date',
                        searchable: false,
                        orderable: true,
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return moment(data).format('DD/MM/YYYY');
                        },
                    },
                    {
                        data: 'assigned_officer',
                        name: 'assigned_officer__first_name, assigned_officer__last_name',
                        orderable: false,
                        searchable: true,
                    },
                    {
                        data: 'id',
                        name: '',
                        searchable: false,
                        orderable: false,
                        mRender: function (data, type, full) {
                            let column;
                            if (
                                full.status == 'Approved' ||
                                full.status == 'Declined'
                            ) {
                                column =
                                    "<a href='/internal/organisations/access/__ID__' >View </a>";
                            } else {
                                if (vm.is_assessor) {
                                    column =
                                        "<a href='/internal/organisations/access/__ID__'> Process </a>";
                                } else {
                                    column =
                                        "<a href='/internal/organisations/access/__ID__' >View </a>";
                                }
                            }
                            return column.replace(/__ID__/g, data);
                        },
                    },
                ],
                initComplete: function () {
                    // vm.isLoading = false;
                },
            },
            dtHeaders: [
                'Request Number',
                'Organisation',
                'Applicant',
                'Role',
                'Status',
                'Lodged on',
                'Assigned To',
                'Action',
            ],
            isLoading: false,
        };
    },
    watch: {
        filterRole: function () {
            let vm = this;
            if (vm.filterRole != 'All') {
                vm.$refs.org_access_table.vmDataTable
                    .columns(3)
                    .search(vm.filterRole)
                    .draw();
            } else {
                vm.$refs.org_access_table.vmDataTable
                    .columns(3)
                    .search('')
                    .draw();
            }
        },
        filterStatus: function () {
            let vm = this;
            if (vm.filterStatus != 'All') {
                vm.$refs.org_access_table.vmDataTable
                    .columns(4)
                    .search(vm.filterStatus)
                    .draw();
            } else {
                vm.$refs.org_access_table.vmDataTable
                    .columns(4)
                    .search('')
                    .draw();
            }
        },
    },
    mounted: function () {
        this.isLoading = true;
        this.fetchFilterLists();
        this.fetchAccessGroupMembers();
        this.fetchProfile();
        this.$nextTick(() => {
            this.addEventListeners();
        });
    },
    methods: {
        is_assessor: function () {
            return this.check_assessor();
        },

        fetchAccessGroupMembers: function () {
            let vm = this;
            helpers
                .fetchUrl(api_endpoints.organisation_access_group_members)
                .then(
                    (response) => {
                        vm.members = response.body;
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },
        fetchProfile: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.profile).then(
                (response) => {
                    vm.profile = response.body;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        check_assessor: function () {
            let vm = this;
            var assessor = vm.members.filter(function (elem) {
                return elem.name == vm.profile.full_name;
            });
            if (assessor.length > 0) return true;
            else return false;
        },
        addEventListeners: function () {
            helpers.initialiseSelect2.bind(this)(
                'select_organisation_access_role',
                'select_organisation_access_role_parent',
                'filterRole',
                'Select Role',
                false
            );
            helpers.initialiseSelect2.bind(this)(
                'select_organisation_access_status',
                'select_organisation_access_status_parent',
                'filterStatus',
                'Select Status',
                false
            );
        },
        fetchFilterLists: function () {
            let vm = this;
            vm.isLoading = true;

            helpers
                .fetchUrl(api_endpoints.filter_list_organisation_requests)
                .then(
                    (response) => {
                        vm.roleChoices = response.role_choices;
                        vm.statusChoices = response.status_choices;
                    },
                    (error) => {
                        console.log(error);
                    }
                )
                .finally(() => {
                    vm.isLoading = false;
                });
        },
    },
};
</script>
