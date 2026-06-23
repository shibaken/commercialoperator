<template>
    <!-- <div v-if="email_user" class="card"> -->
    <div v-if="org" id="organisationLinkedUser" class="container">
        <div class="row">
            <div class="card">
                <div class="card-header fw-bold h4" style="padding: 30px">
                    <div class="row">
                        <div class="col-6">Organisations</div>
                        <div class="col-6 text-end">
                            <i
                                class="bi fw-bold chevron-toggle down-chevron-open"
                                data-bs-target="#organisations-tab-body"
                                onclick=""
                            ></i>
                        </div>
                    </div>
                </div>
                <div id="organisations-tab-body" class="card-body">
                    <FormSection
                        :form-collapse="false"
                        label="Linked User Accounts"
                        index="linked_user_accounts"
                        subtitle="Manage the user accounts linked to the organisation"
                    >
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <div v-if="org" class="row">
                                                <div class="col-sm-12">
                                                    <h4>
                                                        Persons linked to this organisation:
                                                    </h4>
                                                </div>
                                                <div v-for="d in org.delegates" :key="d.id">
                                                    <div v-if="d.is_admin" class="row mb-1">
                                                        <label
                                                            :for="`organisation_admin_${d.id}`"
                                                            class="col-sm-3"
                                                        >
                                                            <i
                                                                class="bi bi-shield-lock-fill"
                                                                style="color: #007bff"
                                                            ></i
                                                            >&nbsp;
                                                            <strong
                                                                >Organisation Admin:</strong
                                                            >
                                                        </label>
                                                        <div class="col-sm-9">
                                                            <input
                                                                class="form-control w-100"
                                                                type="text"
                                                                :value="`${d.name} (${d.email})`"
                                                                aria-label="organisation admin name"
                                                                :name="`organisation_admin_${d.id}`"
                                                                disabled
                                                                readonly
                                                            />
                                                        </div>
                                                    </div>
                                                    <div v-else class="row mb-1">
                                                        <label
                                                            :for="`organisation_user_${d.id}`"
                                                            class="col-sm-3"
                                                        >
                                                            <i
                                                                class="bi bi-person-fill"
                                                                style="color: #007bff"
                                                            ></i
                                                            >&nbsp;
                                                            <strong
                                                                >Organisation User:</strong
                                                            >
                                                        </label>
                                                        <div class="col-sm-9">
                                                            <input
                                                                class="form-control w-100"
                                                                type="text"
                                                                :value="`${d.name} (${d.email})`"
                                                                aria-label="organisation user name"
                                                                :name="`organisation_user_${d.id}`"
                                                                disabled
                                                                readonly
                                                            />
                                                        </div>
                                                    </div>
                                                </div>
                                                <div
                                                    class="col-sm-12 top-buffer-s mb-3 mt-3"
                                                >
                                                    <alert
                                                        type="info"
                                                        icon="info-circle"
                                                        class="alert alert-info"
                                                    >
                                                        <i
                                                            class="bi bi-exclamation-triangle-fill"
                                                            style="color: #dc3545"
                                                        ></i
                                                        >&nbsp; The Department cannot manage
                                                        this list of people. The
                                                        organisation is responsible for
                                                        managing people linked to the
                                                        organisation.
                                                        <br />
                                                    </alert>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <form
                                        v-if="org?.pins"
                                        class="form-horizontal"
                                        action="index.html"
                                        method="post"
                                    >
                                        <div class="row mb-2">
                                            <label
                                                for=""
                                                class="col-sm-3 control-label fw-bold"
                                            >
                                                User Pin Code 1:</label
                                            >
                                            <span class="col-sm-3 fw-light">
                                                {{ org.pins.three }}
                                            </span>
                                            <label
                                                for=""
                                                class="col-sm-3 control-label fw-bold"
                                            >
                                                User Pin Code 2:</label
                                            >
                                            <div class="col-sm-3 fw-light">
                                                {{ org.pins.four }}
                                            </div>
                                        </div>
                                        <div class="row mb-3">
                                            <label
                                                for=""
                                                class="col-sm-3 control-label fw-bold"
                                            >
                                                Admin Pin Code 1:</label
                                            >
                                            <span class="col-sm-3 fw-light">
                                                {{ org.pins.one }}
                                            </span>
                                            <label
                                                for=""
                                                class="col-sm-3 control-label fw-bold"
                                            >
                                                Admin Pin Code 2:</label
                                            >
                                            <div class="col-sm-3 fw-light">
                                                {{ org.pins.two }}
                                            </div>
                                        </div>
                                    </form>
                                    <div>
                                        <datatable
                                            id="organisation_contacts_datatable_ref"
                                            ref="contacts_datatable_user"
                                            v-model="filterOrgContactStatus"
                                            :dt-options="contacts_options_ref"
                                            :dt-headers="contacts_headers_ref"
                                        />
                                    </div>
                    </FormSection>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <div class="d-flex justify-content-center align-items-center mt-5">
            <div class="spinner-grow text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div class="d-flex justify-content-center align-items-center mb-5">
            <strong>Loading</strong>
        </div>
    </div>
</template>

<script>
import { api_endpoints, constants, helpers, utils } from '@/utils/hooks';
import alert from '@vue-utils/alert.vue';
import datatable from '@vue-utils/datatable.vue';
import AddCommLog from '@common-utils/add_comm_log_org.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import $ from 'jquery';
export default {
    name: 'OrganisationComponent',
    components: {
        alert,
        datatable,
        AddCommLog,
        FormSection,
    },
    data() {
        const vm = this;
        return {
            api_endpoints: api_endpoints,
            comms_add_url: helpers.add_endpoint_json(
                api_endpoints.organisations,
                vm.$route.params.org_id + '/add_comms_log'
            ),
            email_user: null,
            selectedOrganisation: null,
            newOrganisation: null,
            organisation_requests: null,
            validatePinsError: null,
            validatingPins: false,
            pins: {
                pin1: '',
                pin2: '',
            },
            helpers: helpers,
            org: null,
            is_org_admin: false,
            contacts_headers_ref: ['Name', 'Role', 'Email', 'Status', 'Action'],
            contacts_options_ref: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                ajax: {
                    url: helpers.add_endpoint_json(
                        api_endpoints.organisations,
                        vm.$route.params.org_id + '/contacts_exclude'
                    ),

                    dataSrc: '',
                },
                columns: [
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            return full.first_name + ' ' + full.last_name;
                        },
                    },
                    {
                        data: 'user_role',
                        mRender: function (data, type, full) {
                            if (full.user_role == 'Organisation Admin') {
                                return `<i class='bi bi-shield-lock-fill' style='color: #007bff' ></i>&nbsp;${full.user_role}`;
                            } else if (full.user_role == 'Organisation User') {
                                return `<i class='bi bi-person-fill' style='color: #007bff' ></i>&nbsp;${full.user_role}`;
                            } else {
                                return full.user_role;
                            }
                        },
                    },
                    { data: 'email' },
                    {
                        data: 'user_status',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (full.user_status == 'Pending') {
                                links += `<span class='badge bg-warning me-1 p-2'>${full.user_status}</span>`;
                            } else if (full.user_status == 'Active') {
                                links += `<span class='badge bg-success me-1 p-2'><i class="fas fa-link"></i> ${full.user_status}</span>`;
                            } else if (full.user_status == 'Declined') {
                                links += `<span class='badge bg-danger me-1 p-2'>${full.user_status}</span>`;
                            } else if (full.user_status == 'Suspended') {
                                links += `<span class='badge bg-danger me-1 p-2'>${full.user_status}</span>`;
                            } else if (full.user_status == 'Unlinked') {
                                links += `<span class='badge bg-secondary me-1 p-2'><i class="fas fa-link-slash"></i> ${full.user_status}</span>`;
                            } else if (full.user_status == 'ContactForm') {
                                links += `<span class='badge bg-info me-1 p-2'>${full.user_status}</span>`;
                            } else {
                                links += `<span class='badge bg-secondary me-1 p-2'>${full.user_status}</span>`;
                            }
                            return links;
                        },
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (vm.is_commercialoperator_admin || vm.is_org_admin) {
                                if (full.user_status == 'Pending') {
                                    links += `<a data-email='${full.email}' data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="accept_contact">Accept</a><br/>`;
                                    links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="decline_contact">Decline</a><br/>`;
                                } else if (full.user_status == 'Suspended') {
                                    links += `<a data-email='${full.email}' data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="reinstate_contact">Reinstate</a><br/>`;
                                } else if (full.user_status == 'Active') {
                                    links += `<button class='btn btn-danger btn-sm btn-status unlink_contact' role='button' data-email='${full.email}' data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}'><i class="fas fa-link-slash"></i> Unlink</button><br/>`;
                                    links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="suspend_contact">Suspend</a><br/>`;
                                    if (full.user_role == 'Organisation User') {
                                        links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="make_admin_contact">Make Organisation Admin</a><br/>`;
                                    } else {
                                        links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="make_user_contact">Make Organisation User</a><br/>`;
                                    }
                                } else if (full.user_status == 'Unlinked') {
                                    links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="relink_contact">Reinstate</a><br/>`;
                                } else if (full.user_status == 'Declined') {
                                    links += `<a data-email='${full.email}'  data-firstname='${full.first_name}' data-lastname='${full.last_name}' data-id='${full.id}' data-mobile='${full.mobile_number}' data-phone='${full.phone_number}' class="accept_declined_contact">Accept (Previously Declined)</a><br/>`;
                                }
                            }
                            return links;
                        },
                    },
                ],
                processing: true,
            },
            filterOrgContactStatus: null,
            is_commercialoperator_admin: false,
            contact_user: {
                first_name: null,
                last_name: null,
                email: null,
                mobile_number: null,
                phone_number: null,
            },
            user_action: 'unlink',
        };
    },
    computed: {
        linkOrganisationTitle: function () {
            if (
                this.organisation_requests &&
                this.organisation_requests.length
            ) {
                return 'Link another Organisation';
            }
            return 'Link an organisation';
        },
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
    },
    created: function () {
        console.log('organisation.vue created');
        this.fetchInitialData().then((response) => {
            console.log('fetch initial data', response);
        });
    },
    mounted: function () {
        console.log('organisation.vue mounted');
        this.$nextTick(() => {
            if (this.$refs.contacts_datatable_user) {
                this.eventListeners();
            }
        });
    },
    methods: {
        orgAction: function (action) {
            let vm = this;
            if (action) {
                if (action == 'unlink') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/unlink_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Unlink',
                                    text:
                                        'You have successfully unlinked ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                        if (vm.contact_user.email == vm.profile.email) {
                                            this.$router.push('/external')
                                        }
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                if (error.status == 500) {
                                    swal.fire({
                                        title: 'Unlink',
                                        text: 'Last Organisation Admin can not be unlinked.',
                                        icon: 'error',
                                    });
                                } else {
                                    swal.fire({
                                        title: 'Unlink',
                                        text:
                                            'There was an error unlinking ' +
                                            error +
                                            '.',
                                        icon: 'error',
                                    });
                                }
                            }
                        );
                } else if (action == 'relink') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/relink_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Relink User',
                                    text:
                                        'You have successfully relinked ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Relink User',
                                    text:
                                        'There was an error relinking ' +
                                        error +
                                        '.',
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'suspend') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/suspend_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Suspend User',
                                    text:
                                        'You have successfully suspended ' +
                                        name +
                                        ' as a User.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                        if (vm.contact_user.email == vm.profile.email) {
                                            this.$router.push('/external')
                                        }
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Suspend User',
                                    text:
                                        'There was an error suspending ' +
                                        error +
                                        ' as a User.',
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'reinstate') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/reinstate_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Reinstate User',
                                    text:
                                        'You have successfully reinstated ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Reinstate User',
                                    text:
                                        'There was an error reinstating ' +
                                        error +
                                        '.',
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'make_admin_contact') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/make_admin_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Organisation Admin',
                                    text:
                                        'You have successfully made ' +
                                        name +
                                        ' an Organisation Admin.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Organisation Admin',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'make_user_contact') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/make_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Organisation User',
                                    text:
                                        'You have successfully made ' +
                                        name +
                                        ' an Organisation User.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                        if (vm.contact_user.email == vm.profile.email) {
                                            this.$router.push('/external')
                                        }
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                console.log(error);
                                var text = helpers.apiVueResourceError(error);
                                swal.fire({
                                    title: 'Company Admin',
                                    text: error,
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'accept') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/accept_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Contact Accept',
                                    text:
                                        'You have successfully accepted ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Contact Accept',
                                    text:
                                        'There was an error accepting ' +
                                        error +
                                        '.',
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'decline') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/decline_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Contact Decline',
                                    text:
                                        'You have successfully declined ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Contact Decline',
                                    text:
                                        'There was an error declining ' +
                                        error +
                                        '.',
                                    icon: 'error',
                                });
                            }
                        );
                } else if (action == 'accept_declined') {
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.organisations,
                                vm.org.id + '/accept_declined_user'
                            ),
                            {
                                method: 'POST',
                                body: JSON.stringify(vm.contact_user),
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                            }
                        )
                        .then(
                            () => {
                                // Note: This block is missing a response to retrieve the name from
                                swal.fire({
                                    title: 'Contact Accept (Previously Declined)',
                                    text:
                                        'You have successfully accepted ' +
                                        name +
                                        '.',
                                    icon: 'success',
                                    confirmButtonText: 'OK',
                                }).then(
                                    () => {
                                        vm.$refs.contacts_datatable_user.vmDataTable.ajax.reload();
                                    },
                                    () => {}
                                );
                            },
                            (error) => {
                                // Note: The alert text seems to indicate to display the user name, but the name is not retrieved from the error response
                                swal.fire({
                                    title: 'Contact Accept (Previously Declined)',
                                    text:
                                        'There was an error accepting ' +
                                        error +
                                        '.',
                                    icon: 'error',
                                });
                            }
                        );
                }
            }
        },
        eventListeners: function () {
            const vm = this;
            
            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.unlink_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Unlink',
                        text:
                            'Are you sure you want to unlink ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        async (result) => {
                            if (!result.isConfirmed) {
                                return;
                            }
                            if (result) {
                                this.orgAction('unlink');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.reinstate_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Reinstate User',
                        text:
                            'Are you sure you want to Reinstate  ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (!result.isConfirmed) {
                                return;
                            }
                            if (result) {
                                this.orgAction('reinstate');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.relink_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Relink User',
                        text:
                            'Are you sure you want to relink  ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('relink');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.suspend_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Suspend User',
                        text:
                            'Are you sure you want to suspend  ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('suspend');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.make_admin_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Organisation Admin',
                        text:
                            'Are you sure you want to make ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ') an Organisation Admin?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('make_admin_contact');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.make_user_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Organisation User',
                        text:
                            'Are you sure you want to make ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ') an Organisation User?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('make_user_contact');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.accept_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Contact Accept',
                        text:
                            'Are you sure you want to accept contact request ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('accept');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.decline_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Contact Decline',
                        text:
                            'Are you sure you want to decline the contact request for ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('decline');
                            }
                        },
                        () => {}
                    );
                }
            );

            vm.$refs.contacts_datatable_user.vmDataTable.on(
                'click',
                '.accept_declined_contact',
                (e) => {
                    e.preventDefault();
                    vm.updateContactUser(e);
                    const name = `${vm.contact_user.first_name} ${vm.contact_user.last_name}`;

                    swal.fire({
                        title: 'Contact Accept (Previously Declined)',
                        text:
                            'Are you sure you want to accept the previously declined contact request for ' +
                            name +
                            ' (' +
                            vm.contact_user.email +
                            ')?',
                        showCancelButton: true,
                        confirmButtonText: 'Accept',
                    }).then(
                        (result) => {
                            if (result) {
                                if (!result.isConfirmed) {
                                    return;
                                }
                                this.orgAction('accept_declined');
                            }
                        },
                        () => {}
                    );
                }
            );
            // Fix the table responsiveness when tab is shown
            $('a[href="#' + vm.oTab + '"]').on('shown.bs.tab', function () {
                vm.$refs.proposals_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
                vm.$refs.approvals_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
                vm.$refs.compliances_table.$refs.proposal_datatable.vmDataTable.columns
                    .adjust()
                    .responsive.recalc();
            });
        },
        fetchInitialData: function () {
            const vm = this;
            const orgId = vm.$route.params.org_id;
            let initialisers = [
                utils.fetchCountries().catch(() => []),
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.organisations,
                            orgId
                        )
                    )
                    .catch(() => null),
                utils.fetchLinkedOrganisation(orgId).catch(() => null),
                utils.fetchProfile().catch(() => ({
                    commercialoperator_organisations: [],
                })),
            ];
            return Promise.all(initialisers).then((data) => {
                vm.countries = data[0] || [];

                const directOrganisation = data[1] || {};
                const linkedOrganisation = data[2] || {};
                vm.org = Object.assign({}, directOrganisation, linkedOrganisation);

                vm.profile = data[3] || {
                    commercialoperator_organisations: [],
                };
                vm.org.organisation_address =
                    vm.org.organisation_address != null
                        ? vm.org.organisation_address
                        : {};
                vm.org.pins = vm.org.pins != null ? vm.org.pins : {};
                vm.is_commercialoperator_admin =
                    vm.profile.is_commercialoperator_admin;
                vm.is_org_access_member = vm.profile.is_org_access_member;
                var profile_org = null;
                (vm.profile.commercialoperator_organisations || []).forEach(
                    (org) => {
                        if (org.id == vm.org.id) {
                            profile_org = org;
                        }
                    }
                );
                vm.is_org_admin = profile_org ? profile_org.is_admin : false;

                if (!vm.org || Object.keys(vm.org).length === 0) {
                    vm.org = {
                        organisation_address: {},
                        pins: {},
                        delegates: [],
                    };
                }

                if (!Array.isArray(vm.org.delegates)) {
                    vm.org.delegates = [];
                }

                if (
                    vm.contacts_options_ref &&
                    vm.contacts_options_ref.ajax &&
                    vm.contacts_options_ref.ajax.url
                ) {
                    vm.contacts_options_ref.ajax.url = helpers.add_endpoint_json(
                        api_endpoints.organisations,
                        orgId + '/contacts_exclude'
                    );
                }

                return { success: true };
            });
        },
        updateContactUser: function (event) {
            const firstname = $(event.target).data('firstname');
            const lastname = $(event.target).data('lastname');
            const email = $(event.target).data('email');
            const mobile = $(event.target).data('mobile');
            const phone = $(event.target).data('phone');

            const new_user = {
                first_name: firstname,
                last_name: lastname,
                email: email,
                mobile_number: mobile,
                phone_number: phone,
            };

            this.contact_user = { ...new_user };
        },
    },
};
</script>

<style scoped>
.btn-status {
    height: 28px;
}
</style>
