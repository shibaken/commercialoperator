<template lang="html">
    <div id="editPark">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="parkForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Park or Reserve</label
                                        >
                                    </div>
                                    <div
                                        id="events_park_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            id="events_park"
                                            ref="events_park"
                                            v-model="events_park_id"
                                            class="form-control"
                                            name="park"
                                            @change="fetchAllowedActivities"
                                        >
                                            <option
                                                v-for="p in parks_list"
                                                :key="p.id"
                                                :value="p.id"
                                            >
                                                {{ p.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Activity Types (application)</label
                                        >
                                    </div>

                                    <div class="col-sm-9">
                                        <input
                                            v-model="park.event_activities"
                                            type="text"
                                            class="form-control"
                                            name="pre_event_name"
                                            :readonly="is_internal"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div v-if="is_internal" class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Activity Types (assessor)</label
                                        >
                                    </div>
                                    <div
                                        id="park_activities_select_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            ref="park_activities_select"
                                            v-model="selected_activities"
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            multiple
                                        >
                                            <!-- NOTE: We want to show all event activities (including internal event activities) here not just the allowed activities (allowed_activities) -->
                                            <option
                                                v-for="a in park_activities"
                                                :key="a.id"
                                                :value="a.id"
                                            >
                                                {{ a.name }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="issuingPark"
                    type="button"
                    disabled
                    class="btn btn-primary"
                    @click="ok"
                >
                    <i class="fas fa-spinner fa-spin"></i> Processing
                </button>
                <button
                    v-else
                    type="button"
                    class="btn btn-primary"
                    @click="ok"
                >
                    Ok
                </button>
                <button type="button" class="btn btn-secondary" @click="cancel">
                    Cancel
                </button>
            </template>
        </modal>
    </div>
</template>

<script>
import modal from '@vue-utils/bootstrap-modal.vue';
import alert from '@vue-utils/alert.vue';
import { helpers, api_endpoints } from '@/utils/hooks.js';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Edit-Park-Activity',
    components: {
        modal,
        alert,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        is_internal: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        park_action: {
            type: String,
            default: 'edit',
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            park: Object,
            park_id: Number,
            events_park_id: Number,
            state: 'proposed_park',
            issuingPark: false,
            parks_list: [],
            park_activities: [],
            allowed_activities: [],
            selected_activities: [],
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            localParkAction: JSON.parse(JSON.stringify(this.park_action)),
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.localParkAction == 'add'
                ? 'Add a new Park or Reserve'
                : 'Edit a Park or Reserve';
        },
        delete_url: function () {
            return this.park_id
                ? '/api/proposal_events_parks/' +
                      this.park_id +
                      '/delete_document/'
                : '';
        },
    },
    watch: {
        park_action: {
            handler(newVal) {
                this.localParkAction = JSON.parse(JSON.stringify(newVal));
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchAllParks();
        vm.form = document.forms.parkForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
            // Note: fetching allowed activities here for the initially selected park
            vm.fetchAllowedActivities();
        });
    },
    methods: {
        refreshFromResponse: function (updated_docs) {
            this.park.events_park_documents = updated_docs;
        },
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
            }
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.park = {};
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            $(this.$refs.park_activities_select).val(null).trigger('change');
            $(this.$refs.events_park).val(null).trigger('change');
            this.selected_activities = [];
            this.events_park_id = null;
            this.validation_form.resetForm();
        },
        fetchContact: function (id) {
            let vm = this;
            helpers.fetchUrl(api_endpoints.contact(id)).then(
                (response) => {
                    vm.contact = response;
                    vm.isModalOpen = true;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        fetchAllParks_orig: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.event_park_container).then(
                (response) => {
                    vm.parks_list = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        fetchAllParks: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.event_park_container).then(
                (response) => {
                    if (vm.is_external) {
                        vm.parks_list = response['parks_external'];
                    } else {
                        vm.parks_list = response['parks'];
                    }
                    vm.park_activities = response['event_activity_types'];
                },
                (error) => {
                    console.log(error);
                }
            );
        },

        fetchActivities: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(api_endpoints.parks, 'land_parks')
                )
                .then(
                    (response) => {
                        vm.land_parks = response;
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },

        fetchPark: function (vid) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_events_parks,
                        vid
                    )
                )
                .then(
                    (res) => {
                        vm.park = res;
                        if (vm.park.park) {
                            vm.events_park_id = vm.park.park.id;
                            $(vm.$refs.events_park)
                                .val(vm.park.park.id)
                                .trigger('change');
                        }
                        if (vm.park.activities_assessor) {
                            vm.selected_activities =
                                vm.park.activities_assessor;
                            $(vm.$refs.park_activities_select)
                                .val(vm.park.activities_assessor)
                                .trigger('change');
                        }
                        vm.fetchAllowedActivities();
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        fetchAllowedActivities: function () {
            /* Searches for dictionary in list */
            let vm = this;
            console.log(
                `Fetching allowed activities for park ID: ${vm.events_park_id}`
            );
            for (var i = 0; i < vm.parks_list.length; i++) {
                if (vm.parks_list[i].id == vm.events_park_id) {
                    vm.allowed_activities = vm.parks_list[i].allowed_activities;
                }
            }
            $(vm.$refs.park_activities_select).trigger('change');
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            if (vm.events_park_id != null) {
                vm.park.park = vm.events_park_id;
            }
            vm.park.activities_assessor = vm.selected_activities;
            let park = JSON.parse(JSON.stringify(vm.park));
            let formData = new FormData();

            formData.append('data', JSON.stringify(park));
            vm.issuingPark = true;
            if (vm.localParkAction == 'add' && vm.park_id == null) {
                helpers
                    .fetchUrl(api_endpoints.proposal_events_parks, {
                        method: 'POST',
                        body: formData,
                    })
                    .then(
                        (response) => {
                            vm.issuingPark = false;
                            vm.park = {};
                            vm.close();
                            swal.fire({
                                title: 'Created',
                                text: 'New park record has been created.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingPark = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.proposal_events_parks,
                            vm.park_id + '/edit_park'
                        ),
                        {
                            method: 'POST',
                            body: formData,
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingPark = false;
                            vm.park = {};
                            vm.close();
                            swal.fire({
                                title: 'Saved',
                                text: 'Park details has been saved.',
                                icon: 'success',
                            });
                            vm.$emit('refreshFromResponse', response);
                        },
                        (error) => {
                            vm.hasErrors = true;
                            vm.issuingPark = false;
                            vm.errorString = helpers.apiVueResourceError(error);
                        }
                    );
            }
        },
        addFormValidations: function () {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {},
                messages: {},
                showErrors: function (errorMap, errorList) {
                    $.each(this.validElements(), function (index, element) {
                        var $element = $(element);
                        $element
                            .attr('data-original-title', '')
                            .parents('.form-group')
                            .removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    // $('.' + this.settings.validClass).tooltip('destroy');
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: 'focus',
                            })
                            .attr('data-original-title', error.message)
                            .parents('.form-group')
                            .addClass('has-error');
                    }
                },
            });
        },
        eventListeners: function () {
            let vm = this;

            helpers.initialiseSelect2
                .bind(this)(
                    'events_park',
                    'events_park_modal',
                    'events_park_id',
                    'Select Park',
                    true
                )
                .on('select2:select', function () {
                    console.log('Park selected');
                    vm.fetchAllowedActivities();
                });

            // Initialise select2 for Activity types
            $(vm.$refs.park_activities_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Activities',
                    dropdownParent: $('#park_activities_select_modal'),
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_activities = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_activities = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
