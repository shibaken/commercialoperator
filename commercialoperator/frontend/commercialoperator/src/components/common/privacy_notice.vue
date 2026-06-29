<template>
    <div class="privacy-notice-container mb-4">
        <div class="card">
            <div
                class="card-header"
                style="cursor: pointer"
                @click="toggleExpanded"
            >
                <div class="row align-items-center">
                    <div class="col">
                        <h5 class="mb-0">
                            <i class="bi bi-info-circle-fill me-2"></i>Privacy
                            Notice
                        </h5>
                    </div>
                    <div class="col-auto">
                        <i
                            :class="
                                isExpanded
                                    ? 'bi bi-chevron-up'
                                    : 'bi bi-chevron-down'
                            "
                        ></i>
                    </div>
                </div>
            </div>
            <transition name="slide">
                <div v-show="isExpanded" class="card-body">
                    <p>
                        The Department of Biodiversity, Conservation and
                        Attractions (DBCA) collects this personal information to
                        order to assess, approve and grant a commercial
                        operations licence to allow you to legally carry out
                        commercial operations in Western Australia's national
                        parks and other conservation reserves.
                    </p>
                    <p>
                        You are required to provide this information under the
                        <em>Conservation and Land Management Act 1984</em> and
                        Conservation and Land Management Regulations 2002.
                    </p>
                    <p>
                        If you choose not to provide personal information, you
                        will not be able to legally carry out commercial
                        operations in Western Australia's national parks and
                        other conservation reserves.
                    </p>
                    <p>
                        For further details on how DBCA manage your personal
                        information, you can read our
                        <a :href="privacyPolicyUrl" target="_blank"
                            >Privacy Policy</a
                        >. If you have any questions about how your personal
                        information will be handled, or if you would like to
                        access your personal information, please contact
                        <a href="mailto:privacy@dbca.wa.gov.au"
                            >privacy@dbca.wa.gov.au</a
                        >.
                    </p>
                </div>
            </transition>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';

export default {
    name: 'PrivacyNotice',
    data() {
        return {
            isExpanded: true,
            privacyPolicyUrl: 'https://www.dbca.wa.gov.au/privacy', // Default fallback
            globalSettings: [],
        };
    },
    mounted() {
        this.fetchGlobalSettings();
    },
    methods: {
        toggleExpanded() {
            this.isExpanded = !this.isExpanded;
        },
        fetchGlobalSettings() {
            helpers
                .fetchUrl('/api/global_settings.json')
                .then((response) => {
                    this.globalSettings = response;
                    // Find privacy_policy_url in the settings
                    const privacySetting = this.globalSettings.find(
                        (setting) => setting.key === 'privacy_policy_url'
                    );
                    if (privacySetting && privacySetting.value) {
                        this.privacyPolicyUrl = privacySetting.value;
                    }
                })
                .catch((error) => {
                    console.error('Error fetching global settings:', error);
                    // Keep using the default fallback URL
                });
        },
    },
};
</script>

<style scoped>
.privacy-notice-container {
    margin-top: 15px;
}

.card-header {
    background-color: #e7f3ff;
    border-bottom: 1px solid #b3d7ff;
}

.card-header:hover {
    background-color: #d0e8ff;
}

.card-header h5 {
    color: #004085;
    font-weight: 600;
}

.card-body {
    background-color: #f8f9fa;
}

.card-body p {
    margin-bottom: 0.75rem;
    line-height: 1.6;
}

.card-body p:last-child {
    margin-bottom: 0;
}

.card-body a {
    color: #0056b3;
    text-decoration: none;
}

.card-body a:hover {
    text-decoration: underline;
}

/* Slide transition for smooth expand/collapse */
.slide-enter-active,
.slide-leave-active {
    transition: max-height 0.3s ease-out, padding 0.3s ease-out, opacity 0.3s ease-out;
    max-height: 500px;
    overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    opacity: 0;
}
</style>
