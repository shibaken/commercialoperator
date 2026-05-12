<template>
    <div id="internalUserInfo" class="container-fluid">
        <div class="row">
            <div class="col-md-10 col-md-offset-1">
                <div class="row">
                    <h3>
                        {{ user.first_name }} {{ user.last_name }} -
                        {{ user.dob }} ({{ user.email }})
                    </h3>
                    <div class="col-md-3">
                        <CommsLogs
                            :comms_url="comms_url"
                            :logs_url="logs_url"
                            :comms_add_url="comms_add_url"
                            :is_user_log="true"
                            :disable_add_entry="false"
                        />
                    </div>
                    <div class="col-md-9">
                        <ul class="nav nav-pills mb-3" role="tablist">
                            <li class="nav-item">
                                <a
                                    id="pills-details-tab"
                                    data-toggle="tab"
                                    class="nav-link active"
                                    data-bs-toggle="pill"
                                    :href="'#' + dTab"
                                    role="tab"
                                    :aria-controls="dTab"
                                    aria-selected="true"
                                    >Details</a
                                >
                            </li>
                            <li class="nav-item">
                                <a
                                    id="pills-other-tab"
                                    data-toggle="tab"
                                    class="nav-link"
                                    data-bs-toggle="pill"
                                    :href="'#' + oTab"
                                    role="tab"
                                    :aria-controls="oTab"
                                    aria-selected="false"
                                    >Other</a
                                >
                            </li>
                        </ul>
                        <div class="tab-content">
                            <div
                                :id="dTab"
                                class="tab-pane fade active show"
                                role="tabpanel"
                                aria-labelledby="pills-details-tab"
                            >
                                <div class="row">
                                    <div class="col-sm-12">
                                        <div class="card">
                                            <FormSection
                                                :form-collapse="false"
                                                label="Personal Details"
                                                index="personal_details"
                                                subtitle=""
                                            >
                                                <form
                                                    class="form-horizontal"
                                                    name="personal_form"
                                                    method="post"
                                                >
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <div
                                                            class="col-sm-3"
                                                        ></div>
                                                        <div class="col-sm-6">
                                                            <p>
                                                                <b
                                                                    >To update
                                                                    your account
                                                                    name or
                                                                    MFA(Multi-Factor
                                                                    Authentication)
                                                                    please click
                                                                    <a
                                                                        href="/sso/setting"
                                                                        >here:</a
                                                                    ></b
                                                                ><br />
                                                                Changes will not
                                                                update until
                                                                your next login.
                                                            </p>
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Given
                                                            Name(s)</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user.first_name
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="first_name"
                                                                disabled
                                                            />
                                                        </div>
                                                    </div>
                                                    <div class="form-group row">
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Last Name</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user.last_name
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="last_name"
                                                                disabled
                                                            />
                                                        </div>
                                                    </div>
                                                </form>
                                            </FormSection>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <div class="card">
                                            <FormSection
                                                :form-collapse="false"
                                                label="Address Details"
                                                index="address_details"
                                                subtitle=""
                                            >
                                                <form
                                                    class="form-horizontal"
                                                    action="index.html"
                                                    method="post"
                                                >
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Street</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user
                                                                        .residential_address
                                                                        .line1
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="street"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Town/Suburb</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user
                                                                        .residential_address
                                                                        .locality
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="surburb"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >State</label
                                                        >
                                                        <div class="col-sm-2">
                                                            <input
                                                                v-model="
                                                                    user
                                                                        .residential_address
                                                                        .state
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="country"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                        <label
                                                            for=""
                                                            class="col-sm-2 control-label"
                                                            >Postcode</label
                                                        >
                                                        <div class="col-sm-2">
                                                            <input
                                                                v-model="
                                                                    user
                                                                        .residential_address
                                                                        .postcode
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="postcode"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Country</label
                                                        >
                                                        <div
                                                            id="select_manage_user_address_country_parent"
                                                            class="col-sm-4"
                                                        >
                                                            <select
                                                                id="select_manage_user_address_country"
                                                                ref="select_manage_user_address_country"
                                                                v-model="
                                                                    user
                                                                        .residential_address
                                                                        .country
                                                                "
                                                                class="form-control"
                                                                name="country"
                                                            >
                                                                <option
                                                                    v-for="c in countries"
                                                                    :key="
                                                                        c.code
                                                                    "
                                                                    :value="
                                                                        c.code
                                                                    "
                                                                >
                                                                    {{ c.name }}
                                                                </option>
                                                            </select>
                                                        </div>
                                                    </div>
                                                    <div class="form-group row">
                                                        <div class="col-sm-12">
                                                            <button
                                                                v-if="
                                                                    !updatingAddress
                                                                "
                                                                class="btn btn-primary float-end"
                                                                @click.prevent="
                                                                    updateAddress()
                                                                "
                                                            >
                                                                Update
                                                            </button>
                                                            <button
                                                                v-else
                                                                disabled
                                                                class="btn btn-primary float-end"
                                                            >
                                                                <i
                                                                    class="fa fa-spin fa-spinner"
                                                                ></i
                                                                >&nbsp;Updating
                                                            </button>
                                                        </div>
                                                    </div>
                                                </form>
                                            </FormSection>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <div class="card">
                                            <FormSection
                                                :form-collapse="false"
                                                label="Contact Details"
                                                index="contact_details"
                                                subtitle=""
                                            >
                                                <form
                                                    class="form-horizontal"
                                                    action="index.html"
                                                    method="post"
                                                >
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Phone (work)</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user.phone_number
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="phone"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Mobile</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user.mobile_number
                                                                "
                                                                type="text"
                                                                class="form-control"
                                                                name="mobile"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-3 control-label"
                                                            >Email</label
                                                        >
                                                        <div class="col-sm-6">
                                                            <input
                                                                v-model="
                                                                    user.email
                                                                "
                                                                type="email"
                                                                class="form-control"
                                                                disabled="disabled"
                                                                name="email"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                    </div>
                                                    <div class="form-group row">
                                                        <div class="col-sm-12">
                                                            <button
                                                                v-if="
                                                                    !updatingContact
                                                                "
                                                                class="btn btn-primary float-end"
                                                                @click.prevent="
                                                                    updateContact()
                                                                "
                                                            >
                                                                Update
                                                            </button>
                                                            <button
                                                                v-else
                                                                disabled
                                                                class="btn btn-primary float-end"
                                                            >
                                                                <i
                                                                    class="fa fa-spin fa-spinner"
                                                                ></i
                                                                >&nbsp;Updating
                                                            </button>
                                                        </div>
                                                    </div>
                                                </form>
                                            </FormSection>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <div class="card">
                                            <FormSection
                                                :form-collapse="false"
                                                label="Organisations"
                                                index="organisations"
                                                subtitle=""
                                            >
                                                <div
                                                    v-for="org in user.commercialoperator_organisations"
                                                    :key="org.id"
                                                >
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-2 control-label"
                                                            >Organisation</label
                                                        >
                                                        <div class="col-sm-3">
                                                            <input
                                                                v-model="
                                                                    org.name
                                                                "
                                                                type="text"
                                                                disabled
                                                                class="form-control"
                                                                name="organisation"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                        <label
                                                            for=""
                                                            class="col-sm-2 control-label"
                                                            >ABN/ACN</label
                                                        >
                                                        <div class="col-sm-3">
                                                            <input
                                                                v-model="
                                                                    org.abn
                                                                "
                                                                type="text"
                                                                disabled
                                                                class="form-control"
                                                                name="organisation"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                        <div class="col-sm-2">
                                                            <a
                                                                style="
                                                                    cursor: pointer;
                                                                    text-decoration: none;
                                                                "
                                                                @click.prevent="
                                                                    unlinkUser(
                                                                        org
                                                                    )
                                                                "
                                                                ><i
                                                                    class="fa fa-chain-broken fa-2x"
                                                                ></i
                                                                >&nbsp;Unlink</a
                                                            >
                                                        </div>
                                                    </div>
                                                </div>
                                                <div
                                                    v-for="orgReq in orgRequest_pending"
                                                    :key="orgReq.id"
                                                >
                                                    <div
                                                        class="form-group row mb-3"
                                                    >
                                                        <label
                                                            for=""
                                                            class="col-sm-2 control-label"
                                                            >Organisation</label
                                                        >
                                                        <div class="col-sm-3">
                                                            <input
                                                                v-model="
                                                                    orgReq.name
                                                                "
                                                                type="text"
                                                                disabled
                                                                class="form-control"
                                                                name="organisation"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                        <label
                                                            for=""
                                                            class="col-sm-2 control-label"
                                                            >ABN/ACN</label
                                                        >
                                                        <div class="col-sm-3">
                                                            <input
                                                                v-model="
                                                                    orgReq.abn
                                                                "
                                                                type="text"
                                                                disabled
                                                                class="form-control"
                                                                name="organisation"
                                                                placeholder=""
                                                            />
                                                        </div>
                                                        <label
                                                            >Pending for
                                                            Approval (#{{
                                                                orgReq.id
                                                            }})</label
                                                        >
                                                    </div>
                                                </div>
                                            </FormSection>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div
                                :id="oTab"
                                class="tab-pane fade"
                                role="tabpanel"
                                aria-labelledby="pills-other-tab"
                            >
                                <FormSection
                                    :form-collapse="false"
                                    label="Applications"
                                    index="applications"
                                >
                                    <ProposalDashTable
                                        ref="proposals_table"
                                        level="internal"
                                        :url="proposals_url"
                                    />
                                </FormSection>
                                <FormSection
                                    :form-collapse="false"
                                    label="Licences"
                                    index="approvals"
                                >
                                    <ApprovalDashTable
                                        ref="approvals_table"
                                        level="internal"
                                        :url="approvals_url"
                                    />
                                </FormSection>
                                <FormSection
                                    :form-collapse="false"
                                    label="Compliances"
                                    index="compliances"
                                >
                                    <ComplianceDashTable
                                        ref="compliance_table"
                                        level="internal"
                                        :url="compliance_url"
                                    />
                                </FormSection>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

//TODO make address and contact details readonly, remove/replace action log and comms log

import { api_endpoints, helpers } from '@/utils/hooks';
import FormSection from '@/components/forms/section_toggle.vue';
import ProposalDashTable from '@common-utils/proposals_dashboard.vue';
import ApprovalDashTable from '@common-utils/approvals_dashboard.vue';
import ComplianceDashTable from '@common-utils/compliances_dashboard.vue';
import CommsLogs from '@common-utils/comms_logs.vue';
import utils from '../utils';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'User',
    components: {
        FormSection,
        ProposalDashTable,
        ApprovalDashTable,
        ComplianceDashTable,
        CommsLogs,
    },
    beforeRouteEnter: function (to, from, next) {
        let initialisers = [
            utils.fetchCountries(),
            utils.fetchUser(to.params.user_id),
            utils.fetchOrgRequestPending(to.params.user_id),
        ];
        Promise.all(initialisers).then((data) => {
            next((vm) => {
                vm.countries = data[0];
                vm.user = data[1];
                vm.user.residential_address =
                    vm.user.residential_address != null
                        ? vm.user.residential_address
                        : {};
                vm.orgRequest_pending = data[2];
            });
        });
    },
    beforeRouteUpdate: function (to, from, next) {
        let initialisers = [utils.fetchUser(to.params.user_id)];
        Promise.all(initialisers).then((data) => {
            next((vm) => {
                vm.user = data[0];
                vm.user.residential_address =
                    vm.user.residential_address != null
                        ? vm.user.residential_address
                        : {};
            });
        });
    },
    data() {
        let vm = this;
        return {
            adBody: 'adBody' + uuid(),
            pdBody: 'pdBody' + uuid(),
            cdBody: 'cdBody' + uuid(),
            odBody: 'odBody' + uuid(),
            idBody: 'idBody' + uuid(),
            dTab: 'dTab' + uuid(),
            oTab: 'oTab' + uuid(),
            user: {
                residential_address: {},
                commercialoperatorcompliance_organisations: [],
            },
            loading: [],
            countries: [],
            updatingPersonal: false,
            updatingAddress: false,
            updatingContact: false,
            uploadingID: false,
            uploadedID: null,
            logsTable: null,
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            activate_tables: false,
            comms_url: helpers.add_endpoint_json(
                api_endpoints.users,
                vm.$route.params.user_id + '/comms_log'
            ),
            logs_url: helpers.add_endpoint_json(
                api_endpoints.users,
                vm.$route.params.user_id + '/action_log'
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.users,
                vm.$route.params.user_id + '/add_comms_log'
            ),
            proposals_url:
                api_endpoints.proposals_paginated_external +
                '&submitter_id=' +
                vm.$route.params.user_id,
            approvals_url:
                api_endpoints.approvals_paginated_external +
                '&submitter_id=' +
                vm.$route.params.user_id,
            compliance_url:
                api_endpoints.compliances_paginated_external +
                '&submitter_id=' +
                vm.$route.params.user_id,
            orgRequest_pending: [],
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length == 0;
        },
        uploadedIDFileName: function () {
            return this.uploadedID != null ? this.uploadedID.name : '';
        },
    },
    mounted: function () {
        this.personal_form = document.forms.personal_form;
        this.$nextTick(() => {
            this.eventListeners();
        });
    },
    methods: {
        eventListeners: function () {
            let vm = this;
            // Fix the table responsiveness when tab is shown
            $('a[href="#' + vm.oTab + '"]').on('shown.bs.tab', function () {
                vm.$refs.proposals_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
                vm.$refs.approvals_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
                vm.$refs.compliance_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            });

            helpers.initialiseSelect2.bind(this)(
                'select_manage_user_address_country',
                'select_manage_user_address_country_parent',
                'user.residential_address.country',
                'Select a Country'
            );
        },
        unlinkUser: function (org) {
            let vm = this;
            let org_name = org.name;
            swal.fire({
                title: 'Unlink From Organisation',
                text:
                    'Are you sure you want to unlink this user from ' +
                    org.name +
                    ' ?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Accept',
            }).then(
                (result) => {
                    if (result.isConfirmed) {
                        helpers
                            .fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.organisations,
                                    org.id + '/unlink_user'
                                ),
                                {
                                    method: 'POST',
                                    body: JSON.stringify(vm.user),
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                }
                            )
                            .then(
                                () => {
                                    helpers
                                        .fetchUrl(
                                            helpers.add_endpoint_json(
                                                api_endpoints.users,
                                                vm.user.id
                                            )
                                        )
                                        .then(
                                            (response) => {
                                                vm.user = response;
                                                if (
                                                    vm.user
                                                        .residential_address ==
                                                    null
                                                ) {
                                                    vm.user.residential_address =
                                                        {};
                                                }
                                                if (
                                                    vm.user
                                                        .commercialoperatorcompliance_organisations &&
                                                    vm.user
                                                        .commercialoperatorcompliance_organisations
                                                        .length > 0
                                                ) {
                                                    vm.managesOrg = 'Yes';
                                                }
                                                swal.fire({
                                                    title: 'Unlink',
                                                    text:
                                                        'The user has been successfully unlinked from ' +
                                                        org_name +
                                                        '.',
                                                    icon: 'success',
                                                });
                                            },
                                            () => {}
                                        );
                                },
                                () => {
                                    swal.fire({
                                        title: 'Unlink',
                                        text:
                                            'There was an error unlinking the user from ' +
                                            org_name +
                                            '.',
                                        icon: 'error',
                                    });
                                }
                            );
                    }
                },
                () => {}
            );
        },
        readFileID: function () {
            let vm = this;
            let _file = null;
            var input = $(vm.$refs.uploadedID)[0];
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(input.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            vm.uploadedID = _file;
        },
    },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.top-buffer-s {
    margin-top: 10px;
}
.actionBtn {
    cursor: pointer;
}
.hidePopover {
    display: none;
}
</style>
