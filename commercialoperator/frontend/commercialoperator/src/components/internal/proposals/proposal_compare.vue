<template lang="html">
    <div v-if="proposal" id="internalProposal">
        <div class="row" style="padding-bottom: 50px">
            <h3>Application: {{ proposal.lodgement_number }}</h3>
            <h4>Application Type: {{ proposal.proposal_type }}</h4>

            <div class="col-md-1"></div>
            <div class="col-md-8">
                <div class="row">
                    <template
                        v-if="
                            canSeeSubmission ||
                            (!canSeeSubmission && showingProposal)
                        "
                    >
                        <div class="">
                            <div class="row">
                                <form
                                    :action="proposal_form_url"
                                    method="post"
                                    name="new_proposal"
                                    enctype="multipart/form-data"
                                >
                                    <ProposalTClass
                                        v-if="
                                            proposal &&
                                            proposal.application_type ==
                                                application_type_tclass
                                        "
                                        id="proposalStart"
                                        :proposal="proposal"
                                        :can-edit-activities="canEditActivities"
                                        :is_internal="true"
                                        :has-assessor-mode="hasAssessorMode"
                                    ></ProposalTClass>
                                    <input
                                        type="hidden"
                                        name="csrfmiddlewaretoken"
                                        :value="csrf_token"
                                    />
                                    <input
                                        type="hidden"
                                        name="schema"
                                        :value="JSON.stringify(proposal)"
                                    />
                                    <input
                                        type="hidden"
                                        name="proposal_id"
                                        :value="1"
                                    />
                                    <div
                                        class="row"
                                        style="margin-bottom: 50px"
                                    >
                                        <div
                                            v-if="hasAssessorMode"
                                            class="navbar navbar-fixed-bottom ms-auto align-items-end"
                                            style="background-color: #f5f5f5"
                                        >
                                            <div class="navbar-inner">
                                                <div
                                                    v-if="hasAssessorMode"
                                                    class="container-fluid"
                                                >
                                                    <p class="pull-right">
                                                        <button
                                                            class="btn btn-primary"
                                                            style="
                                                                margin-top: 5px;
                                                            "
                                                            @click.prevent="
                                                                save()
                                                            "
                                                        >
                                                            Save Changes
                                                        </button>
                                                    </p>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </template>
                </div>
            </div>
        </div>
        <ProposedDecline
            ref="proposed_decline"
            :processing_status="proposal.processing_status"
            :proposal_id="proposal.id"
            @refreshFromResponse="refreshFromResponse"
        ></ProposedDecline>
        <AmendmentRequest
            ref="amendment_request"
            :proposal_id="proposal.id"
            @refreshFromResponse="refreshFromResponse"
        ></AmendmentRequest>
        <ProposedApproval
            ref="proposed_approval"
            :processing_status="proposal.processing_status"
            :proposal_id="proposal.id"
            :proposal_type="proposal.proposal_type"
            :is-approval-level-document="isApprovalLevelDocument || null"
            @refreshFromResponse="refreshFromResponse"
        />
        <OnHold
            ref="on_hold"
            :processing_status="proposal.processing_status"
            :proposal_id="proposal.id"
            @refreshFromResponse="refreshFromResponse"
        ></OnHold>
        <WithQAOfficer
            ref="with_qa_officer"
            :processing_status="proposal.processing_status"
            :proposal_id="proposal.id"
        ></WithQAOfficer>
    </div>
</template>
<script>
import ProposedDecline from './proposal_proposed_decline.vue';
import AmendmentRequest from './amendment_request.vue';
import ProposedApproval from './proposed_issuance.vue';
import ProposalTClass from '@/components/form_tclass.vue';
import OnHold from './proposal_onhold.vue';
import WithQAOfficer from './proposal_qaofficer.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'InternalProposal',
    components: {
        ProposalTClass,
        ProposedDecline,
        AmendmentRequest,
        ProposedApproval,
        OnHold,
        WithQAOfficer,
    },
    filters: {
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
        },
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                `/api/proposal/${to.params.proposal_id}/internal_proposal.json`
            )
            .then(
                (res) => {
                    next((vm) => {
                        vm.proposal = res;
                        vm.original_proposal = helpers.copyObject(res);
                        vm.proposal.org_applicant.address =
                            vm.proposal.org_applicant.address != null
                                ? vm.proposal.org_applicant.address
                                : {};
                        vm.proposal.selected_trails_activities = [];
                        vm.proposal.selected_parks_activities = [];
                        vm.proposal.marine_parks_activities = [];
                    });
                },
                (err) => {
                    console.log(err);
                }
            );
    },
    beforeRouteUpdate: function (to, from, next) {
        helpers.fetchUrl(`/api/proposal/${to.params.proposal_id}.json`).then(
            (res) => {
                next((vm) => {
                    vm.proposal = res;
                    vm.original_proposal = helpers.copyObject(res);
                    vm.proposal.selected_trails_activities = [];
                    vm.proposal.selected_parks_activities = [];
                    vm.proposal.marine_parks_activities = [];
                });
            },
            (err) => {
                console.log(err);
            }
        );
    },
    data: function () {
        let vm = this;
        return {
            detailsBody: 'detailsBody' + uuid(),
            addressBody: 'addressBody' + uuid(),
            contactsBody: 'contactsBody' + uuid(),
            proposal: null,
            original_proposal: null,
            loading: [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            form: null,
            members: [],
            referral_recipient_groups: [],
            contacts_table_initialised: false,
            initialisedSelects: false,
            showingProposal: false,
            showingRequirements: false,
            state_options: ['requirements', 'processing'],
            contacts_table_id: uuid() + 'contacts-table',
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
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            comms_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/comms_log'
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/add_comms_log'
            ),
            logs_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/action_log'
            ),
            panelClickersInitialised: false,
            sendingReferral: false,
        };
    },
    computed: {
        history_url: function () {
            return (
                api_endpoints.site_url +
                '/history/filtered/' +
                this.proposal.id +
                '/?'
            );
        },
        contactsURL: function () {
            return this.proposal != null
                ? helpers.add_endpoint_json(
                      api_endpoints.organisations,
                      this.proposal.org_applicant.id + '/contacts'
                  )
                : '';
        },
        referralListURL: function () {
            return this.proposal != null
                ? helpers.add_endpoint_json(
                      api_endpoints.referrals,
                      'datatable_list'
                  ) +
                      '?proposal=' +
                      this.proposal.id
                : '';
        },
        isLoading: function () {
            return this.loading.length > 0;
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        proposal_form_url: function () {
            return this.proposal
                ? `/api/proposal/${this.proposal.id}/assessor_save.json`
                : '';
        },
        isFinalised: function () {
            return (
                this.proposal.processing_status == 'Declined' ||
                this.proposal.processing_status == 'Approved'
            );
        },
        canAssess: function () {
            return this.proposal &&
                this.proposal.assessor_mode.assessor_can_assess
                ? true
                : false;
        },
        hasAssessorMode: function () {
            return this.proposal &&
                this.proposal.assessor_mode.has_assessor_mode
                ? true
                : false;
        },
        canEditActivities: function () {
            return (
                this.proposal &&
                this.proposal.assessor_mode &&
                this.proposal.assessor_mode.assessor_mode &&
                this.proposal.can_edit_activities
            );
        },
        canAction: function () {
            if (this.proposal.processing_status == 'With Approver') {
                return this.proposal &&
                    (this.proposal.processing_status == 'With Approver' ||
                        this.proposal.processing_status == 'With Assessor' ||
                        this.proposal.processing_status ==
                            'With Assessor (Requirements)') &&
                    !this.isFinalised &&
                    !this.proposal.can_user_edit &&
                    (this.proposal.current_assessor.id ==
                        this.proposal.assigned_approver ||
                        this.proposal.assigned_approver == null) &&
                    this.proposal.assessor_mode.assessor_can_assess
                    ? true
                    : false;
            } else {
                return this.proposal &&
                    (this.proposal.processing_status == 'With QA Officer' ||
                        this.proposal.processing_status == 'On Hold' ||
                        this.proposal.processing_status == 'With Approver' ||
                        this.proposal.processing_status == 'With Assessor' ||
                        this.proposal.processing_status ==
                            'With Assessor (Requirements)') &&
                    !this.isFinalised &&
                    !this.proposal.can_user_edit &&
                    (this.proposal.current_assessor.id ==
                        this.proposal.assigned_officer ||
                        this.proposal.assigned_officer == null) &&
                    this.proposal.assessor_mode.assessor_can_assess
                    ? true
                    : false;
            }
        },
        canLimitedAction: function () {
            if (this.proposal.processing_status == 'With Approver') {
                return this.proposal &&
                    (this.proposal.processing_status == 'With Assessor' ||
                        this.proposal.processing_status == 'With Referral' ||
                        this.proposal.processing_status ==
                            'With Assessor (Requirements)') &&
                    !this.isFinalised &&
                    !this.proposal.can_user_edit &&
                    (this.proposal.current_assessor.id ==
                        this.proposal.assigned_approver ||
                        this.proposal.assigned_approver == null) &&
                    this.proposal.assessor_mode.assessor_can_assess
                    ? true
                    : false;
            } else {
                return this.proposal &&
                    (this.proposal.processing_status == 'With Assessor' ||
                        this.proposal.processing_status == 'With Referral' ||
                        this.proposal.processing_status ==
                            'With Assessor (Requirements)') &&
                    !this.isFinalised &&
                    !this.proposal.can_user_edit &&
                    (this.proposal.current_assessor.id ==
                        this.proposal.assigned_officer ||
                        this.proposal.assigned_officer == null) &&
                    this.proposal.assessor_mode.assessor_can_assess
                    ? true
                    : false;
            }
        },
        canSeeSubmission: function () {
            return (
                this.proposal &&
                this.proposal.processing_status !=
                    'With Assessor (Requirements)' &&
                this.proposal.processing_status != 'With Approver' &&
                !this.isFinalised
            );
        },
        isApprovalLevelDocument: function () {
            return this.proposal &&
                this.proposal.processing_status == 'With Approver' &&
                this.proposal.approval_level != null &&
                this.proposal.approval_level_document == null
                ? true
                : false;
        },
        isQAOfficerAssessmentCompleted: function () {
            return this.proposal &&
                this.proposal.qaofficer_referrals &&
                this.proposal.qaofficer_referrals.length != 0 &&
                this.proposal.qaofficer_referrals[0].processing_status ==
                    'Completed'
                ? true
                : false;
        },
        QAOfficerAssessmentCompletedBy: function () {
            return this.isQAOfficerAssessmentCompleted
                ? this.proposal.qaofficer_referrals[0].qaofficer
                : '';
        },
        application_type_tclass: function () {
            return api_endpoints.t_class;
        },
        application_type_filming: function () {
            return api_endpoints.filming;
        },
        application_type_event: function () {
            return api_endpoints.event;
        },
    },
    watch: {},
    mounted: function () {
        let vm = this;
        vm.fetchReferralRecipientGroups();
        vm.initialiseSelects();
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.form = document.forms.new_proposal;
        });
    },
    methods: {
        initialiseOrgContactTable: function () {
            let vm = this;
            console.log('i am here original');
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
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        proposedDecline: function () {
            this.save_wo();
            this.$refs.proposed_decline.decline =
                this.proposal.proposaldeclineddetails != null
                    ? helpers.copyObject(this.proposal.proposaldeclineddetails)
                    : {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        proposedApproval: function () {
            this.$refs.proposed_approval.approval =
                this.proposal.proposed_issuance_approval != null
                    ? helpers.copyObject(
                          this.proposal.proposed_issuance_approval
                      )
                    : {};
            this.$refs.proposed_approval.isModalOpen = true;
        },
        issueProposal: function () {
            this.$refs.proposed_approval.approval =
                this.proposal.proposed_issuance_approval != null
                    ? helpers.copyObject(
                          this.proposal.proposed_issuance_approval
                      )
                    : {};
            this.$refs.proposed_approval.state = 'final_approval';
            this.$refs.proposed_approval.isApprovalLevelDocument =
                this.isApprovalLevelDocument;
            this.$refs.proposed_approval.isModalOpen = true;
        },
        declineProposal: function () {
            this.$refs.proposed_decline.decline =
                this.proposal.proposaldeclineddetails != null
                    ? helpers.copyObject(this.proposal.proposaldeclineddetails)
                    : {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        amendmentRequest: function () {
            this.save_wo();
            let values = '';
            $('.deficiency').each((i, d) => {
                values +=
                    $(d).val() != ''
                        ? `Question - ${$(d).data('question')}\nDeficiency - ${$(d).val()}\n\n`
                        : '';
            });
            this.$refs.amendment_request.amendment.text = values;

            this.$refs.amendment_request.isModalOpen = true;
        },
        onHold: function () {
            this.save_wo();
            this.$refs.on_hold.isModalOpen = true;
        },
        withQAOfficer: function () {
            this.save_wo();
            this.$refs.with_qa_officer.isModalOpen = true;
        },
        save: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            formData.append(
                'selected_parks_activities',
                JSON.stringify(vm.proposal.selected_parks_activities)
            );
            formData.append(
                'selected_trails_activities',
                JSON.stringify(vm.proposal.selected_trails_activities)
            );
            formData.append(
                'marine_parks_activities',
                JSON.stringify(vm.proposal.marine_parks_activities)
            );
            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        swal.fire({
                            title: 'Saved',
                            text: 'Your application has been saved',
                            icon: 'success',
                        });
                    },
                    () => {}
                );
        },
        save_wo: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            formData.append(
                'selected_parks_activities',
                JSON.stringify(vm.proposal.selected_parks_activities)
            );
            formData.append(
                'selected_trails_activities',
                JSON.stringify(vm.proposal.selected_trails_activities)
            );
            formData.append(
                'marine_parks_activities',
                JSON.stringify(vm.proposal.marine_parks_activities)
            );
            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {},
                    () => {}
                );
        },

        toggleProposal: function () {
            this.showingProposal = !this.showingProposal;
        },
        toggleRequirements: function () {
            this.showingRequirements = !this.showingRequirements;
        },
        updateAssignedOfficerSelect: function () {
            let vm = this;
            if (vm.proposal.processing_status == 'With Approver') {
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_approver);
                $(vm.$refs.assigned_officer).trigger('change');
            } else {
                $(vm.$refs.assigned_officer).val(vm.proposal.assigned_officer);
                $(vm.$refs.assigned_officer).trigger('change');
            }
        },
        assignRequestUser: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        vm.proposal.id + '/assign_request_user'
                    )
                )
                .then(
                    (response) => {
                        vm.proposal = response;
                        vm.original_proposal = helpers.copyObject(response);
                        vm.updateAssignedOfficerSelect();
                    },
                    (error) => {
                        vm.proposal = helpers.copyObject(vm.original_proposal);
                        vm.updateAssignedOfficerSelect();
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        refreshFromResponse: function (response) {
            let vm = this;
            vm.original_proposal = helpers.copyObject(response);
            vm.proposal = helpers.copyObject(response);
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        assignTo: function () {
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.processing_status == 'With Approver') {
                unassign =
                    vm.proposal.assigned_approver != null &&
                    vm.proposal.assigned_approver != 'undefined'
                        ? false
                        : true;
                data = { assessor_id: vm.proposal.assigned_approver };
            } else {
                unassign =
                    vm.proposal.assigned_officer != null &&
                    vm.proposal.assigned_officer != 'undefined'
                        ? false
                        : true;
                data = { assessor_id: vm.proposal.assigned_officer };
            }
            if (!unassign) {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal.id + '/assign_to'
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
                        (response) => {
                            vm.proposal = response;
                            vm.original_proposal = helpers.copyObject(response);
                            vm.updateAssignedOfficerSelect();
                        },
                        (error) => {
                            vm.proposal = helpers.copyObject(
                                vm.original_proposal
                            );
                            vm.proposal.org_applicant.address =
                                vm.proposal.org_applicant.address != null
                                    ? vm.proposal.org_applicant.address
                                    : {};
                            vm.updateAssignedOfficerSelect();
                            swal.fire({
                                title: 'Application Error',
                                text: helpers.apiVueResourceError(error),
                                icon: 'error',
                            });
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal.id + '/unassign'
                        )
                    )
                    .then(
                        (response) => {
                            vm.proposal = response;
                            vm.original_proposal = helpers.copyObject(response);
                            vm.updateAssignedOfficerSelect();
                        },
                        (error) => {
                            vm.proposal = helpers.copyObject(
                                vm.original_proposal
                            );
                            vm.proposal.org_applicant.address =
                                vm.proposal.org_applicant.address != null
                                    ? vm.proposal.org_applicant.address
                                    : {};
                            vm.updateAssignedOfficerSelect();
                            swal.fire({
                                title: 'Application Error',
                                text: helpers.apiVueResourceError(error),
                                icon: 'error',
                            });
                        }
                    );
            }
        },
        switchStatus: function (status) {
            let vm = this;
            if (
                vm.proposal.processing_status == 'With Assessor' &&
                status == 'with_assessor_requirements'
            ) {
                let formData = new FormData(vm.form);
                formData.append(
                    'selected_parks_activities',
                    JSON.stringify(vm.proposal.selected_parks_activities)
                );
                formData.append(
                    'selected_trails_activities',
                    JSON.stringify(vm.proposal.selected_trails_activities)
                );
                formData.append(
                    'marine_parks_activities',
                    JSON.stringify(vm.proposal.marine_parks_activities)
                );
                helpers
                    .fetchUrl(vm.proposal_form_url, {
                        method: 'POST',
                        body: formData,
                    })
                    .then(
                        () => {
                            //save Proposal before changing status so that unsaved assessor data is saved.
                            let data = {
                                status: status,
                                approver_comment: vm.approver_comment,
                            };
                            helpers
                                .fetchUrl(
                                    helpers.add_endpoint_json(
                                        api_endpoints.proposals,
                                        vm.proposal.id + '/switch_status'
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
                                    (response) => {
                                        vm.proposal = response;
                                        vm.original_proposal =
                                            helpers.copyObject(response);
                                        vm.approver_comment = '';
                                        vm.$nextTick(() => {
                                            vm.initialiseAssignedOfficerSelect(
                                                true
                                            );
                                            vm.updateAssignedOfficerSelect();
                                        });
                                    },
                                    (error) => {
                                        vm.proposal = helpers.copyObject(
                                            vm.original_proposal
                                        );
                                        vm.proposal.org_applicant.address =
                                            vm.proposal.org_applicant.address !=
                                            null
                                                ? vm.proposal.org_applicant
                                                      .address
                                                : {};
                                        swal.fire({
                                            title: 'Application Error',
                                            text: helpers.apiVueResourceError(
                                                error
                                            ),
                                            icon: 'error',
                                        });
                                    }
                                );
                        },
                        () => {}
                    );
            }

            //if approver is pushing back proposal to Assessor then navigate the approver back to dashboard page
            if (
                vm.proposal.processing_status == 'With Approver' &&
                (status == 'with_assessor_requirements' ||
                    status == 'with_assessor')
            ) {
                let data = {
                    status: status,
                    approver_comment: vm.approver_comment,
                };
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal.id + '/switch_status'
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
                        (response) => {
                            vm.proposal = response;
                            vm.original_proposal = helpers.copyObject(response);
                            vm.approver_comment = '';
                            vm.$nextTick(() => {
                                vm.initialiseAssignedOfficerSelect(true);
                                vm.updateAssignedOfficerSelect();
                            });
                            vm.$router.push({ path: '/internal' });
                        },
                        (error) => {
                            vm.proposal = helpers.copyObject(
                                vm.original_proposal
                            );
                            swal.fire({
                                title: 'Application Error',
                                text: helpers.apiVueResourceError(error),
                                icon: 'error',
                            });
                        }
                    );
            } else {
                let data = {
                    status: status,
                    approver_comment: vm.approver_comment,
                };
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposals,
                            vm.proposal.id + '/switch_status'
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
                        (response) => {
                            vm.proposal = response;
                            vm.original_proposal = helpers.copyObject(response);
                            vm.approver_comment = '';
                            vm.$nextTick(() => {
                                vm.initialiseAssignedOfficerSelect(true);
                                vm.updateAssignedOfficerSelect();
                            });
                        },
                        (error) => {
                            vm.proposal = helpers.copyObject(
                                vm.original_proposal
                            );
                            swal.fire({
                                title: 'Application Error',
                                text: helpers.apiVueResourceError(error),
                                icon: 'error',
                            });
                        }
                    );
            }
        },
        fetchReferralRecipientGroups: function () {
            let vm = this;
            vm.loading.push('Loading Referral Recipient Groups');
            helpers.fetchUrl(api_endpoints.referral_recipient_groups).then(
                (response) => {
                    vm.referral_recipient_groups = response;
                    vm.loading.splice('Loading Referral Recipient Groups', 1);
                },
                (error) => {
                    console.log(error);
                    vm.loading.splice('Loading Referral Recipient Groups', 1);
                }
            );
        },

        initialiseAssignedOfficerSelect: function (reinit = false) {
            let vm = this;
            if (reinit) {
                $(vm.$refs.assigned_officer).data('select2')
                    ? $(vm.$refs.assigned_officer).select2('destroy')
                    : '';
            }
            // Assigned officer select
            $(vm.$refs.assigned_officer)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Officer',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    if (vm.proposal.processing_status == 'With Approver') {
                        vm.proposal.assigned_approver = selected.val();
                    } else {
                        vm.proposal.assigned_officer = selected.val();
                    }
                    vm.assignTo();
                })
                .on('select2:unselecting', function () {
                    var self = $(this);
                    setTimeout(() => {
                        self.select2('close');
                    }, 0);
                })
                .on('select2:unselect', function (e) {
                    // eslint-disable-next-line no-unused-vars
                    var selected = $(e.currentTarget);
                    if (vm.proposal.processing_status == 'With Approver') {
                        vm.proposal.assigned_approver = null;
                    } else {
                        vm.proposal.assigned_officer = null;
                    }
                    vm.assignTo();
                });
        },
        initialiseSelects: function () {
            let vm = this;
            if (!vm.initialisedSelects) {
                //$(vm.$refs.department_users).select2({
                $(vm.$refs.referral_recipient_groups)
                    .select2({
                        theme: 'bootstrap-5',
                        allowClear: true,
                        placeholder: 'Select Referral',
                    })
                    .on('select2:select', function (e) {
                        var selected = $(e.currentTarget);
                        vm.selected_referral = selected.val();
                    })
                    .on('select2:unselect', function (e) {
                        // eslint-disable-next-line no-unused-vars
                        var selected = $(e.currentTarget);
                        vm.selected_referral = '';
                    });
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function () {
            let vm = this;
            let formData = new FormData(vm.form);
            formData.append(
                'selected_parks_activities',
                JSON.stringify(vm.proposal.selected_parks_activities)
            );
            formData.append(
                'selected_trails_activities',
                JSON.stringify(vm.proposal.selected_trails_activities)
            );
            formData.append(
                'marine_parks_activities',
                JSON.stringify(vm.proposal.marine_parks_activities)
            );

            vm.sendingReferral = true;
            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        let data = {
                            email_group: vm.selected_referral,
                            text: vm.referral_text,
                        };
                        helpers
                            .fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.proposals,
                                    vm.proposal.id + '/assessor_send_referral'
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
                                (response) => {
                                    vm.sendingReferral = false;
                                    vm.original_proposal =
                                        helpers.copyObject(response);
                                    vm.proposal = response;
                                    swal.fire({
                                        title: 'Referral Sent',
                                        text:
                                            'The referral has been sent to ' +
                                            vm.selected_referral,
                                        icon: 'success',
                                    });
                                    $(vm.$refs.referral_recipient_groups)
                                        .val(null)
                                        .trigger('change');
                                    vm.selected_referral = '';
                                    vm.referral_text = '';
                                },
                                (error) => {
                                    console.log(error);
                                    swal.fire({
                                        title: 'Referral Error',
                                        text: helpers.apiVueResourceError(
                                            error
                                        ),
                                        icon: 'error',
                                    });
                                    vm.sendingReferral = false;
                                }
                            );
                    },
                    () => {}
                );
        },
        remindReferral: function (r) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        r.id + '/remind'
                    )
                )
                .then(
                    (response) => {
                        vm.original_proposal = helpers.copyObject(response);
                        vm.proposal = response;
                        swal.fire({
                            title: 'Referral Reminder',
                            text: 'A reminder has been sent to ' + r.referral,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        resendReferral: function (r) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        r.id + '/resend'
                    )
                )
                .then(
                    (response) => {
                        vm.original_proposal = helpers.copyObject(response);
                        vm.proposal = response;
                        swal.fire({
                            title: 'Referral Resent',
                            text:
                                'The referral has been resent to ' + r.referral,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        recallReferral: function (r) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        r.id + '/recall'
                    )
                )
                .then(
                    (response) => {
                        vm.original_proposal = helpers.copyObject(response);
                        vm.proposal = response;
                        swal.fire({
                            title: 'Referral Recall',
                            text:
                                'The referall has been recalled from ' +
                                r.referral,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
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
.separator {
    border: 1px solid;
    margin-top: 15px;
    margin-bottom: 10px;
    width: 100%;
}
</style>
