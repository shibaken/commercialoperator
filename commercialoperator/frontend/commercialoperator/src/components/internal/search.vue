<template>
    <div id="internalSearch" class="container">
        <div class="row">
            <div class="col-sm-12">
                    <FormSection
                        :form-collapse="false"
                        label="Search Organisation"
                        index="search_organisation"
                    >
                        <div class="row">
                            <form name="searchOrganisationForm">
                                <div class="col-md-4">
                                    <div class="form-group">
                                        <!-- Omitting the label for being redundant information -->
                                        <label
                                            class="control-label"
                                            for="Organisation"
                                        ></label>

                                        <TextFilteredOrgField
                                            id="id_org"
                                            :url="filtered_org_url"
                                            name="Organisation"
                                        />
                                    </div>
                                </div>
                                <div class="col-md-12 text-center">
                                    <input
                                        type="button"
                                        class="btn btn-primary"
                                        style="margin-bottom: 5px"
                                        value="View Details"
                                        @click.prevent="viewOrgDetails"
                                    />
                                </div>
                            </form>
                        </div>
                    </FormSection>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                    <FormSection
                        :form-collapse="false"
                        label="Search User"
                        index="search_user"
                    >
                        <div class="row">
                            <form name="searchUserForm">
                                <div class="">
                                    <div class="col-md-4">
                                        <div class="form-group">
                                            <!-- Omitting the label for being redundant information -->
                                            <label
                                                class="control-label"
                                                for="User"
                                            ></label>

                                            <TextFilteredField
                                                id="id_holder"
                                                :url="filtered_url"
                                                name="User"
                                            />
                                        </div>
                                    </div>
                                    <div class="">
                                        <div class="col-md-12 text-center">
                                            <div>
                                                <input
                                                    type="button"
                                                    class="btn btn-primary"
                                                    style="margin-bottom: 5px"
                                                    value="View Details"
                                                    @click.prevent="
                                                        viewUserDetails
                                                    "
                                                />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </FormSection>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                    <FormSection
                        :form-collapse="false"
                        label="Filter"
                        index="filter"
                    >
                        <div class="row">
                            <div>
                                <div class="form-group">
                                    <label
                                        for=""
                                        class="control-label col-lg-12"
                                        >Filter</label
                                    >
                                    <div
                                        class="form-check form-check-inline col-md-3"
                                    >
                                        <input
                                            id="searchProposal"
                                            ref="searchProposal"
                                            v-model="searchProposal"
                                            class="form-check-input"
                                            name="searchProposal"
                                            type="checkbox"
                                        />
                                        <label
                                            class="form-check-label"
                                            for="searchProposal"
                                            >Application</label
                                        >
                                    </div>
                                    <div
                                        class="form-check form-check-inline col-md-3"
                                    >
                                        <input
                                            id="searchApproval"
                                            ref="searchApproval"
                                            v-model="searchApproval"
                                            class="form-check-input"
                                            name="searchApproval"
                                            type="checkbox"
                                        />
                                        <label
                                            class="form-check-label"
                                            for="searchApproval"
                                            >Licence</label
                                        >
                                    </div>
                                    <div
                                        class="form-check form-check-inline col-md-3"
                                    >
                                        <input
                                            id="searchCompliance"
                                            ref="searchCompliance"
                                            v-model="searchCompliance"
                                            class="form-check-input"
                                            name="searchCompliance"
                                            type="checkbox"
                                        />
                                        <label
                                            class="form-check-label"
                                            for="searchCompliance"
                                            >Compliance with requirements</label
                                        >
                                    </div>
                                    <label
                                        for=""
                                        class="control-label col-lg-12"
                                        >Keyword</label
                                    >
                                    <div class="col-md-8">
                                        <input
                                            v-model="keyWord"
                                            type="search"
                                            class="form-control input-sm"
                                            name="details"
                                            placeholder=""
                                        />
                                    </div>
                                    <div class="col-md-1"></div>
                                    <div class="col-md-3">
                                        <input
                                            type="button"
                                            class="btn btn-primary"
                                            value="Add"
                                            @click.prevent="add"
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-lg-12">
                                <ul
                                    class="list-inline"
                                    style="display: inline; width: auto"
                                >
                                    <li
                                        v-for="(item, i) in searchKeywords"
                                        :key="i"
                                        class="list-inline-item"
                                    >
                                        <button
                                            class="btn btn-light"
                                            style="
                                                margin-top: 5px;
                                                margin-bottom: 5px;
                                            "
                                            @click.prevent=""
                                        >
                                            {{ item }}</button
                                        ><a
                                            href=""
                                            @click.prevent="removeKeyword(i)"
                                            ><i class="fas fa-xmark"></i></a>
                                    </li>
                                </ul>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-lg-12">
                                <div>
                                    <input
                                        type="button"
                                        class="btn btn-primary"
                                        style="margin-bottom: 5px"
                                        value="Search"
                                        @click.prevent="search"
                                    />
                                    <input
                                        type="reset"
                                        class="btn btn-primary"
                                        style="margin-bottom: 5px"
                                        value="Clear"
                                        @click.prevent="reset"
                                    />
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-lg-12">
                                <alert v-if="showMessage" type="danger"
                                    ><strong>
                                        <!-- eslint-disable-next-line vue/no-v-html -->
                                        <p v-html="messageString"></p></strong
                                ></alert>
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
                    </FormSection>
            </div>
        </div>
        <div class="row">
            <div class="col-sm-12">
                    <FormSection
                        :form-collapse="false"
                        label="Reference"
                        index="reference"
                    >
                        <div class="row">
                            <label
                                for="input_search_reference"
                                class="control-label col-lg-12"
                                >Reference</label
                            >
                            <div class="col-md-8">
                                <input
                                    id="input_search_reference"
                                    v-model="referenceWord"
                                    type="search"
                                    class="form-control input-sm"
                                    name="referenceWord"
                                    placeholder=""
                                />
                            </div>
                            <div>
                                <input
                                    type="button"
                                    class="btn btn-primary"
                                    style="margin-bottom: 5px"
                                    value="Search"
                                    @click.prevent="search_reference"
                                />
                            </div>
                            <alert v-if="showError" type="danger"
                                ><strong>{{ errorString }}</strong></alert
                            >
                        </div>
                    </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import $ from 'jquery';
import datatable from '@/utils/vue/datatable.vue';
import alert from '@vue-utils/alert.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import TextFilteredField from '@/components/forms/text-filtered.vue';
import TextFilteredOrgField from '@/components/forms/text-filtered-org.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';

export default {
    name: 'ExternalDashboard',
    components: {
        alert,
        FormSection,
        datatable,
        TextFilteredField,
        TextFilteredOrgField,
    },
    props: {
        proposalSearchKeywordsUrl: {
            type: String,
            default: api_endpoints.proposal_search_keywords,
        },
    },
    data() {
        let vm = this;
        return {
            rBody: 'rBody' + uuid(),
            oBody: 'oBody' + uuid(),
            uBody: 'uBody' + uuid(),
            kBody: 'kBody' + uuid(),
            loading: [],
            filtered_url: api_endpoints.filtered_users + '?search=',
            filtered_org_url: api_endpoints.filtered_organisations + '?search=',
            user_id: null,
            searchKeywords: [],
            searchProposal: true,
            searchApproval: false,
            searchCompliance: false,
            referenceWord: '',
            keyWord: null,
            selected_organisation: '',
            organisations: null,
            results: [],
            hasErrors: false,
            errorString: '',
            messages: false,
            messageString: '',
            datatable_id: 'proposal-datatable-' + uuid(),
            proposal_headers: [
                'Number',
                'Type',
                'Proponent',
                'Text found',
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
                        targets: -1,
                    },
                ],
                responsive: true,
                serverSide: true,
                ajax: {
                    url: vm.proposalSearchKeywordsUrl,
                    dataSrc: 'data',
                    data: function (d) {
                        d.searchKeywords = JSON.stringify(vm.searchKeywords);
                        d.searchProposal = vm.searchProposal;
                        d.searchApproval = vm.searchApproval;
                        d.searchCompliance = vm.searchCompliance;
                        d.is_internal = true;
                    },
                },
                order: [[0, 'desc']],
                pageLength: 10,
                columns: [
                    { data: 'number', name: 'lodgement_number' },
                    // NOTE: Changing all columns below to be neither searchable nor orderable, b/c this table's dataset consists of thee different models
                    { data: 'type', searchable: false, orderable: false },
                    { data: 'applicant', searchable: false, orderable: false },
                    {
                        data: 'text',
                        searchable: false,
                        orderable: false,
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            if (data.value) {
                                return data.value;
                            } else {
                                return data;
                            }
                        },
                    },
                    {
                        data: 'id',
                        searchable: false,
                        orderable: false,
                        mRender: function (data, type, full) {
                            let links = '';
                            if (
                                full.type == 'Proposal' ||
                                full.type == 'Application'
                            ) {
                                links += `<a href='/internal/proposal/${full.id}'>View</a><br/>`;
                            }
                            if (full.type == 'Compliance') {
                                links += `<a href='/internal/compliance/${full.id}'>View</a><br/>`;
                            }
                            if (
                                full.type == 'Approval' ||
                                full.type == 'Licence'
                            ) {
                                links += `<a href='/internal/approval/${full.id}'>View</a><br/>`;
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
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        showMessage: function () {
            var vm = this;
            return vm.messages;
        },
    },
    watch: {},
    mounted: function () {
        $('a[data-bs-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.addListeners();
        });
    },
    methods: {
        addListeners: function () {
            let vm = this;
            // Initialise select2 for region
            $(vm.$refs.searchOrg)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Organisation',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_organisation = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_organisation = selected.val();
                });
        },
        viewOrgDetails: function () {
            let vm = this;
            let form = document.forms.searchOrganisationForm;
            const org_selected = form.elements['Organisation-selected'];
            const ledger_selected =
                form.elements['Organisation-selected-ledger'];
            const org_id =
                (ledger_selected && ledger_selected.value) ||
                (org_selected && org_selected.value);
            if (org_id) {
                window.location.href = `/ledger-ui/organisation/${org_id}`;
            } else {
                swal.fire({
                    title: 'Organisation not selected',
                    html: 'Please select the organisation to view the details',
                    icon: 'error',
                }).then(() => {});
                return;
            }
        },
        viewUserDetails: function () {
            let vm = this;
            let form = document.forms.searchUserForm;
            var user_selected = form.elements['User-selected'];
            if (user_selected != undefined || user_selected != null) {
                var user_id = user_selected.value;
                vm.$router.push({
                    name: 'internal-user-detail',
                    params: { user_id: user_id },
                });
            } else {
                swal.fire({
                    title: 'User not selected',
                    html: 'Please select the user to view the details',
                    icon: 'error',
                }).then(() => {});
                return;
            }
        },

        add: function () {
            let vm = this;
            if (vm.keyWord != null) {
                vm.searchKeywords.push(vm.keyWord);
            }
        },
        removeKeyword: function (index) {
            let vm = this;
            if (index > -1) {
                vm.searchKeywords.splice(index, 1);
            }
        },
        reset: function () {
            let vm = this;
            if (vm.keyWord != null) {
                vm.searchKeywords = [];
            }
            vm.keyWord = null;
            vm.results = [];
            vm.messages = false;
            vm.messageString = '';
            vm.$refs.proposal_datatable.vmDataTable.clear();
            vm.$refs.proposal_datatable.vmDataTable.draw();
        },

        search: function () {
            let vm = this;
            console.log('Calling search');
            vm.$refs.proposal_datatable.vmDataTable.clear();
            vm.$refs.proposal_datatable.vmDataTable.draw();

            return;
        },

        search_reference: function () {
            let vm = this;
            console.log('Calling search_reference');
            if (vm.referenceWord) {
                helpers
                    .fetchUrl('/api/search_reference.json', {
                        reference_number: vm.referenceWord,
                        method: 'POST',
                    })
                    .then(
                        (res) => {
                            console.log(res);
                            vm.hasErrors = false;
                            vm.errorString = '';
                            vm.$router.push({
                                path:
                                    '/internal/' +
                                    res.body.type +
                                    '/' +
                                    res.body.id,
                            });
                        },
                        (error) => {
                            console.log(error);
                            vm.hasErrors = true;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
    },
};
</script>
