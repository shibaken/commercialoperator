<template lang="html">
    <div class="row">
        <div class="">
            <div class="col-md-12">
                <div class="">
                    <div class="card">
                        <FormSection
                            v-if="assessment"
                            :form-collapse="false"
                            label="Workflow - Checklist"
                            index="workflow_checklist"
                            :subtitle="
                                assessment.referral_group
                                    ? 'Referral Group: ' +
                                      assessment.referral_group_name
                                    : ''
                            "
                        >
                            <form class="form-horizontal">
                                <ul
                                    v-for="q in assessment.checklist"
                                    :key="q.id"
                                    class="list-unstyled col-sm-12"
                                >
                                    <div class="row">
                                        <div class="col-sm-12">
                                            <li class="col-sm-6">
                                                <label class="control-label">{{
                                                    q.question.text
                                                }}</label>
                                            </li>
                                            <ul
                                                v-if="
                                                    q.question.answer_type ==
                                                    'yes_no'
                                                "
                                                class="list-inline col-sm-6"
                                            >
                                                <li class="list-inline-item">
                                                    <input
                                                        :id="
                                                            'answer_one' + q.id
                                                        "
                                                        ref="Checkbox"
                                                        v-model="q.answer"
                                                        class="form-check-input"
                                                        type="radio"
                                                        :name="'option' + q.id"
                                                        :value="true"
                                                        data-parsley-required
                                                        :disabled="readonly"
                                                    />
                                                    Yes
                                                </li>
                                                <li class="list-inline-item">
                                                    <input
                                                        :id="
                                                            'answer_two' + q.id
                                                        "
                                                        ref="Checkbox"
                                                        v-model="q.answer"
                                                        class="form-check-input"
                                                        type="radio"
                                                        :name="'option' + q.id"
                                                        :value="false"
                                                        data-parsley-required
                                                        :disabled="readonly"
                                                    />
                                                    No
                                                </li>
                                            </ul>
                                            <ul
                                                v-else
                                                class="list-inline col-sm-6"
                                            >
                                                <li class="list-inline-item">
                                                    <textarea
                                                        v-model="q.text_answer"
                                                        :disabled="readonly"
                                                        class="form-control"
                                                        name="text_answer"
                                                        placeholder=""
                                                    ></textarea>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </ul>
                                <div
                                    v-if="hasAssessorMode || hasReferralMode"
                                    class="form-group col-sm-12"
                                >
                                    <button
                                        class="btn btn-primary float-end"
                                        style="margin-top: 5px"
                                        @click.prevent="update()"
                                    >
                                        Update
                                    </button>
                                </div>
                            </form>
                        </FormSection>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import FormSection from '@/components/forms/section_toggle.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';
import $ from 'jquery'
export default {
    name: 'AssessmentComponent',
    components: {
        FormSection,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        assessment: {
            type: Object,
            required: false,
            default: null,
        },
        hasAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_internal: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        is_referral: {
            type: Boolean,
            default: false,
        },
        hasReferralMode: {
            type: Boolean,
            default: false,
        },
    },
    data: function () {
        return {
            values: null,
            detailsBody: 'detailsBody' + uuid(),
            addressBody: 'addressBody' + uuid(),
            contactsBody: 'contactsBody' + uuid(),
            panelClickersInitialised: false,
            // Note: added localAssesment to prevent mutating the original assessment object
            localAssessment: JSON.parse(JSON.stringify(this.assessment)),
        };
    },
    computed: {
        readonly: function () {
            return !this.hasReferralMode && !this.hasAssessorMode
                ? true
                : false;
        },
    },
    watch: {
        assessment: {
            handler(newVal) {
                this.localAssessment = JSON.parse(JSON.stringify(newVal));
            },
            deep: true,
        },
    },
    mounted: function () {
        let vm = this;
        if (!vm.panelClickersInitialised) {
            $('.panelClicker[data-toggle="collapse"]').on('click', function () {
                var chev = $(this).children()[0];
                window.setTimeout(function () {
                    $(chev).toggleClass(
                        'glyphicon-chevron-down glyphicon-chevron-up'
                    );
                }, 100);
            });
            vm.panelClickersInitialised = true;
        }
        this.$nextTick(() => {
            //vm.initialiseOrgContactTable();
        });
    },
    methods: {
        update: function () {
            let vm = this;
            let assessment = JSON.parse(JSON.stringify(vm.localAssessment));
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.assessments,
                        vm.assessment.id + '/update_assessment'
                    ),
                    {
                        method: 'POST',
                        body: JSON.stringify(assessment),
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                )
                .then(
                    (response) => {
                        vm.localAssessment = helpers.copyObject(response);
                        swal.fire({
                            title: 'Checklist update',
                            text: 'Checklist has been updated',
                            icon: 'success',
                        });
                    },
                    (error) => {
                        vm.errorString = helpers.apiVueResourceError(error);
                        swal({
                            title: 'Checklist Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
    },
};
</script>

<style lang="css" scoped></style>
