<template lang="html">
    <div v-if="proposal" id="internalReferral" class="container">
        <div class="row">
            <h3>Application: {{ proposal.lodgement_number }}</h3>
            <h4>Application Type: {{ proposal.proposal_type }}</h4>
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
                                <div class="col-sm-12">
                                    <strong>Submitted by</strong><br />
                                    {{ proposal.submitter.first_name }}
                                    {{ proposal.submitter.last_name }}
                                </div>
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Lodged on</strong><br />
                                    {{ formatDate(proposal.lodgement_date) }}
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
                                    {{ proposal.processing_status }}
                                </div>
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                                <div
                                    v-if="!isFinalised"
                                    class="col-sm-12 top-buffer-s"
                                >
                                    <strong>Currently assigned to</strong><br />
                                    <div class="form-group">
                                        <select
                                            ref="assigned_officer"
                                            v-model="referral.assigned_officer"
                                            :disabled="!referral.can_process"
                                            class="form-control"
                                        >
                                            <option
                                                v-for="member in referral.allowed_assessors"
                                                :key="member.id"
                                                :value="member.id"
                                            >
                                                {{ member.first_name }}
                                                {{ member.last_name }}
                                            </option>
                                        </select>
                                        <a
                                            v-if="
                                                referral.can_process &&
                                                referral.assigned_officer !=
                                                    referral.current_assessor.id
                                            "
                                            class="actionBtn pull-right"
                                            @click.prevent="assignRequestUser()"
                                            >Assign to me</a
                                        >
                                    </div>
                                </div>
                                <div class="col-sm-12 top-buffer-s">
                                    <table class="table small-table">
                                        <thead>
                                            <tr>
                                                <th>Referral</th>
                                                <th>Status/Action</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr
                                                v-for="r in referral.latest_referrals"
                                                :key="r.id"
                                            >
                                                <td>
                                                    <small
                                                        ><strong>{{
                                                            r.referral
                                                        }}</strong></small
                                                    ><br />
                                                    <small
                                                        ><strong>{{
                                                            formatDate(
                                                                r.lodged_on
                                                            )
                                                        }}</strong></small
                                                    >
                                                </td>
                                                <td>
                                                    <small
                                                        ><strong>{{
                                                            r.processing_status
                                                        }}</strong></small
                                                    ><br />
                                                    <template
                                                        v-if="
                                                            !isFinalised &&
                                                            referral.referral ==
                                                                proposal
                                                                    .current_assessor
                                                                    .id
                                                        "
                                                    >
                                                        <template
                                                            v-if="
                                                                r.processing_status ==
                                                                'Awaiting'
                                                            "
                                                        >
                                                            <small
                                                                ><a
                                                                    href="#"
                                                                    @click.prevent="
                                                                        remindReferral(
                                                                            r
                                                                        )
                                                                    "
                                                                    >Remind</a
                                                                >
                                                                /
                                                                <a
                                                                    href="#"
                                                                    @click.prevent="
                                                                        recallReferral(
                                                                            r
                                                                        )
                                                                    "
                                                                    >Recall</a
                                                                ></small
                                                            >
                                                        </template>
                                                        <template v-else>
                                                            <small
                                                                ><a
                                                                    href="#"
                                                                    @click.prevent="
                                                                        resendReferral(
                                                                            r
                                                                        )
                                                                    "
                                                                    >Resend</a
                                                                ></small
                                                            >
                                                        </template>
                                                    </template>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    <MoreReferrals
                                        :proposal="proposal"
                                        :can-action="
                                            !isFinalised &&
                                            referral.referral ==
                                                proposal.current_assessor.id
                                        "
                                        :is-finalised="isFinalised"
                                        :referral_url="referralListURL"
                                        @refreshFromResponse="
                                            refreshFromResponse
                                        "
                                    />
                                </div>
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                                <div class="col-sm-12">
                                    <strong>Application</strong><br />
                                    <a
                                        v-if="!showingProposal"
                                        class="actionBtn"
                                        @click.prevent="toggleProposal()"
                                        >Show Application</a
                                    >
                                    <a
                                        v-else
                                        class="actionBtn"
                                        @click.prevent="toggleProposal()"
                                        >Hide Application</a
                                    >
                                </div>
                                <div class="col-sm-12">
                                    <div class="separator"></div>
                                </div>
                                <div
                                    v-if="canComplete"
                                    class="col-sm-12 top-buffer-s"
                                >
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <strong>Action</strong><br />
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    @click.prevent="
                                                        completeReferral2()
                                                    "
                                                >
                                                    Complete Referral Task</button
                                                ><br />
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <CompleteReferral
                    ref="complete_referral"
                    :referral_id="referral.id"
                    :proposal_id="referral.proposal.id"
                    @refreshFromResponse="refreshFromResponse"
                ></CompleteReferral>
            </div>

            <div class="col-md-1"></div>
            <div class="col-md-8">
                <div class="row">
                    <Requirements
                        :proposal="proposal"
                        :has-referral-mode="hasReferralMode"
                        :referral_group="referral.referral_group"
                    />
                    <Assessment
                        :proposal="proposal"
                        :assessment="referral.referral_assessment"
                        :has-referral-mode="hasReferralMode"
                        :is_internal="is_internal"
                        :is_referral="is_referral"
                    ></Assessment>
                    <div v-if="showingProposal" class="col-md-12">
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
                                        proposal_parks &&
                                        proposal.application_type ==
                                            application_type_tclass
                                    "
                                    id="proposalStart"
                                    :proposal="proposal"
                                    :can-edit-activities="false"
                                    :is_external="false"
                                    :is_referral="true"
                                    :referral="referral"
                                    :has-referral-mode="hasReferralMode"
                                    :proposal_parks="proposal_parks"
                                ></ProposalTClass>
                                <ProposalFilming
                                    v-else-if="
                                        proposal &&
                                        proposal.application_type ==
                                            application_type_filming
                                    "
                                    id="proposalStart"
                                    ref="proposal_filming"
                                    :proposal="proposal"
                                    :can-edit-activities="false"
                                    :is_external="false"
                                    :proposal_parks="proposal_parks"
                                    :is_referral="true"
                                    :referral="referral"
                                    :has-referral-mode="hasReferralMode"
                                ></ProposalFilming>
                                <ProposalEvent
                                    v-else-if="
                                        proposal &&
                                        proposal.application_type ==
                                            application_type_event
                                    "
                                    id="proposalStart"
                                    ref="proposal_event"
                                    :proposal="proposal"
                                    :can-edit-activities="false"
                                    :is_external="false"
                                    :proposal_parks="proposal_parks"
                                    :is_referral="true"
                                    :referral="referral"
                                    :has-referral-mode="hasReferralMode"
                                ></ProposalEvent>
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
                                    v-if="
                                        !proposal.can_user_edit && !isFinalised
                                    "
                                    class="navbar navbar-fixed-bottom ms-auto align-items-end"
                                    style="background-color: #f5f5f5"
                                >
                                    <div class="navbar-inner">
                                        <div
                                            v-if="!isFinalised"
                                            class="container-fluid"
                                        >
                                            <p class="pull-right">
                                                <button
                                                    class="btn btn-primary"
                                                    style="margin-top: 5px"
                                                    @click.prevent="save()"
                                                >
                                                    Save Changes
                                                </button>
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import ProposalTClass from '@/components/form_tclass.vue';
import ProposalFilming from '@/components/form_filming.vue';
import ProposalEvent from '@/components/form_event.vue';
import CommsLogs from '@common-utils/comms_logs.vue';
import MoreReferrals from '@common-utils/more_referrals.vue';
import CompleteReferral from './complete_referral.vue';
import Requirements from '@/components/internal/proposals/proposal_requirements.vue';
import Assessment from '@/components/common/tclass/assessment.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Referral',
    components: {
        CommsLogs,
        MoreReferrals,
        CompleteReferral,
        ProposalTClass,
        ProposalFilming,
        ProposalEvent,
        Requirements,
        Assessment,
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                helpers.add_endpoint_json(
                    api_endpoints.referrals,
                    to.params.referral_id
                )
            )
            .then(
                (res) => {
                    next((vm) => {
                        vm.referral = res;
                        vm.fetchProposalParks(vm.referral.proposal.id);
                        vm.referral.proposal.org_applicant.organisation_address =
                            vm.proposal.org_applicant.organisation_address !=
                            null
                                ? vm.proposal.org_applicant.organisation_address
                                : {};
                    });
                },
                (err) => {
                    console.log(err);
                }
            );
    },
    beforeRouteUpdate: function (to, from, next) {
        helpers
            .fetchUrl(
                `/api/proposal/${to.params.proposal_id}/referral_proposal.json`
            )
            .then(
                (res) => {
                    next((vm) => {
                        vm.referral = res;
                        vm.fetchProposalParks(vm.referral.proposal.id);
                        vm.referral.proposal.org_applicant.organisation_address =
                            vm.referral.proposal.org_applicant
                                .organisation_address != null
                                ? vm.referral.proposal.org_applicant
                                      .organisation_address
                                : {};
                    });
                },
                (err) => {
                    console.log(err);
                }
            );
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        is_internal: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_referral: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            detailsBody: 'detailsBody' + uuid(),
            addressBody: 'addressBody' + uuid(),
            contactsBody: 'contactsBody' + uuid(),
            //"proposal": null,
            // referral: null,
            referral_sent_list: null,
            loading: [],
            selected_referral: '',
            referral_text: '',
            referral_comment: '',
            proposal_parks: null,
            sendingReferral: false,
            showingProposal: false,
            form: null,
            members: [],
            referral_recipient_groups: [],
            contacts_table_initialised: false,
            initialisedSelects: false,
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
            logs_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/action_log'
            ),
            comms_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/comms_log'
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/add_comms_log'
            ),
            panelClickersInitialised: false,
            referral: {},
        };
    },
    computed: {
        proposal: {
            get: function () {
                return this.referral != null && this.referral != 'undefined'
                    ? this.referral.proposal
                    : null;
            },
            set: function (value) {
                this.referral.proposal = value;
                this.proposal.org_applicant.organisation_address =
                    this.proposal.org_applicant.organisation_address != null
                        ? this.proposal.org_applicant.organisation_address
                        : {};
            },
        },
        hasReferralMode: function () {
            return this.referral && this.referral.can_process ? true : false;
        },
        contactsURL: function () {
            return this.proposal != null
                ? helpers.add_endpoint_json(
                      api_endpoints.organisations,
                      this.proposal.applicant.id + '/contacts'
                  )
                : '';
        },
        referralListURL: function () {
            return this.referral != null
                ? helpers.add_endpoint_json(
                      api_endpoints.referrals,
                      this.referral.id + '/referral_list'
                  )
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
            return !(
                this.referral != null &&
                this.referral.processing_status == 'Awaiting'
            );
        },
        referral_form_url: function () {
            return this.referral
                ? `/api/referrals/${this.referral.id}/complete_referral.json`
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
        canComplete: function () {
            let vm = this;
            if (vm.referral.can_process && vm.referral.can_be_completed) {
                if (vm.referral.assigned_officer) {
                    if (
                        vm.referral.assigned_officer ==
                        vm.referral.current_assessor.id
                    ) {
                        return true;
                    }
                } else return true;
            }
            return false;
        },
    },
    watch: {},
    mounted: function () {
        let vm = this;
        vm.fetchProposalGroupMembers();
        vm.fetchReferralRecipientGroups();
        vm.initialiseSelects();
    },
    updated: function () {
        let vm = this;
        if (!vm.panelClickersInitialised) {
            $('.panelClicker[data-bs-toggle="collapse"]').on('click', function () {
                var chev = $(this).children()[0];
                window.setTimeout(function () {
                    $(chev).toggleClass(
                        'fa-chevron-down fa-chevron-up'
                    );
                }, 100);
            });
            vm.panelClickersInitialised = true;
        }
        this.$nextTick(() => {
            vm.initialiseOrgContactTable();
            vm.form = document.forms.new_proposal;
        });
    },
    methods: {
        completeReferral2: function () {
            this.$refs.complete_referral.isModalOpen = true;
        },
        toggleProposal: function () {
            this.showingProposal = !this.showingProposal;
        },
        save_wo: function () {
            let vm = this;
            let data = { email: vm.selected_referral, text: vm.referral_text };
            helpers
                .fetchUrl(vm.referral_form_url, {
                    method: 'POST',
                    body: JSON.stringify(data),
                })
                .then(
                    () => {},
                    () => {}
                );
        },

        refreshFromResponse: function (response) {
            let vm = this;
            vm.proposal = helpers.copyObject(response);
        },
        initialiseOrgContactTable: function () {
            let vm = this;
            if (vm.proposal && !vm.contacts_table_initialised) {
                vm.contacts_options.ajax.url = helpers.add_endpoint_json(
                    api_endpoints.organisations,
                    vm.proposal.applicant.id + '/contacts'
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
            this.$refs.proposed_decline.isModalOpen = true;
        },
        ammendmentRequest: function () {
            this.$refs.ammendment_request.isModalOpen = true;
        },
        save: function () {
            let vm = this;
            let formData = new FormData(vm.form);
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
        assignTo: function () {
            let vm = this;
            if (vm.referral.assigned_officer == null) {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.referrals,
                            vm.referral.id + '/unassign'
                        )
                    )
                    .then(
                        (response) => {
                            vm.referral = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            } else {
                let data = { user_id: vm.referral.assigned_officer };
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.referrals,
                            vm.referral.id + '/assign_to'
                        ),
                        {
                            method: 'POST',
                            body: JSON.stringify(data),
                        }
                    )
                    .then(
                        (response) => {
                            vm.referral = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            }
        },
        fetchProposalGroupMembers: function () {
            let vm = this;
            vm.loading.push('Loading Application Group Members');
            helpers
                .fetchUrl(api_endpoints.organisation_access_group_members)
                .then(
                    (response) => {
                        vm.members = response;
                        vm.loading.splice(
                            'Loading Application Group Members',
                            1
                        );
                    },
                    (error) => {
                        console.log(error);
                        vm.loading.splice(
                            'Loading Application Group Members',
                            1
                        );
                    }
                );
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

        initialiseSelects: function () {
            let vm = this;
            if (!vm.initialisedSelects) {
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
                        var selected = $(e.currentTarget);
                        vm.selected_referral = selected.val();
                    });
                // Assigned officer select
                $(vm.$refs.assigned_officer)
                    .select2({
                        theme: 'bootstrap-5',
                        allowClear: true,
                        placeholder: 'Select Officer',
                    })
                    .on('select2:select', function (e) {
                        var selected = $(e.currentTarget);
                        vm.$emit('input', selected[0]);
                    })
                    .on('select2:unselect', function (e) {
                        var selected = $(e.currentTarget);
                        vm.$emit('input', selected[0]);
                    });
                vm.initialiseAssignedOfficerSelect();
                vm.initialisedSelects = true;
            }
        },
        sendReferral: function () {
            let vm = this;

            vm.sendingReferral = true;
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
                    }
                )
                .then(
                    (response) => {
                        vm.sendingReferral = false;
                        vm.proposal = helpers.copyObject(response);
                        swal.fire({
                            title: 'Referral Sent',
                            text:
                                'The referral has been sent to ' +
                                vm.selected_referral,
                            icon: 'success',
                        });
                        vm.fetchProposalParks(vm.proposal.id);
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
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                        vm.sendingReferral = false;
                        vm.selected_referral = '';
                        vm.referral_text = '';
                    }
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
                    () => {
                        vm.fetchReferral(vm.referral.id);
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
                    () => {
                        vm.fetchReferral(vm.referral.id);
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
                    () => {
                        vm.fetchReferral(vm.referral.id);

                        swal.fire({
                            title: 'Referral Recall',
                            text:
                                'The referral has been recalled from ' +
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
        updateAssignedOfficerSelect: function () {
            let vm = this;
            $(vm.$refs.assigned_officer).val(vm.referral.assigned_officer);
            $(vm.$refs.assigned_officer).trigger('change');
        },
        assignRequestUser: function () {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        vm.referral.id + '/assign_request_user'
                    )
                )
                .then(
                    (response) => {
                        vm.referral = response;
                        vm.updateAssignedOfficerSelect();
                    },
                    (error) => {
                        vm.updateAssignedOfficerSelect();
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        fetchreferrallist: function (referral_id) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        referral_id + '/referral_list'
                    )
                )
                .then(
                    (response) => {
                        vm.referral_sent_list = response;
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        fetchReferral: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        vm.referral.id
                    )
                )
                .then(
                    (res) => {
                        vm.referral = res;
                        vm.fetchProposalParks(vm.referral.proposal.id);
                        vm.referral.proposal.org_applicant.organisation_address =
                            vm.proposal.org_applicant.organisation_address !=
                            null
                                ? vm.proposal.org_applicant.organisation_address
                                : {};
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        fetchProposalParks: function (proposal_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        proposal_id + '/parks_and_trails'
                    )
                )
                .then(
                    (response) => {
                        vm.proposal_parks = helpers.copyObject(response);
                    },
                    () => {}
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
                    vm.referral.assigned_officer = selected.val();
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
                    vm.referral.assigned_officer = null;
                    vm.assignTo();
                });
        },
        completeReferral: function () {
            let vm = this;
            let data = { referral_comment: vm.referral_comment };

            swal.fire({
                title: 'Complete Referral',
                text: 'Are you sure you want to complete this referral?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Submit',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.referrals,
                                vm.$route.params.referral_id + '/complete'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(data),
                            }
                        )
                        .then(
                            (res) => {
                                vm.referral = res;
                                vm.fetchProposalParks(vm.referral.proposal.id);
                            },
                            (error) => {
                                swal.fire({
                                    title: 'Referral Error',
                                    text: helpers.apiVueResourceError(error),
                                    icon: 'error',
                                });
                            }
                        );
                    }
                },
            );
        },
        formatDate: function (data) {
            return data ? moment(data).format('DD/MM/YYYY HH:mm:ss') : '';
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
