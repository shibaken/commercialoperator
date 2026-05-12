<template lang="html">
    <div id="editTrailActivities">
        <modal
            transition="modal fade"
            :title="title"
            large
            @ok="ok()"
            @cancel="cancel()"
        >
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="vehicleForm">
                        <alert v-if="showError" type="danger"
                            ><strong>{{ errorString }}</strong></alert
                        >
                        <div class="col-sm-12">
                            <form>
                                <div class="form-horizontal col-sm-3">
                                    <label class="control-label"
                                        >Sections</label
                                    >
                                </div>
                            </form>
                            <form>
                                <div class="form-horizontal col-sm-9">
                                    <label class="control-label"
                                        >Activities</label
                                    >
                                </div>
                            </form>
                            <form>
                                <div
                                    v-for="s in trail.sections"
                                    :key="s.name"
                                    class="row"
                                >
                                    <div class="form-horizontal col-sm-3">
                                        <div class="">
                                            <div class="form-check">
                                                <input
                                                    ref="Checkbox"
                                                    v-model="s.checked"
                                                    class="form-check-input"
                                                    type="checkbox"
                                                    data-parsley-required
                                                    :disabled="
                                                        !canEditActivities
                                                    "
                                                /><a
                                                    v-if="s.doc_url"
                                                    :href="s.doc_url"
                                                    target="_blank"
                                                >
                                                    {{ s.name }}</a
                                                ><span v-else>
                                                    {{ s.name }}</span
                                                >
                                            </div>
                                        </div>
                                    </div>

                                    <div class="form-horizontal col-sm-9">
                                        <div
                                            v-for="a in trail.allowed_activities"
                                            :key="a.name"
                                        >
                                            <div class="form-check">
                                                <input
                                                    :id="
                                                        'section' +
                                                        s.id +
                                                        'activity' +
                                                        a.id
                                                    "
                                                    ref="Checkbox"
                                                    v-model="s.new_activities"
                                                    :disabled="
                                                        !s.checked ||
                                                        !canEditActivities
                                                    "
                                                    class="form-check-input"
                                                    type="checkbox"
                                                    :value="a.id"
                                                    data-parsley-required
                                                />
                                                {{ a.name }}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                    </form>
                </div>
            </div>
            <template #footer>
                <button
                    v-if="issuingVehicle"
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
                    :disabled="!canEditActivities"
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
    name: 'Edit-Trail-Activities',
    components: {
        modal,
        alert,
    },
    props: {
        canEditActivities: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            isModalOpen: false,
            form: null,
            trail: Object,
            trail_id: null,
            trail_name: '',
            allowed_activities: [],
            trail_sections: [],
            trail_activities: [],
            issuingVehicle: false,
            validation_form: null,
            hasErrors: false,
            errorString: '',
            successString: '',
            success: false,
            act: [],
        };
    },
    computed: {
        showError: function () {
            var vm = this;
            return vm.hasErrors;
        },
        title: function () {
            return this.trail && this.trail.name
                ? 'Edit Sections and Activities for ' + this.trail.name
                : 'Edit Sections and Activities';
        },
    },
    watch: {
        trail_sections: {
            handler: function () {
                const vm = this;
                // Note: removed_trail was called removed_section, I renamed it to removed_trail
                var removed_trail = $(vm.trail_sections_before)
                    .not(vm.trail_sections)
                    .get();
                // Note: added_trail was called added_section, I renamed it to added_trail
                var added_trail = $(vm.trail_sections)
                    .not(vm.trail_sections_before)
                    .get();
                vm.trail_sections_before = vm.trail_sections;

                if (added_trail.length != 0) {
                    for (var i = 0; i < added_trail.length; i++) {
                        var found = false;
                        for (
                            var j = 0;
                            j < vm.trail_sections_activities.length;
                            j++
                        ) {
                            if (
                                vm.trail_sections_activities[j].trail ==
                                added_trail[i]
                            ) {
                                found = true;
                            }
                        }
                        if (found == false) {
                            const data = {
                                trail: added_trail[i],
                                activities: [],
                            };
                            vm.trail_sections_activities.push(data);
                        }
                    }
                }
                if (removed_trail.length != 0) {
                    // eslint-disable-next-line no-redeclare
                    for (var i = 0; i < removed_trail.length; i++) {
                        for (
                            // eslint-disable-next-line no-redeclare
                            var j = 0;
                            j < vm.trail_sections_activities.length;
                            j++
                        ) {
                            if (
                                vm.trail_sections_activities[j].trail ==
                                removed_trail[i]
                            ) {
                                vm.trail_sections_activities.splice(j, 1);
                            }
                        }
                    }
                }
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.vehicleForm;
        vm.addFormValidations();
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },
    methods: {
        ok: function () {
            let vm = this;

            var allowed_activities_id = [];
            var new_activities = [];
            for (var i = 0; i < vm.trail.allowed_activities.length; i++) {
                allowed_activities_id.push(vm.trail.allowed_activities[i].id);
            }
            for (var j = 0; j < vm.trail.sections.length; j++) {
                if (vm.trail.sections[j].checked == true) {
                    for (
                        var k = 0;
                        k < vm.trail.sections[j].new_activities.length;
                        k++
                    ) {
                        if (
                            allowed_activities_id.indexOf(
                                vm.trail.sections[j].new_activities[k]
                            ) == -1
                        ) {
                            vm.trail.sections[j].new_activities.splice(k, 1);
                        }
                    }
                    var data = {
                        section: vm.trail.sections[j].id,
                        activities: vm.trail.sections[j].new_activities,
                    };
                    new_activities.push(data);
                }
            }
            vm.$emit('refreshTrailFromResponse', vm.trail.id, new_activities);

            vm.close();
        },
        cancel: function () {
            this.close();
        },
        close: function () {
            this.isModalOpen = false;
            this.trail = {};
            this.trail.sections = {};
            this.trail_id = null;
            this.hasErrors = false;
            $('.has-error').removeClass('has-error');
        },
        addnewdata: function () {
            let vm = this;
            for (var i = 0; i < vm.trail.sections.length; i++) {
                vm.trail.sections[i].checked = true;
                vm.trail.sections[i].new_activities = [];
            }
        },
        fetchTrail: function (trail_id) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(api_endpoints.trails, trail_id)
                )
                .then(
                    (res) => {
                        vm.trail = res;
                    },
                    (err) => {
                        console.log(err);
                    }
                );
        },

        addFormValidations: function () {},
        eventListeners: function () {},
    },
};
</script>

<style lang="css"></style>
