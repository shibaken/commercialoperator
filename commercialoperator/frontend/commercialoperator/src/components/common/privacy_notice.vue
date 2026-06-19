<template>
    <div class="privacy-notice">
        <div class="panel panel-info">
            <div class="panel-heading" @click="toggleExpanded" style="cursor: pointer;">
                <h4 class="panel-title">
                    Privacy Notice
                    <span :class="isExpanded ? 'glyphicon glyphicon-chevron-up' : 'glyphicon glyphicon-chevron-down'" class="pull-right"></span>
                </h4>
            </div>
            <transition name="slide">
                <div v-show="isExpanded" class="panel-body">
                    <p>
                        The Department of Biodiversity, Conservation and Attractions (DBCA) collects this personal
                        information to order to assess, approve and grant a commercial operations licence to allow you to
                        legally carry out commercial operations in Western Australia's national parks and other conservation reserves.
                    </p>
                    <p>
                        You are required to provide this information under the
                        <em>Conservation and Land Management Act 1984</em> and
                        <em>Conservation and Land Management Regulations 2002</em>.
                    </p>
                    <p>
                        If you choose not to provide personal information, you will not be able to legally carry
                        out commercial operations in Western Australia's national parks and other conservation reserves.
                    </p>
                    <p>
                        For further details on how DBCA manage your personal information, you can read our
                        <a :href="privacyPolicyUrl" target="_blank">Privacy Policy</a>.
                        If you have any questions about how your personal information will be handled, or if you
                        would like to access your personal information, please contact
                        <a href="mailto:privacy@dbca.wa.gov.au">privacy@dbca.wa.gov.au</a>.
                    </p>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import { api_endpoints } from '@/utils/hooks';

export default {
    name: 'PrivacyNotice',
    data() {
        return {
            isExpanded: true,
            privacyPolicyUrl: api_endpoints.privacy_policy_url || '#'
        }
    },
    methods: {
        toggleExpanded() {
            this.isExpanded = !this.isExpanded;
        }
    }
}
</script>

<style scoped>
.privacy-notice {
    margin-bottom: 20px;
}

.panel-heading {
    user-select: none;
}

.slide-enter-active {
    transition: all 0.3s ease;
}

.slide-leave-active {
    transition: all 0.3s ease;
}

.slide-enter,
.slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
}
</style>
