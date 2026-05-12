<template lang="html">
    <div id="vehiclesVesselsInfo" class="row">
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Vehicles/Vessels"
                    index="vehicles_vessels"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="">
                                <div class="row">&nbsp;</div>
                                <div class="">
                                    <label class=""
                                        >Provide details of every vehicle you
                                        plan to use when accessing the parks.
                                        'Hire vehicle' can be entered as the
                                        vehicle registration if the hire vehicle
                                        details are not yet known.</label
                                    >
                                    <VehicleTable
                                        ref="vehicles_table"
                                        :url="vehicles_url"
                                        :proposal="proposal"
                                        :access_types="access_types"
                                    ></VehicleTable>
                                </div>
                                <div class="row">&nbsp;</div>
                            </div>
                        </div>

                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <label class="control-label"
                                >Provide details of every vessel you plan to use
                                when accessing the parks for the event</label
                            >
                            <VesselTable
                                ref="vessel_table"
                                :url="vessels_url"
                                :proposal="proposal"
                            ></VesselTable>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
    </div>
</template>

<script>
import { helpers, api_endpoints } from '@/utils/hooks.js';
import FormSection from '@/components/forms/section_toggle.vue';
import VehicleTable from '@/components/common/vehicle_table.vue';
import VesselTable from '@/components/common/vessel_table.vue';
import { v4 as uuid } from 'uuid';

export default {
    components: {
        FormSection,
        VehicleTable,
        VesselTable,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
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
                    vm.access_types = response.results;
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
