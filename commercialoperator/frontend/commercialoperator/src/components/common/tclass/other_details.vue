<!-- eslint-disable vue/no-mutating-props -->
<template lang="html">
    <div id="userInfo" class="row">
        <div class="col-sm-12">
            <div class="card">
                <FormSection
                    :form-collapse="false"
                    label="Tourism Accreditation"
                    index="tourism_accreditation"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <label class="control-label"
                                >Select which tourism accreditation you
                                have achieved and attach a copy of your certificate.
                                <a
                                    href="https://parks.dpaw.wa.gov.au/for-business/training-accreditation-insurance-fees"
                                    target="_blank"
                                    ><i
                                        class="fa fa-question-circle"
                                        style="color: blue"
                                        >&nbsp;</i
                                    ></a
                                ></label
                            >
                            <ul class="list-inline">
                                <li
                                    v-for="c in accreditation_choices"
                                    :key="c.key"
                                    class="form-check list-inline-item"
                                >
                                    <input
                                        ref="Checkbox"
                                        class="form-check-input"
                                        type="checkbox"
                                        :value="c.key"
                                        data-parsley-required
                                        :disabled="proposal.readonly"
                                        @click="selectAccreditation($event, c)"
                                        :checked="selected_accreditations.includes(c.key)"
                                    />
                                    {{ c.value }}
                                </li>
                            </ul>
                            <div
                                v-for="accreditation in proposal.other_details
                                    .accreditations"
                                :key="accreditation.id"
                            >
                                <div
                                    v-if="
                                        !accreditation.is_deleted &&
                                        accreditation.accreditation_type != 'no' &&
                                        accreditation.accreditation_type != 'narta'
                                    "
                                    class="col-sm-12"
                                >
                                    <Accreditation
                                        id="accreditation"
                                        :ref="accreditation.accreditation_type"
                                        :accreditation="accreditation"
                                        :proposal_id="proposal.id"
                                        :readonly="proposal.readonly"
                                        :can-edit-activities="canEditActivities"
                                    ></Accreditation>
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
                label="Tourism accessibility and emissions reduction standards"
                index="tourism_accessibility_emission_standards"
                subtitle=""
            >
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        <label class="">Select which provider you have used to complete your assessments and provide a link to your publicly available information. Click  <a :href="tourism_standards_link" target="_blank"><i class="fa fa-question-circle" style="color:blue">&nbsp;</i></a> for more information.</label>
                        <label class="">Accessible Tourism Information Standard</label>
                        <ul class="list-inline"  >
                            <li 
                                v-for="c in information_standard_choices" 
                                class="form-check list-inline-item"
                                :key="c.key"
                            >
                                <input  
                                    class="form-check-input" 
                                    ref="Checkbox" 
                                    type="checkbox" 
                                    @click="selectInformationStandard($event, c)" 
                                    :checked="selected_information_standards.includes(c.key)" 
                                    :value="c.key" 
                                    data-parsley-required 
                                    :disabled="proposal.readonly" 
                                />
                                        {{ c.value }}
                            </li>
                        </ul>
                        <div v-for=" information_standard in proposal.other_details.information_standards">
                            <div v-if="!information_standard.is_deleted" class="col-sm-12">
                                <InformationStandard :information_standard="information_standard":proposal_id="proposal.id" :readonly="proposal.readonly" id="information_standard" :ref="information_standard.accreditation_type" :canEditActivities="canEditActivities"></InformationStandard >
                            </div>
                        </div>
                        <label class="control-label">Tourism Emissions Reduction Standard</label>
                        <ul class="list-inline"  >
                            <li 
                                v-for="c in emission_standard_choices" 
                                class="form-check list-inline-item"
                                :key="c.key"
                            >
                                <input  class="form-check-input" ref="Checkbox" type="checkbox" @click="selectEmissionStandard($event, c)" :checked="selected_emission_standards.includes(c.key)" :value="c.key" data-parsley-required :disabled="proposal.readonly" />
                                        {{ c.value }}
                            </li>
                        </ul>
                        <div v-for=" emission_standard in proposal.other_details.emission_standards">
                            <div v-if="!emission_standard.is_deleted " class="col-sm-12">
                                <EmissionStandard :emission_standard="emission_standard":proposal_id="proposal.id" :readonly="proposal.readonly" id="emission_standard" :ref="emission_standard.accreditation_type" :canEditActivities="canEditActivities"></EmissionStandard >
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
                    label="Licence Term"
                    index="licence_term"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Preferred licence term</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="
                                            margin-bottom: 5px;
                                            width: 53% !important;
                                        "
                                    >
                                        <select
                                            ref="preferred_licence_period"
                                            v-model="
                                                proposal.other_details
                                                    .preferred_licence_period
                                            "
                                            class="form-control"
                                            :disabled="
                                                proposal.readonly ||
                                                proposal.pending_amendment_request ||
                                                proposal.is_amendment_proposal
                                            "
                                        >
                                            <option
                                                v-for="l in licence_period_choices"
                                                :key="l.key"
                                                :value="l.key"
                                            >
                                                {{ l.value }}
                                            </option>
                                        </select>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Nominated start date</label
                                        >
                                    </div>
                                    <div class="col-sm-9">
                                        <div
                                            ref="nominated_start_date"
                                            class="input-group date"
                                            style="width: 70%"
                                        >
                                            <input
                                                v-model="
                                                    proposal.other_details
                                                        .nominated_start_date
                                                "
                                                type="date"
                                                class="form-control"
                                                name="nominated_start_date"
                                                max="2999-12-31"
                                                placeholder="DD/MM/YYYY"
                                                required
                                                :disabled="
                                                    proposal.readonly ||
                                                    proposal.pending_amendment_request ||
                                                    proposal.is_amendment_proposal
                                                "
                                            />
                                            <span class="input-group-addon">
                                                <span
                                                    class="glyphicon glyphicon-calendar"
                                                ></span>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">&nbsp;</div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        Application and licence fee information
                                        <a
                                            href="https://parks.dpaw.wa.gov.au/for-business/training-accreditation-insurance-fees"
                                            target="_blank"
                                            ><i
                                                class="fa fa-question-circle"
                                                style="color: blue"
                                                >&nbsp;</i
                                            ></a
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
                    label="Moorings"
                    index="moorings"
                    subtitle="(marine-based activities)"
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            >Provide the mooring number or GPS
                                            coordinates for any mooring within a
                                            marine reserve your operation will
                                            use.</label
                                        >
                                    </div>
                                </div>
                                <div
                                    v-for="(m, index) in proposal.other_details
                                        .mooring"
                                    :key="index"
                                    class="row"
                                >
                                    <div class="col-sm-3">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Mooring number or GPS
                                            coordinates</label
                                        >
                                    </div>
                                    <div
                                        class="col-sm-9"
                                        style="margin-bottom: 5px"
                                    >
                                        <input
                                            v-model="
                                                proposal.other_details.mooring[
                                                    index
                                                ]
                                            "
                                            type="text"
                                            class="form-control"
                                            name="Mooring number"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        />
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <span
                                            ><a
                                                v-if="!proposal.readonly"
                                                target="_blank"
                                                class="control-label pull-left"
                                                style="cursor: pointer"
                                                @click="addMooring()"
                                                >Add another mooring</a
                                            ></span
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
                                                    licence, and in the name of
                                                    the applicant to the extent
                                                    of its rights and interests,
                                                    for a sum of not less than
                                                    AU$10 million per event.
                                                </li>
                                                <li>
                                                    It is a requirement of all
                                                    licenced operators to
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
                                                v-model="
                                                    proposal.other_details
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
                                            <span class="input-group-addon">
                                                <span
                                                    class="glyphicon glyphicon-calendar"
                                                ></span>
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
                                            >Provide information to support your
                                            application. This may include
                                            brochures, itineraries or other
                                            advertising material.</label
                                        >
                                        <label
                                            >If you would like to apply for a
                                            park or activity that is not listed
                                            in the previous sections, please
                                            include details.</label
                                        >
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-12">
                                        <textarea
                                            v-model="
                                                proposal.other_details
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
                                            name="other_details"
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
                    label="Park Entry and Camping Fees"
                    index="park_entry_fees"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-left"
                                        for="Name"
                                        >Do you require credit facilities for
                                        payment of fees</label
                                    >
                                </div>
                                <div class="col-sm-3">
                                    <label>
                                        <input
                                            ref="credit_fees_yes"
                                            v-model="
                                                proposal.other_details
                                                    .credit_fees
                                            "
                                            type="radio"
                                            value="true"
                                            :disabled="proposal.readonly"
                                            @change="handleSelectionChange"
                                        />Yes
                                    </label>
                                </div>
                                <div class="col-sm-3">
                                    <label>
                                        <input
                                            v-model="
                                                proposal.other_details
                                                    .credit_fees
                                            "
                                            type="radio"
                                            value="false"
                                            :disabled="proposal.readonly"
                                            @change="handleSelectionChange"
                                        />No
                                    </label>
                                </div>
                                <div id="show_credit_link" class="hidden">
                                    <div class="col-sm-6"></div>
                                    <div class="col-sm-6">
                                        <label class=""
                                            ><a
                                                :href="credit_facility_link"
                                                target="_blank"
                                                >Link</a
                                            ></label
                                        >
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-6">
                                    <label
                                        class="control-label pull-left"
                                        for="Name"
                                        >Do you require Cash / Credit Payment
                                        Docket books?</label
                                    >
                                </div>
                                <div class="col-sm-3">
                                    <label>
                                        <input
                                            ref="docket_books_yes"
                                            v-model="
                                                proposal.other_details
                                                    .credit_docket_books
                                            "
                                            type="radio"
                                            value="true"
                                            :disabled="proposal.readonly"
                                            @change="handleRadioChange"
                                        />Yes
                                    </label>
                                </div>
                                <div class="col-sm-3">
                                    <label>
                                        <input
                                            v-model="
                                                proposal.other_details
                                                    .credit_docket_books
                                            "
                                            type="radio"
                                            value="false"
                                            :disabled="proposal.readonly"
                                            @change="handleRadioChange"
                                        />No
                                    </label>
                                </div>
                            </div>
                            <div>
                                <div id="show_docket" class="hidden">
                                    <div class="col-sm-6">
                                        <label
                                            class="control-label pull-left"
                                            for="Name"
                                            >Number of docket books</label
                                        >
                                    </div>
                                    <div class="col-sm-6">
                                        <input
                                            v-model="
                                                proposal.other_details
                                                    .docket_books_number
                                            "
                                            type="text"
                                            class="form-control"
                                            name="docket_books_number"
                                            placeholder=""
                                            :disabled="proposal.readonly"
                                        />
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <label
                                        >Did you know you can use this system to
                                        pay park entry fees? Click on the Park
                                        Entry Fees page above.</label
                                    >
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
                    index="dee_poll"
                    subtitle=""
                >
                    <div class="">
                        <div class="form-horizontal col-sm-12 borderDecoration">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-12">
                                        <label
                                            >It is a requirement of all
                                            commercial operations licence
                                            holders to sign a deed poll to
                                            release and indemnify the State of
                                            Western Australia. Please note:
                                            electronic or digital signatures
                                            cannot be accepted.</label
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
import Accreditation from './accreditation_type.vue';
import InformationStandard from './information_standard.vue'
import EmissionStandard from './emission_standard.vue'
import FileField from '@/components/forms/filefield.vue';
import { helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    components: {
        FormSection,
        FileField,
        Accreditation,
        InformationStandard,
        EmissionStandard,
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
            accreditation_choices: [],
            accreditation_type: [],
            selected_accreditations: [],
            information_standard_choices:[],
            selected_information_standards:[],
            emission_standard_choices:[],
            selected_emission_standards:[],
            licence_period_choices: [],
            mooring: [''],
            global_settings: [],
        };
    },
    computed: {
        deed_poll_url: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (vm.global_settings[i].key == 'deed_poll') {
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
        tourism_standards_link: function(){
            let vm=this;
            if(vm.global_settings){
                for(var i=0; i<vm.global_settings.length; i++){
                    if(vm.global_settings[i].key=='tourism_standards_link'){
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        }
    },
    watch: {
        accreditation_type: {
            handler: function () {
                // eslint-disable-next-line vue/no-mutating-props
                this.proposal.other_details.accreditation_type =
                    this.accreditation_type.key;
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        vm.fetchAccreditationChoices();
        vm.fetchTourismStandards();
        vm.fetchLicencePeriodChoices();
        vm.fetchGlobalSettings();
        vm.checkProposalAccreditation();
        vm.checkProposalInformationStandard();
        vm.checkProposalEmissionStandard();
        vm.showDockteNumber();
        vm.showCreditFacilityLink();
        this.$nextTick(() => {
            vm.eventListeners();
            helpers.addDateFieldMinValues(
                vm,
                null,
                'nominated_start_date',
                'insurance_expiry'
            );
        });
    },
    methods: {
        handleRadioChange: function (e) {
            if (e.target.value == 'true') {
                console.log(e.target.value);
                $('#show_docket').removeClass('hidden');
            } else {
                $('#show_docket').addClass('hidden');
            }
        },
        handleSelectionChange: function (e) {
            if (e.target.value == 'true') {
                console.log(e.target.value);
                $('#show_credit_link').removeClass('hidden');
            } else {
                $('#show_credit_link').addClass('hidden');
            }
        },
        showDockteNumber: function () {
            let vm = this;
            if (vm.proposal && vm.proposal.other_details.credit_docket_books) {
                var input = this.$refs.docket_books_yes;
                var e = document.createEvent('HTMLEvents');
                e.initEvent('change', true, true);
                var disabledStatus = input.disabled;
                try {
                    /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                    if (disabledStatus) {
                        input.disabled = false;
                    }
                    input.dispatchEvent(e);
                } finally {
                    if (disabledStatus) {
                        input.disabled = true;
                    }
                }
            }
        },
        showCreditFacilityLink: function () {
            let vm = this;
            if (vm.proposal && vm.proposal.other_details.credit_fees) {
                var input = this.$refs.credit_fees_yes;
                var e = document.createEvent('HTMLEvents');
                e.initEvent('change', true, true);
                var disabledStatus = input.disabled;
                try {
                    /* Firefox will not fire events for disabled widgets, so (temporarily) enabling them */
                    if (disabledStatus) {
                        input.disabled = false;
                    }
                    input.dispatchEvent(e);
                } finally {
                    if (disabledStatus) {
                        input.disabled = true;
                    }
                }
            }
        },
        addMooring: function () {
            let vm = this;
            var new_mooring = helpers.copyObject(
                vm.proposal.other_details.mooring
            );
            new_mooring.push('');
            vm.proposal.other_details.mooring = new_mooring;
            console.log(vm.proposal.other_details.mooring);
        },
        fetchAccreditationChoices: function () {
            let vm = this;
            helpers.fetchUrl('/api/accreditation_choices.json').then(
                (response) => {
                    vm.accreditation_choices = response;
                    if (vm.proposal.other_details.accreditation_type) {
                        for (
                            var i = 0;
                            i < vm.accreditation_choices.length;
                            i++
                        ) {
                            if (
                                vm.accreditation_choices[i].key ==
                                vm.proposal.other_details.accreditation_type
                            ) {
                                vm.accreditation_type =
                                    vm.accreditation_choices[i];
                            }
                        }
                    }
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        fetchTourismStandards: function(){
                let vm = this;
                
                helpers.fetchUrl('/api/tourism_standard_choices.json').then((response) => {
                    //vm.tourism_standard_choices = response.body;
                    vm.information_standard_choices = response.information_standard_choices;
                    vm.emission_standard_choices = response.emission_standard_choices;
                    
                },(error) => {
                    console.log(error);
                } );
        },
        fetchLicencePeriodChoices: function () {
            let vm = this;
            helpers.fetchUrl('/api/licence_period_choices.json').then(
                (response) => {
                    vm.licence_period_choices = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
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
        checkProposalAccreditation: function () {
            let vm = this;
            if (vm.proposal && vm.proposal.other_details) {
                for (
                    var i = 0;
                    i < vm.proposal.other_details.accreditations.length;
                    i++
                ) {
                    vm.proposal.other_details.accreditations[i].is_deleted =
                        false;
                    vm.selected_accreditations.push(
                        vm.proposal.other_details.accreditations[i]
                            .accreditation_type
                    );
                }
            }
        },
        checkProposalInformationStandard: function(){
                let vm= this;
                if(vm.proposal && vm.proposal.other_details){
                    for(var i=0; i<vm.proposal.other_details.information_standards.length; i++){
                        vm.proposal.other_details.information_standards[i].is_deleted=false;
                        vm.selected_information_standards.push(vm.proposal.other_details.information_standards[i].information_standard_type);
                    }
                }
        },
        checkProposalEmissionStandard: function(){
                let vm= this;
                if(vm.proposal && vm.proposal.other_details){
                    for(var i=0; i<vm.proposal.other_details.emission_standards.length; i++){
                        vm.proposal.other_details.emission_standards[i].is_deleted=false;
                        vm.selected_emission_standards.push(vm.proposal.other_details.emission_standards[i].emission_standard_type);
                    }
                }
        },
        selectAccreditation: function (e, accreditation_type) {
            console.log("selectAccreditation")
            let vm = this;
            if (e.target.checked) {
                var found = false;
                for (
                    var i = 0;
                    i < vm.proposal.other_details.accreditations.length;
                    i++
                ) {
                    if (
                        vm.proposal.other_details.accreditations[i]
                            .accreditation_type == accreditation_type.key
                    ) {
                        found = true;
                        vm.proposal.other_details.accreditations[i].is_deleted =
                            false;
                    }
                }
                console.log(found)
                if (!found) {
                    var data = {
                        accreditation_type: accreditation_type.key,
                        accreditation_expiry: null,
                        comments: '',
                        proposal_other_details: vm.proposal.other_details.id,
                        is_deleted: false,
                        accreditation_type_value: accreditation_type.value,
                    };
                    var acc = helpers.copyObject(
                        vm.proposal.other_details.accreditations
                    );
                    acc.push(data);
                    vm.proposal.other_details.accreditations = acc;
                }
            } else {
                for (
                    let i = 0;
                    i < vm.proposal.other_details.accreditations.length;
                    i++
                ) {
                    if (
                        vm.proposal.other_details.accreditations[i]
                            .accreditation_type == accreditation_type.key
                    ) {
                        if (vm.proposal.other_details.accreditations[i].id) {
                            const acc = helpers.copyObject(
                                vm.proposal.other_details.accreditations
                            );
                            acc[i].is_deleted = true;
                            vm.proposal.other_details.accreditations = acc;
                        } else {
                            const acc = helpers.copyObject(
                                vm.proposal.other_details.accreditations
                            );
                            acc.splice(i, 1);
                            vm.proposal.other_details.accreditations = acc;
                        }
                    }
                }
            }
        },
        selectInformationStandard: function(e, info_standard_type){
                let vm=this;
                if(e.target.checked){
                    var found=false;
                    for(var i=0;i<vm.proposal.other_details.information_standards.length; i++){
                        if(vm.proposal.other_details.information_standards[i].information_standard_type==info_standard_type.key){
                            found=true;
                            vm.proposal.other_details.information_standards[i].is_deleted=false;
                        }
                    }
                    if(found==false){
                    var data={
                        'information_standard_type': info_standard_type.key,
                        'comments':'',
                        'proposal_other_details': vm.proposal.other_details.id,
                        'is_deleted': false,
                        'information_standard_type_value': info_standard_type.value
                    }
                    var acc=helpers.copyObject(vm.proposal.other_details.information_standards);
                    acc.push(data);
                    vm.proposal.other_details.information_standards=acc;
                    }
                }
                else{
                    for(var i=0;i<vm.proposal.other_details.information_standards.length; i++)
                    {

                        if(vm.proposal.other_details.information_standards[i].information_standard_type==info_standard_type.key)
                        {
                            if(vm.proposal.other_details.information_standards[i].id){
                                //console.log('yes')
                                var acc=helpers.copyObject(vm.proposal.other_details.information_standards);
                                acc[i].is_deleted=true;
                                vm.proposal.other_details.information_standards=acc;
                            }
                            else{
                                var acc=helpers.copyObject(vm.proposal.other_details.information_standards);
                                acc.splice(i,1);
                                vm.proposal.other_details.information_standards=acc;
                            }
                        }
                    }
                }
            },
            selectEmissionStandard: function(e, emission_standard_type){
                    let vm=this;
                    if(e.target.checked){
                        var found=false;
                        for(var i=0;i<vm.proposal.other_details.emission_standards.length; i++){
                            if(vm.proposal.other_details.emission_standards[i].emission_standard_type==emission_standard_type.key){
                                found=true;
                                vm.proposal.other_details.emission_standards[i].is_deleted=false;
                            }
                        }
                        if(found==false){
                        var data={
                            'emission_standard_type': emission_standard_type.key,
                            'comments':'',
                            'proposal_other_details': vm.proposal.other_details.id,
                            'is_deleted': false,
                            'emission_standard_type_value': emission_standard_type.value
                        }
                        var acc=helpers.copyObject(vm.proposal.other_details.emission_standards);
                        acc.push(data);
                        vm.proposal.other_details.emission_standards=acc;
                        }
                    }
                    else{
                        for(var i=0;i<vm.proposal.other_details.emission_standards.length; i++)
                        {
    
                            if(vm.proposal.other_details.emission_standards[i].emission_standard_type==emission_standard_type.key)
                            {
                                if(vm.proposal.other_details.emission_standards[i].id){
                                    //console.log('yes')
                                    var acc=helpers.copyObject(vm.proposal.other_details.emission_standards);
                                    acc[i].is_deleted=true;
                                    vm.proposal.other_details.emission_standards=acc;
                                }
                                else{
                                    var acc=helpers.copyObject(vm.proposal.other_details.emission_standards);
                                    acc.splice(i,1);
                                    vm.proposal.other_details.emission_standards=acc;
                                }
                            }
                        }
                    }
        },
        eventListeners: function () {
            let vm = this;

            // Intialise select2
            $(vm.$refs.preferred_licence_period)
                .select2({
                    theme: 'bootstrap-5',
                    allowClear: true,
                    placeholder: 'Select preferred licence term',
                })
                .on('select2:select', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period =
                        selected.val();
                    vm.proposal.other_details.preferred_licence_period_id =
                        selected.val();
                })
                .on('select2:unselect', function (e) {
                    var selected = $(e.currentTarget);
                    vm.proposal.other_details.preferred_licence_period =
                        selected.val();
                    vm.proposal.other_details.preferred_licence_period_id =
                        selected.val();
                });
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
.hidden {
    display: none;
}
</style>
