<template lang="html">
    <div id="equipmentInfo" class="row">
        <div class="col-sm-12">
                <FormSection
                    :form-collapse="false"
                    label="Vehicles, Vessels, RPA and other Equipment"
                    index="vehicles_vessels_rpa"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group col-sm-12">
                                <div class="row">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Are your vehicles
                                        </label>
                                    </div>
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    v-if="
                                                        proposal.filming_equipment
                                                    "
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .filming_equipment
                                                            .vehicle_owned
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="vehicle_owned"
                                                />
                                                Owned
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    v-if="
                                                        proposal.filming_equipment
                                                    "
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .filming_equipment
                                                            .vehicle_owned
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="vehicle_owned"
                                                />
                                                Hired
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div
                                    v-if="
                                        proposal.filming_equipment &&
                                        proposal.filming_equipment.vehicle_owned
                                    "
                                    class=""
                                >
                                    <VehicleTable
                                        ref="vehicles_table"
                                        :url="vehicles_url"
                                        :proposal="proposal"
                                        :access_types="access_types"
                                    ></VehicleTable>
                                </div>
                            </div>
                        </div>
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <VesselTable
                                ref="vessel_table"
                                :url="vessels_url"
                                :proposal="proposal"
                            ></VesselTable>
                        </div>

                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                        >Are you using a Remotely Piloted
                                        Aircraft (RPA) for your filming and/or
                                        photography activities?</label
                                    >
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <ul class="list-inline">
                                        <li class="form-check list-inline-item">
                                            <input
                                                v-if="
                                                    proposal.filming_equipment
                                                "
                                                ref="Radio"
                                                v-model="
                                                    // eslint-disable-next-line vue/no-mutating-props
                                                    proposal.filming_equipment
                                                        .rps_used
                                                "
                                                class="form-check-input"
                                                type="radio"
                                                :value="true"
                                                data-parsley-required
                                                :disabled="proposal.readonly"
                                                name="rps_used"
                                            />
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input
                                                v-if="
                                                    proposal.filming_equipment
                                                "
                                                ref="Radio"
                                                v-model="
                                                    // eslint-disable-next-line vue/no-mutating-props
                                                    proposal.filming_equipment
                                                        .rps_used
                                                "
                                                class="form-check-input"
                                                type="radio"
                                                :value="false"
                                                data-parsley-required
                                                :disabled="proposal.readonly"
                                                name="rps_used"
                                            />
                                            No
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div
                                v-if="
                                    proposal.filming_equipment &&
                                    proposal.filming_equipment.rps_used
                                "
                                class="row"
                            >
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                    >
                                        Please specify the model of RPA you
                                        intend to use and attach a copy of your
                                        CASA remotely piloted aircraft operator
                                        accreditation or licence (RePL) and
                                        operator's certificate (ReOC)
                                    </label>
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_equipment"
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_equipment
                                                    .rps_used_details
                                            "
                                            :disabled="proposal.readonly"
                                            class="form-control"
                                            name="camp_location"
                                            placeholder=""
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div
                                v-if="
                                    proposal.filming_equipment &&
                                    proposal.filming_equipment.rps_used
                                "
                                class="row"
                            >
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                    >
                                        Attach document</label
                                    >
                                </div>
                                <div class="col-sm-6">
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            ref="rps_certificate"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="rps_certificate"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div>

                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                        >Number and type of cameras to be used
                                    </label>
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_equipment"
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_equipment
                                                    .num_cameras
                                            "
                                            type="text"
                                            class="form-control"
                                            name="num_cameras"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                        >Will any stuctures or facilities be
                                        erected or does the area require any
                                        alteration to occur to allow the
                                        filming?</label
                                    >
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <div class="col-sm-6">
                                        <ul class="list-inline">
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    v-if="
                                                        proposal.filming_equipment
                                                    "
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .filming_equipment
                                                            .alteration_required
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="true"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="alteration_required"
                                                />
                                                Yes
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    v-if="
                                                        proposal.filming_equipment
                                                    "
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal
                                                            .filming_equipment
                                                            .alteration_required
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    :value="false"
                                                    data-parsley-required
                                                    :disabled="
                                                        proposal.readonly
                                                    "
                                                    name="alteration_required"
                                                />
                                                No
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div
                                v-if="
                                    proposal.filming_equipment &&
                                    proposal.filming_equipment
                                        .alteration_required
                                "
                                class="row"
                            >
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                    >
                                        Please provide details and/or attach a
                                        copy of the plans or specifications
                                    </label>
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_equipment"
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_equipment
                                                    .alteration_required_details
                                            "
                                            :disabled="proposal.readonly"
                                            class="form-control"
                                            name="camp_location"
                                            placeholder=""
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                            <div
                                v-if="
                                    proposal.filming_equipment &&
                                    proposal.filming_equipment
                                        .alteration_required
                                "
                                class="row"
                            >
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                    >
                                        Attach document</label
                                    >
                                </div>
                                <div class="col-sm-6">
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="alteration_required"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>
                            </div>

                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-right"
                                        for="Name"
                                        >List any other significant equipment
                                        that may be used during the proposed
                                        operations</label
                                    >
                                </div>
                                <div
                                    class="col-sm-6"
                                    style="margin-bottom: 5px"
                                >
                                    <div
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="proposal.filming_equipment"
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_equipment
                                                    .other_equipments
                                            "
                                            type="text"
                                            class="form-control"
                                            name="num_cameras"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </FormSection>
        </div>
    </div>
</template>

<script>
import { helpers, api_endpoints } from '@/utils/hooks.js';
import FormSection from '@/components/forms/section_toggle.vue';
import VehicleTable from '@/components/common/vehicle_table.vue';
import VesselTable from '@/components/common/vessel_table.vue';
import FileField from '@/components/forms/filefield.vue';
import { v4 as uuid } from 'uuid';

export default {
    name: 'FilmingEquipment',
    components: {
        FormSection,
        VehicleTable,
        VesselTable,
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
        let vm = this;
        return {
            lBody: 'lBody' + uuid(),
            values: null,
            access_types: [],
            vehicles_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/vehicles'
            ),
            vessels_url: helpers.add_endpoint_json(
                api_endpoints.proposals,
                vm.$route.params.proposal_id + '/vessels'
            ),
        };
    },
    mounted: function () {
        let vm = this;
        vm.fetchAccessTypes();
    },
    methods: {
        fetchAccessTypes: function () {
            let vm = this;
            helpers.fetchUrl(api_endpoints.access_types).then(
                (response) => {
                    vm.access_types = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
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
</style>
