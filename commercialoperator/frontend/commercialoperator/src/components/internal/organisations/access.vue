<template>
    <div id="internalOrgAccess" class="container">
        <div class="row">
            <h3>Organisation Access Request {{ access.id }}</h3>
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
                                    {{ access.requester.full_name }}
                                </div>
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Lodged on</strong><br />
                                    {{ formatDate(access.lodgement_date) }}
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
                                    {{ access.status }}
                                </div>
                                <div class="col-sm-12 top-buffer-s">
                                    <strong>Currently assigned to</strong><br />
                                    <div
                                        id="select_org_access_assigned_to_parent"
                                        class="form-group"
                                    >
                                        <div v-show="isLoading">
                                            <select class="form-control">
                                                <option value="">
                                                    Loading...
                                                </option>
                                            </select>
                                        </div>
                                        <div v-show="!isLoading">
                                            <select
                                                id="select_org_access_assigned_to"
                                                ref="select_org_access_assigned_to"
                                                v-model="
                                                    access.assigned_officer
                                                "
                                                :disabled="
                                                    isFinalised ||
                                                    !check_assessor()
                                                "
                                                class="form-control"
                                                @change="assignTo"
                                            >
                                                <option value="null">
                                                    Unassigned
                                                </option>
                                                <option
                                                    v-for="member in members"
                                                    :key="member.id"
                                                    :value="member.id"
                                                >
                                                    {{ member.name }}
                                                </option>
                                            </select>
                                            <a
                                                v-if="
                                                    !isFinalised &&
                                                    check_assessor()
                                                "
                                                class="actionBtn pull-right"
                                                @click.prevent="assignMyself()"
                                                >Assign to me</a
                                            >
                                        </div>
                                    </div>
                                </div>
                                <div
                                    v-if="!isFinalised && check_assessor()"
                                    class="col-sm-12 top-buffer-s"
                                >
                                    <strong>Action</strong><br />
                                    <button
                                        class="btn btn-primary"
                                        @click.prevent="acceptRequest()"
                                    >
                                        Accept</button
                                    ><br />
                                    <button
                                        class="btn btn-primary top-buffer-s"
                                        @click.prevent="declineRequest()"
                                    >
                                        Decline
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-1"></div>
            <div class="col-md-8">
                <div class="">
                    <div class="card mb-3">
                        <div class="card-header">
                            <h3>Organisation Access Request</h3>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-sm-12">
                                    <form
                                        class="form-horizontal"
                                        name="access_form"
                                    >
                                        <div class="form-group row mb-3">
                                            <label
                                                for="name"
                                                class="col-sm-3 control-label"
                                                >Organisation</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="access.name"
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="name"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                        <div class="form-group row mb-3">
                                            <label
                                                for="abn"
                                                class="col-sm-3 control-label"
                                                >ABN</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="access.abn"
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="abn"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                        <div class="form-group row mb-3">
                                            <label
                                                for=""
                                                class="col-sm-3 control-label"
                                                >Letter</label
                                            >
                                            <div class="col-sm-6">
                                                <a
                                                    target="_blank"
                                                    :href="
                                                        access.identification
                                                    "
                                                    ><i
                                                        class="fa fa-file-pdf"
                                                    ></i
                                                    >&nbsp;Letter</a
                                                >
                                            </div>
                                        </div>
                                        <div
                                            class="form-group row mb-3"
                                            style="margin-top: 50px"
                                        >
                                            <label
                                                for="phone"
                                                class="col-sm-3 control-label"
                                                >Phone</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="
                                                        access.requester
                                                            .phone_number
                                                    "
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="phone"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                        <div class="form-group row mb-3">
                                            <label
                                                for="mobile"
                                                class="col-sm-3 control-label"
                                                >Mobile</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="
                                                        access.requester
                                                            .mobile_number
                                                    "
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="mobile"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                        <div class="form-group row">
                                            <label
                                                for="email"
                                                class="col-sm-3 control-label"
                                                >Email</label
                                            >
                                            <div class="col-sm-6">
                                                <input
                                                    v-model="
                                                        access.requester.email
                                                    "
                                                    type="text"
                                                    disabled
                                                    class="form-control"
                                                    name="email"
                                                    placeholder=""
                                                />
                                            </div>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import $ from 'jquery';
import CommsLogs from '@common-utils/comms_logs.vue';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import _ from 'lodash';

export default {
    name: 'OrganisationAccess',
    components: {
        CommsLogs,
    },
    beforeRouteEnter: function (to, from, next) {
        helpers
            .fetchUrl(
                helpers.add_endpoint_json(
                    api_endpoints.organisation_requests,
                    to.params.access_id
                )
            )
            .then(
                (response) => {
                    next((vm) => {
                        vm.access = response;
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
            profile: {},
            access: {
                requester: {},
            },
            DATE_TIME_FORMAT: 'DD/MM/YYYY HH:mm:ss',
            members: [],
            // Filters
            logs_url: helpers.add_endpoint_json(
                api_endpoints.organisation_requests,
                vm.$route.params.access_id + '/action_log'
            ),
            comms_url: helpers.add_endpoint_json(
                api_endpoints.organisation_requests,
                vm.$route.params.access_id + '/comms_log'
            ),
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.organisation_requests,
                vm.$route.params.access_id + '/add_comms_log'
            ),
            actionDtOptions: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                deferRender: true,
                autowidth: true,
                order: [[2, 'desc']],
                dom:
                    "<'row'<'col-sm-5'l><'col-sm-6'f>>" +
                    "<'row'<'col-sm-12'tr>>" +
                    "<'row'<'col-sm-5'i><'col-sm-7'p>>",
                processing: true,
                ajax: {
                    url: helpers.add_endpoint_json(
                        api_endpoints.organisation_requests,
                        vm.$route.params.access_id + '/action_log'
                    ),
                    dataSrc: '',
                },
                columns: [
                    {
                        data: 'who',
                    },
                    {
                        data: 'what',
                    },
                    {
                        data: 'when',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return moment(data).format(vm.DATE_TIME_FORMAT);
                        },
                    },
                ],
            },
            dtHeaders: ['Who', 'What', 'When'],
            actionsTable: null,
            commsDtOptions: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                deferRender: true,
                autowidth: true,
                order: [[0, 'desc']],
                processing: true,
                ajax: {
                    url: helpers.add_endpoint_json(
                        api_endpoints.organisation_requests_datatable,
                        vm.$route.params.access_id + '/comms_log'
                    ),
                    dataSrc: '',
                },
                columns: [
                    {
                        title: 'Date',
                        data: 'created',
                        render: function (date) {
                            return moment(date).format(vm.DATE_TIME_FORMAT);
                        },
                    },
                    {
                        title: 'Type',
                        data: 'type',
                    },
                    {
                        title: 'Reference',
                        data: 'reference',
                    },
                    {
                        title: 'To',
                        data: 'to',
                        render: vm.commaToNewline,
                    },
                    {
                        title: 'CC',
                        data: 'cc',
                        render: vm.commaToNewline,
                    },
                    {
                        title: 'From',
                        data: 'fromm',
                        render: vm.commaToNewline,
                    },
                    {
                        title: 'Subject/Desc.',
                        data: 'subject',
                    },
                    {
                        title: 'Text',
                        data: 'text',
                        render: function (value) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 100,
                                    omission: ellipsis,
                                    separator: ' ',
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template(
                                    '<a href="#" ' +
                                        'role="button" ' +
                                        'data-bs-toggle="popover" ' +
                                        'data-trigger="click" ' +
                                        'data-placement="top auto"' +
                                        'data-html="true" ' +
                                        'data-content="<%= text %>" ' +
                                        '>more</a>'
                                );
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value,
                                });
                            }

                            return result;
                        },
                        createdCell: function (cell) {
                            // the call to popover is done in the 'draw' event
                            $(cell).popover();
                        },
                    },
                    {
                        title: 'Documents',
                        data: 'documents',
                        render: function (values) {
                            var result = '';
                            _.forEach(values, function (value) {
                                // We expect an array [docName, url]
                                // if it's a string it is the url
                                var docName = '',
                                    url = '';
                                if (_.isArray(value) && value.length > 1) {
                                    docName = value[0];
                                    url = value[1];
                                }
                                if (typeof s === 'string') {
                                    url = value;
                                    // display the first  chars of the filename
                                    docName = _.last(value.split('/'));
                                    docName = _.truncate(docName, {
                                        length: 18,
                                        omission: '...',
                                        separator: ' ',
                                    });
                                }
                                result +=
                                    '<a href="' +
                                    url +
                                    '" target="_blank"><p>' +
                                    docName +
                                    '</p></a><br>';
                            });
                            return result;
                        },
                    },
                ],
            },
            commsTable: null,
        };
    },
    computed: {
        isLoading: function () {
            return this.loading.length > 0;
        },
        isFinalised: function () {
            return (
                this.access.status == 'With Assesor' ||
                this.access.status == 'Approved' ||
                this.access.status == 'Declined'
            );
        },
    },
    watch: {},
    mounted: function () {
        const assignTo = this.assignTo;
        this.fetchAccessGroupMembers();
        this.fetchProfile();
        this.$nextTick(() => {
            this.initialiseAssessorSelect(assignTo);
        });
    },
    methods: {
        commaToNewline(s) {
            return s.replace(/[,;]/g, '\n');
        },
        fetchAccessGroupMembers: function () {
            let vm = this;
            vm.loading.push('Loading Access Group Members');
            helpers
                .fetchUrl(api_endpoints.organisation_access_group_members)
                .then(
                    (response) => {
                        vm.members = response;
                        vm.loading.splice('Loading Access Group Members', 1);
                    },
                    (error) => {
                        console.log(error);
                        vm.loading.splice('Loading Access Group Members', 1);
                    }
                );
        },
        assignMyself: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.organisation_requests,
                        vm.access.id + '/assign_request_user'
                    )
                )
                .then(
                    (response) => {
                        console.log(response);
                        vm.access = Object.assign({}, response);
                        vm.$nextTick(() => {
                            vm.initialiseAssessorSelect(vm.assignTo);
                        });
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },
        assignTo: function () {
            let vm = this;
            if (vm.access.assigned_officer != 'null') {
                let data = { user_id: vm.access.assigned_officer };
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.organisation_requests,
                            vm.access.id + '/assign_to'
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
                            console.log(response);
                            vm.access = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.organisation_requests,
                            vm.access.id + '/unassign'
                        )
                    )
                    .then(
                        (response) => {
                            console.log(response);
                            vm.access = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            }
        },
        acceptRequest: function () {
            let vm = this;
            swal.fire({
                title: 'Accept Organisation Request',
                text: 'Are you sure you want to accept this organisation request?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Accept',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisation_requests,
                                vm.access.id + '/accept'
                            )
                        )
                        .then(
                            (response) => {
                                console.log(response);
                                vm.access = response;
                                swal.fire({
                                    title: 'Success',
                                    text: 'Organisation request has been accepted',
                                    icon: 'success',
                                });
                            },
                            (error) => {
                                console.log(error);
                                var text = helpers.apiVueResourceError(error);
                                if (typeof text == 'object') {
                                    // eslint-disable-next-line no-prototype-builtins
                                    if (text.hasOwnProperty('email')) {
                                        text = text.email[0];
                                    }
                                }
                                swal.fire({
                                    title: 'Error',
                                    text:
                                        'Organisation request cannot be accepted because of the following error: ' +
                                        text,
                                    icon: 'error',
                                });
                            }
                        );
                    }
                },
                () => {}
            );
        },

        declineRequest: function () {
            let vm = this;
            swal.fire({
                title: 'Decline Organisation Request',
                text: 'Are you sure you want to decline this organisation request?',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Decline',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisation_requests,
                                vm.access.id + '/decline'
                            )
                        )
                        .then(
                            (response) => {
                                console.log(response);
                                vm.access = response;
                            },
                            (error) => {
                                console.log(error);
                            }
                        );
                    }
                },
            );
        },

        fetchProfile: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.profile).then(
                (response) => {
                    vm.profile = response;
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
        /**
         * Initialise the select2 for the Assessor
         * @param callback A function to call when the select2 is initialised
         */
        initialiseAssessorSelect: function (callback) {
            helpers.initialiseSelect2
                .bind(this)(
                    'select_org_access_assigned_to',
                    'select_org_access_assigned_to_parent',
                    'access.assigned_officer',
                    'Select an Assessor',
                    false,
                    0,
                    'null'
                )
                .on('select2:select', function () {
                    callback();
                });
        },
        formatDate: function (data) {
            return moment(data).format('DD/MM/YYYY HH:mm:ss');
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
