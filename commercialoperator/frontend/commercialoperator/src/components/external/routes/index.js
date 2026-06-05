import { RouterView } from 'vue-router';

import ExternalDashboard from '../dashboard.vue';
import Proposal from '../proposal.vue';
import ProposalApply from '../proposal_apply.vue';
import ProposalSubmit from '../proposal_submit.vue';
import Compliance from '../compliances/access.vue';
import ComplianceSubmit from '../compliances/submit.vue';
import Approval from '../approvals/approval.vue';
import PaymentOrder from '@/components/common/tclass/payment_order.vue';
import PaymentDash from '@/components/common/payments_dashboard.vue';

export default {
    path: '/external',
    component: RouterView,
    children: [
        {
            path: '',
            component: ExternalDashboard,
            name: 'external-proposals-dash',
        },
        {
            path: 'compliance/:compliance_id',
            component: Compliance,
        },
        {
            path: 'compliance/submit/:compliance_id',
            component: ComplianceSubmit,
            name: 'submit_compliance',
        },
        {
            path: 'approval/:approval_id',
            component: Approval,
        },
        {
            path: 'payment',
            component: PaymentDash,
            props: { level: 'external' },
        },
        {
            path: 'payment_order',
            component: PaymentOrder,
            name: 'external-payment_order',
        },
        {
            path: 'proposal',
            component: RouterView,
            children: [
                {
                    path: '',
                    component: ProposalApply,
                    name: 'apply_proposal',
                },
                {
                    path: 'submit/:proposal_id',
                    component: ProposalSubmit,
                    name: 'submit_proposal',
                },
                {
                    path: ':proposal_id',
                    component: Proposal,
                    name: 'draft_proposal',
                },
            ],
        },
    ],
};
