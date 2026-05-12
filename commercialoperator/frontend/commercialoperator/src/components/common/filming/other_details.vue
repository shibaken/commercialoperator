<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div id="otherInfo" class="row">
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Safety"
                    index="safety"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row" style="margin-bottom: 5px">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >What steps have been taken to
                                            ensure the safety of your filming
                                            party?
                                            <small>
                                                (Provide details of your safety
                                                and communication equipment
                                                and/or attach a copy of your
                                                safety and risk management
                                                plan)</small
                                            >
                                        </label>
                                    </div>
                                    <div class="col-sm-6">
                                        <div
                                            ref="safety_details"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <textarea
                                                v-if="
                                                    proposal.filming_other_details
                                                "
                                                v-model="
                                                    proposal
                                                        .filming_other_details
                                                        .safety_details
                                                "
                                                type="text"
                                                class="form-control"
                                                name="safety_details"
                                                :disabled="
                                                    proposal.readonly ||
                                                    proposal.pending_amendment_request ||
                                                    proposal.is_amendment_proposal
                                                "
                                            ></textarea>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="filming_safety_details"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Other"
                    index="other"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            >Provide any additional information
                                            to support your application. If you
                                            would like to access a park that is
                                            not listed in the previous sections,
                                            please include here.</label
                                        >
                                    </div>
                                </div>
                                <div class="row">
                                    <div
                                        class="col-sm-12"
                                        style="margin-bottom: 5px"
                                    >
                                        <textarea
                                            v-if="
                                                proposal.filming_other_details
                                            "
                                            v-model="
                                                proposal.filming_other_details
                                                    .other_comments
                                            "
                                            class="form-control"
                                            :disabled="proposal.readonly"
                                        ></textarea>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="true"
                                            name="filming_other_details"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>

        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Payment of Fees and Charges"
                    index="payment_of_fees_and_charges"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            >Depending on the filming operation,
                                            fees and charges may apply. Please
                                            see commercial filming
                                            <a
                                                :href="fees_and_charges"
                                                target="_blank"
                                                >website</a
                                            >
                                            for information on fees and
                                            charges.</label
                                        >
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div
                                    v-if="
                                        proposal.filming_other_details &&
                                        proposal.filming_other_details
                                            .camping_fee_waived
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >For how many people
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
                                            <input
                                                v-if="
                                                    proposal.filming_other_details
                                                "
                                                v-model="
                                                    proposal
                                                        .filming_other_details
                                                        .fee_waived_num_people
                                                "
                                                type="text"
                                                class="form-control"
                                                name="num_cameras"
                                                placeholder=""
                                                :disabled="proposal.readonly"
                                            />
                                        </div>
                                    </div>
                                </div>
                                <div
                                    v-if="
                                        proposal.filming_other_details &&
                                        proposal.filming_other_details
                                            .camping_fee_waived
                                    "
                                    class="row"
                                >
                                    <div class="col-sm-12">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Make sure that you have a copy of
                                            the licence or lawful authority if
                                            issued. Camping gess may still
                                            apply.</label
                                        >
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Insurance"
                    index="insurance"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label>
                                            <ol type="a">
                                                <li>
                                                    Attach your policy for
                                                    public liability insurance
                                                    that covers the areas and
                                                    operations allowed under the
                                                    filming authority, and in
                                                    the name of the applicant to
                                                    the extent of its rights and
                                                    interests, for a sum of not
                                                    less than AU$10 million per
                                                    event.
                                                </li>
                                                <li>
                                                    It is a requirement of all
                                                    filming authority holders to
                                                    maintain appropriate public
                                                    liability insurance.
                                                </li>
                                            </ol></label
                                        >
                                    </div>
                                </div>

                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Certificate of currency
                                        </label>
                                    </div>
                                    <div class="col-sm-3">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            ref="currency_doc"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="false"
                                            name="currency_certificate"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Expiry Date
                                        </label>
                                    </div>
                                    <div class="col-sm-3">
                                        <div
                                            ref="insurance_expiry"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-if="
                                                    proposal.filming_other_details
                                                "
                                                v-model="
                                                    proposal
                                                        .filming_other_details
                                                        .insurance_expiry
                                                "
                                                type="date"
                                                class="form-control"
                                                name="insurance_expiry"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                                :disabled="proposal.readonly"
                                            />
                                            <span class="input-group-text">
                                                <i class="fas fa-calendar-days"></i>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </FormSection>
            </div>
        </div>
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Deed Poll"
                    index="deed_poll"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            >It is a requirement of all filming
                                            authority holders to sign a deed
                                            poll to release and indemnify the
                                            State of Western Australia. Please
                                            note: electronic or digital
                                            signatures cannot be
                                            accepted.</label
                                        >
                                        <label v-if="deed_poll_url"
                                            >Please click
                                            <a
                                                :href="deed_poll_url"
                                                target="_blank"
                                                >here</a
                                            >
                                            to download the deed poll. The deed
                                            poll must be signed and have a
                                            witness signature and be dated. Once
                                            signed and dated, please scan and
                                            attach the deed poll below.</label
                                        >
                                        <label v-else
                                            >Please click here to download the
                                            deed poll. The deed poll must be
                                            signed and have a witness signature
                                            and be dated. Once signed and dated,
                                            please scan and attach the deed poll
                                            below.</label
                                        >
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <FileField
                                            :id="'proposal' + proposal.id"
                                            ref="deed_poll_doc"
                                            :proposal_id="proposal.id"
                                            :is-repeatable="false"
                                            name="deed_poll"
                                            :readonly="!canEditActivities"
                                        ></FileField>
                                    </div>
                                </div>
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
            pBody: 'pBody' + uuid(),
            lBody: 'lBody' + uuid(),
            iBody: 'iBody' + uuid(),
            mBody: 'mBody' + uuid(),
            oBody: 'oBody' + uuid(),
            cBody: 'cBody' + uuid(),
            dBody: 'dBody' + uuid(),
            values: null,
            global_settings: [],
        };
    },
    computed: {
        deed_poll_url: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (vm.global_settings[i].key == 'deed_poll_filming') {
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        },
        credit_facility_link: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (vm.global_settings[i].key == 'credit_facility_link') {
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        },
        fees_and_charges: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (vm.global_settings[i].key == 'fees_and_charges') {
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        },
    },
    watch: {},
    mounted: function () {
        let vm = this;
        vm.fetchGlobalSettings();
        this.$nextTick(() => {
            helpers.addDateFieldMinValues(vm, null, 'insurance_expiry');
        });
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

<style lang="css" scoped>
fieldset.scheduler-border {
    border: 1px groove #ddd !important;
    padding: 0 1.4em 1.4em 1.4em !important;
    margin: 0 0 1.5em 0 !important;
    -webkit-box-shadow: 0px 0px 0px 0px #000;
    box-shadow: 0px 0px 0px 0px #000;
}
legend.scheduler-border {
    width: inherit; /* Or auto */
    padding: 0 10px; /* To give a bit of padding on the left and right */
    border-bottom: none;
}
</style>
