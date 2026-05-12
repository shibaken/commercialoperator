<template>
    <div id="externalApproval" class="container">
        <div class="row">
            <h3>Licence {{ approval.lodgement_number }}</h3>

            <div class="col-sm-12">
                <div class="row">
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
                                            <label
                                                v-if="
                                                    approval.applicant_type ==
                                                    'org_applicant'
                                                "
                                                for="name"
                                                class="col-sm-3 control-label"
                                                >Organisation</label
                                            >
                                            <label
                                                v-else
                                                for="name"
                                                class="col-sm-3 control-label"
                                                >Applicant</label
                                            >
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
                                            <label
                                                for="abn"
                                                class="col-sm-3 control-label"
                                                >ABN</label
                                            >
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
                                    <label
                                        for="street"
                                        class="col-sm-3 control-label"
                                        >Street</label
                                    >
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
                                    <label
                                        for="suburb"
                                        class="col-sm-3 control-label"
                                        >Town/Suburb</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="applicant.address.locality"
                                            type="text"
                                            disabled
                                            class="form-control"
                                            name="surburb"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-3">
                                    <label
                                        for="country"
                                        class="col-sm-3 control-label"
                                        >State</label
                                    >
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
                                    <label
                                        for="postcode"
                                        class="col-sm-1 control-label text-nowrap"
                                        >Postcode</label
                                    >
                                    <div class="col-sm-2">
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
                                    <label
                                        for="country"
                                        class="col-sm-3 control-label"
                                        >Country</label
                                    >
                                    <div class="col-sm-4">
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
                                    <label
                                        for="issue_date"
                                        class="col-sm-3 control-label"
                                        >Issue Date</label
                                    >
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
                                    <label
                                        for="start_date"
                                        class="col-sm-3 control-label"
                                        >Start Date</label
                                    >
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
                                    <label
                                        for="expiry_date"
                                        class="col-sm-3 control-label"
                                        >Expiry Date</label
                                    >
                                    <div class="col-sm-3">
                                        <input
                                            :value="
                                                formatDate(approval.expiry_date)
                                            "
                                            type="text"
                                            class="form-control control-label pull-left"
                                            name="expiry_date"
                                            disabled
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label
                                        for="licence_document"
                                        class="col-sm-3 control-label"
                                        >Document</label
                                    >
                                    <div
                                        v-if="!approval.migrated"
                                        class="col-sm-4"
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
                                        <label class="control-label pull-left"
                                            ><a target="_blank" href=""
                                                >Licence.pdf</a
                                            >
                                            (This is a migrated Licence.)</label
                                        >
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
import { api_endpoints, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';

export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Approval',
    components: {
        FormSection,
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
                        vm.fetchApplicant(
                            vm.approval.applicant_id,
                            vm.approval.applicant_type
                        );
                    });
                },
                (error) => {
                    console.log(error);
                }
            );
    },
    data() {
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
            org: {
                address: {},
            },

            // Filters
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0;
        },
    },
    watch: {},
    mounted: function () {},
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        fetchOrganisation(applicant_id) {
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
                        vm.org = response;
                        vm.org.address = response.address;
                    },
                    (error) => {
                        console.log(error);
                    }
                );
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
