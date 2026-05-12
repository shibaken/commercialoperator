<!-- eslint-disable vue/no-v-html -->
<template lang="html">
    <div class="row">
        <div class="col-sm-12">
                <FormSection
                    :form-collapse="false"
                    label="Activities and Location"
                    index="activities_and_location"
                    subtitle="(Parks)"
                >
                    <div class="borderDecoration col-sm-12">
                        <form v-if="park_error_list">
                            <div class="col-sm-12">
                                <div v-for="e in park_error_list" :key="e">
                                    <label style="color: orange">{{ e }}</label>
                                </div>
                            </div>
                        </form>
                        <form>
                            <div
                                v-if="land_access_options.length"
                                class="col-sm-12"
                            >
                                <div>
                                    <label class="control-label"
                                        >Select the required access</label
                                    >
                                    <TreeSelect
                                        ref="selected_access"
                                        v-model="selected_access"
                                        :proposal="proposal"
                                        :options="land_access_options"
                                        :default_expand_level="1"
                                        :disabled="!canEditActivities"
                                    ></TreeSelect>
                                </div>
                            </div>
                            <div v-else>
                                <div v-if="isLoading" class="col-sm-12">
                                    <i class="fas fa-spinner fa-spin"></i>
                                    Loading
                                </div>
                            </div>
                        </form>
                    </div>

                    <div class="borderDecoration col-sm-12">
                        <form>
                            <div
                                v-if="land_activity_options.length"
                                class="col-sm-12"
                            >
                                <div>
                                    <label class="control-label"
                                        >Select the required activities</label
                                    >
                                    <TreeSelect
                                        v-model="selected_activities"
                                        :proposal="proposal"
                                        :options="land_activity_options"
                                        :default_expand_level="1"
                                        :disabled="!canEditActivities"
                                    ></TreeSelect>
                                </div>
                            </div>
                            <div v-else>
                                <div v-if="isLoading" class="col-sm-12">
                                    <i class="fas fa-spinner fa-spin"></i>
                                    Loading
                                </div>
                            </div>
                        </form>
                    </div>

                    <div class="borderDecoration col-sm-12">
                        <form>
                            <div v-if="park_options.length" class="col-sm-12">
                                <div>
                                    <label class="control-label"
                                        >Select Parks</label
                                    >
                                    <TreeSelect
                                        v-model="selected_parks"
                                        :proposal="proposal"
                                        :options="park_options"
                                        :default_expand_level="1"
                                        :allow_edit="true"
                                        :disabled="!canEditActivities"
                                    ></TreeSelect>
                                </div>
                            </div>
                            <div v-else>
                                <div v-if="isLoading" class="col-sm-12">
                                    <i class="fas fa-spinner fa-spin"></i>
                                    Loading
                                </div>
                            </div>
                        </form>
                    </div>

                    <div class="borderDecoration col-sm-12">
                        <div v-for="rd in required_documents_list" :key="rd.id">
                            <div v-if="rd.can_view">
                                <label for="label" v-html="rd.question"></label>
                                <FileField
                                    :id="
                                        'proposal' +
                                        proposal.id +
                                        'req_doc' +
                                        rd.id
                                    "
                                    :proposal_id="proposal.id"
                                    :is-repeatable="true"
                                    :name="'req_doc' + rd.id"
                                    :required_doc_id="rd.id"
                                    label="Add Document"
                                    :readonly="!canEditActivities"
                                ></FileField>
                            </div>
                        </div>
                    </div>
                    <div class="borderDecoration col-sm-12">
                        <label class="control-label"
                            >Provide details of every vehicle you plan to use
                            when accessing the parks. 'Hire vehicle' can be
                            entered as the vehicle registration if the hire
                            vehicle details are not yet known.</label
                        >
                        <VehicleTable
                            ref="vehicles_table"
                            :url="vehicles_url"
                            :proposal="proposal"
                            :access_types="land_access_types"
                        ></VehicleTable>
                    </div>
                </FormSection>

                <FormSection
                    :form-collapse="false"
                    label="Activities and Location"
                    index="activities_and_location"
                    subtitle="(Trails)"
                >
                    <div>
                        <div class="borderDecoration col-sm-12">
                            <form v-if="trail_error_list">
                                <div class="col-sm-12">
                                    <div v-for="e in trail_error_list" :key="e">
                                        <label style="color: orange">{{
                                            e
                                        }}</label>
                                    </div>
                                </div>
                            </form>
                            <form>
                                <div
                                    v-if="trail_activity_options.length"
                                    class="col-sm-12"
                                >
                                    <div>
                                        <label class="control-label"
                                            >Select the required activities for
                                            trails</label
                                        >
                                        <TreeSelect
                                            v-model="trail_activities"
                                            :proposal="proposal"
                                            :options="trail_activity_options"
                                            :default_expand_level="1"
                                            :disabled="!canEditActivities"
                                        ></TreeSelect>
                                    </div>
                                </div>
                                <div v-else>
                                    <div v-if="isLoading" class="col-sm-12">
                                        <i class="fas fa-spinner fa-spin"></i>
                                        Loading
                                    </div>
                                </div>
                            </form>
                        </div>

                        <div class="borderDecoration col-sm-12">
                            <form>
                                <div
                                    v-if="trail_options.length"
                                    class="col-sm-12"
                                >
                                    <div>
                                        <label class="control-label"
                                            >Select the long distance
                                            trails</label
                                        >
                                        <TreeSelect
                                            v-model="selected_trail_ids"
                                            :proposal="proposal"
                                            :options="trail_options"
                                            :default_expand_level="1"
                                            open_direction="top"
                                            :allow_edit="true"
                                            :disabled="!canEditActivities"
                                        ></TreeSelect>
                                    </div>
                                </div>
                                <div v-else>
                                    <div v-if="isLoading" class="col-sm-12">
                                        <i class="fas fa-spinner fa-spin"></i>
                                        Loading
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </FormSection>

            <div>
                <editParkActivities
                    ref="edit_activities"
                    :proposal="proposal"
                    :can-edit-activities="canEditActivities"
                    @refreshSelectionFromResponse="refreshSelectionFromResponse"
                ></editParkActivities>
            </div>
            <div>
                <editTrailActivities
                    ref="edit_sections"
                    :proposal="proposal"
                    :can-edit-activities="canEditActivities"
                    @refreshTrailFromResponse="refreshTrailFromResponse"
                ></editTrailActivities>
            </div>
        </div>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import VehicleTable from '@/components/common/vehicle_table.vue';
import editParkActivities from './edit_park_activities.vue';
import editTrailActivities from './edit_trail_activities.vue';
import FileField from './required_docs.vue';
import TreeSelect from '@/components/forms/treeview.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'ActivitiesLand',
    components: {
        FormSection,
        VehicleTable,
        editParkActivities,
        editTrailActivities,
        FileField,
        TreeSelect,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        canEditActivities: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        proposal_parks: {
            type: Object,
            required: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        let vm = this;
        return {
            park_options: [],
            land_access_options: [],
            land_activity_options: [],
            trail_options: [],
            trail_activity_options: [],
            land_access_types: [],
            added_trail_id: [],
            removed_trail_id: [],

            pBody: 'pBody' + uuid(),
            tBody: 'lBody' + uuid(),
            values: null,
            accessTypes: null,
            api_regions: null,
            trails: null,
            required_documents_list: null,
            selected_parks: [],
            selected_parks_before: [],
            selected_access: [],
            selected_access_before: [],
            selected_activities: [],
            selected_activities_before: [],
            selected_trails: [],
            selected_trail_ids: [],
            selected_trail_ids_before: [],
            trail_activities: [],
            trail_activities_before: [],
            activities: [],
            access: [],
            selected_regions: [],
            selected_regions_before: [],
            selected_districts: [],
            select_all: false,
            vehicles_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/vehicles'
            ),
            selected_parks_activities: [],
            selected_trails_activities: [],
            trail_error_list: [],
            park_error_list: [],
            isLoading: false,
            selected_activities_initialised: false, //track whether or not selected activities have been initialised - prevent other values being altered until initial state loaded
            selected_access_initialised: false,
        };
    },
    computed: {},
    watch: {
        selected_trail_ids: {
            handler: function () {
                let vm = this;

                vm.selected_trails = [];
                for (var i = 0; i < vm.selected_trail_ids.length; i++) {
                    var data = vm.get_selected_trail_data(
                        vm.selected_trail_ids[i]
                    );
                    if (data !== null) {
                        vm.selected_trails.push(data);
                    }
                }

                try {
                    var removed_trail_id = $(vm.selected_trail_ids_before)
                        .not(vm.selected_trail_ids)
                        .get();
                } catch (error) {
                    console.log('removed_trail: ' + error);
                }

                try {
                    var added_trail_id = $(vm.selected_trail_ids)
                        .not(vm.selected_trail_ids_before)
                        .get();
                } catch (error) {
                    console.log('added_trail: ' + error);
                }
                vm.selected_trail_ids_before = vm.selected_trail_ids;

                var current_activities = vm.trail_activities;

                if (vm.selected_trails_activities.length == 0) {
                    for (let i = 0; i < vm.selected_trails.length; i++) {
                        // eslint-disable-next-line no-redeclare
                        var data = null;
                        var section_activities = [];

                        for (
                            var j = 0;
                            j < vm.selected_trails[i].sections.length;
                            j++
                        ) {
                            var section_data = {
                                section: vm.selected_trails[i].sections[j],
                                activities: current_activities,
                            };
                            section_activities.push(section_data);
                        }
                        data = {
                            trail: vm.selected_trails[i].trail,
                            activities: section_activities,
                        };
                        vm.selected_trails_activities.push(data);
                    }
                } else {
                    if (added_trail_id.length != 0) {
                        for (let i = 0; i < added_trail_id.length; i++) {
                            var found = false;
                            for (
                                let j = 0;
                                j < vm.selected_trails_activities.length;
                                j++
                            ) {
                                if (
                                    vm.selected_trails_activities[j].trail ==
                                    added_trail_id[i]
                                ) {
                                    found = true;
                                }
                            }
                            if (found == false) {
                                //original data object
                                // eslint-disable-next-line no-redeclare
                                var section_activities = [];
                                var trail_data = vm.get_selected_trail_data(
                                    added_trail_id[i]
                                );
                                if (trail_data !== null) {
                                    for (
                                        var k = 0;
                                        k < trail_data.sections.length;
                                        k++
                                    ) {
                                        // eslint-disable-next-line no-redeclare
                                        var section_data = {
                                            section: trail_data.sections[k],
                                            activities: current_activities,
                                        };
                                        section_activities.push(section_data);
                                    }
                                    data = {
                                        trail: added_trail_id[i],
                                        activities: section_activities,
                                    };
                                }
                                vm.selected_trails_activities.push(data);
                            }
                        }
                    }
                    if (removed_trail_id.length != 0) {
                        for (let i = 0; i < removed_trail_id.length; i++) {
                            for (
                                let j = 0;
                                j < vm.selected_trails_activities.length;
                                j++
                            ) {
                                if (
                                    vm.selected_trails_activities[j].trail ==
                                    removed_trail_id[i]
                                ) {
                                    vm.selected_trails_activities.splice(j, 1);
                                }
                            }
                        }
                    }
                }
                if (vm.proposal) {
                    vm.proposal.trails = vm.selected_trails;
                    vm.proposal.selected_trails_activities =
                        vm.selected_trails_activities;
                }
            },
            deep: true,
        },

        selected_parks: {
            handler: function () {
                let vm = this;
                var removed_park = $(vm.selected_parks_before)
                    .not(vm.selected_parks)
                    .get();
                var added_park = $(vm.selected_parks)
                    .not(vm.selected_parks_before)
                    .get();
                vm.selected_parks_before = vm.selected_parks;

                var current_activities = vm.selected_activities;
                var current_access = vm.selected_access;

                if (vm.selected_parks_activities.length == 0) {
                    for (var i = 0; i < vm.selected_parks.length; i++) {
                        var data = null;
                        data = {
                            park: vm.selected_parks[i],
                            activities: current_activities,
                            access: current_access,
                        };
                        vm.selected_parks_activities.push(data);
                    }
                } else {
                    if (added_park.length != 0) {
                        for (let i = 0; i < added_park.length; i++) {
                            var found = false;
                            for (
                                var j = 0;
                                j < vm.selected_parks_activities.length;
                                j++
                            ) {
                                if (
                                    vm.selected_parks_activities[j].park ==
                                    added_park[i]
                                ) {
                                    found = true;
                                }
                            }
                            if (found == false) {
                                data = {
                                    park: added_park[i],
                                    activities: current_activities,
                                    access: current_access,
                                };
                                vm.selected_parks_activities.push(data);
                            }
                        }
                    }
                    if (removed_park.length != 0) {
                        for (let i = 0; i < removed_park.length; i++) {
                            for (
                                let j = 0;
                                j < vm.selected_parks_activities.length;
                                j++
                            ) {
                                if (
                                    vm.selected_parks_activities[j].park ==
                                    removed_park[i]
                                ) {
                                    vm.selected_parks_activities.splice(j, 1);
                                }
                            }
                        }
                    }
                }
            },
            deep: true,
        },
        selected_activities: {
            handler: function () {
                let vm = this;
                var removed = $(vm.selected_activities_before)
                    .not(vm.selected_activities)
                    .get();
                var added = [];
                if (vm.selected_activities_initialised) {
                    added = $(vm.selected_activities)
                        .not(vm.selected_activities_before)
                        .get();
                } else {
                    vm.selected_activities_initialised = true;
                }
                vm.selected_activities_before = vm.selected_activities;
                if (vm.selected_parks_activities.length == 0) {
                    for (var i = 0; i < vm.selected_parks.length; i++) {
                        var data = null;
                        data = {
                            park: vm.selected_parks[i],
                            activities: vm.selected_activities,
                            access: vm.selected_access,
                        };
                        vm.selected_parks_activities.push(data);
                    }
                } else {
                    for (
                        let i = 0;
                        i < vm.selected_parks_activities.length;
                        i++
                    ) {
                        if (added.length != 0) {
                            for (var j = 0; j < added.length; j++) {
                                if (
                                    vm.selected_parks_activities[
                                        i
                                    ].activities.indexOf(added[j]) < 0
                                ) {
                                    vm.selected_parks_activities[
                                        i
                                    ].activities.push(added[j]);
                                }
                            }
                        }
                        if (removed.length != 0) {
                            for (let j = 0; j < removed.length; j++) {
                                var index = vm.selected_parks_activities[
                                    i
                                ].activities.indexOf(removed[j]);
                                if (index != -1) {
                                    vm.selected_parks_activities[
                                        i
                                    ].activities.splice(index, 1);
                                }
                            }
                        }
                    }
                }
                vm.checkRequiredDocuements(vm.selected_parks_activities);
                vm.checkAllowedActivitiesPark();
            },
            deep: true,
        },
        selected_access: {
            handler: function () {
                let vm = this;
                var removed = $(vm.selected_access_before)
                    .not(vm.selected_access)
                    .get();
                var added = [];
                if (vm.selected_access_initialised) {
                    added = $(vm.selected_access)
                        .not(vm.selected_access_before)
                        .get();
                } else {
                    vm.selected_access_initialised = true;
                }
                vm.selected_access_before = vm.selected_access;
                if (vm.selected_parks_activities.length == 0) {
                    for (var i = 0; i < vm.selected_parks.length; i++) {
                        var data = null;
                        data = {
                            park: vm.selected_parks[i],
                            activities: vm.selected_activities,
                            access: vm.selected_access,
                        };
                        vm.selected_parks_activities.push(data);
                    }
                } else {
                    for (
                        let i = 0;
                        i < vm.selected_parks_activities.length;
                        i++
                    ) {
                        if (added.length != 0) {
                            for (var j = 0; j < added.length; j++) {
                                if (
                                    vm.selected_parks_activities[
                                        i
                                    ].access.indexOf(added[j]) < 0
                                ) {
                                    vm.selected_parks_activities[i].access.push(
                                        added[j]
                                    );
                                }
                            }
                        }
                        if (removed.length != 0) {
                            for (let j = 0; j < removed.length; j++) {
                                var index = vm.selected_parks_activities[
                                    i
                                ].access.indexOf(removed[j]);
                                if (index != -1) {
                                    vm.selected_parks_activities[
                                        i
                                    ].access.splice(index, 1);
                                }
                            }
                        }
                    }
                }
                vm.checkAllowedActivitiesPark();
            },
            deep: true,
        },
        selected_parks_activities: {
            handler: function () {
                let vm = this;
                vm.checkRequiredDocuements(vm.selected_parks_activities);
                if (vm.proposal) {
                    vm.proposal.selected_parks_activities =
                        vm.selected_parks_activities;
                    vm.proposal.selected_land_access = vm.selected_access;
                    vm.proposal.selected_land_activities =
                        vm.selected_activities;
                }
                vm.checkAllowedActivitiesPark();
            },
            deep: true,
        },
        selected_trails_activities: {
            handler: function () {
                let vm = this;
                vm.checkAllowedActivities();
                if (vm.proposal) {
                    vm.proposal.selected_trails_activities =
                        vm.selected_trails_activities;
                }
            },
            deep: true,
        },
        trail_activities: {
            handler: function () {
                let vm = this;
                var removed = $(vm.trail_activities_before)
                    .not(vm.trail_activities)
                    .get();
                var added = $(vm.trail_activities)
                    .not(vm.trail_activities_before)
                    .get();
                vm.trail_activities_before = vm.trail_activities;
                if (vm.selected_trails_activities.length == 0) {
                    for (var i = 0; i < vm.selected_trail_ids.length; i++) {
                        var data = null;
                        data = {
                            trail: vm.selected_trail_ids[i],
                            activities: vm.trail_activities,
                        };
                        vm.selected_trails_activities.push(data);
                    }
                } else {
                    for (
                        let i = 0;
                        i < vm.selected_trails_activities.length;
                        i++
                    ) {
                        if (added.length != 0) {
                            for (var j = 0; j < added.length; j++) {
                                for (
                                    var k = 0;
                                    k <
                                    vm.selected_trails_activities[i].activities
                                        .length;
                                    k++
                                ) {
                                    if (
                                        vm.selected_trails_activities[
                                            i
                                        ].activities[k].activities.indexOf(
                                            added[j]
                                        ) < 0
                                    ) {
                                        vm.selected_trails_activities[
                                            i
                                        ].activities[k].activities.push(
                                            added[j]
                                        );
                                    }
                                }
                            }
                        }
                        if (removed.length != 0) {
                            for (let j = 0; j < removed.length; j++) {
                                for (
                                    let k = 0;
                                    k <
                                    vm.selected_trails_activities[i].activities
                                        .length;
                                    k++
                                ) {
                                    var index = vm.selected_trails_activities[
                                        i
                                    ].activities[k].activities.indexOf(
                                        removed[j]
                                    );
                                    if (index != -1) {
                                        vm.selected_trails_activities[
                                            i
                                        ].activities[k].activities.splice(
                                            index,
                                            1
                                        );
                                    }
                                }
                            }
                        }
                    }
                }
                vm.checkAllowedActivities();
            },
            deep: true,
        },
    },

    mounted: function () {
        let vm = this;
        vm.fetchParkTreeview();

        vm.proposal.selected_trails_activities = [];
        vm.proposal.selected_parks_activities = [];
        vm.selected_parks_activities = [];

        if (vm.proposal_parks && Object.keys(vm.proposal_parks).length > 0) {
            for (var i = 0; i < vm.proposal_parks.land_parks.length; i++) {
                if (
                    vm.is_external &&
                    !vm.proposal_parks.land_parks[i].park.visible_to_external
                ) {
                    //
                } else {
                    var current_park = vm.proposal_parks.land_parks[i].park.id;
                    var current_activities = [];
                    var current_access = [];
                    for (
                        var j = 0;
                        j <
                        vm.proposal_parks.land_parks[i].land_activities.length;
                        j++
                    ) {
                        current_activities.push(
                            vm.proposal_parks.land_parks[i].land_activities[j]
                                .activity.id
                        );
                    }
                    for (
                        var k = 0;
                        k < vm.proposal_parks.land_parks[i].access_types.length;
                        k++
                    ) {
                        current_access.push(
                            vm.proposal_parks.land_parks[i].access_types[k]
                                .access_type.id
                        );
                    }
                    var data = {
                        park: current_park,
                        activities: current_activities,
                        access: current_access,
                    };
                    vm.selected_parks_activities.push(data);
                }
            }

            var activity_list = [];
            var access_list = [];
            var park_list = [];
            for (let i = 0; i < vm.selected_parks_activities.length; i++) {
                park_list.push(vm.selected_parks_activities[i].park);
                activity_list.push({
                    key: vm.selected_parks_activities[i].activities,
                });
                access_list.push({
                    key: vm.selected_parks_activities[i].access,
                });
            }

            vm.selected_parks = park_list;
            vm.selected_activities = vm.find_repeated(activity_list);
            vm.selected_access = vm.find_repeated(access_list);
        }
        this.$nextTick(() => {});

        vm.store_trails(vm.proposal_parks.trails);

        vm.selected_trail_ids = vm.get_selected_trail_ids();
        vm.selected_trail_ids_before = vm.selected_trail_ids;

        $('a[data-bs-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
    },
    updated: function () {},
    created: function () {},
    methods: {
        get_selected_trail_data: function (trail_id) {
            let vm = this;
            if (!vm.trails) {
                // trails may be null if the API call has not returned yet
                return null;
            }
            for (var i = 0; i < vm.trails.length; i++) {
                if (vm.trails[i].id == trail_id) {
                    return {
                        trail: trail_id,
                        sections: vm.trails[i].section_ids,
                    };
                }
            }
            return null;
        },
        get_selected_trail_ids: function () {
            let vm = this;

            var ids = [];
            for (var i = 0; i < vm.selected_trails.length; i++) {
                ids.push(vm.selected_trails[i].trail);
            }
            return ids.filter(function (item, pos) {
                return ids.indexOf(item) == pos;
            }); // returns unique array ids
        },

        fetchParkTreeview: function () {
            let vm = this;
            vm.isLoading = true;

            helpers.fetchUrl(api_endpoints.tclass_container_land).then(
                (response) => {
                    if (vm.is_external) {
                        vm.park_options = [
                            {
                                id: 'All',
                                name: 'Select all parks from all regions external',
                                children: response['land_parks_external'], // land_parks --> regions/districts/parks nested json
                            },
                        ];
                    } else {
                        vm.park_options = [
                            {
                                id: 'All',
                                name: 'Select all parks from all regions',
                                children: response['land_parks'], // land_parks --> regions/districts/parks nested json
                            },
                        ];
                    }
                    vm.api_regions = response['land_parks'];

                    vm.land_access_options = [
                        {
                            id: 'All',
                            name: 'Select all',
                            children: response['access_types'],
                        },
                    ];
                    vm.land_access_types = response['access_types']; // needed to pass to Vehicle component
                    vm.access = response['access_types']; // needed to pass to Vehicle component

                    vm.land_activity_options = [
                        {
                            id: 'All',
                            name: 'Select all',
                            children: response['land_activity_types'],
                        },
                    ];
                    vm.trail_activity_options = [
                        {
                            id: 'All',
                            name: 'Select all',
                            children: response['trail_activity_types'],
                        },
                    ];

                    vm.activities = response['land_activity_types']; // needed to pass to Vehicle component

                    vm.trail_options = [
                        {
                            id: 'All',
                            name: 'Select all',
                            children: response['trails'],
                        },
                    ];
                    vm.trails = response['trails'];
                    vm.required_documents_list =
                        response['land_required_documents'];
                    vm.fetchRequiredDocumentList();
                    vm.isLoading = false;
                },
                (error) => {
                    console.log(error);
                    vm.isLoading = false;
                }
            );
        },
        fetchRequiredDocumentList: function () {
            let vm = this;
            for (var l = 0; l < vm.required_documents_list.length; l++) {
                vm.required_documents_list[l].can_view = false;
                vm.checkRequiredDocuements(vm.selected_parks_activities);
            }
        },
        checkRequiredDocuements: function (selected_parks_activities) {
            let vm = this;
            //Check if the combination of selected park and activities require a document to be attahced
            if (vm.required_documents_list) {
                for (var l = 0; l < vm.required_documents_list.length; l++) {
                    vm.required_documents_list[l].can_view = false;
                }

                for (var i = 0; i < selected_parks_activities.length; i++) {
                    for (
                        var j = 0;
                        j < vm.required_documents_list.length;
                        j++
                    ) {
                        if (vm.required_documents_list[j].park != null) {
                            if (
                                vm.required_documents_list[j].activity == null
                            ) {
                                if (
                                    vm.required_documents_list[j].park ==
                                    selected_parks_activities[i].park
                                ) {
                                    vm.required_documents_list[j].can_view =
                                        true;
                                }
                            } else {
                                for (
                                    var k = 0;
                                    k <
                                    selected_parks_activities[i].activities
                                        .length;
                                    k++
                                ) {
                                    if (
                                        vm.required_documents_list[j].park ==
                                        selected_parks_activities[i].park
                                    ) {
                                        if (
                                            vm.required_documents_list[j]
                                                .activity ==
                                            selected_parks_activities[i]
                                                .activities[k]
                                        ) {
                                            vm.required_documents_list[
                                                j
                                            ].can_view = true;
                                        }
                                    }
                                }
                            }
                        } else if (
                            vm.required_documents_list[j].activity != null
                        ) {
                            for (
                                let k = 0;
                                k <
                                selected_parks_activities[i].activities.length;
                                k++
                            ) {
                                if (
                                    vm.required_documents_list[j].activity ==
                                    selected_parks_activities[i].activities[k]
                                ) {
                                    vm.required_documents_list[j].can_view =
                                        true;
                                }
                            }
                        }
                    }
                }
            }
        },
        checkAllowedActivities: function () {
            let trails = [];
            let vm = this;
            if (vm.trail_options.length) {
                // Note: Had to add this check to avoid throwing an error due to an empty list
                trails = vm.trail_options[0].children;
            }
            vm.trail_error_list = [];
            let trails_list = [];

            for (var i = 0; i < vm.selected_trails_activities.length; i++) {
                for (var j = 0; j < trails.length; j++) {
                    let allowed = false;
                    if (
                        vm.selected_trails_activities[i].trail == trails[j].id
                    ) {
                        for (
                            var k = 0;
                            k <
                            vm.selected_trails_activities[i].activities.length;
                            k++
                        ) {
                            for (
                                var l = 0;
                                l <
                                vm.selected_trails_activities[i].activities[k]
                                    .activities.length;
                                l++
                            ) {
                                if (
                                    trails[j].allowed_activities_ids.indexOf(
                                        vm.selected_trails_activities[i]
                                            .activities[k].activities[l]
                                    ) != -1
                                ) {
                                    allowed = true;
                                }
                            }
                        }
                        if (!allowed) {
                            trails_list.push(trails[j].name);
                        }
                    }
                }
            }
            if (trails_list.length > 0) {
                let unique_trail_list = [];
                unique_trail_list = [...new Set(trails_list)];
                vm.trail_error_list.push(
                    'Notice: You have not selected any activity that is permitted on the following trail(s): ' +
                        unique_trail_list +
                        '. Click the trail name to view and edit the permitted activities.'
                );
            }
        },

        checkAllowedActivitiesParkOriginal: function () {
            let parks = [];
            let vm = this;
            vm.park_error_list = [];

            var regions = [];
            regions = vm.park_options[0].children;
            for (var x = 0; x < regions.length; x++) {
                var districts = [];
                districts = regions[x].children;
                for (var y = 0; y < districts.length; y++) {
                    parks = districts[y].children;

                    for (var j = 0; j < parks.length; j++) {
                        for (
                            var i = 0;
                            i < vm.selected_parks_activities.length;
                            i++
                        ) {
                            let not_allowed = false;
                            if (
                                vm.selected_parks_activities[i].park ==
                                parks[j].id
                            ) {
                                var not_allowed_activities = [];
                                for (
                                    var k = 0;
                                    k <
                                    vm.selected_parks_activities[i].activities
                                        .length;
                                    k++
                                ) {
                                    if (
                                        parks[j].allowed_activities_ids.indexOf(
                                            vm.selected_parks_activities[i]
                                                .activities[k]
                                        ) == -1
                                    ) {
                                        var activity_name = '';
                                        activity_name =
                                            vm.land_activity_options[0].children.find(
                                                (act) =>
                                                    parseInt(act.id) ===
                                                    parseInt(
                                                        vm
                                                            .selected_parks_activities[
                                                            i
                                                        ].activities[k]
                                                    )
                                            ).name;
                                        if (
                                            not_allowed_activities.indexOf(
                                                activity_name
                                            ) == -1
                                        ) {
                                            not_allowed_activities.push(
                                                activity_name
                                            );
                                        }
                                        not_allowed = true;
                                    }
                                }
                                if (not_allowed) {
                                    vm.park_error_list.push(
                                        'Warning: ' +
                                            not_allowed_activities +
                                            ' activities is/are not allowed for the park: ' +
                                            parks[j].name
                                    );
                                }
                            }
                        }
                    }
                }
            }
        },
        checkAllowedActivitiesPark: function () {
            let parks = [];
            let vm = this;
            vm.park_error_list = [];
            let parks_list = [];

            var regions = [];
            if (vm.park_options.length) {
                // Note: Had to add this check to avoid throwing an error due to an empty list
                regions = vm.park_options[0].children;
            }
            for (var x = 0; x < regions.length; x++) {
                var districts = [];
                districts = regions[x].children;
                for (var y = 0; y < districts.length; y++) {
                    parks = districts[y].children;

                    for (var j = 0; j < parks.length; j++) {
                        for (
                            var i = 0;
                            i < vm.selected_parks_activities.length;
                            i++
                        ) {
                            let allowed = false;
                            if (
                                vm.selected_parks_activities[i].park ==
                                parks[j].id
                            ) {
                                for (
                                    var k = 0;
                                    k <
                                    vm.selected_parks_activities[i].activities
                                        .length;
                                    k++
                                ) {
                                    if (
                                        parks[j].allowed_activities_ids.indexOf(
                                            vm.selected_parks_activities[i]
                                                .activities[k]
                                        ) != -1
                                    ) {
                                        allowed = true;
                                    }
                                }
                                for (
                                    var l = 0;
                                    l <
                                    vm.selected_parks_activities[i].access
                                        .length;
                                    l++
                                ) {
                                    if (
                                        parks[j].allowed_access_ids.indexOf(
                                            vm.selected_parks_activities[i]
                                                .access[l]
                                        ) != -1
                                    ) {
                                        allowed = true;
                                    }
                                }
                                if (!allowed) {
                                    parks_list.push(parks[j].name);
                                }
                            }
                        }
                    }
                }
            }
            if (parks_list.length > 0) {
                let unique_park_list = [];
                unique_park_list = [...new Set(parks_list)];
                vm.park_error_list.push(
                    'Notice: You have not selected any activity or access that is permitted within the following park(s): ' +
                        unique_park_list +
                        '. Click the park name to view and edit the permitted access and activities.'
                );
            }
        },
        edit_activities_child_test: function (node) {
            alert(
                'IN PARENT:  park_id: ' +
                    node.raw.id +
                    ', park_name: ' +
                    node.raw.label
            );
        },
        edit_activities: function (node) {
            let vm = this;
            var p_id = node.raw.id;
            var p_name = node.raw.name;

            for (var j = 0; j < vm.selected_parks_activities.length; j++) {
                if (vm.selected_parks_activities[j].park == p_id) {
                    this.$refs.edit_activities.park_activities =
                        vm.selected_parks_activities[j].activities;
                    this.$refs.edit_activities.park_access =
                        vm.selected_parks_activities[j].access;
                }
            }
            this.$refs.edit_activities.park_id = p_id;
            this.$refs.edit_activities.park_name = p_name;
            this.$refs.edit_activities.fetchAllowedActivities(p_id);
            this.$refs.edit_activities.fetchAllowedAccessTypes(p_id);
            this.$refs.edit_activities.isModalOpen = true;
        },
        edit_sections: function (node) {
            let vm = this;
            var trail = node.raw;

            //inserting a temporary variables checked and new_activities to store and display selected activities for each section.
            for (var l = 0; l < trail.sections.length; l++) {
                trail.sections[l].checked = false;
                trail.sections[l].activities = [];
            }

            for (var i = 0; i < vm.selected_trails_activities.length; i++) {
                if (vm.selected_trails_activities[i].trail == trail.id) {
                    for (
                        var j = 0;
                        j < vm.selected_trails_activities[i].activities.length;
                        j++
                    ) {
                        for (var k = 0; k < trail.sections.length; k++) {
                            if (
                                trail.sections[k].id ==
                                vm.selected_trails_activities[i].activities[j]
                                    .section
                            ) {
                                trail.sections[k].checked = true;
                                trail.sections[k].new_activities =
                                    vm.selected_trails_activities[i].activities[
                                        j
                                    ].activities;
                            }
                        }
                    }
                }
            }

            this.$refs.edit_sections.trail = trail;
            this.$refs.edit_sections.isModalOpen = true;
        },
        refreshSelectionFromResponse: function (
            park_id,
            park_activities,
            park_access
        ) {
            let vm = this;
            for (var j = 0; j < vm.selected_parks_activities.length; j++) {
                if (vm.selected_parks_activities[j].park == park_id) {
                    vm.selected_parks_activities[j].activities =
                        park_activities;
                    vm.selected_parks_activities[j].access = park_access;
                }
            }
            vm.checkRequiredDocuements(vm.selected_parks_activities);
            vm.checkAllowedActivitiesPark();
        },
        refreshTrailFromResponse: function (trail_id, new_activities) {
            let vm = this;
            for (var j = 0; j < vm.selected_trails_activities.length; j++) {
                if (vm.selected_trails_activities[j].trail == trail_id) {
                    vm.selected_trails_activities[j].activities =
                        new_activities;
                }
            }
            vm.checkAllowedActivities();
        },
        find_repeated: function (array) {
            var common = new Map();
            array.forEach(function (obj) {
                var values = Object.values(obj)[0];
                values.forEach(function (val) {
                    common.set(val, (common.get(val) || 0) + 1);
                });
            });
            var result = [];
            common.forEach(function (appearance, el) {
                result.push(el);
            });
            return result;
        },

        find_recurring: function (array) {
            var common = new Map();
            array.forEach(function (obj) {
                var values = Object.values(obj)[0];
                values.forEach(function (val) {
                    common.set(val, (common.get(val) || 0) + 1);
                });
            });
            var result = [];
            common.forEach(function (appearance, el) {
                if (appearance === array.length) {
                    result.push(el);
                }
            });
            return result;
        },

        store_trails: function (trails) {
            let vm = this;
            var all_activities = []; //to store all activities for all sections so can find recurring ones to display selected_activities
            var trail_list = [];
            for (var i = 0; i < trails.length; i++) {
                var current_trail = trails[i].trail.id;
                var current_activities = [];

                for (var j = 0; j < trails[i].sections.length; j++) {
                    var trail_activities = [];
                    for (
                        var k = 0;
                        k < trails[i].sections[j].trail_activities.length;
                        k++
                    ) {
                        trail_activities.push(
                            trails[i].sections[j].trail_activities[k].activity
                        );
                    }
                    var data_section = {
                        section: trails[i].sections[j].section,
                        activities: trail_activities,
                    };
                    current_activities.push(data_section);
                    all_activities.push({ key: trail_activities });
                }

                var data = {
                    trail: current_trail,
                    activities: current_activities,
                };
                vm.selected_trails_activities.push(data);
            }

            for (let i = 0; i < trails.length; i++) {
                trail_list.push({
                    trail: trails[i].trail.id,
                    sections: trails[i].trail.section_ids,
                });
            }
            vm.selected_trails = trail_list;
            vm.trail_activities = vm.find_repeated(all_activities);
        },
        eventListeners: function () {},
    },
};
</script>

<style lang="css" scoped>
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    margin-top: 5px;
}
.just-padding {
    padding: 15px;
}

.list-group {
    padding: 0;
}

.list-group.list-group-root {
    padding: 0;
    overflow: hidden;
}

.list-group.list-group-root .list-group {
    margin-bottom: 0;
}

.list-group.list-group-root .list-group-item {
    border-radius: 0;
    border-width: 1px 0 0 0;
}

.list-group.list-group-root > .list-group-item:first-child {
    border-top-width: 0;
}

.list-group.list-group-root > .list-group > .list-group-item {
    padding-left: 30px;
}

.list-group.list-group-root > .list-group > .list-group > .list-group-item {
    padding-left: 45px;
}

.list-group-item .fas {
    margin-right: 5px;
}
</style>
