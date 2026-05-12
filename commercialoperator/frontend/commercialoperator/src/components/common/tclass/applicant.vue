<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div class="row">
        <div class="col-sm-12">
            <div class="col-md-12">
                <div class="row">
                    <div class="card">
                        <FormSection
                            v-if="applicantType == 'ORG'"
                            :form-collapse="false"
                            label="Applicant"
                            index="applicant"
                            subtitle=""
                        >
                            <form class="form-horizontal">
                                <div class="form-group row mb-2">
                                    <label
                                        for="applicantName"
                                        class="col-sm-3 control-label"
                                        >Name</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_name
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantName"
                                            placeholder=""
                                            style="width: 100%"
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-2">
                                    <label
                                        for="applicantName"
                                        class="col-sm-3 control-label"
                                        >Trading Name</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_trading_name
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantName"
                                            placeholder=""
                                            style="width: 100%"
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label
                                        for="applicantName"
                                        class="col-sm-3 control-label"
                                        >ABN/ACN</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_abn
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantABN"
                                            placeholder=""
                                            style="width: 100%"
                                        />
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                        <FormSection
                            v-if="applicantType == 'SUB'"
                            :form-collapse="false"
                            label="Approval Type"
                            index="approval_type"
                            subtitle=""
                        >
                            <form class="form-horizontal">
                                <div class="form-group row">
                                    <label
                                        for="applicantName"
                                        class="col-sm-3 control-label"
                                        >Given Name(s)</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter.first_name
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantName"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label
                                        for="applicantName"
                                        class="col-sm-3 control-label"
                                        >Surname</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter.last_name
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantName"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="row">
                    <div class="card">
                        <FormSection
                            v-if="
                                applicantType == 'ORG' &&
                                proposal.org_applicant.organisation_address
                            "
                            :form-collapse="false"
                            label="Address Details"
                            index="address_details"
                            subtitle=""
                        >
                            <form class="form-horizontal">
                                <div class="form-group row mb-2">
                                    <label
                                        for="street"
                                        class="col-sm-3 control-label"
                                        >Street</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_address.line1
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="street"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-2">
                                    <label
                                        for="suburb"
                                        class="col-sm-3 control-label"
                                        >Town/Suburb</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_address
                                                    .locality
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="surburb"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-2">
                                    <label
                                        for="country"
                                        class="col-sm-3 control-label"
                                        >State</label
                                    >
                                    <div class="col-sm-2">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_address.state
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="country"
                                            placeholder=""
                                        />
                                    </div>
                                    <label
                                        for="postcode"
                                        class="col-sm-2 control-label text-nowrap"
                                        >Postcode</label
                                    >
                                    <div class="col-sm-2">
                                        <input
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_address
                                                    .postcode
                                            "
                                            disabled
                                            type="text"
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
                                            v-model="
                                                proposal.org_applicant
                                                    .organisation_address
                                                    .country
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="country"
                                        />
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                        <FormSection
                            v-if="
                                applicantType == 'SUB' &&
                                proposal.submitter.residential_address
                            "
                            :form-collapse="false"
                            label="Address Details"
                            index="address_details"
                            subtitle=""
                        >
                            <form class="form-horizontal">
                                <div class="form-group">
                                    <label
                                        for="street"
                                        class="col-sm-3 control-label"
                                        >Street</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter
                                                    .residential_address.line1
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="street"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label
                                        for="suburb"
                                        class="col-sm-3 control-label"
                                        >Town/Suburb</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter
                                                    .residential_address
                                                    .locality
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="surburb"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label
                                        for="country"
                                        class="col-sm-3 control-label"
                                        >State</label
                                    >
                                    <div class="col-sm-2">
                                        <input
                                            v-model="
                                                proposal.submitter
                                                    .residential_address.state
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="country"
                                            placeholder=""
                                        />
                                    </div>
                                    <label
                                        for="postcode"
                                        class="col-sm-2 control-label text-nowrap"
                                        >Postcode</label
                                    >
                                    <div class="col-sm-2">
                                        <input
                                            v-model="
                                                proposal.submitter
                                                    .residential_address
                                                    .postcode
                                            "
                                            disabled
                                            type="text"
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
                                            v-model="
                                                proposal.submitter
                                                    .residential_address.country
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="country"
                                        />
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="row">
                    <div class="card">
                        <FormSection
                            v-if="applicantType == 'ORG'"
                            :form-collapse="false"
                            label="Contact Details"
                            index="contact_details"
                            subtitle=""
                        >
                            <table
                                :id="contacts_table_id"
                                ref="contacts_datatable"
                                class="hover table table-striped table-bordered dt-responsive"
                                cellspacing="0"
                                width="100%"
                            ></table>
                        </FormSection>
                        <!-- <div
                            v-if="applicantType == 'SUB'"
                            :id="contactsBody"
                            class="panel-body panel-collapse collapse"
                        > -->
                        <FormSection
                            v-if="applicantType == 'SUB'"
                            :form-collapse="false"
                            label="Contact Details"
                            index="contact_details"
                            subtitle=""
                        >
                            <form class="form-horizontal">
                                <div class="form-group row mb-2">
                                    <label
                                        for="applicantPhoneNumber"
                                        class="col-sm-3 control-label"
                                        >Phone (work)</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter.phone_number
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantPhoneNumber"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row mb-2">
                                    <label
                                        for="applicantMobileNumber"
                                        class="col-sm-3 control-label"
                                        >Mobile</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.submitter.mobile_number
                                            "
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantMobileNumber"
                                            placeholder=""
                                        />
                                    </div>
                                </div>
                                <div class="form-group row">
                                    <label
                                        for="applicantEmail"
                                        class="col-sm-3 control-label"
                                        >Email</label
                                    >
                                    <div class="col-sm-6">
                                        <input
                                            v-model="proposal.submitter.email"
                                            disabled
                                            type="text"
                                            class="form-control"
                                            name="applicantEmail"
                                            placeholder=""
                                        />
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
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'ApplicantComponent',
    components: { FormSection },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            values: null,
            detailsBody: 'detailsBody' + uuid(),
            addressBody: 'addressBody' + uuid(),
            contactsBody: 'contactsBody' + uuid(),
            panelClickersInitialised: false,
            contacts_table_id: uuid() + 'contacts-table',
            contacts_table_initialised: false,
            contacts_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                ajax: {
                    url: vm.contactsURL,
                    dataSrc: '',
                },
                columns: [
                    {
                        title: 'Name',
                        data: 'id',
                        mRender: function (data, type, full) {
                            return full.first_name + ' ' + full.last_name;
                        },
                    },
                    {
                        title: 'Phone',
                        data: 'phone_number',
                    },
                    {
                        title: 'Mobile',
                        data: 'mobile_number',
                    },
                    {
                        title: 'Fax',
                        data: 'fax_number',
                    },
                    {
                        title: 'Email',
                        data: 'email',
                    },
                ],
                processing: true,
            },
            contacts_table: null,
        };
    },
    computed: {
        contactsURL: function () {
            return this.proposal != null
                ? helpers.add_endpoint_json(
                      api_endpoints.organisations,
                      this.proposal.org_applicant.id + '/contacts'
                  )
                : '';
        },
        applicantType: function () {
            return this.proposal.applicant_type;
        },
    },
    mounted: function () {
        let vm = this;
        if (!vm.panelClickersInitialised) {
            $('.panelClicker[data-toggle="collapse"]').on('click', function () {
                var chev = $(this).children()[0];
                window.setTimeout(function () {
                    $(chev).toggleClass(
                        'glyphicon-chevron-down glyphicon-chevron-up'
                    );
                }, 100);
            });
            vm.panelClickersInitialised = true;
        }
        this.$nextTick(() => {
            vm.initialiseOrgContactTable();
        });
    },
    methods: {
        initialiseOrgContactTable: function () {
            let vm = this;
            if (vm.proposal && !vm.contacts_table_initialised) {
                vm.contacts_options.ajax.url = helpers.add_endpoint_json(
                    api_endpoints.organisations,
                    vm.proposal.org_applicant.id + '/contacts'
                );
                vm.contacts_table = $('#' + vm.contacts_table_id).DataTable(
                    vm.contacts_options
                );
                vm.contacts_table_initialised = true;
            }
        },
    },
};
</script>

<style lang="css" scoped></style>
