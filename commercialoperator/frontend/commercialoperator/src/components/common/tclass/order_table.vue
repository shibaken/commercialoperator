<template lang="html">
    <div>
        <div class="form-group">
            <label :id="id" for="label" class="inline">{{ label }}</label>
            <div id="content-editable-table">
                <table class="table table-striped editable-table">
                    <thead v-if="table.thead.length">
                        <tr>
                            <th
                                v-for="(heading, index) in tableHeader"
                                :key="index"
                            >
                                {{ tableHeader[index] }}
                                <span
                                    v-if="
                                        table.thead[index] == 'Same tour group'
                                    "
                                >
                                    <i
                                        class="fas fa-circle-info"
                                        aria-hidden="true"
                                        title="If a tour is entering multiple parks with entry fees on the same day, only one entry fee applies per passenger. When adding additional parks to a payment, check the ‘same tour group’ box which will reduce the fee to zero dollars for passengers who have already paid an entry fee on that date. If a tour is visiting Nambung and Yanchep National parks on the same day, a per passenger fee will be charged for both parks."
                                        style="cursor: pointer;  color: blue"
                                    ></i>
                                </span>
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr
                            v-for="(row, row_idx) in filteredRows"
                            :key="row_idx"
                        >
                            <td
                                v-for="(_, col_idx) in row"
                                :key="col_idx"
                                :set="
                                    row_item_value = rowItem(row_idx, col_idx)
                                "
                                width="30%"
                            >
                                <div
                                    v-if="col_types[col_idx] == 'select'"
                                    id="select_order_table_park_parent"
                                    class="select_order_table_park_parent"
                                >
                                    <select
                                        :id="`select_order_table_park-${row_idx}-${col_idx}`"
                                        :ref="`select_order_table_park-${row_idx}-${col_idx}`"
                                        v-model="row[col_idx]"
                                        class="tbl_input form-control"
                                        :title="
                                            'Adult Price: ' +
                                            row[col_idx] +
                                            ', Child Price: ' +
                                            row[col_idx]
                                        "
                                        :disabled="disabled"
                                        :clearable="false"
                                        :required="!disabled"
                                        @change="
                                            park_change(
                                                row[col_idx],
                                                row,
                                                row_idx
                                            )
                                        "
                                    >
                                        <option
                                            v-for="o in options"
                                            :key="o.value"
                                            :value="o.value"
                                        >
                                            {{ o.label }}
                                        </option>
                                    </select>
                                </div>
                                <template v-if="col_types[col_idx] == 'date'">
                                    <input
                                        id="id_arrival_date"
                                        style="width:100%"
                                        v-model="row[col_idx]"
                                        class="tbl_input form-control"
                                        :type="col_types[col_idx]"
                                        :max="expiry_date"
                                        :min="today()"
                                        :onclick="isClickable"
                                        :disabled="
                                            [undefined, null, ''].includes(
                                                row[0]
                                            ) === true
                                        "
                                        :required="
                                            [undefined, null, ''].includes(
                                                row[0]
                                            ) === false
                                        "
                                        @change="
                                            date_change(
                                                row[col_idx],
                                                row,
                                                row_idx
                                            )
                                        "
                                    />
                                </template>
                                <template
                                    v-if="col_types[col_idx] == 'checkbox'"
                                >
                                    <input
                                        :id="'id_checkbox_' + row_idx"
                                        v-model="row[col_idx]"
                                        class="tbl_input form-check-input"
                                        :type="col_types[col_idx]"
                                        :checkbox="
                                            get_same_tour_group_checkbox(
                                                row_idx
                                            ).checked
                                        "
                                        :title="
                                            tooltip_same_group_tour(
                                                row,
                                                row_idx
                                            )
                                        "
                                        :disabled="
                                            get_same_tour_group_checkbox(
                                                row_idx
                                            ).disabled
                                        "
                                        @change="
                                            calcPrice(row, row_idx, col_idx)
                                        "
                                    />
                                </template>
                                <template
                                    v-if="
                                        col_types[col_idx] == 'text' ||
                                        col_types[col_idx] == 'number'
                                    "
                                >
                                    <input
                                        v-model="row[col_idx]"
                                        :readonly="readonly"
                                        class="tbl_input form-control"
                                        :class="`row-input row-${row_idx}-input`"
                                        :type="col_types[col_idx]"
                                        min="0"
                                        :required="true"
                                        :onclick="isClickable"
                                        :disabled="row[1] == ''"
                                        @change="tour_group_change(row, row_idx)"
                                    />
                                </template>
                                <template v-if="col_types[col_idx] == 'total'">
                                    <div class="currencyinput">
                                        <input
                                            v-model="row[col_idx]"
                                            class="tbl_input form-control"
                                            :type="col_types[col_idx]"
                                            min="0"
                                            disabled
                                        />
                                    </div>
                                </template>
                            </td>
                            <td v-if="!readonly">
                                <a
                                    title="Delete row"
                                    :disabled="disabled"
                                    @click="deleteRow(row, row_idx)"
                                >
                                    <i
                                        class="fas fa-trash"
                                        style="cursor: pointer; color: red"
                                    ></i>
                                </a>
                            </td>
                        </tr>

                        <tr>
                            <td colspan="6" align="right">
                                <div><label>Total:</label></div>
                            </td>
                            <td align="left">
                                <div class="currencyinput">
                                    <input
                                        class="tbl_input form-control"
                                        type="total"
                                        min="0"
                                        :value="total_price()"
                                        disabled
                                    />
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <span
                    ><button
                        class="btn btn-primary"
                        type="button"
                        :disabled="disabled"
                        @click="addRow()"
                    >
                        +</button
                    >Add another park and/or date</span
                >
            </div>
        </div>
        <!-- Hidden input field for form submission (by name and value) -->
        <input
            type="hidden"
            class="form-control"
            :name="name"
            :value="localValue"
        />
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';
import _ from 'lodash';
import $ from 'jquery'
export default {
    components: {},
    filters: {
        _price: function (row_idx) {
            let vm = this;
            return row_idx ? vm.net_park_prices[row_idx] : '';
        },
        price: function (dict, key) {
            return dict[key];
        },
    },
    props: {
        headers: {
            type: String,
            required: true,
        },
        options: {
            type: Array,
            required: true,
        },
        name: {
            type: String,
            default: function () {
                return '';
            },
        },
        label: {
            type: String,
            default: function () {
                return '';
            },
        },
        // eslint-disable-next-line vue/prop-name-casing
        expiry_date: {
            type: String,
            default: function () {
                return '';
            },
        },
        id: {
            type: String,
            default: function () {
                return '';
            },
        },
        isRequired: {
            type: Boolean,
            default: function () {
                return false;
            },
        },
        // eslint-disable-next-line vue/prop-name-casing
        comment_value: {
            type: String,
            default: function () {
                return '';
            },
        },
        disabled: Boolean,
        readonly: Boolean,
        value: {
            type: String,
            default: function () {
                return null;
            },
        },
    },
    data() {
        return {
            idx_park: 0,
            idx_arrival_date: 1,
            idx_same_group_tour: 2,
            idx_adult: 3,
            idx_child: 4,
            idx_free: 5,
            idx_price: 6,
            idx_adult_same_tour: 7, // these are the net number of adults (that must pay admission fee). Required for invoicing
            idx_child_same_tour: 8,
            idx_free_same_tour: 9,

            isClickable: 'return true;',
            selected_park: {
                default: function () {
                    return {
                        value: String,
                        label: String,
                        prices: Object,
                    };
                },
            },
            net_park_prices: {
                default: function () {
                    return {
                        value: Number,
                        idx: Number,
                    };
                },
            },
            max_group_arrival: [],

            total_adults_same_group: 0,
            total_children_same_group: 0,
            regions: [],
            arrival_dates: [],
            region_arrival_map: [],
            localValue: JSON.parse(JSON.stringify(this.value)),
            table: {
                thead: [],
                tbody: [],
            },
            same_tour_group_checkbox: [],
        };
    },

    computed: {
        wc_version: function () {
            return this.$root.wc_version;
        },
        tableHeader: function () {
            if (!this.table.thead) {
                return [];
            }
            if (!this.readonly) {
                return [...this.table.thead, ...['Action']];
            }
            return this.table.thead;
        },
        filteredRows: function () {
            return this.table.tbody.map((row) => {
                return row.slice(0, this.table.thead.length);
            });
        },
        rowItem: {
            get: function () {
                return (row_idx, col_idx) => {
                    return this.table.tbody[row_idx][col_idx];
                };
            },
        },
    },
    watch: {
        options: {
            handler: function () {
                this.add_previous_visitors_same_group_tour();
                this.regions = this.get_regions();
                this.arrival_dates = this.get_arrival_dates();
                console.log('regions: ' + this.regions);
                console.log('arrivals: ' + this.arrival_dates);
            },
            deep: true,
        },
        'table.tbody': {
            handler: function () {
                this.update_arrival_dates();
            },
            deep: true,
        },
        value: {
            handler: function (value) {
                this.localValue = value;
            },
            deep: true,
        },
    },
    beforeUpdate() {},
    created: function () {
        console.log('In created');
        let vm = this;
        var value = JSON.parse(vm.value);

        var headers = JSON.parse(vm.headers);
        vm.col_headers = Object.keys(headers);
        vm.col_types = Object.values(headers);

        // setup initial empty row for display
        vm.init_row = vm.reset_row();

        if (value == null) {
            for (let header_item of vm.col_headers) {
                vm.table.thead.push(header_item);
            }
            vm.table.tbody.push(vm.init_row);
        } else {
            for (let header_item of value['thead']) {
                vm.table.thead.push(header_item);
            }
            for (let body_item of value['tbody']) {
                vm.table.tbody.push(body_item);
            }
        }
        for (var i = 0; i < vm.table.tbody.length; i++) {
            vm.same_tour_group_checkbox.push({
                disabled: true,
                checked: false,
            });
        }
    },
    mounted: function () {
        let vm = this;

        vm.updateTableJSON();

        //$('#content-editable-table').on('change', '[type="text"]', function() {
        $('#content-editable-table').on('change', '.tbl_input', function () {
            vm.updateTableJSON();
        });

        $('#content-editable-table').on('click', '.ibtnDel', function () {
            $(this).closest('tr').remove();
        });

        if (vm.isChecked) {
            var input = this.$refs.Checkbox;
            var e = document.createEvent('HTMLEvents');
            e.initEvent('change', true, true);

            /* replacing input.disabled with onclick because disabled checkbox does NOT get posted with form on submit */
            if (vm.readonly) {
                vm.isClickable = 'return false;';
            } else {
                vm.isClickable = 'return true;';
            }
            input.dispatchEvent(e);
        }

        $('#id_arrival_date').keypress(function (event) {
            event.preventDefault();
        });

        this.$nextTick(() => {
            vm.filteredRows.forEach((row, row_idx) => {
                // Initialise select2 for each row
                vm.initialiseRowSelect2(row, row_idx);
            });
        });
    },

    updated() {},
    methods: {
        total_price: function () {
            let vm = this;
            var total = 0.0;
            for (var key in vm.table.tbody) {
                total += isNaN(parseFloat(vm.table.tbody[key][vm.idx_price]))
                    ? 0.0
                    : parseFloat(vm.table.tbody[key][vm.idx_price]);
            }
            return total.toFixed(2);
        },

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

            return yyyy + '-' + mm + '-' + dd;
        },
        reset_row: function () {
            var init_row = [];
            var length = this.col_headers.length + 3; // adding 3, for 3 same_tour_group values for number of adults, children and free_of_charge
            for (var i = 0; i < length; i++) {
                init_row.push(i == 2 ? false : '');
            }
            return init_row;
        },
        reset_row_part: function (row) {
            // reset part of the row (from date onwards)
            for (var i = 1; i < row.length; i++) {
                row[i] = '';
            }
            return row;
        },

        reset_row_checkbox: function (row) {
            // reset part of the row (checkbox only)
            row[this.idx_same_group_tour] = '';
            return row;
        },
        updateTableJSON: function () {
            let vm = this;
            vm.tableJSON = JSON.stringify(vm.table);
            vm.localValue = vm.tableJSON;
        },
        addRow: function () {
            let vm = this;
            var newRow = [];
            // var length = vm.table.thead.length + 3; // adding 3, for 3 same_tour_group values for number of adults, children and free_of_charge

            for (var i = 0; i < vm.table.thead.length; i++) {
                newRow.push('');
            }
            newRow[vm.idx_same_group_tour] = false;

            vm.table.tbody.push(newRow);
            vm.same_tour_group_checkbox.push({
                disabled: true,
                checked: false,
            });

            vm.updateTableJSON();
            this.$nextTick(() => {
                vm.initialiseRowSelect2(newRow, vm.table.tbody.length - 1);
            });
        },
        deleteRow: function (row, row_idx) {
            let vm = this;

            // pop row from data structure by row index
            vm.table.tbody = vm.table.tbody.filter((_, idx) => idx != row_idx);
            vm.updateTableJSON();

            /* need to recalc table prices, because same_tour group calc may have changed for one or more rows */
            vm.update_arrival_dates();
            vm.same_tour_group_checkbox.splice(row_idx, 1);
            vm.calcPrice(row, row_idx, -1); // dummy col_idx=-1
        },

        adult_price: function (row) {
            const options = this.options_by_row(row);
            return row[this.idx_park] ? options.prices.adult : '';
        },
        child_price: function (row) {
            const options = this.options_by_row(row);
            return row[this.idx_park] ? options.prices.child : '';
        },
        // eslint-disable-next-line no-unused-vars
        tooltip_same_group_tour: function (row, row_idx) {
            let vm = this;
            var selected_arrival = row[vm.idx_arrival_date];
            var selected_region_name = row[vm.idx_park]?.region_name;

            if ([undefined, null, ''].includes(selected_region_name) === true) {
                return '';
            }
            return (
                'Tick if this is for the same tour group as the booking for region ' +
                selected_region_name +
                ' for ' +
                selected_arrival +
                '.'
            );
        },
        disable_same_tour_group_checkbox: function (row, row_idx) {
            let vm = this;
            if (
                !(row && (row[vm.idx_park] == '' || row[vm.idx_park] == null))
            ) {
                var selected_arrival = row[vm.idx_arrival_date];
                var selected_region_id = row[vm.idx_park].region_id;
                if (selected_arrival == '' || selected_region_id == '') {
                    return true;
                }
                var arrival_dates = [];
                var region_id;
                vm.get_region_arrival_map(row, row_idx);

                for (var i = 0; i < vm.region_arrival_map.length; i++) {
                    region_id = vm.region_arrival_map[i].region_id;
                    if (region_id == selected_region_id) {
                        arrival_dates = vm.region_arrival_map[i].arrival_dates;
                        if (arrival_dates.indexOf(selected_arrival) > -1) {
                            console.log('False');
                            return false;
                        }
                    }
                }
            }
            console.log('True');
            return true;
        },
        // eslint-disable-next-line no-unused-vars
        calcPrice: function (row, row_idx, col_idx) {
            
            let vm = this;

            var total_adults_same_group = 0;
            var total_children_same_group = 0;
            var total_adults_same_group_prev = 0;
            var total_children_same_group_prev = 0;
            var no_adults = 0;
            var no_children = 0;
            var selected_adults = 0;
            var selected_children = 0;
            var adult_price = 0;
            var child_price = 0;

            var selected_arrival_date = row[vm.idx_arrival_date];

            if (selected_arrival_date !== '') {
                for (var i = 0; i < vm.regions.length; i++) {
                    for (var j = 0; j < vm.arrival_dates.length; j++) {
                        total_adults_same_group = 0;
                        total_children_same_group = 0;
                        total_adults_same_group_prev = 0;
                        total_children_same_group_prev = 0;
                        var count = 0;
                        for (var k = 0; k < vm.table.tbody.length; k++) {
                            // k is the row index
                            var region_id = vm.regions[i];
                            var arrival = vm.arrival_dates[j];
                            row = vm.table.tbody[k];
                            var same_tour_group_checked =
                                row[vm.idx_same_group_tour];

                            const options = vm.options_by_row(row);
                            const park_region_id = options.region_id;
                            if (
                                region_id == park_region_id &&
                                arrival == row[vm.idx_arrival_date]
                            ) {
                                console.log(row)
                                selected_adults = isNaN(parseInt(row[vm.idx_adult]))? 0: parseInt(row[vm.idx_adult]);
                                selected_children = isNaN(parseInt(row[vm.idx_child]))? 0: parseInt(row[vm.idx_child]);

                                console.log(selected_adults,selected_children)

                                if (same_tour_group_checked) {
                                    if (count == 0) {
                                        /* Previous Sessions - total no_adults and children, excluding those from the same tour group, previously already paid for */
                                        [
                                            total_adults_same_group,
                                            total_children_same_group,
                                        ] = vm.get_visitors_same_tour(
                                            arrival,
                                            region_id
                                        );
                                    } else {
                                        /* Current Sessions - total no_adults and children, from the last known row */
                                        total_adults_same_group =
                                            total_adults_same_group_prev;
                                        total_children_same_group =
                                            total_children_same_group_prev;
                                    }
                                    no_adults = Math.max(
                                        selected_adults -
                                            total_adults_same_group,
                                        0
                                    );
                                    no_children = Math.max(
                                        selected_children -
                                            total_children_same_group,
                                        0
                                    );
                                } else {
                                    no_adults = selected_adults;
                                    no_children = selected_children;
                                }

                                adult_price =
                                    no_adults == 0
                                        ? 0.0
                                        : no_adults * vm.adult_price(row);
                                child_price =
                                    no_children == 0
                                        ? 0.0
                                        : no_children * vm.child_price(row);

                                vm.net_park_prices[k] = (
                                    adult_price + child_price
                                ).toFixed(2);
                                vm.table.tbody[k][vm.idx_price] = (
                                    adult_price + child_price
                                ).toFixed(2);
                                vm.updateTableJSON();

                                if (same_tour_group_checked) {
                                    vm.table.tbody[k][vm.idx_adult_same_tour] =
                                        no_adults.toString();
                                    vm.table.tbody[k][vm.idx_child_same_tour] =
                                        no_children.toString();
                                } else {
                                    vm.table.tbody[k][vm.idx_adult_same_tour] =
                                        '';
                                    vm.table.tbody[k][vm.idx_child_same_tour] =
                                        '';
                                }
                                total_adults_same_group_prev = Math.max(
                                    selected_adults,
                                    total_adults_same_group
                                );
                                total_children_same_group_prev = Math.max(
                                    selected_children,
                                    total_children_same_group
                                );
                                count += 1;
                            }
                        }
                    }
                }

                // Get a list of the number of visitors for each category for the current row (as string values)
                const visitors = $(`.row-${row_idx}-input`)
                    .map(function () {
                        return $(this).val();
                    })
                    .get();
                // The total number of visitors
                const totalVisitors = _.sum(visitors.map(Number));
                if (totalVisitors == 0) {
                    if (
                        visitors.every(function (element) {
                            return String(element).length > 0;
                        })
                    ) {
                        // Cannot have _all_ visitors to be zero, even though 0 is a valid number in the input field
                        $(`.row-${row_idx}-input`).each(function () {
                            this.setCustomValidity(
                                'The numbers must not be all zero!'
                            );
                            this.reportValidity();
                        });
                    }
                    $(`.row-${row_idx}-input`).prop('required', true);
                } else {
                    // If at least one category of visitors is greater than zero, then any other category can be zero and doesn't need to be required anymore
                    $(`.row-${row_idx}-input`).each(function () {
                        if (Number($(this).val()) > 0) {
                            this.setCustomValidity('');
                            $(this).prop('required', true);
                        } else {
                            this.setCustomValidity('');
                            $(this).prop('required', false);
                        }
                    });
                }
            }
        },

        find_region_idx2: function (region_id) {
            let vm = this;
            for (var i = 0; i < vm.region_arrival_map.length; i++) {
                if (region_id == vm.region_arrival_map[i].region_id) {
                    return i;
                }
            }
            return -1;
        },

        find_arrival_idx2: function (array_list, arrival) {
            for (var i = 0; i < array_list.length; i++) {
                if (arrival == array_list[i]) {
                    return i;
                }
            }
            return -1;
        },

        get_nrows: function (arrival, region_id) {
            /* from current session */
            let vm = this;
            var row_region_id;
            var row_arrival_date;
            var count = 0;
            for (var i = 0; i < vm.table.tbody.length; i++) {
                row_region_id = vm.table.tbody[i][vm.idx_park].region_id;
                row_arrival_date = vm.table.tbody[i][vm.idx_arrival_date];
                if (region_id == row_region_id && arrival == row_arrival_date) {
                    count += 1;
                }
            }
            return count;
        },

        get_region_arrival_map: function (row, row_idx) {
            /* lookup map to allow 'same_tour group' checkbox to be enabled/disabled. Enabled if region_id/arrival_date combination exists in map */
            let vm = this;
            var region_id;
            var arrival_dates;
            var arrival_date;
            var idx;

            vm.region_arrival_map = [];
            /* from prior sessions */
            for (let i = 0; i < vm.options.length; i++) {
                region_id = vm.options[i].region_id;
                // I added empty list as fallback in case max_group_arrival_by_date is not defined in options
                arrival_dates = Object.keys(
                    vm.options[i].max_group_arrival_by_date || {}
                );
                idx = vm.find_region_idx2(region_id);
                if (!(idx > -1)) {
                    vm.region_arrival_map.push({
                        region_id: region_id,
                        arrival_dates: arrival_dates,
                    });
                } else {
                    vm.region_arrival_map[idx].arrival_dates =
                        vm.region_arrival_map[idx].arrival_dates.concat(
                            arrival_dates
                        );
                }
            }

            /* from current session */
            for (let i = 0; i < vm.table.tbody.length; i++) {
                if (i != row_idx) {
                    region_id = vm.table.tbody[i][0].region_id;
                    arrival_date = vm.table.tbody[i][1];
                    idx = vm.find_region_idx2(region_id);
                    if (!(idx > -1)) {
                        vm.region_arrival_map.push({
                            region_id: region_id,
                            arrival_dates: [arrival_date],
                        });
                    } else {
                        vm.region_arrival_map[idx].arrival_dates =
                            vm.region_arrival_map[idx].arrival_dates.concat([
                                arrival_date,
                            ]);
                    }
                }
            }

            /* make arrival_dates unique and sort */
            for (let i = 0; i < vm.region_arrival_map.length; i++) {
                vm.region_arrival_map[i].arrival_dates = [
                    ...new Set(vm.region_arrival_map[i].arrival_dates),
                ].sort();
            }
        },

        get_regions: function () {
            let vm = this;
            var regions = [];
            var region_id;
            for (var i = 0, length = vm.options.length; i < length; i++) {
                region_id = vm.options[i].region_id;
                if (!(regions.indexOf(region_id) > -1)) {
                    regions.push(region_id);
                }
            }
            return regions.sort();
        },

        get_arrival_dates: function () {
            let vm = this;
            var arrival_dates = [];
            var keys = [];
            var arrival = '';
            for (var i = 0; i < vm.options.length; i++) {
                // I added empty list as fallback in case max_group_arrival_by_date is not defined in options
                keys = Object.keys(
                    vm.options[i].max_group_arrival_by_date || {}
                );
                for (var j = 0; j < keys.length; j++) {
                    arrival = keys[j];
                    if (!(arrival_dates.indexOf(arrival) > -1)) {
                        arrival_dates.push(arrival);
                    }
                }
            }
            return arrival_dates.sort();
        },

        update_arrival_dates: function (selected_date = '') {
            /* updates vm.arrival_dates list with current arrival dates from the table
               (initial update to vm.arrival_dates occured 
            */
            let vm = this;

            for (var i = 0; i < vm.table.tbody.length; i++) {
                selected_date = selected_date
                    ? selected_date
                    : vm.table.tbody[i][1];
                if (
                    selected_date.length &&
                    !(vm.arrival_dates.indexOf(selected_date) > -1)
                ) {
                    vm.arrival_dates.push(selected_date);
                }
            }
            console.log('arrival_dates: ' + vm.arrival_dates);
        },

        park_change: function (selected_park, row, row_idx) {
            let vm = this;
            var selected_date = row[vm.idx_arrival_date];

            if ([null, undefined].includes(row[vm.idx_park]) === false) {
                // eslint-disable-next-line no-unused-vars
                var selected_region_id = row[vm.idx_park].region_id;
            }

            if ([null, undefined, ''].includes(selected_park) === true) {
                // reset the row
                vm.table.tbody[row_idx] = vm.reset_row();
            }
            vm.updateTableJSON();

            /* need to recalc table prices, because same_tour group calc may have changed for one or more rows */
            vm.update_arrival_dates();
            vm.calcPrice(row, row_idx, vm.idx_park);
            if (selected_date) {
                var is_disabled = vm.disable_same_tour_group_checkbox(
                    row,
                    row_idx
                );
                if (is_disabled) {
                    vm.same_tour_group_checkbox[row_idx].checked = false;
                    vm.table.tbody[row_idx] = vm.reset_row_checkbox(row);
                }
                vm.same_tour_group_checkbox[row_idx].disabled = is_disabled;
            }
        },
        
        tour_group_change: function (row, row_idx) {
            let vm = this;   
            console.log(vm.table.tbody[row_idx], row)         
            vm.table.tbody[row_idx] = row;
            vm.updateTableJSON();
            vm.calcPrice(row, row_idx);
        },

        date_change: function (selected_date, row, row_idx) {
            let vm = this;

            if ([null, undefined, ''].includes(selected_date) === true) {
                // reset part of the row (date onwards)
                vm.table.tbody[row_idx] = vm.reset_row_part(row);
            }
            vm.updateTableJSON();

            /* need to recalc table prices, because same_tour group calc may have changed for one or more rows */
            vm.update_arrival_dates(selected_date);
            vm.calcPrice(row, row_idx, vm.idx_arrival_date);

            var is_disabled = vm.disable_same_tour_group_checkbox(row, row_idx);
            if (is_disabled) {
                vm.same_tour_group_checkbox[row_idx].checked = false;
                vm.table.tbody[row_idx] = vm.reset_row_checkbox(row);
            }
            vm.same_tour_group_checkbox[row_idx].disabled = is_disabled;
        },

        get_visitors_same_tour: function (arrival, region_id) {
            let vm = this;

            for (var i = 0; i < vm.max_group_arrival.length; i++) {
                if (arrival == vm.max_group_arrival[i].arrival) {
                    for (
                        var j = 0;
                        j < vm.max_group_arrival[i].region.length;
                        j++
                    ) {
                        if (
                            region_id ==
                            vm.max_group_arrival[i].region[j].region_id
                        ) {
                            return [
                                vm.max_group_arrival[i].region[j].total_adults,
                                vm.max_group_arrival[i].region[j]
                                    .total_children,
                            ];
                        }
                    }
                }
            }
            return [0, 0];
        },

        find_arrival_idx: function (arrival) {
            let vm = this;

            for (var i = 0; i < vm.max_group_arrival.length; i++) {
                if (arrival == vm.max_group_arrival[i].arrival) {
                    return i;
                }
            }
            return -1;
        },
        find_region_idx: function (arrival, region_id) {
            let vm = this;

            var idx = vm.find_arrival_idx(arrival);
            if (idx > -1) {
                for (
                    var j = 0;
                    j < vm.max_group_arrival[idx].region.length;
                    j++
                ) {
                    if (
                        region_id ==
                        vm.max_group_arrival[idx].region[j].region_id
                    ) {
                        return j;
                    }
                }
            }
            return -1;
        },
        __update_visitors_same_group_tour: function (
            arrival,
            region_id,
            total_adults,
            total_children
        ) {
            /*
                Checks if a park in this region has been previously booked on the same arrival date, if so pay for only excess adults and children
            */
            let vm = this;

            var idx1 = vm.find_arrival_idx(arrival);
            var idx2 = vm.find_region_idx(arrival, region_id);
            if (idx1 > -1 && idx2 > -1) {
                if (
                    region_id ==
                    vm.max_group_arrival[idx1]['region'][idx2]['region_id']
                ) {
                    vm.max_group_arrival[idx1]['arrival'] = arrival;

                    if (
                        total_adults >
                        vm.max_group_arrival[idx1]['region'][idx2][
                            'total_adults'
                        ]
                    ) {
                        vm.max_group_arrival[idx1]['region'][idx2][
                            'total_adults'
                        ] = total_adults;
                    }

                    if (
                        total_children >
                        vm.max_group_arrival[idx1]['region'][idx2][
                            'total_children'
                        ]
                    ) {
                        vm.max_group_arrival[idx1]['region'][idx2][
                            'total_children'
                        ] = total_children;
                    }
                }
            } else if (idx1 > -1) {
                vm.max_group_arrival[idx1]['region'].push({
                    region_id: region_id,
                    total_adults: total_adults,
                    total_children: total_children,
                });
            } else if (idx2 > -1) {
                vm.max_group_arrival.push({
                    arrival: arrival,
                    region: [
                        {
                            region_id: region_id,
                            total_adults: total_adults,
                            total_children: total_children,
                        },
                    ],
                });
            }
        },
        add_previous_visitors_same_group_tour: function () {
            /*
                Checks if a park in this region has been previously booked on the same arrival date, if so add it to the max_group_arrival dict
            */
            let vm = this;
            var arrival_dates = [];
            var arrival = '';
            var region_id = '';
            // eslint-disable-next-line no-unused-vars
            var key = '';
            var total_adults = 0;
            var total_children = 0;

            for (var i = 0; i < vm.options.length; i++) {
                // I added empty list as fallback in case max_group_arrival_by_date is not defined in options
                arrival_dates = Object.keys(
                    vm.options[i].max_group_arrival_by_date || {}
                );
                region_id = vm.options[i].region_id;
                for (var j = 0; j < arrival_dates.length; j++) {
                    arrival = arrival_dates[j];
                    total_adults =
                        vm.options[i].max_group_arrival_by_date[arrival]
                            .total_adults;
                    total_children =
                        vm.options[i].max_group_arrival_by_date[arrival]
                            .total_children;
                    vm.max_group_arrival.push({
                        arrival: arrival,
                        region: [
                            {
                                region_id: region_id,
                                total_adults: total_adults,
                                total_children: total_children,
                            },
                        ],
                    });
                }
            }
        },
        /**
         * Get the options object by park id for a specific row
         * @param row A row of the table
         */
        options_by_row: function (row) {
            const park_id = row[this.idx_park];
            return this.options.find((option) => option.value == park_id);
        },
        /**
         * Get the same tour group checkbox for a specific row
         * @param row_idx The index of the row
         */
        get_same_tour_group_checkbox: function (row_idx) {
            const checkbox = this.same_tour_group_checkbox[row_idx];
            if (!checkbox) {
                console.error(
                    `Checkbox not found for row index ${row_idx}. Please check the data structure.`
                );
                // Default to unchecked and disabled
                return { checked: false, disabled: true };
            }
            return checkbox;
        },
        initialiseRowSelect2: function (row, row_idx) {
            const vm = this;
            row.forEach((_, idx) => {
                helpers.initialiseSelect2
                    .bind(this)(
                        `select_order_table_park-${row_idx}-${idx}`, // select id
                        'select_order_table_park_parent', // parent id
                        vm.table.tbody[row_idx][0], // selected value (v-model)
                        'Select a park', // placeholder
                        true, // allow clear
                        0, // minimum input length
                        '', // unselect value
                        '15rem' // width
                    )
                    .on('select2:select', function (e) {
                        const data = e.params.data.id;
                        const tbody = [...vm.table.tbody];
                        tbody[row_idx][idx] = data;
                        vm.table.tbody = tbody;
                        // Trigger change event to update the model being selected
                        vm.$refs[
                            `select_order_table_park-${row_idx}-${idx}`
                        ][0].dispatchEvent(
                            new Event('change', { target: e.target })
                        );
                    })
                    .on('select2:unselect', function (e) {
                        vm.table.tbody[row_idx][idx] = '';
                        // Trigger change event to update the model being unselected
                        vm.$refs[
                            `select_order_table_park-${row_idx}-${idx}`
                        ][0].dispatchEvent(
                            new Event('change', { target: e.target })
                        );
                    });
            });
        },
    },
};
</script>

<style scoped lang="css">
.container {
    padding: 30px;
    width: 100%;
}

.editable-table input[type='number'] {
    width: 90px;
}

.editable-table input[type='total'] {
    width: 100px;
}

.output {
    white-space: normal;
}

input[id='header'] {
    outline-style: none;
}

div.currencyinput {
    position: relative;
    padding-left: 15px;
}

div.currencyinput:after {
    position: absolute;
    left: 6px;
    top: 2px;
    content: '$';
}
.select_order_table_park_parent {
    display: block;
}
</style>
<!-- Having this rule non-scoped to ensure it takes precedence -->
<style lang="css">
.select2-container--bootstrap-5
    .select2-selection--single
    .select2-selection__rendered {
    display: inline-block;
    padding: 0px 0px 0px 8px !important;
    word-wrap: break-word;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    height: 35px;
    width: calc(90%);
    position: sticky;
}
</style>
