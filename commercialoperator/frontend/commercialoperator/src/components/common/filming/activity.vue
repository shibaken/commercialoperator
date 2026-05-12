<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div id="activityInfo" class="row">
        <div class="col-sm-12">
                <FormSection
                    :form-collapse="false"
                    label="Filming Details"
                    index="filming_details"
                    subtitle=""
                >
                    <div class="">
                        <div
                            class="form-horizontal col-sm-12 borderDecoration"
                            style="z-index: 0"
                        >
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="filming_activity_commencement_date"
                                            >Period of proposed filming/
                                            photography</label
                                        >
                                    </div>
                                    <div class="col-sm-3">
                                        <div
                                            ref="commencement_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-if="proposal.filming_activity"
                                                id="filming_activity_commencement_date"
                                                v-model="
                                                    proposal.filming_activity
                                                        .commencement_date
                                                "
                                                class="form-control"
                                                type="date"
                                                max="2999-12-31"
                                                name="commencement_date"
                                                placeholder="Commencement date"
                                                required
                                                :disabled="
                                                    !canEditPeriod ||
                                                    proposal.pending_amendment_request ||
                                                    proposal.is_amendment_proposal
                                                "
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                        <label
                                            class="control-label small-label"
                                            for="commencement_date"
                                            >Commencement date</label
                                        >
                                    </div>
                                    <div class="col-sm-3">
                                        <!-- <div class="col-sm-3"> -->
                                        <!-- </div> -->
                                        <div
                                            ref="completion_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-if="proposal.filming_activity"
                                                v-model="
                                                    proposal.filming_activity
                                                        .completion_date
                                                "
                                                type="date"
                                                max="2999-12-31"
                                                class="form-control"
                                                name="completion_date"
                                                placeholder="Completion date"
                                                required
                                                :disabled="
                                                    !canEditPeriod ||
                                                    proposal.pending_amendment_request ||
                                                    proposal.is_amendment_proposal
                                                "
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                        <label
                                            class="control-label small-label"
                                            for="completion_date"
                                            >Completion date
                                        </label>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="filming_activity_title"
                                            >Title of film/ name of program/
                                            name of product</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <input
                                            v-if="proposal.filming_activity"
                                            id="filming_activity_title"
                                            v-model="
                                                proposal.filming_activity
                                                    .activity_title
                                            "
                                            type="text"
                                            class="form-control"
                                            name="Activity title"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        />
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="filming_activity_previous_contact_person"
                                            >Previous contact person in the
                                            Department</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <input
                                            v-if="proposal.filming_activity"
                                            id="filming_activity_previous_contact_person"
                                            v-model="
                                                proposal.filming_activity
                                                    .previous_contact_person
                                            "
                                            type="text"
                                            class="form-control"
                                            name="Previous contact Person"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        />
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="filming_activity_sponsorship_choices"
                                            >Does the film have Tourism WA
                                            sponsorship</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <ul
                                            id="filming_activity_sponsorship_choices"
                                            class="list-inline"
                                        >
                                            <li
                                                v-for="s in sponsorship_choices"
                                                :key="s.key"
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    v-if="
                                                        proposal.filming_activity
                                                    "
                                                    ref="Radio"
                                                    v-model="
                                                        proposal
                                                            .filming_activity
                                                            .sponsorship
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="s.key"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="sponsorship"
                                                    @click="
                                                        selectFilmType(
                                                            $event,
                                                            s
                                                        )
                                                    "
                                                />
                                                {{ s.value }}
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.filming_activity &&
                                        proposal.filming_activity.sponsorship ==
                                            'other'
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="filming_activity_sponsorship_choices"
                                            >Details</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_activity"
                                            id="filming_activity_sponsorship_details"
                                            v-model="
                                                proposal.filming_activity
                                                    .sponsorship_details
                                            "
                                            class="form-control"
                                            :disabled="proposal.readonly"
                                            style="width: 80%"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="filming_activity_production_description"
                                            >Description of production</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_activity"
                                            id="filming_activity_production_description"
                                            v-model="
                                                proposal.filming_activity
                                                    .production_description
                                            "
                                            class="form-control"
                                            :disabled="proposal.readonly"
                                            style="width: 80%"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="film_type_select"
                                            >Type of film to be
                                            undertaken</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <select
                                            v-if="proposal.filming_activity"
                                            id="film_type_select"
                                            ref="film_type_select"
                                            v-model="
                                                proposal.filming_activity
                                                    .film_type
                                            "
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            multiple
                                            :disabled="!canEditPeriod"
                                        >
                                            <option
                                                v-for="f in film_type_choices"
                                                :key="f.key"
                                                :value="f.key"
                                            >
                                                {{ f.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="filmPurposeSelect"
                                            >Purpose of still or motion
                                            film</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <select
                                            v-if="proposal.filming_activity"
                                            id="filmPurposeSelect"
                                            ref="filmPurposeSelect"
                                            v-model="
                                                proposal.filming_activity
                                                    .film_purpose
                                            "
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            multiple
                                            :disabled="proposal.readonly"
                                        >
                                            <option
                                                v-for="p in purpose_choices"
                                                :key="p.key"
                                                :value="p.key"
                                            >
                                                {{ p.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div v-if="showPurposeOtherDetails" class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="filming_activity_film_purpose_details"
                                            >Please provide details</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            id="filming_activity_film_purpose_details"
                                            v-model="
                                                proposal.filming_activity
                                                    .film_purpose_details
                                            "
                                            class="form-control"
                                            :disabled="proposal.readonly"
                                            style="width: 80%"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="filmUsageSelect"
                                            >How will the still or motion film
                                            be used or shown</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <select
                                            v-if="proposal.filming_activity"
                                            id="filmUsageSelect"
                                            ref="filmUsageSelect"
                                            v-model="
                                                proposal.filming_activity
                                                    .film_usage
                                            "
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            multiple
                                            :disabled="proposal.readonly"
                                        >
                                            <option
                                                v-for="u in film_usage_choices"
                                                :key="u.key"
                                                :value="u.key"
                                            >
                                                {{ u.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div v-if="showUsageDetails" class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-right"
                                            for="filming_activity_film_usage_details"
                                            >Please specify
                                        </label>
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            id="filming_activity_film_usage_details"
                                            v-model="
                                                proposal.filming_activity
                                                    .film_usage_details
                                            "
                                            class="form-control"
                                            :disabled="proposal.readonly"
                                            style="width: 80%"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">&nbsp;</div>
                            </div>
                        </div>
                    </div>
                </FormSection>
        </div>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import { helpers } from '@/utils/hooks.js';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'FilmingActivity',
    components: {
        FormSection,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        hasDistrictAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        district_proposal: {
            type: Object,
            default: null,
        },
        canEditActivities: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_external: {
            type: Boolean,
            default: false,
        },
        canEditPeriod: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            lBody: 'lBody' + uuid(),
            values: null,
            film_type_choices: [],
            sponsorship_choices: [],
            film_usage_choices: [],
            purpose_choices: [],
            selected_film_type: [],
            selected_film_purpose: [],
            selected_film_usage: [],
        };
    },
    computed: {
        showUsageDetails: function () {
            let vm = this;
            if (
                vm.proposal &&
                vm.proposal.filming_activity &&
                vm.proposal.filming_activity.film_usage
            ) {
                if (vm.proposal.filming_activity.film_usage.length > 0) {
                    return true;
                }
            }
            return false;
        },
        showPurposeOtherDetails: function () {
            let vm = this;
            if (
                vm.proposal &&
                vm.proposal.filming_activity &&
                vm.proposal.filming_activity.film_purpose
            ) {
                for (
                    var i =
                        vm.proposal.filming_activity.film_purpose.length - 1;
                    i >= 0;
                    i--
                ) {
                    if (
                        vm.proposal.filming_activity.film_purpose[i] == 'other'
                    ) {
                        return true;
                    }
                }
            }
            return false;
        },
        canEditFilmType: function () {
            let vm = this;
            var status_list = [
                'Approved',
                'Awaiting Payment',
                'Declined',
                'Discarded',
            ];
            if (status_list.indexOf(vm.proposal.processing_status) > -1) {
                return false;
            }
            return true;
        },
    },
    mounted: function () {
        let vm = this;
        this.fetchActivityTabData();
        this.$nextTick(() => {
            vm.eventListeners();
            helpers.addDateFieldMinValues(
                vm,
                null,
                'commencement_date',
                'completion_date'
            );
        });
    },
    methods: {
        fetchActivityTabData: function () {
            let vm = this;
            helpers.fetchUrl('/api/filming_activity_tab').then(
                (response) => {
                    vm.film_type_choices = response.film_type_choices;
                    vm.sponsorship_choices = response.sponsorship_choices;
                    vm.film_usage_choices = response.film_usage_choices;
                    vm.purpose_choices = response.purpose_choices;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        selectFilmType: function () {},
        eventListeners: function () {
            let vm = this;

            // Initialise select2 for Film Type
            $(vm.$refs.film_type_select)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Film Type',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_type = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_type = selected.val();
                });
            // Initialise select2 for Film Purpose
            $(vm.$refs.filmPurposeSelect)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Film Purpose',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_purpose = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_purpose = selected.val();
                });
            // Initialise select2 for Film Usage
            $(vm.$refs.filmUsageSelect)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select Film Usage',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_usage = selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.filming_activity.film_usage = selected.val();
                });
        },
    },
};
</script>

<style lang="css" scoped>
.small-label {
    font-size: 12px;
    color: #555;
    margin-bottom: 4px;
}
</style>
