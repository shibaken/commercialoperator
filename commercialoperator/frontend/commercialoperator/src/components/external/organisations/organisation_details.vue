<template>
    <div class="container">
        <!-- <PrivacyNotice /> -->

        <div id="userInfo" class="row">
        <div class="col-sm-12">
            <div class="row">
                <div class="col-sm-12">
                        <FormSection
                            :form-collapse="false"
                            label="Organisation Details"
                            index="organisation_details"
                        >
                            <form
                                class="form-horizontal"
                                name="personal_form"
                                method="post"
                            >
                                <div v-if="org">
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >Organisation Name</label
                                        >
                                        <div class="col-sm-9">
                                            <input
                                                v-model="org.organisation_name"
                                                type="text"
                                                disabled
                                                class="form-control"
                                                name="first_name"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >Trading Name</label
                                        >
                                        <div class="col-sm-9">
                                            <input
                                                v-model="
                                                    org.organisation_trading_name
                                                "
                                                type="text"
                                                disabled
                                                class="form-control"
                                                name="trading_name"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >ABN</label
                                        >
                                        <div class="col-sm-9">
                                            <input
                                                v-model="org.organisation_abn"
                                                type="text"
                                                disabled
                                                class="form-control"
                                                name="last_name"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >Email</label
                                        >
                                        <div class="col-sm-9">
                                            <input
                                                v-model="org.organisation_email"
                                                type="text"
                                                class="form-control"
                                                disabled
                                                name="email"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>

                                    <div class="form-group row">
                                        <div class="col-sm-12">
                                            <strong>Update Organisation Details <a :href="`/ledger-ui/organisation/`+org.organisation_id" target="_blank">here</a>.</strong>
                                        </div>
                                    </div>
                                </div>
                            </form>
                        </FormSection>
                </div>
            </div>
            <div class="row">
                <div class="col-sm-12">
                        <FormSection
                            :form-collapse="false"
                            label="Address Details"
                            index="address_details"
                        >
                            <form
                                class="form-horizontal"
                                action="index.html"
                                method="post"
                            >
                                <div v-if="org">
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >Street</label
                                        >
                                        <div class="col-sm-6">
                                            <input
                                                v-model="
                                                    org.organisation_address
                                                        .line1
                                                "
                                                type="text"
                                                disabled
                                                class="form-control"
                                                name="street"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >Town/Suburb</label
                                        >
                                        <div class="col-sm-6">
                                            <input
                                                v-model="
                                                    org.organisation_address
                                                        .locality
                                                "
                                                type="text"
                                                disabled
                                                class="form-control"
                                                name="surburb"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for=""
                                            class="col-sm-3 control-label"
                                            >State</label
                                        >
                                        <div class="col-sm-3">
                                            <input
                                                v-model="
                                                    org.organisation_address
                                                        .state
                                                "
                                                type="text"
                                                class="form-control"
                                                disabled
                                                name="country"
                                                placeholder=""
                                            />
                                        </div>
                                        <label
                                            for=""
                                            class="col-sm-1 control-label text-nowrap"
                                            >Postcode</label
                                        >
                                        <div class="col-sm-2">
                                            <input
                                                v-model="
                                                    org.organisation_address
                                                        .postcode
                                                "
                                                type="text"
                                                class="form-control"
                                                disabled
                                                name="postcode"
                                                placeholder=""
                                            />
                                        </div>
                                    </div>
                                    <div class="form-group row mb-3">
                                        <label
                                            for="select_manage_org_address_country"
                                            class="col-sm-3 control-label"
                                            >Country</label
                                        >
                                        <div
                                            id="select_manage_org_address_country_parent"
                                            class="col-sm-4"
                                        >
                                            <select
                                                id="select_manage_org_address_country"
                                                ref="select_manage_org_address_country"
                                                v-model="
                                                    org.organisation_address
                                                        .country
                                                "
                                                disabled
                                                class="form-control"
                                                name="country"
                                            >
                                                <option
                                                    v-for="c in countries"
                                                    :key="c.code"
                                                    :value="c.code"
                                                >
                                                    {{ c.name }}
                                                </option>
                                            </select>
                                        </div>
                                    </div>
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
import utils from '../utils';
import FormSection from '@/components/forms/section_toggle.vue';
// import PrivacyNotice from '@/components/common/privacy_notice.vue';
import _ from 'lodash';
import $ from 'jquery'
export default {
    // eslint-disable-next-line vue/multi-word-component-names
    name: 'Organisation',
    components: {
        FormSection
        // PrivacyNotice,
    },
    beforeRouteEnter: function (to, from, next) {
        let initialisers = [
            utils.fetchCountries(),
            utils.fetchOrganisation(to.params.org_id),
        ];
        Promise.all(initialisers).then((data) => {
            next((vm) => {
                vm.countries = data[0];
                vm.org = data[1];
                vm.org.organisation_address =
                    vm.org.organisation_address != null
                        ? vm.org.organisation_address
                        : {};
            });
        });
    },
    beforeRouteUpdate: function (to, from, next) {
        let initialisers = [
            utils.fetchOrganisation(to.params.org_id),
        ];
        Promise.all(initialisers).then((data) => {
            next((vm) => {
                vm.org = data[0];
                vm.org.organisation_address =
                    vm.org.organisation_address != null
                        ? vm.org.organisation_address
                        : {};
            });
        });
    },
    props: {
        // eslint-disable-next-line vue/prop-name-casing
        org_id: {
            type: Number,
            default: null,
        },
    },
    data() {
        let vm = this;
        return {
            org: {
                organisation_address: {},
            },
            countries: [],
        };
    },
    mounted: function () {
        let vm = this;
        vm.personal_form = document.forms.personal_form;
        if (!vm.org_id) {
            // Prop org_id is null when using the external/organisations/manage/org_id route
            return;
        }

        let initialisers = [
            utils.fetchCountries(),
            utils.fetchOrganisation(vm.org_id),
        ];
        Promise.all(initialisers).then((data) => {
            vm.countries = data[0];
            vm.org = data[1];
            vm.org.organisation_address =
                vm.org.organisation_address != null
                    ? vm.org.organisation_address
                    : {};
            vm.org.pins = vm.org.pins != null ? vm.org.pins : {};
        });
    },
    updated: function () {
        $('.panelClicker[data-bs-toggle="collapse"]').on('click', function () {
            var chev = $(this).children()[0];
            window.setTimeout(function () {
                $(chev).toggleClass(
                    'fa-chevron-down fa-chevron-up'
                );
            }, 100);
        });
        this.$nextTick(() => {
            this.eventListeners();
        });
    },
};
</script>

<style scoped>
.top-buffer-s {
    margin-top: 25px;
}
</style>
