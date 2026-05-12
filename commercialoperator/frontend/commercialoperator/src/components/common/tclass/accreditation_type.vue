<!-- eslint-disable vue/no-mutating-props -->
<template lang="html" :id="id">
    <div>
        <div class="row">
            <fieldset class="scheduler-border">
                <legend class="scheduler-border">
                    {{ accreditation.accreditation_type_value }}
                </legend>
                <div class="form-group">
                    <div class="row">
                        <div class="col-sm-3">
                            <label class="control-label pull-right" for="Name"
                                >Expiry Date</label
                            >
                        </div>
                        <div class="col-sm-9">
                            <div
                                ref="accreditation_expiry"
                                class="input-group date"
                                style="width: 70%"
                            >
                                <input
                                    v-model="accreditation.accreditation_expiry"
                                    type="date"
                                    class="form-control"
                                    name="accreditation_expiry"
                                    max="2999-12-31"
                                    placeholder="DD/MM/YYYY"
                                    :disabled="readonly"
                                />
                                <span class="input-group-text">
                                    <i class="fas fa-calendar-days"></i>
                                </span>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-sm-3">
                            <label class="control-label pull-right" for="Name"
                                >Accreditation certificates</label
                            >
                        </div>
                        <div class="col-sm-9">
                            <FileField
                                :id="
                                    'accreditation' +
                                    accreditation.accreditation_type +
                                    proposal_id
                                "
                                ref="accreditation_file"
                                :proposal_id="proposal_id"
                                :is-repeatable="false"
                                :name="
                                    'accreditation' +
                                    accreditation.accreditation_type
                                "
                                :readonly="!canEditActivities"
                            ></FileField>
                        </div>
                    </div>
                    <div v-if="typeOther" class="row">
                        <div class="col-sm-3">
                            <label class="control-label pull-right" for="Name"
                                >Details</label
                            >
                        </div>
                        <div class="col-sm-9">
                            <div
                                ref="accreditation_comments"
                                class=""
                                style="width: 70%"
                            >
                                <input
                                    v-model="accreditation.comments"
                                    type="textarea"
                                    class="form-control"
                                    name="accreditation_comments"
                                    :disabled="readonly"
                                />
                            </div>
                        </div>
                    </div>
                </div>
            </fieldset>
        </div>
    </div>
</template>

<script>
import FileField from '@/components/forms/filefield.vue';

export default {
    // eslint-disable-next-line vue/component-definition-name-casing, vue/multi-word-component-names
    name: 'accreditation',
    components: {
        FileField,
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        proposal_id: null,
        accreditation: {
            type: Object,
            required: true,
        },
        // eslint-disable-next-line vue/require-default-prop
        id: String,
        // eslint-disable-next-line vue/prop-name-casing
        assessor_readonly: Boolean,
        // eslint-disable-next-line vue/require-prop-types
        assessorMode: {
            default: function () {
                return false;
            },
        },
        // eslint-disable-next-line vue/require-prop-types
        value: {
            default: function () {
                return null;
            },
        },
        readonly: Boolean,
        canEditActivities: {
            type: Boolean,
            default: true,
        },
    },
    data: function () {
        return {
            repeat: 1,
        };
    },

    computed: {
        typeOther: function () {
            return this.accreditation &&
                this.accreditation.accreditation_type == 'other'
                ? true
                : false;
        },
    },
    mounted: function () {
        let vm = this;
        this.$nextTick(() => {
            vm.eventListeners();
        });
    },

    methods: {
        eventListeners: function () {},
    },
};
</script>

<style lang="css">
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
