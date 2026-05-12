<template lang="html">
    <div id="eventManagementInfo" class="row">
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Event Management"
                    index="event_management"
                    subtitle=""
                >
                    <div v-if="proposal.event_management">
                        <div class="col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Number of participants
                                            expected</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .num_participants
                                            "
                                            type="number"
                                            class="form-control"
                                            name="num_participants"
                                            :disabled="
                                                proposal.readonly ||
                                                proposal.pending_amendment_request ||
                                                proposal.is_amendment_proposal
                                            "
                                            step="1"
                                            onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189"
                                            @paste.prevent
                                        />
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Number of spectators
                                            expected</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .num_spectators
                                            "
                                            type="number"
                                            class="form-control"
                                            name="num_spectators"
                                            :disabled="
                                                proposal.readonly ||
                                                proposal.pending_amendment_request ||
                                                proposal.is_amendment_proposal
                                            "
                                            onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189"
                                            @paste.prevent
                                        />
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Number of officials</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .num_officials
                                            "
                                            type="number"
                                            class="form-control"
                                            name="num_officials"
                                            :disabled="
                                                proposal.readonly ||
                                                proposal.pending_amendment_request ||
                                                proposal.is_amendment_proposal
                                            "
                                            onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189"
                                            @paste.prevent
                                        />
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Number of vehicles/ vessels</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .num_vehicles
                                            "
                                            type="number"
                                            class="form-control"
                                            name="num_vehicles"
                                            :disabled="
                                                proposal.readonly ||
                                                proposal.pending_amendment_request ||
                                                proposal.is_amendment_proposal
                                            "
                                            onkeydown="return event.keyCode !== 69 && event.keyCode !== 187 && event.keyCode !== 189"
                                            @paste.prevent
                                        />
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Will the media be involved?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .media_involved
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="media_involved"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .media_involved
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="media_involved"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management.media_involved
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide details</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .media_details
                                            "
                                            class="form-control"
                                            name="off_road_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Will any structures, facilities,
                                            signs or markers be erected on CALM
                                            land or water for the purpose of the
                                            event?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .structure_change
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="structure_change"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .structure_change
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="structure_change"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management
                                            .structure_change
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide details</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .structure_change_details
                                            "
                                            class="form-control"
                                            name="structure_change_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Will food or other supply vendors
                                            be hired or contracted to operate on
                                            CALM Act land during the
                                            event?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .vendor_hired
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="vendor_hired"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .vendor_hired
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="vendor_hired"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management.vendor_hired
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide details</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .vendor_hired_details
                                            "
                                            class="form-control"
                                            name="vendor_hired_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >List any special equipment,
                                            facilities or materials required to
                                            conduct the proposed activity or
                                            event</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .equipment_details
                                            "
                                            class="form-control"
                                            name="equipment_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Will portable toilets and/ or
                                            showers be provided?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .toilets_provided
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="toilets_provided"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .toilets_provided
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="toilets_provided"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management
                                            .toilets_provided
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide details</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .toilets_provided_details
                                            "
                                            class="form-control"
                                            name="toilets_provided_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Please explain how you will manage
                                            waste to avoid impacts on the park/
                                            reserve and remove waste from the
                                            park/ reserve following the
                                            event</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .rubbish_removal_details
                                            "
                                            class="form-control"
                                            name="rubbish_removal_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Have any other agencies, local
                                            government representatives,
                                            community groups or local committees
                                            been consulted and all necessary
                                            approvals gained regarding this
                                            event?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .approvals_gained
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="approvals_gained"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .approvals_gained
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="approvals_gained"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management
                                            .approvals_gained
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide details</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .approvals_gained_details
                                            "
                                            class="form-control"
                                            name="approvals_gained_details"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Please attach a copy of the below
                                            listed plans for your event
                                        </label>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <ul class="list-block">
                                            <li
                                                class="control-label list-inline-item"
                                            >
                                                Event Management plan
                                            </li>
                                            <li
                                                class="control-label list-inline-item"
                                            >
                                                Emergency response plan
                                            </li>
                                            <li
                                                class="control-label list-inline-item"
                                            >
                                                Risk Management plan
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            ref="event_risk_management_plan"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="event_risk_management_plan"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>

                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Does your event route cross or use
                                            sections of public road on
                                            Conservation and Land Management Act
                                            1984 Land?</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .traffic_management_plan
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="traffic_management_plan"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .event_management
                                                            .traffic_management_plan
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="traffic_management_plan"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.event_management
                                            .traffic_management_plan
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Please attach Traffic Management
                                            Plan that has been prepared and
                                            approved by an accredited body in
                                            line with Mainroads WA -
                                            <a
                                                :href="
                                                    event_traffic_code_of_practice
                                                "
                                                target="_blank"
                                                >Traffic Management for Events
                                                Code of Practice</a
                                            >
                                        </label>
                                    </div>
                                    <div class="col-sm-6">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            ref="event_management_traffic_management_plan"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="event_management_traffic_management_plan"
                                            :readonly="proposal.readonly"
                                        ></FileField>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        !proposal.event_management
                                            .traffic_management_plan
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-12">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Please note it is a requirement to
                                            provide an approved Traffic
                                            Management Plan for any event which
                                            impacts on public roads.</label
                                        >
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Provide any other information that
                                            will be relevant to your
                                            application.</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <textarea
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.event_management
                                                    .other_info
                                            "
                                            class="form-control"
                                            name="other_info"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import FileField from '@/components/forms/filefield.vue';
import { helpers } from '@/utils/hooks.js';
import { v4 as uuid } from 'uuid';

export default {
    components: {
        FormSection,
        FileField,
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
    },
    data: function () {
        return {
            lBody: 'lBody' + uuid(),
            values: null,
            global_settings: [],
        };
    },
    computed: {
        event_traffic_code_of_practice: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (
                        vm.global_settings[i].key ==
                        'event_traffic_code_of_practice'
                    ) {
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        },
    },
    mounted: function () {
        let vm = this;

        vm.fetchGlobalSettings();
        this.$nextTick(() => {});
    },
    methods: {
        fetchGlobalSettings: function () {
            let vm = this;
            helpers.fetchUrl('/api/global_settings.json').then(
                (response) => {
                    vm.global_settings = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
    },
};
</script>

<style lang="css" scoped></style>
