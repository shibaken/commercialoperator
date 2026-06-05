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
                                            for="filming_park"
                                            >Park or Reserve</label
                                        >
                                    </div>
                                    <div
                                        id="selected_park_modal"
                                        class="col-sm-9"
                                    >
                                        <select
                                            id="filming_park"
                                            ref="filming_park"
                                            v-model="selected_park_id"
                                            class="form-control"
                                            name="park"
                                        >
                                            <option
                                                v-for="p in all_parks"
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
                                            for="feature_of_interest"
                                            >Feature or site of Interest</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <input
                                            id="feature_of_interest"
                                            ref="feature_of_interest"
                                            v-model="park.feature_of_interest"
                                            class="form-control"
                                            name="feature_of_interest"
                                            type="text"
                                        />
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="park_from_date"
                                            >From</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="from_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                id="park_from_date"
                                                v-model="park.from_date"
                                                type="date"
                                                class="form-control"
                                                name="from_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="park_to_date"
                                            >To</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="to_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                id="park_to_date"
                                                v-model="park.to_date"
                                                type="date"
                                                class="form-control"
                                                name="to_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label class="text-left" for="filefield"
                                            >Please attach a detailed itinerary
                                            and maps which outline specific
                                            locations and roads/tracks/trails to
                                            be used
                                        </label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="add_attachments"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <FileField2
                                                id="filefield"
                                                ref="filefield"
                                                :uploaded_documents="
                                                    park.filming_park_documents
                                                "
                                                :delete_url="delete_url"
                                                :proposal_id="park_id"
                                                :is-repeatable="true"
                                                name="filming_park_file"
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
import FileField2 from '@/components/forms/filefield2.vue';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/component-definition-name-casing
    name: 'Edit-Park',
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
        // eslint-disable-next-line vue/prop-name-casing
        district_proposal: {
            type: Object,
            default: null,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: false,
        },
        canEditActivities: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            park: Object,
            park_id: Number,
            state: 'proposed_park',
            issuingPark: false,
            all_parks: [],
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            dateFormat: 'YYYY-MM-DD',
            selected_park_id: null,
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
                ? '/api/proposal_filming_parks/' +
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
        if (vm.district_proposal) {
            vm.fetchDistrictParks(vm.district_proposal.district);
        } else {
            vm.fetchAllParks();
        }
        vm.form = document.forms.parkForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
        });
        vm.park.filming_park_documents = vm.$refs.filefield.uploaded_documents;
    },
    methods: {
        refreshFromResponse: function (updated_docs) {
            this.park.filming_park_documents = updated_docs;
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
            $(this.$refs.filming_park).val(null).trigger('change');
            // this.$refs.feature_of_interest = '';
            // this.$refs.park = '';
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
        fetchLandParks: function () {
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
        fetchDistrictLandParks: function (id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.districts,
                        id + '/land_parks'
                    )
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
        fetchAllParks: function () {
            let vm = this;
            if (vm.is_external) {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.parks,
                            'filming_parks_external_list'
                        )
                    )
                    .then(
                        (response) => {
                            vm.all_parks = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            } else {
                helpers
                    .fetchUrl(
                        helpers.add_endpoint_json(
                            api_endpoints.parks,
                            'filming_parks_list'
                        )
                    )
                    .then(
                        (response) => {
                            vm.all_parks = response;
                        },
                        (error) => {
                            console.log(error);
                        }
                    );
            }
        },

        fetchDistrictParks: function (id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.districts,
                        id + '/parks'
                    )
                )
                .then(
                    (response) => {
                        vm.all_parks = response;
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
                        api_endpoints.proposal_filming_parks,
                        vid
                    )
                )
                .then(
                    (res) => {
                        vm.park = res;
                        if (vm.park.park) {
                            vm.selected_park_id = vm.park.park.id;
                            $(vm.$refs.filming_park)
                                .val(vm.park.park.id)
                                .trigger('change');
                        }
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },

        sendData: function () {
            let vm = this;
            vm.hasErrors = false;
            if (vm.selected_park_id != null) {
                vm.park.park = vm.selected_park_id;
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
            park.input_name = 'filming_park_doc';

            formData.append('data', JSON.stringify(park));
            vm.issuingPark = true;
            if (vm.localParkAction == 'add' && vm.park_id == null) {
                helpers
                    .fetchUrl(api_endpoints.proposal_filming_parks, {
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
                                text: 'New park record has been created',
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
                            api_endpoints.proposal_filming_parks,
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
                                text: 'Park details has been saved',
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
                rules: {
                    access_type: 'required',
                },
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
            $(vm.$refs.filming_park)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Park',
                    dropdownParent: $('#selected_park_modal'),
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_park_id = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.selected_park_id = selected.val();
                });
        },
    },
};
</script>

<style lang="css"></style>
