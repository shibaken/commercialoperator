<template lang="html">
    <div class="container">
        <div class="col-sm-12">
            <div class="row">
                    <FormSection
                        :form-collapse="false"
                        label="Park Entry Fees"
                        index="payment"
                        subtitle=""
                    >
                        <form
                            method="post"
                            name="new_payment"
                            novalidate
                            @submit.prevent="submit()"
                        >
                            <input
                                type="hidden"
                                name="csrfmiddlewaretoken"
                                :value="csrf_token"
                            />

                            <div
                                v-if="formErrors.length > 0"
                                id="error"
                                style="
                                    margin: 10px;
                                    padding: 5px;
                                    color: red;
                                    border: 1px solid red;
                                "
                            >
                                <b>Please correct the error(s) in row(s):</b>
                                <BootstrapAlert
                                    v-for="(error, index) in formErrors"
                                    :key="`bs-alert-${index}-${error.id}`"
                                    type="danger"
                                >
                                    {{ error.name }}: {{ error.label }}
                                </BootstrapAlert>
                            </div>

                            <div
                                v-if="warnings.length > 0"
                                id="id_warning"
                                style="
                                    margin: 10px;
                                    padding: 5px;
                                    color: blue;
                                    border: 1px solid blue;
                                    display: none;
                                "
                            >
                                <div
                                    ref="warning"
                                    :key="JSON.stringify(tbody)"
                                    style="text-align: left"
                                    :data="tbody"
                                >
                                    <b>Multiple payment(s) selected:</b>
                                    <ul>
                                        <li
                                            v-for="warning in warnings"
                                            :key="warning.id"
                                        >
                                            {{ warning.name }}:
                                            {{ warning.label }}
                                        </li>
                                    </ul>
                                </div>
                            </div>

                            <label for="select_id_licence">Licence</label>
                            <select
                                id="select_id_licence"
                                ref="select_id_licence"
                                v-model="selected_licence_id"
                                class="form-control"
                                :clearable="false"
                                required
                                @change="proposal_parks()"
                            >
                                <option
                                    v-for="l in licences"
                                    :key="l.value"
                                    :value="l.value"
                                >
                                    {{ l.label }}
                                </option>
                            </select>
                            <OrderTable
                                id="id_payment"
                                ref="order_table"
                                :expiry_date="selected_licence.expiry_date"
                                :disabled="!parks_available"
                                :headers="headers"
                                :options="parks"
                                name="payment"
                                label=""
                            />

                            <div
                                v-if="selected_licence.org_applicant == null || (!selected_licence.bpay_allowed && !selected_licence.monthly_invoicing_allowed && !selected_licence.other_allowed)"
                                style="float: right"
                            >
                                <!-- Individual applicants must pay using Credit Card -->
                                <button
                                    :disabled="!parks_available"
                                    class="btn btn-primary float-end"
                                    type="submit"
                                    style="margin-top: 5px"
                                >
                                    Proceed to Payment
                                </button>
                            </div>
                            <div v-else class="container-fluid">
                                <div class="row">
                                    <div class="col-md-9">
                                        <select name="payment_method" class="form-control float-end" style="width: 50%" required>
                                            <option value="" disabled selected>Select Payment Method...</option>
                                            <option value="credit_card">Pay by Credit Card</option>
                                            <option v-if="selected_licence.bpay_allowed" value="bpay">Pay by BPAY</option>
                                            <option v-if="selected_licence.monthly_invoicing_allowed || selected_licence.other_allowed" value="monthly_invoicing">Monthly Invoicing</option>
                                            <option v-if="selected_licence.other_allowed" value="other">Other</option>
                                        </select>
                                    </div>
                                    <div class="col-md-3">
                                        <button
                                            :disabled="!parks_available"
                                            class="btn btn-primary float-end"
                                            style="margin-top: 5px"
                                        >
                                            Proceed to Payment
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </FormSection>
            </div>
        </div>
    </div>
</template>

<script>
import OrderTable from './order_table.vue';
import { api_endpoints, helpers } from '@/utils/hooks';
import FormSection from '@/components/forms/section_toggle.vue';
import BootstrapAlert from '@/components/vue2-components/BootstrapAlert.vue';
import $ from 'jquery'
export default {
    name: 'PaymentOrder',
    components: {
        OrderTable,
        FormSection,
        BootstrapAlert,
    },
    data: function () {
        return {
            values: null,
            headers:
                '{"Park": "select", "Arrival": "date", "Same tour group": "checkbox", "Passengers (6yrs+)": "number", "Children under 6 years": "number", "Free of charge":"number", "Cost":"total"}',
            parks: [],
            land_parks: [],
            parks_available: false,
            licences: [],
            formErrors: [],
            warnings: [],
            table_values: null,
            payment_method: null,
            selected_licence_id: null,
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        selected_licence: function () {
            return (
                this.licences.find(
                    (licence) => licence.value == this.selected_licence_id
                ) || {
                    value: null,
                    label: null,
                    expiry_date: null,
                }
            );
        },
    },
    watch: {
        options: function () {
            if (!this.parks_available) {
                this.$refs.order_table.options.length = 0;
                this.$refs.order_table.table_values.length = 0;
            }
        },
    },
    mounted: function () {
        let vm = this;
        vm.form = document.forms.new_payment;
        vm.get_user_approvals();
        this.$nextTick(() => {
            const select2 = helpers.initialiseSelect2.bind(this)(
                'select_id_licence',
                null,
                'selected_licence_id',
                'Select a License',
                true,
                0,
                null
            );
            select2
                .on('select2:select', function () {
                    vm.proposal_parks();
                })
                .on('select2:unselect', function () {
                    vm.proposal_parks();
                });
        });
    },
    methods: {
        today: function () {
            var day = new Date();
            var dd = day.getDate();
            var mm = day.getMonth() + 1; //January is 0!
            var yyyy = day.getFullYear();
            if (dd < 10) {
                dd = '0' + dd;
            }
            if (mm < 10) {
                mm = '0' + mm;
            }

            return new Date(yyyy + '-' + mm + '-' + dd);
        },

        resetTable: function () {
            /* Removes the rows, keeos the first and clears the td contents */
            let vm = this;
            $('.editable-table tbody')
                .find('tr:not(:first):not(:last)')
                .remove(); // last row contains total price cell

            vm.$refs.order_table.table.tbody = [
                vm.$refs.order_table.reset_row(),
            ];
            $('.editable-table .selected-tag').text('');
            $('.tbl_input').val('');
        },
        park_options: function () {
            let vm = this;
            vm.parks = [];
            for (
                var i = 0, length = vm.proposal.land_parks.length;
                i < length;
                i++
            ) {
                vm.parks.push({
                    label: vm.proposal.land_parks[i].park.name,
                    value: vm.proposal.land_parks[i].park.id,
                });
            }
        },
        calc_order: function () {
            let vm = this;
            var formData = new FormData(vm.form);
            vm.order_details = formData.get('payment');
            vm.$refs.payment_calc.order_details = vm.order_details;
            vm.$refs.payment_calc.isModalOpen = true;
        },
        payment: function () {
            let vm = this;
            var proposal_id = vm.selected_licence.value;

            let formData = new FormData(vm.form);
            formData.append(
                'tbody',
                JSON.stringify(vm.$refs.order_table.table.tbody)
            );
            helpers
                .fetchUrl(`/payment/${proposal_id}/`, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'Content-Type': 'application/json',
                    },
                })
                .then(
                    () => {
                        swal.fire({
                            title: 'Payment',
                            text: 'Your payment has been completed',
                            icon: 'success',
                        });
                    },
                    () => {}
                );
        },

        check_form_valid: function () {
            let vm = this;
            var idx_park = vm.$refs.order_table.idx_park;
            var idx_arrival_date = vm.$refs.order_table.idx_arrival_date;
            var idx_adult = vm.$refs.order_table.idx_adult;
            var idx_child = vm.$refs.order_table.idx_child;
            var idx_free = vm.$refs.order_table.idx_free;
            // eslint-disable-next-line no-unused-vars
            var idx_price = vm.$refs.order_table.idx_price;
            // eslint-disable-next-line no-unused-vars
            var idx_adult_same_tour = vm.$refs.order_table.idx_adult_same_tour;
            // eslint-disable-next-line no-unused-vars
            var idx_child_same_tour = vm.$refs.order_table.idx_child_same_tour;
            // eslint-disable-next-line no-unused-vars
            var idx_free_same_tour = vm.$refs.order_table.idx_free_same_tour;

            var errors = [];
            var tbody = vm.$refs.order_table.table.tbody;
            for (var row_idx in tbody) {
                var row = tbody[row_idx];
                const adults = Number(row[idx_adult]) || 0;
                const children = Number(row[idx_child]) || 0;
                const free = Number(row[idx_free]) || 0;
                // Whether there is any visitor at all
                const anyVisitor = adults + children + free > 0;

                if (!(row[idx_park] || row[idx_arrival_date]) || !anyVisitor) {
                    // Cannot have no selected park, no arrival date, or no visitors
                    errors.push({
                        id: parseInt(row_idx),
                        name: 'Row',
                        label: parseInt(row_idx) + 1,
                    });
                }

                var arrival_date = new Date(row[idx_arrival_date]);
                if (arrival_date < vm.today()) {
                    errors.push({
                        id: parseInt(row_idx),
                        name: 'Arrival Date',
                        label: 'Cannot be in the past',
                    });
                }

                if (arrival_date > new Date(vm.selected_licence.expiry_date)) {
                    errors.push({
                        id: parseInt(row_idx),
                        name: 'Arrival Date',
                        label:
                            'Cannot be beyond Licence expiry (Expiry:' +
                            vm.selected_licence.expiry_date +
                            ')',
                    });
                }
            }

            return errors;
        },
        check_duplicate_parks: function () {
            /* https://stackoverflow.com/questions/53452875/find-if-two-arrays-are-repeated-in-array-and-then-select-them/53453045#53453045 */
            var t = {};
            var data = [];
            var tbody = this.$refs.order_table.table.tbody;
            for (var i in tbody) {
                // keep first 3 elements
                var row = tbody[i];
                data.push([row[0], row[1], row[2] == '' ? false : true]);
            }
            let duplicates = data.filter(((t = {}), (a) => (t[a] = a in t)));
            return duplicates;
        },
        duplicate_parks_str: function () {
            var msg =
                // eslint-disable-next-line no-useless-escape
                '<div style=\"text-align:left;\"> <b>Multiple payment(s) selected:</b> <ul>';
            for (var i in this.warnings) {
                console.log(this.warnings[i]);
                msg +=
                    '<li>' +
                    this.warnings[i][0].label +
                    ': ' +
                    this.warnings[i][1] +
                    '</li>';
            }
            msg += '</ul> </div>';

            return msg;
        },
        submit: function () {
            let vm = this;

            vm.formErrors = vm.check_form_valid();
            vm.warnings = vm.check_duplicate_parks();

            if (vm.warnings.length > 0) {
                swal.fire({
                    title: 'Multiple park entry fee payments exist for the same date. Are you sure you want to continue?',
                    html: vm.duplicate_parks_str(),
                    icon: 'question',
                    showCancelButton: true,
                    confirmButtonText: 'Accept',
                }).then(
                    async (result) => {
                        if (result.isConfirmed) {
                            if (
                                vm.payment_method == 'monthly_invoicing' ||
                                vm.payment_method == 'bpay' ||
                                vm.payment_method == 'other'
                            ) {
                                vm.form.action =
                                    '/preview_deferred/' +
                                    vm.selected_licence.value +
                                    '/?method=' +
                                    vm.payment_method;
                            } else {
                                vm.form.action =
                                    '/payment/' +
                                    vm.selected_licence.value +
                                    '/';
                            }
                            if (
                                helpers.validateForm(vm.form) &&
                                vm.formErrors.length == 0
                            ) {
                                vm.form.submit();
                            } else {
                                return;
                            }
                        }
                    },
                );
            } else {
                if (
                    vm.payment_method == 'monthly_invoicing' ||
                    vm.payment_method == 'bpay' ||
                    vm.payment_method == 'other'
                ) {
                    vm.form.action =
                        '/preview_deferred/' +
                        vm.selected_licence.value +
                        '/?method=' +
                        vm.payment_method;
                } else {
                    vm.form.action =
                        '/payment/' + vm.selected_licence.value + '/';
                }
                if (
                    helpers.validateForm(vm.form) &&
                    vm.formErrors.length == 0
                ) {
                    vm.form.submit();
                } else {
                    return;
                }
            }

            this.warnings = [];
        },

        get_user_approvals: function () {
            let vm = this;
            helpers.fetchUrl('/api/filtered_payments').then(
                (res) => {
                    var licences = res.results;
                    for (var i in licences) {
                        vm.licences.push({
                            value: licences[i].current_proposal,
                            label: licences[i].lodgement_number,
                            expiry_date: licences[i].expiry_date,
                            org_applicant: licences[i].org_applicant,
                            bpay_allowed: licences[i].bpay_allowed,
                            monthly_invoicing_allowed:
                                licences[i].monthly_invoicing_allowed,
                            other_allowed: licences[i].other_allowed,
                        });
                    }
                    console.log(vm.licences);
                },
                () => {}
            );
        },
        proposal_parks: function () {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_park,
                        vm.selected_licence.value + '/proposal_parks'
                    )
                )
                .then(
                    (res) => {
                        vm.resetTable();
                        vm.land_parks = res.land_parks;
                        vm.parks = [];
                        for (var i in vm.land_parks) {
                            vm.parks.push({
                                value: vm.land_parks[i].park.id,
                                label: vm.land_parks[i].park.name,
                                prices: {
                                    adult: vm.land_parks[i].park.adult_price,
                                    child: vm.land_parks[i].park.child_price,
                                },
                                region_id: vm.land_parks[i].park.region.id,
                                region_name: vm.land_parks[i].park.region.name,
                                max_group_arrival_by_date:
                                    vm.land_parks[i].park
                                        .max_group_arrival_by_date,
                            });
                        }
                        if (vm.parks.length == 0) {
                            vm.parks_available = false;
                            vm.parks.push({
                                value: 0,
                                label: 'No parks available',
                            });
                        } else {
                            vm.parks_available = true;
                        }
                        console.log(vm.land_parks);
                    },
                    () => {}
                );
        },
    },
};
</script>
