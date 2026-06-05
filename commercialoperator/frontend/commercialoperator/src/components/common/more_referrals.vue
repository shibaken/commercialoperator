<template id="more-referrals">
    <div>
        <a
            v-if="!isFinalised"
            ref="showRef"
            class="actionBtn top-buffer-s"
            @click.prevent=""
            >Show Referrals</a
        >
    </div>
</template>

<script>
import { v4 as uuid } from 'uuid';
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import _ from 'lodash';
import $ from 'jquery'
export default {
    name: 'MoreReferrals',
    props: {
        isFinalised: {
            type: Boolean,
            required: true,
        },
        canAction: {
            type: Boolean,
            required: true,
        },
        proposal: {
            type: Object,
            required: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        referral_url: {
            type: String,
            default: null,
        },
    },
    data() {
        let vm = this;
        return {
            uuid: uuid(),
            table: null,
            dateFormat: 'DD/MM/YYYY HH:mm:ss',
            datatable_url: '',
            datatable_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                responsive: true,
                deferRender: true,
                autowidth: true,
                processing: true,
                ajax: {
                    url: this.referral_url,
                    dataSrc: '',
                },
                columns: [
                    {
                        title: 'Sent On',
                        data: 'lodged_on',
                        render: function (date) {
                            return moment(date).format(vm.dateFormat);
                        },
                    },
                    {
                        title: 'Referral',
                        data: 'referral',
                        // eslint-disable-next-line no-unused-vars
                        render: function (data, type, full) {
                            return `<span>${data}</span>`;
                        },
                    },
                    {
                        title: 'Status',
                        data: 'referral_status',
                    },
                    {
                        title: 'Action',
                        data: 'id',
                        render: function (data, type, full) {
                            var result = '';
                            if (!vm.canAction) {
                                return result;
                            }
                            var user = full.referral;
                            if (full.referral_status == 'Awaiting') {
                                result = `<a href="" data-id="${data}" data-user="${user}" class="remindRef">Remind</a>/<a href="" data-id="${data}" data-user="${user}" class="recallRef">Recall</a>`;
                            } else {
                                result = `<a href="" data-id="${data}" data-user="${user}" class="resendRef">Resend</a>`;
                            }
                            return result;
                        },
                    },
                    {
                        title: 'Referral Comments',
                        data: 'referral_text',

                        render: function (value) {
                            var ellipsis = '...',
                                truncated = _.truncate(value, {
                                    length: 20,
                                    omission: ellipsis,
                                    separator: ' ',
                                }),
                                result = '<span>' + truncated + '</span>',
                                popTemplate = _.template(
                                    '<a href="javascript://" ' +
                                        'role="button" ' +
                                        'data-bs-toggle="popover" ' +
                                        'data-trigger="click" ' +
                                        'data-placement="top auto"' +
                                        'data-html="true" ' +
                                        'data-bs-content="<%= text %>" ' +
                                        '>more</a>'
                                );
                            if (_.endsWith(truncated, ellipsis)) {
                                result += popTemplate({
                                    text: value,
                                });
                            }

                            return result;
                        },
                    },
                    {
                        title: 'Attached Document',
                        data: 'document',
                        render: function (data, type, full) {
                            var result = '';
                            if (
                                Array.isArray(full.document) &&
                                full.document.length
                            ) {
                                // if array exists and is not empty
                                var filename = full.document[0];
                                var file_url = full.document[1];
                                result = `<a href="${file_url}" data-id="${filename}" target="_blank">${filename}</a>`;
                            }
                            return result;
                        },
                    },
                ],
            },
        };
    },
    computed: {},
    mounted() {
        this.$nextTick(() => {
            this.initialiseTable();
        });
    },
    methods: {
        remindReferral: function (_id, user) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        _id + '/remind'
                    )
                )
                .then(
                    (response) => {
                        vm.$emit('refreshFromResponse', response);
                        vm.table.ajax.reload();
                        swal.fire({
                            title: 'Referral Reminder',
                            text: 'A reminder has been sent to ' + user,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        resendReferral: function (_id, user) {
            let vm = this;
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        _id + '/resend'
                    )
                )
                .then(
                    (response) => {
                        vm.$emit('refreshFromResponse', response);
                        vm.table.ajax.reload();
                        swal.fire({
                            title: 'Referral Resent',
                            text: 'The referral has been resent to ' + user,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        recallReferral: function (_id, user) {
            let vm = this;

            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.referrals,
                        _id + '/recall'
                    )
                )
                .then(
                    (response) => {
                        vm.$emit('refreshFromResponse', response);
                        vm.table.ajax.reload();
                        swal.fire({
                            title: 'Referral Recall',
                            text: 'The referral has been recalled from ' + user,
                            icon: 'success',
                        });
                    },
                    (error) => {
                        swal.fire({
                            title: 'Application Error',
                            text: helpers.apiVueResourceError(error),
                            icon: 'error',
                        });
                    }
                );
        },
        initialiseTable: function () {
            // To allow table elements (ref: https://getbootstrap.com/docs/5.1/getting-started/javascript/#sanitizer)
            var myDefaultAllowList = bootstrap.Tooltip.Default.allowList;
            myDefaultAllowList.table = [];

            let vm = this;
            let table_id = 'more-referrals-table' + vm.uuid;
            let popover_name = 'popover-' + vm.uuid + '-referrals';
            let popover_elem = $(vm.$refs.showRef)[0];
            if (!popover_elem) {
                console.info('More referral popover element not found');
                return;
            }
            let my_content =
                '<table id="' +
                table_id +
                '" class="hover table table-striped table-bordered dt-responsive" cellspacing="0" width="100%"></table>';
            let my_template =
                '<div class="popover ' +
                popover_name +
                '" role="tooltip"><div class="popover-arrow" style="top:110px;"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>';
            new bootstrap.Popover(popover_elem, {
                sanitize: false,
                html: true,
                content: my_content,
                template: my_template,
                title: 'Referrals',
                container: 'body',
                placement: 'auto',
                trigger: 'click',
            });

            popover_elem.addEventListener('inserted.bs.popover', function () {
                vm.table = $('#' + table_id).DataTable(vm.datatable_options);

                // activate popover when table is drawn.
                vm.table
                    .on('draw', function () {
                        var popoverTriggerList = [].slice.call(
                            document.querySelectorAll(
                                '#' + table_id + ' [data-bs-toggle="popover"]'
                            )
                        );
                        // eslint-disable-next-line no-unused-vars
                        var popoverList = popoverTriggerList.map(
                            function (popoverTriggerEl) {
                                return new bootstrap.Popover(popoverTriggerEl);
                            }
                        );
                    })
                    .on('click', '.resendRef', function (e) {
                        e.preventDefault();
                        var _id = $(this).data('id');
                        var user = $(this).data('user');
                        vm.resendReferral(_id, user);
                    })
                    .on('click', '.recallRef', function (e) {
                        e.preventDefault();
                        var _id = $(this).data('id');
                        var user = $(this).data('user');
                        vm.recallReferral(_id, user);
                    })
                    .on('click', '.remindRef', function (e) {
                        e.preventDefault();
                        var _id = $(this).data('id');
                        var user = $(this).data('user');
                        vm.remindReferral(_id, user);
                    });
            });
            // .on('shown.bs.popover', function () {
            popover_elem.addEventListener('shown.bs.popover', function () {
                var el = vm.$refs.showRef;
                // eslint-disable-next-line no-unused-vars
                var popoverheight = parseInt($('.' + popover_name).height());

                var popover_bounding_top = parseInt(
                    $('.' + popover_name)[0].getBoundingClientRect().top
                );
                // eslint-disable-next-line no-unused-vars
                var popover_bounding_bottom = parseInt(
                    $('.' + popover_name)[0].getBoundingClientRect().bottom
                );

                var el_bounding_top = parseInt(
                    $(el)[0].getBoundingClientRect().top
                );
                // eslint-disable-next-line no-unused-vars
                var el_bounding_bottom = parseInt(
                    $(el)[0].getBoundingClientRect().top
                );

                var diff = el_bounding_top - popover_bounding_top;

                // eslint-disable-next-line no-unused-vars
                var position = parseInt($('.' + popover_name).position().top);
                // eslint-disable-next-line no-unused-vars
                var pos2 = parseInt($(el).position().top) - 5;

                var x = diff + 5;
                $('.' + popover_name)
                    .children('.arrow')
                    .css('top', x + 'px');
            });
        },
    },
};
</script>

<style scoped>
.top-buffer-s {
    margin-top: 10px;
}
.actionBtn {
    cursor: pointer;
}
</style>
