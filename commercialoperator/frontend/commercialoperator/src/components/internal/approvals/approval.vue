<template>
    <div id="internalApproval" class="container">
        <div class="row">
            <h3>
                Licence {{ approval.lodgement_number }} ({{
                    approval.application_type
                }})
            </h3>
            <div class="col-md-3">
                <CommsLogs
                    :comms_url="comms_url"
                    :logs_url="logs_url"
                    :comms_add_url="comms_add_url"
                    :disable_add_entry="false"
                />
                <div class="">
                    <div class="card mb-3">
                        <div class="card-header">Submission</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Issued on</strong><br />
                                    {{ formatDate(approval.issued_date) }}
                                </div>
                                <div class="col-sm-12 top-buffer-s">
                                    <table class="table small-table">
                                        <thead>
                                            <tr>
                                                <th>Lodgement</th>
                                                <th>Date</th>
                                                <th>Action</th>
                                            </tr>
                                        </thead>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="">
                    <div class="card mb-3">
                        <div class="card-header">Workflow</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-12">
                                    <strong>Status</strong><br />
                                    {{ approval.status }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-1"></div>
            <div class="col-md-8">
                <div class="">
                    <div class="card">
                        <FormSection
                            :form-collapse="false"
                            label="Holder"
                            index="holder"
                            subtitle=""
                        >
                            <div class="row">
                                <div class="col-sm-12">
                                    <form
                                        class="form-horizontal"
                                        name="approval_form"
                                    >
                                        <div class="form-group row mb-3">
                                            <div class="col-sm-3">
                                                <label
                                                    v-if="
                                                        approval.applicant_type ==
                                                        'org_applicant'
                                                    "
                                                    for="name"
                                                    class="control-label text-nowrap"
                                                    >Organisation</label
                                                >
                                                <label
                                                    v-else
                                                    for="name"
                                                    class="control-label text-nowrap"
                                                    >Applicant</label
                                                >
                                            </div>
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="applicant.name"
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="name"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                        <div
                                            v-if="
                                                approval.applicant_type ==
                                                'org_applicant'
                                            "
                                            class="form-group row"
                                        >
                                            <div class="col-sm-3">
                                                <label
                                                    for="abn"
                                                    class="control-label text-nowrap"
                                                    >ABN</label
                                                >
                                            </div>
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="applicant.abn"
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="abn"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </FormSection>
                    </div>
                </div>

                <div class="row">
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
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="street"
                                            class="control-label text-nowrap text-nowrap"
                                            >Street</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="applicant.address.line1"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="street"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="suburb"
                                            class="col-sm-3 control-label text-nowrap"
                                            >Town/Suburb</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="applicant.address.locality"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="suburb"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="country"
                                            class="col-sm-3 control-label text-nowrap"
                                            >State</label
                                        >
                                    </div>
                                    <div class="col-sm-3">
                                        <input
                                            v-model="applicant.address.state"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="country"
                                            placeholder=""
                                        />
                                    </div>
                                    <div class="col-sm-3">
                                        <label
                                            for="postcode"
                                            class="col-sm-1 control-label text-nowrap"
                                            >Postcode</label
                                        >
                                    </div>
                                    <div class="col-sm-3">
                                        <input
                                            v-model="applicant.address.postcode"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="postcode"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <div class="col-sm-3">
                                        <label
                                            for="country"
                                            class="control-label text-nowrap"
                                            >Country</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="applicant.address.country"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="country"
                                        />
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                    </div>
                </div>

                <div class="row">
                    <div class="card">
                        <FormSection
                            :form-collapse="false"
                            label="Licence Details"
                            index="licence_details"
                            subtitle=""
                        >
                            <form
                                class="form-horizontal"
                                action="index.html"
                                method="post"
                            >
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="issue_date"
                                            class="control-label text-nowrap"
                                            >Issue Date</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            :value="
                                                formatDate(approval.issue_date)
                                            "
                                            type="text"
                                            class="form-control control-label pull-left"
                                            name="issue_date"
                                            disabled
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="start_date"
                                            class="control-label text-nowrap"
                                            >Start Date</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            :value="
                                                formatDate(approval.start_date)
                                            "
                                            type="text"
                                            class="form-control control-label pull-left"
                                            name="start_date"
                                            disabled
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-3">
                                    <div class="col-sm-3">
                                        <label
                                            for="expiry_date"
                                            class="control-label text-nowrap"
                                            >Expiry Date</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            :value="
                                                formatDate(approval.expiry_date)
                                            "
                                            type="text"
                                            class="form-control control-label pull-left"
                                            name="expiry_date"
                                            disabled
                                        />
                                        <span
                                            v-if="extended"
                                            class="control-label pull-left"
                                            style="color: green"
                                            >(Extended)</span
                                        >
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <div class="col-sm-3">
                                        <label
                                            for="licence_document"
                                            class="control-label text-nowrap"
                                            >Document</label
                                        >
                                    </div>
                                    <div
                                        v-if="!approval.migrated"
                                        class="col-sm-6"
                                    >
                                        <p>
                                            <a
                                                target="_blank"
                                                :href="
                                                    approval.licence_document
                                                "
                                                class="control-label pull-left"
                                                >Licence.pdf</a
                                            >
                                        </p>
                                        <br />
                                        <div
                                            v-for="r in approval.requirement_docs"
                                            :key="r[0]"
                                        >
                                            <p>
                                                <a
                                                    target="_blank"
                                                    :href="r[1]"
                                                    class="control-label pull-left"
                                                    >{{ r[0] }}</a
                                                >
                                            </p>
                                            <br />
                                        </div>
                                    </div>
                                    <div v-else class="col-sm-4">
                                        <p class="">
                                            <a target="_blank" href=""
                                                >Licence.pdf</a
                                            >
                                            (This is a migrated licence)
                                        </p>
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import FormSection from '@/components/forms/section_toggle.vue';
import CommsLogs from '@common-utils/comms_logs.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Approval',
    components: {
        FormSection,
        CommsLogs,
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                helpers.add_endpoint_json(
                    api_endpoints.approvals,
                    to.params.approval_id
                )
            )
            .then(
                (response) => {
                    next((vm) => {
                        vm.approval = response;
                        vm.approval.applicant_id = response.applicant_id;
                        vm.approval.applicant_type = response.applicant_type;
                        //vm.fetchOrganisation(vm.approval.applicant_id)
                        vm.fetchApplicant(
                            vm.approval.applicant_id,
                            vm.approval.applicant_type
                        );
                        vm.extended =
                            vm.approval.application_type == 'E Class' &&
                            !vm.approval.can_extend;
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    },
    data() {
        let vm = this;
        return {
            loading: [],
            approval: {
                applicant_id: null,
                applicant_type: null,
            },
            applicant: {
                address: {},
            },
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            adBody: 'adBody' + uuid(),
            pBody: 'pBody' + uuid(),
            cBody: 'cBody' + uuid(),
            oBody: 'oBody' + uuid(),
            extended: false,

            // Filters
            logs_url: helpers.add_endpoint_json(
                api_endpoints.approvals,
                vm.$route.params.approval_id + '/action_log'
            ),
            comms_url: helpers.add_endpoint_json(
                api_endpoints.approvals,
                vm.$route.params.approval_id + '/comms_log'
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.approvals,
                vm.$route.params.approval_id + '/add_comms_log'
            ),
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0;
        },
        address_default: function () {
            return {
                line1: 'Is address saved?',
                locality: '',
                state: '',
                postcode: '',
                country: '',
            };
        },
    },
    watch: {},
    mounted: function () {},
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        fetchOrgApplicant(applicant_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.organisations,
                        applicant_id
                    )
                )
                .then(
                    (response) => {
                        vm.applicant = response;
                        vm.applicant.name = response.organisation_name;
                        vm.applicant.abn = response.organisation_abn;
                        if (response.organisation_address == null) {
                            vm.applicant.address = vm.address_default;
                        } else {
                            vm.applicant.address =
                                response.organisation_address;
                        }
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },
        fetchProxyApplicant(applicant_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(api_endpoints.users, applicant_id)
                )
                .then(
                    (response) => {
                        vm.applicant = response;
                        vm.applicant.name = response.full_name;
                        if (response.residential_address == null) {
                            vm.applicant.address = vm.address_default;
                        } else {
                            vm.applicant.address = response.residential_address;
                        }
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },
        fetchApplicant(applicant_id, applicant_type) {
            let vm = this;
            if (applicant_type == 'org_applicant') {
                vm.fetchOrgApplicant(applicant_id);
            } else {
                vm.fetchProxyApplicant(applicant_id);
            }
        },
        formatDate: function (data) {
            return moment(data).format('DD/MM/YYYY');
        },
    },
};
</script>
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
