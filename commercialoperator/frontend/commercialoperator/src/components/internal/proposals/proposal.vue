<template lang="html">
    <div v-if="proposal.id" id="internalProposal" class="container">
        <div class="row" style="padding-bottom: 50px">
            <h3>Application: {{ proposal.lodgement_number }}</h3>
            <h4>
                Application Type: {{ proposal.application_type }}
                {{
                    proposal.proposal_type ? `(${proposal.proposal_type})` : ''
                }}
            </h4>
            <div v-if="!comparing" class="col-md-3">
                <CommsLogs
                    :comms_url="comms_url"
                    :logs_url="logs_url"
                    :comms_add_url="comms_add_url"
                    :disable_add_entry="false"
                />
                <div v-if="canSeeSubmission">
                    <div class="card mb-3">
                        <div class="card-header">Submission</div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-12">
                                    <strong>Submitted by</strong><br />
                                    <span v-if="proposal.submitter">
                                        {{ proposal.submitter.first_name }}
                                        {{ proposal.submitter.last_name }}
                                    </span>
                                    <span v-else>Not available</span>
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

                <div v-if="canSeeSubmission">
                    <div class="card mb-3">
                        <div class="card-header">History</div>
                        <div class="card-body">
                            <table class="table small-table">
                                <thead>
                                    <tr>
                                        <th>Last Modified</th>
                                        <th></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="h in proposal.history"
                                        :key="`history-${h.id}`"
                                    >
                                        <td>{{ formatDate(h.modified) }}</td>
                                        <td>
                                            <a
                                                :href="
                                                    history_url +
                                                    'version_id2=' +
                                                    h.version_id +
                                                    '&version_id1=' +
                                                    h.prev_version_id
                                                "
                                                target="_blank"
                                                >compare</a
                                            >
                                        </td>
                                    </tr>
                                    <tr
                                        v-for="p in proposal.reversion_ids"
                                        :key="`reversion-${p.cur_version_id}`"
                                    >
                                        <td>{{ formatDate(p.created) }}</td>
                                        <td>
                                            <a
                                                id="history_id"
                                                :href="
                                                    history_url +
                                                    'version_id2=' +
                                                    p.cur_version_id +
                                                    '&version_id1=' +
                                                    p.prev_version_id
                                                "
                                                target="_blank"
                                                >compare</a
                                            >
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div>
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
                                <template
                                    v-if="
                                        proposal.processing_status ==
                                            'With Assessor' ||
                                        proposal.processing_status ==
                                            'With Referral'
                                    "
                                >
                                    <div class="col-sm-12 top-buffer-s">
                                        <strong>Referrals</strong><br />
                                        <div class="form-group">
                                            <select
                                                ref="referral_recipient_groups"
                                                :disabled="!canLimitedAction"
                                                class="form-control"
                                            >
                                                <option value="null"></option>
                                                <option
                                                    v-for="group in referral_recipient_groups"
                                                    :key="`referral-group-${group}`"
                                                    :value="group"
                                                >
                                                    {{ group }}
                                                </option>
                                            </select>

                                            <template v-if="!sendingReferral">
                                                <template
                                                    v-if="selected_referral"
                                                >
                                                    <label
                                                        class="control-label pull-left"
                                                        for="Name"
                                                        >Comments</label
                                                    >
                                                    <textarea
                                                        v-model="referral_text"
                                                        class="form-control"
                                                        name="name"
                                                    ></textarea>
                                                    <a
                                                        v-if="canLimitedAction"
                                                        class="actionBtn pull-right"
                                                        @click.prevent="
                                                            sendReferral()
                                                        "
                                                        >Send</a
                                                    >
                                                </template>
                                            </template>
                                            <template v-else>
                                                <span
                                                    v-if="canLimitedAction"
                                                    disabled
                                                    class="actionBtn text-primary pull-right"
                                                    @click.prevent="
                                                        sendReferral()
                                                    "
                                                >
                                                    Sending Referral&nbsp;
                                                    <i
                                                        class="fas fa-circle-notch fa-spin fa-fw"
                                                    ></i>
                                                </span>
                                            </template>
                                        </div>
                                        <table class="table small-table">
                                            <thead>
                                                <tr>
                                                    <th>Referral</th>
                                                    <th>Status/Action</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr
                                                    v-for="r in proposal.latest_referrals"
                                                    :key="`referral-${r.id}`"
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
                                                                r.processing_status ==
                                                                'Awaiting'
                                                            "
                                                        >
                                                            <small
                                                                v-if="
                                                                    canLimitedAction
                                                                "
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
                                                                v-if="
                                                                    canLimitedAction
                                                                "
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
                                                    </td>
                                                </tr>
                                            </tbody>
                                        </table>
                                        <MoreReferrals
                                            :proposal="proposal"
                                            :can-action="canLimitedAction"
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
                                </template>
                                <div
                                    v-if="!isFinalised"
                                    class="col-sm-12 top-buffer-s"
                                >
                                    <strong>Currently assigned to</strong><br />
                                    <div class="form-group">
                                        <template
                                            v-if="
                                                proposal.processing_status ==
                                                'With Approver'
                                            "
                                        >
                                            <select
                                                ref="assigned_officer"
                                                v-model="
                                                    proposal.assigned_approver
                                                "
                                                :disabled="!canAction"
                                                class="form-control"
                                            >
                                                <option
                                                    v-for="member in proposal.allowed_assessors"
                                                    :key="member.id"
                                                    :value="member.id"
                                                >
                                                    {{ member.first_name }}
                                                    {{ member.last_name }}
                                                </option>
                                            </select>
                                            <a
                                                v-if="
                                                    canAssess &&
                                                    proposal.assigned_approver !=
                                                        proposal
                                                            .current_assessor.id
                                                "
                                                class="actionBtn pull-right"
                                                @click.prevent="
                                                    assignRequestUser()
                                                "
                                                >Assign to me</a
                                            >
                                        </template>
                                        <template v-else>
                                            <select
                                                ref="assigned_officer"
                                                v-model="
                                                    proposal.assigned_officer
                                                "
                                                :disabled="!canAction"
                                                class="form-control"
                                            >
                                                <option
                                                    v-for="member in proposal.allowed_assessors"
                                                    :key="member.id"
                                                    :value="member.id"
                                                >
                                                    {{ member.first_name }}
                                                    {{ member.last_name }}
                                                </option>
                                            </select>
                                            <a
                                                v-if="
                                                    canAssess &&
                                                    proposal.assigned_officer !=
                                                        proposal
                                                            .current_assessor.id
                                                "
                                                class="actionBtn pull-right"
                                                @click.prevent="
                                                    assignRequestUser()
                                                "
                                                >Assign to me</a
                                            >
                                        </template>
                                    </div>
                                </div>
                                <template
                                    v-if="
                                        proposal.processing_status ==
                                            'With Assessor (Requirements)' ||
                                        proposal.processing_status ==
                                            'With Approver' ||
                                        isFinalised
                                    "
                                >
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
                                </template>
                                <template
                                    v-if="
                                        proposal.processing_status ==
                                            'With Approver' || isFinalised
                                    "
                                >
                                    <div class="col-sm-12">
                                        <strong>Requirements</strong><br />
                                        <a
                                            v-if="!showingRequirements"
                                            class="actionBtn"
                                            @click.prevent="
                                                toggleRequirements()
                                            "
                                            >Show Requirements</a
                                        >
                                        <a
                                            v-else
                                            class="actionBtn"
                                            @click.prevent="
                                                toggleRequirements()
                                            "
                                            >Hide Requirements</a
                                        >
                                    </div>
                                    <div class="col-sm-12">
                                        <div class="separator"></div>
                                    </div>
                                </template>
                                <div
                                    v-if="!isFinalised && canAction"
                                    class="col-sm-12 top-buffer-s"
                                >
                                    <template
                                        v-if="
                                            proposal.processing_status ==
                                                'With Assessor' ||
                                            proposal.processing_status ==
                                                'With Referral'
                                        "
                                    >
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div
                                            v-if="
                                                proposal.application_type ==
                                                    application_type_filming &&
                                                proposal.filming_approval_type ==
                                                    'lawful_authority'
                                            "
                                            class="row"
                                        >
                                            <div class="col-sm-12">
                                                <button
                                                    v-if="sendingToDistrict"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    disabled
                                                >
                                                    Send to Districts&nbsp;
                                                    <i
                                                        class="fas fa-circle-notch fa-spin fa-fw"
                                                    ></i>
                                                </button>
                                                <button
                                                    v-if="!sendingToDistrict"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        sendToDistricts()
                                                    "
                                                >
                                                    Send to Districts</button
                                                ><br />
                                                <button
                                                    v-if="sendingToKensington"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    disabled
                                                >
                                                    Send to Kensington&nbsp;
                                                    <i
                                                        class="fas fa-circle-notch fa-spin fa-fw"
                                                    ></i>
                                                </button>
                                                <button
                                                    v-if="!sendingToKensington"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        sendToKensington()
                                                    "
                                                >
                                                    Send to Kensington</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div v-else class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    v-if="changingStatus"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    disabled
                                                >
                                                    Enter Requirements&nbsp;
                                                    <i
                                                        class="fas fa-circle-notch fa-spin fa-fw"
                                                    ></i>
                                                </button>
                                                <button
                                                    v-if="!changingStatus"
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        switchStatus(
                                                            'with_assessor_requirements'
                                                        )
                                                    "
                                                >
                                                    Enter Requirements</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        amendmentRequest()
                                                    "
                                                >
                                                    Request Amendment</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        proposedDecline()
                                                    "
                                                >
                                                    Propose to Decline
                                                </button>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="onHold()"
                                                >
                                                    Put On-hold
                                                </button>
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div
                                                v-if="
                                                    isQAOfficerAssessmentCompleted
                                                "
                                                class="col-sm-12"
                                            >
                                                <div class="col-sm-12">
                                                    <div
                                                        class="separator"
                                                    ></div>
                                                </div>
                                                <table
                                                    class="table small-table"
                                                >
                                                    <thead>
                                                        <tr>
                                                            <th>QA Officer</th>
                                                            <th>
                                                                Status/Action
                                                            </th>
                                                        </tr>
                                                    </thead>
                                                    <tbody>
                                                        <tr>
                                                            <th>
                                                                QA Officer
                                                                Referral
                                                            </th>
                                                            <th>
                                                                Status/Action
                                                            </th>
                                                        </tr>
                                                        <tr
                                                            v-for="r in proposal.qaofficer_referrals"
                                                            :key="r.id"
                                                        >
                                                            <td>
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
                                                                <small
                                                                    ><strong>{{
                                                                        r.qaofficer
                                                                    }}</strong></small
                                                                ><br />
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </div>

                                            <div v-else class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        withQAOfficer()
                                                    "
                                                >
                                                    Send to QA Officer
                                                </button>
                                            </div>
                                        </div>
                                    </template>
                                    <template
                                        v-else-if="
                                            proposal.processing_status ==
                                            'With Assessor (Requirements)'
                                        "
                                    >
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    v-if="changingStatus"
                                                    style="width: 80%"
                                                    class="btn btn-primary"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                >
                                                    Back To Processing&nbsp;
                                                    <i
                                                        class="fas fa-circle-notch fa-spin fa-fw"
                                                    ></i>
                                                </button>
                                                <button
                                                    v-if="!changingStatus"
                                                    style="width: 80%"
                                                    class="btn btn-primary"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        switchStatus(
                                                            'with_assessor'
                                                        )
                                                    "
                                                >
                                                    Back To Processing</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div
                                            v-if="requirementsComplete"
                                            class="row"
                                        >
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        proposedApproval()
                                                    "
                                                >
                                                    Propose to Approve</button
                                                ><br />
                                            </div>
                                        </div>
                                    </template>
                                    <template
                                        v-else-if="
                                            proposal.processing_status ==
                                            'With Approver'
                                        "
                                    >
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>

                                        <div class="row">
                                            <div class="col-sm-12">
                                                <label
                                                    class="control-label pull-left"
                                                    for="Name"
                                                    >Approver Comments</label
                                                >
                                                <textarea
                                                    v-model="approver_comment"
                                                    class="form-control"
                                                    name="name"
                                                ></textarea
                                                ><br />
                                            </div>
                                        </div>

                                        <div class="row">
                                            <div
                                                v-if="
                                                    proposal.proposed_decline_status
                                                "
                                                class="col-sm-12"
                                            >
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        switchStatus(
                                                            'with_assessor'
                                                        )
                                                    "
                                                >
                                                    <!-- Back To Processing -->Back
                                                    To Assessor</button
                                                ><br />
                                            </div>
                                            <div v-else class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        switchStatus(
                                                            'with_assessor_requirements'
                                                        )
                                                    "
                                                >
                                                    <!-- Back To Requirements -->Back
                                                    To Assessor</button
                                                ><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        issueProposal()
                                                    "
                                                >
                                                    Approve</button
                                                ><br />
                                            </div>
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="
                                                        declineProposal()
                                                    "
                                                >
                                                    Decline</button
                                                ><br />
                                            </div>
                                        </div>
                                    </template>
                                    <template
                                        v-else-if="
                                            proposal.processing_status ==
                                            'On Hold'
                                        "
                                    >
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit
                                                    "
                                                    @click.prevent="onHold()"
                                                >
                                                    Remove On-hold
                                                </button>
                                            </div>
                                        </div>
                                    </template>
                                    <template
                                        v-else-if="
                                            proposal.processing_status ==
                                            'With QA Officer'
                                        "
                                    >
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <strong>Action</strong><br />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <button
                                                    style="width: 80%"
                                                    class="btn btn-primary top-buffer-s"
                                                    :disabled="
                                                        proposal.can_user_edit &&
                                                        proposal.is_qa_officer
                                                    "
                                                    @click.prevent="
                                                        withQAOfficer()
                                                    "
                                                >
                                                    Complete QA Assessment
                                                </button>
                                            </div>
                                        </div>
                                    </template>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div v-if="!comparing" class="col-md-1"></div>
            <div :class="class_ncols">
                <div class="row">
                    <template
                        v-if="
                            proposal.processing_status == 'With Approver' ||
                            isFinalised
                        "
                    >
                        <ApprovalScreen
                            :proposal="proposal"
                            @refreshFromResponse="refreshFromResponse"
                        />
                    </template>
                    <template v-if="proposal.can_view_district_table">
                        <FilmingDistrictProposalsTable
                            :proposal="proposal"
                            :url="district_proposals_url"
                            @refreshFromResponse="refreshFromResponse"
                        />
                    </template>
                    <template
                        v-if="
                            proposal.processing_status ==
                                'With Assessor (Requirements)' ||
                            ((proposal.processing_status == 'With Approver' ||
                                isFinalised) &&
                                showingRequirements)
                        "
                    >
                        <Requirements
                            :proposal="proposal"
                            @refreshRequirements="refreshRequirements"
                        />
                    </template>
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
                                            proposal_parks &&
                                            proposal.application_type ==
                                                application_type_tclass
                                        "
                                        id="proposalStart"
                                        ref="tclass"
                                        :key="keyProposalTClass"
                                        :proposal="proposal"
                                        :can-edit-activities="canEditActivities"
                                        :is_internal="true"
                                        :has-assessor-mode="hasAssessorMode"
                                        :proposal_parks="proposal_parks"
                                    ></ProposalTClass>
                                    <ProposalFilming
                                        v-else-if="
                                            proposal &&
                                            proposal.application_type ==
                                                application_type_filming
                                        "
                                        id="proposalStart"
                                        ref="filming"
                                        :key="keyProposalFilming"
                                        :proposal="proposal"
                                        :can-edit-activities="canEditActivities"
                                        :can-edit-period="canEditPeriod"
                                        :is_internal="true"
                                        :has-assessor-mode="hasAssessorMode"
                                        :proposal_parks="proposal_parks"
                                    ></ProposalFilming>
                                    <ProposalEvent
                                        v-else-if="
                                            proposal &&
                                            proposal.application_type ==
                                                application_type_event
                                        "
                                        id="proposalStart"
                                        ref="event"
                                        :key="keyProposalEvent"
                                        :proposal="proposal"
                                        :can-edit-activities="canEditActivities"
                                        :can-edit-period="canEditPeriod"
                                        :is_internal="true"
                                        :has-assessor-mode="hasAssessorMode"
                                        :proposal_parks="proposal_parks"
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
                                        class="row"
                                        style="margin-bottom: 50px"
                                    >
                                        <div
                                            v-if="hasAssessorMode"
                                            class="navbar navbar-nav navbar-fixed-bottom ms-auto align-items-end"
                                            style="background-color: #f5f5f5"
                                        >
                                            <div>
                                                <div
                                                    v-if="hasAssessorMode"
                                                    class="container-fluid"
                                                >
                                                    <button
                                                        v-if="savingProposal"
                                                        class="btn btn-primary"
                                                        style="margin-top: 5px"
                                                        disabled
                                                    >
                                                        Save Changes&nbsp;
                                                        <i
                                                            class="fas fa-circle-notch fa-spin fa-fw"
                                                        ></i>
                                                    </button>
                                                    <button
                                                        v-else
                                                        class="btn btn-primary"
                                                        style="margin-top: 5px"
                                                        @click.prevent="save()"
                                                    >
                                                        Save Changes
                                                    </button>
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
import Requirements from './proposal_requirements.vue';
import ProposedApproval from './proposed_issuance.vue';
import ApprovalScreen from './proposal_approval.vue';
import CommsLogs from '@common-utils/comms_logs.vue';
import MoreReferrals from '@common-utils/more_referrals.vue';
import ProposalTClass from '@/components/form_tclass.vue';
import ProposalFilming from '@/components/form_filming.vue';
import ProposalEvent from '@/components/form_event.vue';
import OnHold from './proposal_onhold.vue';
import WithQAOfficer from './proposal_qaofficer.vue';
import FilmingDistrictProposalsTable from '@common-utils/filming_district_proposals_table.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'InternalProposal',
    components: {
        ProposalTClass,
        ProposedDecline,
        AmendmentRequest,
        Requirements,
        ProposedApproval,
        ApprovalScreen,
        CommsLogs,
        MoreReferrals,
        ProposalFilming,
        ProposalEvent,
        OnHold,
        WithQAOfficer,
        FilmingDistrictProposalsTable,
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                `/api/proposal/${to.params.proposal_id}/internal_proposal.json`
            )
            .then(
                (res) => {
                    next((vm) => {
                        vm.proposal = Object.assign({}, res);
                        vm.fetchProposalParks(to.params.proposal_id);
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
                    vm.proposal = Object.assign({}, res);
                    vm.fetchProposalParks(to.params.proposal_id);
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
            proposal: {
                selected_trails_activities: [],
                selected_parks_activities: [],
                marine_parks_activities: [],
            },
            original_proposal: null,
            loading: [],
            selected_referral: '',
            referral_text: '',
            approver_comment: '',
            form: null,
            members: [],
            proposal_parks: {},
            referral_recipient_groups: [],
            contacts_table_initialised: false,
            initialisedSelects: false,
            showingProposal: false,
            showingRequirements: false,
            savingProposal: false,
            changingStatus: false,
            requirementsComplete: true,
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
            district_proposals_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/district_proposals'
            ),
            panelClickersInitialised: false,
            sendingReferral: false,
            comparing: false,
            sendingToDistrict: false,
            sendingToKensington: false,
            keyProposalFilming: uuid(),
            keyProposalEvent: uuid(),
            keyProposalTClass: uuid(),
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
                this.proposal.processing_status == 'Approved' ||
                this.proposal.processing_status == 'Awaiting Payment'
            );
        },
        canAssess: function () {
            return this.proposal &&
                this.proposal.assessor_mode &&
                this.proposal.assessor_mode.assessor_can_assess
                ? true
                : false;
        },
        hasAssessorMode: function () {
            return this.proposal &&
                this.proposal.assessor_mode &&
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
        canEditPeriod: function () {
            return (
                this.proposal &&
                this.proposal.assessor_mode &&
                this.proposal.assessor_mode.assessor_mode &&
                this.proposal.can_edit_period
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
        class_ncols: function () {
            return this.comparing ? 'col-md-12' : 'col-md-8';
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
    },
    updated: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.initialiseSelects();
            vm.proposalAddSelectedParkActivities();
            vm.form = document.forms.new_proposal;
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
            let test_approval;
            if (
                this.proposal.application_type == this.application_type_tclass
            ) {
                if (
                    (this.proposal.proposed_issuance_approval == null ||
                        this.proposal.proposed_issuance_approval.expiry_date ==
                            null) &&
                    this.proposal.other_details.proposed_end_date != null
                ) {
                    test_approval = {
                        start_date:
                            this.proposal.other_details.nominated_start_date,
                        expiry_date:
                            this.proposal.other_details.proposed_end_date,
                    };
                    this.$refs.proposed_approval.approval =
                        helpers.copyObject(test_approval);
                }
            }
            if (
                this.proposal.application_type == this.application_type_filming
            ) {
                if (
                    (this.proposal.proposed_issuance_approval == null ||
                        this.proposal.proposed_issuance_approval.expiry_date ==
                            null) &&
                    this.proposal.filming_activity.completion_date != null &&
                    this.proposal.filming_activity.commencement_date != null
                ) {
                    test_approval = {
                        start_date:
                            this.proposal.filming_activity.commencement_date,
                        expiry_date:
                            this.proposal.filming_activity.completion_date,
                    };
                    this.$refs.proposed_approval.approval =
                        helpers.copyObject(test_approval);
                }
            }
            if (this.proposal.application_type == this.application_type_event) {
                if (
                    (this.proposal.proposed_issuance_approval == null ||
                        this.proposal.proposed_issuance_approval.expiry_date ==
                            null) &&
                    this.proposal.event_activity.completion_date != null &&
                    this.proposal.event_activity.commencement_date != null
                ) {
                    test_approval = {
                        start_date:
                            this.proposal.event_activity.commencement_date,
                        expiry_date:
                            this.proposal.event_activity.completion_date,
                    };
                    this.$refs.proposed_approval.approval =
                        helpers.copyObject(test_approval);
                }
            }

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
            if (this.proposal.proposed_issuance_approval) {
                this.$refs.proposed_approval.approval.start_date =
                    this.proposal.proposed_issuance_approval.start_date !=
                        null &&
                    this.proposal.proposed_issuance_approval.start_date !=
                        undefined
                        ? moment(
                              this.proposal.proposed_issuance_approval
                                  .start_date,
                              'DD/MM/YYYY'
                          ).format('YYYY-MM-DD')
                        : '';
                this.$refs.proposed_approval.approval.expiry_date =
                    this.proposal.proposed_issuance_approval.expiry_date !=
                        null &&
                    this.proposal.proposed_issuance_approval.expiry_date !=
                        undefined
                        ? moment(
                              this.proposal.proposed_issuance_approval
                                  .expiry_date,
                              'DD/MM/YYYY'
                          ).format('YYYY-MM-DD')
                        : '';
            }
            this.$refs.proposed_approval.isModalOpen = true;
        },
        declineProposal: function () {
            this.$refs.proposed_decline.decline =
                this.proposal.proposaldeclineddetails != null
                    ? helpers.copyObject(this.proposal.proposaldeclineddetails)
                    : {};
            this.$refs.proposed_decline.isModalOpen = true;
        },
        sendToDistricts: function () {
            console.log('hello');
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

            vm.sendingToDistrict = true;
            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        helpers
                            .fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.proposals,
                                    vm.proposal.id + '/send_to_districts'
                                ),
                                {
                                    method: 'POST',
                                }
                            )
                            .then(
                                (response) => {
                                    vm.sendingToDistrict = false;
                                    vm.original_proposal =
                                        helpers.copyObject(response);
                                    vm.proposal = Object.assign({}, response);
                                    swal.fire({
                                        title: 'Sent',
                                        text: 'The proposal has been sent to Districts',
                                        icon: 'success',
                                    });
                                },
                                (error) => {
                                    console.log(error);
                                    swal.fire({
                                        title: 'Error',
                                        text: helpers.apiVueResourceError(
                                            error
                                        ),
                                        icon: 'error',
                                    });
                                    vm.sendingToDistrict = false;
                                }
                            );
                    },
                    () => {}
                );
        },
        sendToKensington: function () {
            console.log('hello');
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

            vm.sendingToKensington = true;
            helpers
                .fetchUrl(vm.proposal_form_url, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    () => {
                        helpers
                            .fetchUrl(
                                helpers.add_endpoint_json(
                                    api_endpoints.proposals,
                                    vm.proposal.id + '/send_to_kensington'
                                ),
                                {
                                    method: 'POST',
                                }
                            )
                            .then(
                                (response) => {
                                    vm.sendingToKensington = false;
                                    vm.original_proposal =
                                        helpers.copyObject(response);
                                    vm.proposal = Object.assign({}, response);
                                    swal.fire({
                                        title: 'Sent',
                                        text: 'The proposal has been sent to Kensington',
                                        icon: 'success',
                                    });
                                },
                                (error) => {
                                    console.log(error);
                                    swal.fire({
                                        title: 'Error',
                                        text: helpers.apiVueResourceError(
                                            error
                                        ),
                                        icon: 'error',
                                    });
                                    vm.sendingToKensington = false;
                                }
                            );
                    },
                    () => {}
                );
        },
        amendmentRequest: function () {
            this.save_wo();
            let values = '';
            // Note: What are these values for? The only deficiency class is in comment.vue and that component is not imported here
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
            vm.savingProposal = true;
            if (!helpers.validateForm(vm.form)) {
                vm.savingProposal = false;
                swal.fire({
                    title: 'Error',
                    text: 'Please fix the form errors before saving',
                    icon: 'error',
                });
                return;
            }
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
                    (response) => {
                        vm.refreshFromResponse(response);
                        // Note: commented this out for now, as it doesn't play well with existing logic of the component
                        // vm.refreshApplicationTypeKey(
                        //     vm.proposal.application_type
                        // );
                        swal.fire({
                            title: 'Saved',
                            text: 'Your application has been saved',
                            icon: 'success',
                        });
                        vm.savingProposal = false;
                    },
                    (e) => {
                        swal.fire({
                            title: 'Error',
                            text: e,
                            icon: 'error',
                        });
                        vm.savingProposal = false;
                    }
                );
        },
        save_wo: function () {
            let vm = this;
            if (!helpers.validateForm(vm.form)) {
                swal.fire({
                    title: 'Error',
                    text: 'Please fix the form errors before saving',
                    icon: 'error',
                });
                return;
            }
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
                        vm.proposal = Object.assign({}, response);
                        vm.fetchProposalParks(vm.proposal.id);
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
            console.log('Tree selection: refreshFromResponse');
            let vm = this;
            vm.original_proposal = helpers.copyObject(response);
            vm.proposal = helpers.copyObject(response);
            vm.fetchProposalParks(vm.proposal.id);
            vm.$nextTick(() => {
                vm.initialiseAssignedOfficerSelect(true);
                vm.updateAssignedOfficerSelect();
            });
        },
        refreshRequirements: function (bool) {
            let vm = this;
            vm.requirementsComplete = bool;
        },
        assignTo: function () {
            let vm = this;
            let unassign = true;
            let data = {};
            if (vm.proposal.processing_status == 'With Approver') {
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
                            vm.proposal = Object.assign({}, response);
                            vm.original_proposal = helpers.copyObject(response);

                            vm.updateAssignedOfficerSelect();
                            vm.fetchProposalParks(vm.proposal.id);
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
                            vm.fetchProposalParks(vm.proposal.id);
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
                            vm.proposal = Object.assign({}, response);
                            vm.original_proposal = helpers.copyObject(response);

                            vm.updateAssignedOfficerSelect();
                            vm.fetchProposalParks(vm.proposal.id);
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
                            vm.fetchProposalParks(vm.proposal.id);
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
                vm.changingStatus = true;
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
                                        vm.proposal = Object.assign(
                                            {},
                                            response
                                        );
                                        vm.original_proposal =
                                            helpers.copyObject(response);
                                        vm.fetchProposalParks(vm.proposal.id);
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
                                        vm.fetchProposalParks(vm.proposal.id);
                                        swal.fire({
                                            title: 'Application Error',
                                            text: helpers.apiVueResourceError(
                                                error
                                            ),
                                            icon: 'error',
                                        });
                                    }
                                );
                            vm.changingStatus = false;
                        },
                        () => {
                            vm.changingStatus = false;
                        }
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
                            vm.proposal = Object.assign({}, response);
                            vm.original_proposal = helpers.copyObject(response);
                            vm.fetchProposalParks(vm.proposal.id);
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
                vm.changingStatus = true;
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
                            vm.proposal = Object.assign({}, response);
                            vm.original_proposal = helpers.copyObject(response);
                            vm.fetchProposalParks(vm.proposal.id);
                            vm.approver_comment = '';
                            vm.$nextTick(() => {
                                vm.initialiseAssignedOfficerSelect(true);
                                vm.updateAssignedOfficerSelect();
                            });
                            vm.changingStatus = false;
                        },
                        (error) => {
                            vm.proposal = helpers.copyObject(
                                vm.original_proposal
                            );
                            vm.fetchProposalParks(vm.proposal.id);
                            swal.fire({
                                title: 'Application Error',
                                text: helpers.apiVueResourceError(error),
                                icon: 'error',
                            });
                            vm.changingStatus = false;
                        }
                    );
            }
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
                        vm.proposal_parks = structuredClone(response);
                    },
                    () => {}
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
                .on('select2:unselect', function () {
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
                    .on('select2:unselect', function () {
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
                                    vm.proposal.id + '/assesor_send_referral'
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
                                    vm.proposal = Object.assign({}, response);
                                    vm.fetchProposalParks(vm.proposal.id);
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
                                    vm.refreshApplicationTypeKey(
                                        vm.proposal.application_type
                                    );
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
                        vm.proposal = Object.assign({}, response);
                        vm.fetchProposalParks(vm.proposal.id);
                        swal.fire({
                            title: 'Referral Reminder',
                            text: 'A reminder has been sent to ' + r.referral,
                            icon: 'success',
                        });
                        vm.refreshApplicationTypeKey(
                            vm.proposal.application_type
                        );
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
                        vm.proposal = Object.assign({}, response);
                        vm.fetchProposalParks(vm.proposal.id);
                        swal.fire({
                            title: 'Referral Resent',
                            text:
                                'The referral has been resent to ' + r.referral,
                            icon: 'success',
                        });
                        vm.refreshApplicationTypeKey(
                            vm.proposal.application_type
                        );
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
                        vm.proposal = Object.assign({}, response);
                        vm.fetchProposalParks(vm.proposal.id);
                        swal.fire({
                            title: 'Referral Recall',
                            text:
                                'The referral has been recalled from ' +
                                r.referral,
                            icon: 'success',
                        });
                        vm.refreshApplicationTypeKey(
                            vm.proposal.application_type
                        );
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
        /**
         * Refreshes the key for the given application type, or all if not specified
         * @param application_type The application type to refresh the key for
         */
        refreshApplicationTypeKey: function (application_type) {
            let vm = this;
            console.log(
                'Refreshing keys for application type: ' + application_type
            );
            if (application_type == vm.application_type_filming) {
                vm.keyProposalFilming = uuid();
            } else if (application_type == vm.application_type_event) {
                vm.keyProposalEvent = uuid();
            } else if (application_type == vm.application_type_tclass) {
                vm.keyProposalTClass = uuid();
            } else {
                vm.keyProposalFilming = uuid();
                vm.keyProposalEvent = uuid();
                vm.keyProposalTClass = uuid();
            }
        },
        proposalAddSelectedParkActivities: function () {
            let vm = this;

            if (
                typeof vm.$refs.tclass !== 'undefined' &&
                vm.$refs.tclass !== null
            ) {
                //  hack - after a local update (re-assign assessor or send referral) these are being reset to null, so resetting these to the correct values here
                if (vm.$refs.tclass.$refs.activities_land) {
                    console.log(
                        'Tree selection: ADDING selected park activities from tclass activities_land to proposal'
                    );
                    vm.proposal.selected_parks_activities =
                        vm.$refs.tclass.$refs.activities_land.selected_parks_activities;
                    vm.proposal.selected_trails_activities =
                        vm.$refs.tclass.$refs.activities_land.selected_trails_activities;
                }
                //  hack - after a local update (re-assign assessor or send referral) these are being reset to null, so resetting these to the correct values here
                if (vm.$refs.tclass.$refs.activities_marine) {
                    console.log(
                        'Tree selection: ADDING marine parks activities from tclass activities_marine to proposal'
                    );
                    vm.proposal.marine_parks_activities =
                        vm.$refs.tclass.$refs.activities_marine.marine_parks_activities;
                }
            }
            if (
                typeof vm.$refs.event !== 'undefined' &&
                vm.$refs.event !== null
            ) {
                //  hack - after a local update (re-assign assessor or send referral) these are being reset to null, so resetting these to the correct values here
                if (vm.$refs.event.$refs.event_activities) {
                    console.log(
                        'Tree selection: ADDING selected park activities from event activities to proposal'
                    );
                    vm.proposal.selected_trails_activities =
                        vm.$refs.event.$refs.event_activities.selected_trails_activities;
                }
            }
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
