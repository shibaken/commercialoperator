<template lang="html">
    <div id="editEventTrailSection2">
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
                                            >Trail</label
                                        >
                                    </div>
                                    <div
                                        id="events_trail_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            ref="events_trail"
                                            v-model="events_trail_id"
                                            class="form-control"
                                            name="event_trail_new"
                                        >
                                            <option
                                                v-for="t in trails_list"
                                                :key="t.id"
                                                :value="t.id"
                                            >
                                                {{ t.name }}
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
                                            >Sections</label
                                        >
                                    </div>
                                    <div
                                        id="events_section_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            ref="events_section"
                                            v-model="section_id"
                                            class="form-control"
                                            name="event_trail_section"
                                        >
                                            <option
                                                v-for="s in trail_list_filter"
                                                :key="s.id"
                                                :value="s.id"
                                            >
                                                {{ s.name }}
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
                                            >Activity Types</label
                                        >
                                    </div>

                                    <div class="col-sm-9">
                                        <input
                                            v-model="
                                                trail.event_trail_activities
                                            "
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
                                            >Activity Types (internal)
                                        </label>
                                    </div>
                                    <div
                                        id="trail_activities_select_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            ref="trail_activities_select"
                                            v-model="selected_activities"
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            multiple
                                        >
                                            <option
                                                v-for="a in trail_activities"
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
                    class="btn btn-secondary"
                    @click="ok"
                >
                    <i class="fas fa-spinner fa-spin"></i> Processing
                </button>
                <button
                    v-else
                    type="button"
                    class="btn btn-secondary"
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
    name: 'Edit-Trail-Activity-Event',
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
        trail_action: {
            type: String,
            default: 'edit',
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            trail: Object,
            trail_id: Number,
            section_id: Number,
            events_trail_id: Number,
            state: 'proposed_park',
            issuingPark: false,
            trails_list: [],
            section_list: [],
            trail_activities: [],
            selected_activities: [],
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            localTrailAction: JSON.parse(JSON.stringify(this.trail_action)),
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.localTrailAction == 'add'
                ? 'Add a new Trail'
                : 'Edit a Trail';
        },
        delete_url: function () {
            return this.park_id
                ? '/api/proposal_events_trails/' +
                      this.park_id +
                      '/delete_document/'
                : '';
        },
        trail_list_filter: function () {
            let trail_list = [];
            var vm = this;
            for (var i = 0; i < vm.trails_list.length; i++) {
                if (vm.trails_list[i].id == vm.events_trail_id) {
                    //vm.section_list = vm.trails_list[i].sections;
                    //vm.section_list = helpers.copyObject(vm.trails_list[i].sections)
                    return vm.trails_list[i].sections;
                }
            }

            // Note: I added this return statement. It didn't exist before.
            return trail_list;
        },
    },
    watch: {
        trail_action: {
            handler(newVal) {
                this.localTrailAction = JSON.parse(JSON.stringify(newVal));
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchAllTrails();
        vm.form = document.forms.parkForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        refreshFromResponse: function (updated_docs) {
            this.park.events_trail_documents = updated_docs;
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
            this.trail = {};
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            $(this.$refs.trail_activities_select).val(null).trigger('change');
            $(this.$refs.events_trail).val(null).trigger('change');
            $(this.$refs.events_section).val(null).trigger('change');
            this.selected_activities = [];
            this.section_list = [];
            this.events_trail_id = null;
            this.section_id = null;
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

        fetchAllTrails_orig: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.trails).then(
                (response) => {
                    vm.trails_list = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        fetchAllTrails: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.event_trail_container).then(
                (response) => {
                    vm.trails_list = response['trails'];
                    vm.trail_activities = response['event_activity_types'];
                },
                (error) => {
                    console.log(error);
                }
            );
        },

        fetchTrail: function (vid) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_events_trails,
                        vid
                    )
                )
                .then(
                    (res) => {
                        vm.trail = res;
                        if (vm.trail.trail) {
                            vm.events_trail_id = vm.trail.trail.id;
                            if (vm.trail.section) {
                                vm.section_id = vm.trail.section.id;
                            }

                            $(vm.$refs.events_trail)
                                .val(vm.trail.trail.id)
                                .trigger('change');
                            vm.fetchSections();
                            if (vm.trail.section) {
                                $(vm.$refs.events_section)
                                    .val(vm.trail.section.id)
                                    .trigger('change');
                            }
                        }
                        if (vm.trail.activities_assessor) {
                            vm.selected_activities =
                                vm.trail.activities_assessor;
                            $(vm.$refs.trail_activities_select)
                                .val(vm.trail.activities_assessor)
                                .trigger('change');
                        }
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },

        fetchSections: function () {
            /* Searches for dictionary in list */
            let vm = this;
            vm.section_list = [];
            $(this.$refs.events_section).val(null).trigger('change');
            for (var i = 0; i < vm.trails_list.length; i++) {
                if (vm.trails_list[i].id == vm.events_trail_id) {
                    vm.section_list = helpers.copyObject(
                        vm.trails_list[i].sections
                    );
                }
            }
            $(vm.$refs.events_section).val(vm.section_list).trigger('change');
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            if (vm.events_trail_id != null) {
                vm.trail.trail = vm.events_trail_id;
            }
            if (vm.section_id != null) {
                vm.trail.section = vm.section_id;
            }
            vm.trail.activities_assessor = vm.selected_activities;
            let trail = JSON.parse(JSON.stringify(vm.trail));
            let formData = new FormData();

            formData.append('data', JSON.stringify(trail));
            vm.issuingPark = true;
            if (vm.localTrailAction == 'add' && vm.trail_id == null) {
                helpers
                    .fetchUrl(api_endpoints.proposal_events_trails, {
                        method: 'POST',
                        body: formData,
                    })
                    .then(
                        (response) => {
                            vm.issuingPark = false;
                            vm.trail = {};
                            vm.close();
                            swal.fire({
                                title: 'Created',
                                text: 'New trail record has been created',
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
                            api_endpoints.proposal_events_trails,
                            vm.trail_id + '/edit_trail'
                        ),
                        {
                            method: 'POST',
                            body: formData,
                        }
                    )
                    .then(
                        (response) => {
                            vm.issuingPark = false;
                            vm.trail = {};
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
            // $(vm.$refs.events_trail)
            //     .select2({
            //         theme: 'bootstrap-5',
            //         allowClear: true,
            //         placeholder: 'Select Park',
            //         dropdownParent: $('#events_trail_modal'),
            //     })
            //     .on('select2:select', function (e) {
            //         var selected = $(e.currentTarget);
            //         vm.events_trail_id = selected.val();
            //     })
            //     .on('select2:unselect', function (e) {
            //         var selected = $(e.currentTarget);
            //         vm.events_trail_id = selected.val();
            //     });
            // $(vm.$refs.events_section)
            //     .select2({
            //         theme: 'bootstrap-5',
            //         allowClear: true,
            //         placeholder: 'Select section',
            //         dropdownParent: $('#events_section_modal'),
            //     })
            //     .on('select2:select', function (e) {
            //         var selected = $(e.currentTarget);
            //         vm.section_id = selected.val();
            //     })
            //     .on('select2:unselect', function (e) {
            //         var selected = $(e.currentTarget);
            //         vm.section_id = selected.val();
            //     });
            //Initialise select2 for Activity types
            $(vm.$refs.trail_activities_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Activities',
                    dropdownParent: $('#trail_activities_select_modal'),
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
