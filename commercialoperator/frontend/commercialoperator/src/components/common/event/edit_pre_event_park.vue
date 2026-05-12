<template lang="html">
    <div id="editPreEventPark">
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
                                    <!-- Attach the select2 dropdown to this id -->
                                    <div
                                        id="pre_event_park_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            ref="pre_event_park"
                                            v-model="pre_event_park_id"
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
                                            >Activity Types</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            v-model="park.activities"
                                            type="text"
                                            class="form-control"
                                            name="pre_event_name"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Maps/ Documents</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="add_attachments"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <FileField2
                                                ref="filefield"
                                                :uploaded_documents="
                                                    park.pre_event_park_documents
                                                "
                                                :delete_url="delete_url"
                                                :proposal_id="park_id"
                                                :is-repeatable="true"
                                                name="pre_event_park_file"
                                                @refreshFromResponse="
                                                    refreshFromResponse
                                                "
                                            />
                                        </div>
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
                    <i class="fa fa-spinner fa-spin"></i> Processing
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
import FileField2 from '@/components/forms/filefield2.vue';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Edit-Park-Activity',
    components: {
        modal,
        alert,
        FileField2,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        park_action: {
            type: String,
            default: 'edit',
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            park: Object,
            park_id: Number,
            pre_event_park_id: Number,
            state: 'proposed_park',
            issuingPark: false,
            parks_list: [],
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
                ? '/api/proposal_pre_event_parks/' +
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
        });
        vm.park.pre_event_park_documents =
            vm.$refs.filefield.uploaded_documents;
    },
    methods: {
        refreshFromResponse: function (updated_docs) {
            this.park.pre_event_park_documents = updated_docs;
        },
        ok: function () {
            let vm = this;
            if ($(vm.form).valid()) {
                vm.sendData();
                vm.$refs.filefield.reset_files();
            }
        },
        cancel: function () {
            this.close();
            this.$refs.filefield.reset_files();
        },
        close: function () {
            this.isModalOpen = false;
            this.park = {};
            this.$refs.filefield.reset_files();
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
            $(this.$refs.pre_event_park).val(null).trigger('change');
            this.selected_activities = [];
            this.pre_event_park_id = null;
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
        fetchAllParks: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.parks,
                        'events_parks_list'
                    )
                )
                .then(
                    (response) => {
                        vm.parks_list = response;
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
                        api_endpoints.proposal_pre_event_parks,
                        vid
                    )
                )
                .then(
                    (res) => {
                        vm.park = res;
                        if (vm.park.park) {
                            vm.pre_event_park_id = vm.park.park.id;
                            $(vm.$refs.pre_event_park)
                                .val(vm.park.park.id)
                                .trigger('change');
                        }
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },
        fetchAllowedActivities: function () {
            /* Searches for dictionary in list */
            let vm = this;
            for (var i = 0; i < vm.parks_list.length; i++) {
                if (vm.parks_list[i].id == vm.pre_event_park_id) {
                    vm.allowed_activities = vm.parks_list[i].allowed_activities;
                }
            }
            $(vm.$refs.activities_select).trigger('change');
        },
        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            if (vm.pre_event_park_id != null) {
                vm.park.park = vm.pre_event_park_id;
            }
            let park = JSON.parse(JSON.stringify(vm.park));
            let formData = new FormData();
            var files = vm.$refs.filefield.files;
            $.each(files, function (idx, v) {
                var file = v['file'];
                var filename = v['name'];
                var name = 'file-' + idx;
                formData.append(name, file, filename);
            });
            park.num_files = files.length;
            park.input_name = 'pre_event_park_doc';

            formData.append('data', JSON.stringify(park));
            vm.issuingPark = true;
            if (vm.localParkAction == 'add' && vm.park_id == null) {
                helpers
                    .fetchUrl(api_endpoints.proposal_pre_event_parks, {
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
                            api_endpoints.proposal_pre_event_parks,
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
            $(vm.$refs.pre_event_park)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Park',
                    dropdownParent: $('#pre_event_park_modal'),
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.pre_event_park_id = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.pre_event_park_id = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
