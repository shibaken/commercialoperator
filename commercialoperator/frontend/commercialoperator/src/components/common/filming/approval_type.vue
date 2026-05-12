<template lang="html">
    <div id="approvalType" class="row">
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Approval Type"
                    index="approval_type"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12">
                            <div class="form-group row">
                                <div class="">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                        >
                                            This Application should result in a
                                        </label>
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
                                                        proposal.filming_approval_type
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    value="lawful_authority"
                                                    data-parsley-required
                                                    :disabled="readonly"
                                                    name="filming_approval_type"
                                                />
                                                Lawful Authority
                                            </li>
                                            <li
                                                class="form-check list-inline-item"
                                            >
                                                <input
                                                    ref="Radio"
                                                    v-model="
                                                        // eslint-disable-next-line vue/no-mutating-props
                                                        proposal.filming_approval_type
                                                    "
                                                    class="form-check-input"
                                                    type="radio"
                                                    value="licence"
                                                    data-parsley-required
                                                    :disabled="readonly"
                                                    name="filming_approval_type"
                                                />
                                                Licence
                                            </li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div
                                    v-if="
                                        proposal.filming_approval_type ==
                                        'licence'
                                    "
                                    class=""
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                        >
                                            Filming licence charge type
                                        </label>
                                    </div>
                                    <div
                                        id="filming_licence_charge_parent"
                                        class="col-sm-6"
                                        style="margin-bottom: 5px"
                                    >
                                        <select
                                            id="filming_licence_charge"
                                            ref="filming_licence_charge"
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_licence_charge_type
                                            "
                                            style="width: 100%"
                                            class="form-control input-sm"
                                            :disabled="readonly"
                                        >
                                            <option
                                                v-for="f in filming_licence_charge_choices"
                                                :key="f.key"
                                                :value="f.key"
                                            >
                                                {{ f.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div
                                    v-if="
                                        proposal.filming_licence_charge_type ==
                                        'non_standard_charge'
                                    "
                                    class=""
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                        >
                                            Non standard licence charge
                                        </label>
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                // eslint-disable-next-line vue/no-mutating-props
                                                proposal.filming_non_standard_charge
                                            "
                                            type="number"
                                            :disabled="readonly"
                                            class="form-control"
                                            name="non_standard_charge"
                                            min="0.00"
                                            step="0.01"
                                            placeholder="0.00"
                                            @blur="focusOut"
                                        />
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
import { helpers } from '@/utils/hooks.js';
import { v4 as uuid } from 'uuid';

export default {
    components: { FormSection },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        hasAssessorMode: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            lBody: 'lBody' + uuid(),
            values: null,
            selected_approval_type: '',
            filming_licence_charge_choices: '',
            non_standard_charge: 0.0,
        };
    },
    computed: {
        readonly: function () {
            return !this.hasAssessorMode ? true : false;
        },
    },
    watch: {},
    mounted: function () {
        this.selected_approval_type = this.proposal.filming_approval_type;
        this.fetchLicenceChargeChoices();
        this.$nextTick(() => {
            helpers.initialiseSelect2.bind(this)(
                'filming_licence_charge',
                'filming_licence_charge_parent',
                'proposal.filming_licence_charge_type',
                'Select a filming licence charge type'
            );
        });
    },
    methods: {
        fetchLicenceChargeChoices: function () {
            let vm = this;
            helpers.fetchUrl('/api/filming_licence_charge_choices').then(
                (response) => {
                    vm.filming_licence_charge_choices = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        focusOut: function () {
            let vm = this;
            var total = 0.0;

            total = isNaN(parseFloat(vm.proposal.filming_non_standard_charge))
                ? 0.0
                : parseFloat(vm.proposal.filming_non_standard_charge);
            console.log(total.toFixed(2));

            // eslint-disable-next-line vue/no-mutating-props
            this.proposal.filming_non_standard_charge = total.toFixed(2);
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
