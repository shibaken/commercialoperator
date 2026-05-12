<template id="district_proposal_approval">
    <div>
        <template v-if="isFinalised">
            <div
                v-if="district_proposal.processing_status == 'Approved'"
                class="col-md-12 alert alert-success"
            >
                <p>
                    The Lawful Authority has been issued and has been emailed to
                    {{ district_proposal.proposal.applicant }}
                </p>
                <p>
                    Expiry date:
                    {{
                        district_proposal.proposed_issuance_approval.expiry_date
                    }}
                </p>
                <p>
                    Lawful Authority:
                    <a target="_blank" :href="district_proposal.proposal.permit"
                        >lawful_authority.pdf</a
                    >
                </p>
            </div>
            <div v-else class="col-md-12 alert alert-warning">
                <p>
                    The application was declined. The decision was emailed to
                    {{ district_proposal.proposal.applicant }}
                </p>
            </div>
        </template>

        <div class="col-md-12">
            <div class="row">
                    <FormSection
                        :form-collapse="false"
                        :label="!isFinalised ? 'Proposed Decision' : 'Decision'"
                        index="proposed_decision"
                        subtitle=""
                    >
                        <div class="row">
                            <div class="col-sm-12">
                                <template
                                    v-if="
                                        !district_proposal.proposed_decline_status
                                    "
                                >
                                    <template v-if="isFinalised">
                                        <p><strong>Decision: Issue</strong></p>
                                        <p>
                                            <strong
                                                >Start date:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .start_date
                                                }}</strong
                                            >
                                        </p>
                                        <p>
                                            <strong
                                                >Expiry date:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .expiry_date
                                                }}</strong
                                            >
                                        </p>
                                        <p>
                                            <strong
                                                >CC emails:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .cc_email
                                                }}</strong
                                            >
                                        </p>
                                    </template>
                                    <template v-else>
                                        <p>
                                            <strong
                                                >Proposed decision:
                                                Issue</strong
                                            >
                                        </p>
                                        <p>
                                            <strong
                                                >Proposed start date:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .start_date
                                                }}</strong
                                            >
                                        </p>
                                        <p>
                                            <strong
                                                >Proposed expiry date:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .expiry_date
                                                }}</strong
                                            >
                                        </p>
                                        <p>
                                            <strong
                                                >Proposed cc emails:
                                                {{
                                                    district_proposal
                                                        .proposed_issuance_approval
                                                        .cc_email
                                                }}</strong
                                            >
                                        </p>
                                    </template>
                                </template>
                                <template v-else>
                                    <strong v-if="!isFinalised"
                                        >Proposed decision: Decline</strong
                                    >
                                    <strong v-else>Decision: Decline</strong>
                                </template>
                            </div>
                        </div>
                    </FormSection>
            </div>
        </div>
    </div>
</template>
<script>
import { api_endpoints, helpers } from '@/utils/hooks';
import FormSection from '@/components/forms/section_toggle.vue';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'InternalProposalApproval',
    components: {
        FormSection,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        district_proposal: Object,
    },
    data: function () {
        return {
            proposedDecision: 'district_proposal-decision-' + uuid(),
            proposedLevel: 'district_proposal-level-' + uuid(),
            uploadedFile: null,
        };
    },
    computed: {
        isFinalised: function () {
            return (
                this.district_proposal.processing_status == 'Approved' ||
                this.district_proposal.processing_status == 'Declined'
            );
        },
    },
    watch: {},
    mounted: function () {},
    methods: {
        readFile: function () {
            let vm = this;
            let _file = null;
            var input = $(vm.$refs.uploadedFile)[0];
            if (input.files && input.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(input.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = input.files[0];
            }
            vm.uploadedFile = _file;
            vm.save();
        },
        removeFile: function () {
            let vm = this;
            vm.uploadedFile = null;
            vm.save();
        },
        save: function () {
            let vm = this;
            let data = new FormData(vm.form);
            data.append('approval_level_document', vm.uploadedFile);
            if (vm.district_proposal.approval_level_document) {
                data.append(
                    'approval_level_document_name',
                    vm.district_proposal.approval_level_document[0]
                );
            }
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.district_proposals,
                        vm.district_proposal.id + '/approval_level_document'
                    ),
                    {
                        method: 'POST',
                        body: data,
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                )
                .then(
                    (res) => {
                        vm.district_proposal = res;
                        vm.$emit('refreshFromResponse', res);
                    },
                    (err) => {
                        swal.fire({
                            title: 'Submit Error',
                            text: helpers.apiVueResourceError(err),
                            icon: 'error',
                        });
                    }
                );
        },
        uploadedFileName: function () {
            return this.uploadedFile != null ? this.uploadedFile.name : '';
        },
        addRequirement() {
            this.$refs.requirement_detail.isModalOpen = true;
        },
        removeRequirement(_id) {
            let vm = this;
            swal.fire({
                title: 'Remove Requirement',
                text: 'Are you sure you want to remove this requirement?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Remove Requirement',
                confirmButtonColor: '#d9534f',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.district_proposal_requirements,
                                _id
                            ),
                            {
                                method: 'DELETE',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                vm.$refs.requirements_datatable.vmDataTable.ajax.reload();
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
    },
};
</script>
<style scoped></style>
