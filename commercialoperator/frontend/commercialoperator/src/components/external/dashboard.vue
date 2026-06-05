<template>
    <div id="externalDash" class="container">
        <div class="row">
            <div class="col-sm-12 mb-2">
                <div class="card">
                    <div class="card-header">
                        Welcome to the {{ system_name }} dashboard.
                    </div>
                    <div class="card card-body bg-light p-2">
                        <p class="card-text">
                            From this page you can view existing applications,
                            create new applications,<br />
                            view current licences, apply to amend a licence,
                            check through conditions of your licence.
                        </p>
                    </div>
                </div>
            </div>
        </div>
        <FormSection
            :form-collapse="false"
            label="Applications"
            index="applications"
            subtitle="View existing proposals and lodge new ones"
        >
            <ProposalDashTable level="external" :url="proposals_url" />
        </FormSection>
        <FormSection
            :form-collapse="false"
            label="Licences"
            index="approvals"
            subtitle="View existing licences and amend or renew them"
        >
            <ApprovalDashTable level="external" :url="approvals_url" />
        </FormSection>
        <FormSection
            :form-collapse="false"
            label="Compliances with requirements"
            index="compliances"
            subtitle="View submitted compliances and submit new ones"
        >
            <ComplianceDashTable level="external" :url="compliances_url" />
        </FormSection>
    </div>
</template>
<script>
import FormSection from '@/components/forms/section_toggle.vue';
import ProposalDashTable from '@common-utils/proposals_dashboard.vue';
import ApprovalDashTable from '@common-utils/approvals_dashboard.vue';
import ComplianceDashTable from '@common-utils/compliances_dashboard.vue';
import { api_endpoints } from '@/utils/hooks';
export default {
    name: 'ExternalDashboard',
    components: {
        FormSection,
        ProposalDashTable,
        ApprovalDashTable,
        ComplianceDashTable,
    },
    data() {
        return {
            proposals_url: api_endpoints.proposals_paginated_external,
            approvals_url: api_endpoints.approvals_paginated_external,
            compliances_url: api_endpoints.compliances_paginated_external,

            system_name: api_endpoints.system_name,
        };
    },
    computed: {},
    watch: {},
    mounted: function () {},
    methods: {},
};
</script>
