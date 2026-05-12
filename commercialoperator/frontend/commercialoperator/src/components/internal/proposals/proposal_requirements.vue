<template id="proposal_requirements">
    <div class="col-md-12">
        <div class="row">
                <FormSection
                    :form-collapse="false"
                    label="Requirements"
                    index="requirements"
                    subtitle=""
                >
                    <form
                        class="form-horizontal"
                        action="index.html"
                        method="post"
                    >
                        <div class="col-sm-12">
                            <div
                                v-if="
                                    proposal.application_type ==
                                    application_type_filming
                                "
                                class="row mb-1"
                            >
                                <small
                                    ><br />Only add requirements that are
                                    additional to the general conditions in the
                                    Commercial Filming Handbook
                                    <a
                                        :href="commercial_filming_handbook"
                                        target="_blank"
                                        >here</a
                                    >. Please ensure each condition added
                                    references a specific park or district and
                                    is written in a format consistent with the
                                    handbook.</small
                                >
                            </div>
                            <div class="row">
                                <div class="col-sm-12">
                                    <button
                                        v-if="
                                            hasAssessorMode ||
                                            hasReferralMode ||
                                            hasDistrictAssessorMode
                                        "
                                        class="btn btn-primary mb-3 float-end"
                                        @click.prevent="addRequirement()"
                                    >
                                        Add Requirement
                                    </button>
                                </div>
                            </div>
                        </div>
                        <datatable
                            :id="datatableId"
                            ref="requirements_datatable"
                            :dt-options="requirement_options"
                            :dt-headers="requirement_headers"
                        />
                    </form>
                </FormSection>
        </div>
        <RequirementDetail
            ref="requirement_detail"
            :proposal_id="proposal.id"
            :requirements="requirements"
            :has-referral-mode="hasReferralMode"
            :referral_group="referral_group"
            :has-district-assessor-mode="hasDistrictAssessorMode"
            :district_proposal="district_proposal"
            :district="district"
        />
    </div>
</template>
<script>
import { api_endpoints, constants, helpers } from '@/utils/hooks';
import datatable from '@vue-utils/datatable.vue';
import RequirementDetail from './proposal_add_requirement.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import '@/../../../static/commercialoperator/css/extra.css';
import { v4 as uuid } from 'uuid';
import _ from 'lodash';
import $ from 'jquery'
export default {
    name: 'InternalProposalRequirements',
    components: {
        datatable,
        RequirementDetail,
        FormSection,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        hasReferralMode: {
            type: Boolean,
            default: false,
        },
        hasDistrictAssessorMode: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        referral_group: {
            type: Number,
            default: null,
        },
        // eslint-disable-next-line vue/prop-name-casing
        district_proposal: {
            type: Number,
            default: null,
        },
        district: {
            type: Number,
            default: null,
        },
    },
    data: function () {
        let vm = this;
        return {
            global_settings: [],
            panelBody: 'proposal-requirements-' + uuid(),
            requirements: [],
            requirement_headers: [
                '',
                'Requirement',
                'Due Date',
                'Recurrence',
                'Action',
                'Order',
                'Documents',
            ],
            requirement_options: {
                autoWidth: false,
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    {
                        responsivePriority: 2,
                        targets: 5, // Order column
                    },
                    {
                        responsivePriority: 3,
                        targets: 4, // Action column
                    },
                ],
                responsive: true,
                ajax: {
                    url: helpers.add_endpoint_json(
                        api_endpoints.proposals,
                        vm.proposal.id + '/requirements'
                    ),
                    dataSrc: '',
                },
                order: [6, 'asc'],
                dom: constants.DATATABLE_DOM_HTML,
                buttons: [
                    {
                        extend: 'excelHtml5',
                        text: 'Excel',
                        className: 'btn btn-primary me-2 rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                    {
                        extend: 'csvHtml5',
                        text: 'CSV',
                        className: 'btn btn-primary rounded',
                        exportOptions: {
                            orthogonal: 'export',
                        },
                    },
                ],
                columns: [
                    {
                        data: 'id',
                        className: 'dtr-control',
                        orderable: false,
                        targets: 0,
                        render: function () {
                            return '';
                        },
                    },
                    {
                        data: 'requirement',
                        //orderable: false,
                        render: function (value, type) {
                            const result = helpers.addEllipsis(
                                value,
                                'Requirement'
                            );

                            return type == 'export' ? value : result;
                        },
                    },
                    {
                        data: 'due_date',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            return data != '' && data != null
                                ? moment(data).format('DD/MM/YYYY')
                                : '';
                        },
                        orderable: false,
                    },
                    {
                        data: 'recurrence',
                        mRender: function (data, type, full) {
                            if (full.recurrence) {
                                switch (full.recurrence_pattern) {
                                    case 1:
                                        return `Once per ${full.recurrence_schedule} week(s)`;
                                    case 2:
                                        return `Once per ${full.recurrence_schedule} month(s)`;
                                    case 3:
                                        return `Once per ${full.recurrence_schedule} year(s)`;
                                    default:
                                        return '';
                                }
                            }
                            return '';
                        },
                        orderable: false,
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (vm.proposal.assessor_mode.has_assessor_mode) {
                                if (full.copied_from == null) {
                                    links += `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                }
                                links += `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                            } else if (
                                vm.hasReferralMode &&
                                full.can_referral_edit
                            ) {
                                if (full.copied_from == null) {
                                    links += `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                }
                                links += `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                            } else {
                                if (
                                    vm.hasDistrictAssessorMode &&
                                    full.can_district_assessor_edit
                                ) {
                                    if (full.copied_from == null) {
                                        links += `<a href='#' class="editRequirement" data-id="${full.id}">Edit</a><br/>`;
                                    }
                                    links += `<a href='#' class="deleteRequirement" data-id="${full.id}">Delete</a><br/>`;
                                }
                            }
                            return links;
                        },
                        orderable: false,
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';
                            if (vm.proposal.assessor_mode.has_assessor_mode) {
                                links += `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fas fa-angle-up fa-2x"></i></a><br/>`;
                                links += `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fas fa-angle-down fa-2x"></i></a><br/>`;
                            } else {
                                if (
                                    vm.hasReferralMode &&
                                    full.can_referral_edit
                                ) {
                                    links += `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fas fa-angle-up fa-2x"></i></a><br/>`;
                                    links += `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fas fa-angle-down fa-2x"></i></a><br/>`;
                                } else if (
                                    vm.hasDistrictAssessorMode &&
                                    full.can_district_assessor_edit
                                ) {
                                    links += `<a class="dtMoveUp" data-id="${full.id}" href='#'><i class="fas fa-angle-up fa-2x"></i></a><br/>`;
                                    links += `<a class="dtMoveDown" data-id="${full.id}" href='#'><i class="fas fa-angle-down fa-2x"></i></a><br/>`;
                                }
                            }
                            return links;
                        },
                        orderable: false,
                    },
                    {
                        data: 'requirement_documents',
                        // eslint-disable-next-line no-unused-vars
                        mRender: function (data, type, full) {
                            let links = '';
                            _.forEach(data, function (doc) {
                                links +=
                                    '<a href="' +
                                    doc._file +
                                    '" target="_blank"><p>' +
                                    doc.name +
                                    '</p></a><br>';
                            });
                            return links;
                        },
                    },
                ],
                processing: true,
                // eslint-disable-next-line no-unused-vars
                rowCallback: function (row, data, index) {
                    if (
                        data.copied_for_renewal &&
                        data.require_due_date &&
                        !data.due_date
                    ) {
                        $('td', row).css('background-color', 'Red');
                        vm.setApplicationWorkflowState(false);
                        //vm.$emit('refreshRequirements',false);
                    }
                },
                drawCallback: function () {
                    $(vm.$refs.requirements_datatable.table)
                        .find('tr:last .dtMoveDown')
                        .remove();
                    $(vm.$refs.requirements_datatable.table)
                        .children('tbody')
                        .find('tr:first .dtMoveUp')
                        .remove();

                    // Remove previous binding before adding it
                    $('.dtMoveUp').unbind('click');
                    $('.dtMoveDown').unbind('click');

                    // Bind clicks to functions
                    $('.dtMoveUp').click(vm.moveUp);
                    $('.dtMoveDown').click(vm.moveDown);
                },
                preDrawCallback: function () {
                    vm.setApplicationWorkflowState(true);
                },
            },
        };
    },
    computed: {
        hasAssessorMode() {
            return this.proposal.assessor_mode.has_assessor_mode;
        },
        commercial_filming_handbook: function () {
            let vm = this;
            if (vm.global_settings) {
                for (var i = 0; i < vm.global_settings.length; i++) {
                    if (
                        vm.global_settings[i].key ==
                        'commercial_filming_handbook'
                    ) {
                        return vm.global_settings[i].value;
                    }
                }
            }
            return '';
        },
        application_type_tclass: function () {
            return api_endpoints.t_class;
        },
        application_type_filming: function () {
            return api_endpoints.filming;
        },
        application_type_event: function () {
            return api_endpoints.event;
        },
        datatableId: function () {
            return 'requirements-datatable-' + uuid();
        },
    },
    watch: {
        hasAssessorMode() {
            // reload the table
            this.updatedRequirements();
        },
    },
    mounted: function () {
        let vm = this;
        this.fetchRequirements();
        vm.fetchGlobalSettings();
        vm.$nextTick(() => {
            this.eventListeners();
            const table = this.$refs.requirements_datatable.vmDataTable;
            helpers.addEllipsisEventListeners(table);
        });
    },
    methods: {
        fetchGlobalSettings: function () {
            let vm = this;
            helpers.fetchUrl('/api/global_settings.json').then(
                (response) => {
                    vm.global_settings = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        addRequirement() {
            this.$refs.requirement_detail.requirement.referral_group =
                this.referral_group;
            this.$refs.requirement_detail.requirement.district_proposal =
                this.district_proposal;
            this.$refs.requirement_detail.requirement.district = this.district;
            this.$refs.requirement_detail.isModalOpen = true;
        },
        removeRequirement(_id) {
            let vm = this;
            swal.fire({
                title: 'Remove Requirement',
                text: 'Are you sure you want to remove this requirement?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Remove Requirement',
                confirmButtonColor: '#d9534f',
            }).then(
                (result) => {
                    if (!result.isConfirmed) {
                        return;
                    }
                    helpers
                        .fetchUrl(
                            helpers.add_endpoint_json(
                                api_endpoints.proposal_requirements,
                                _id + '/discard'
                            )
                        )
                        .then(
                            () => {
                                vm.$refs.requirements_datatable.vmDataTable.ajax.reload();
                            },
                            (error) => {
                                console.log(error);
                            }
                        );
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        fetchRequirements() {
            let vm = this;

            helpers.fetchUrl(api_endpoints.proposal_standard_requirements).then(
                (response) => {
                    vm.requirements = response;
                },
                (error) => {
                    console.log(error);
                }
            );
        },
        editRequirement(_id) {
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_requirements,
                        _id
                    )
                )
                .then(
                    (response) => {
                        this.$refs.requirement_detail.requirement = response;
                        this.$refs.requirement_detail.requirement.due_date =
                            response.due_date != null &&
                            response.due_date != undefined
                                ? moment(response.due_date).format('YYYY-MM-DD')
                                : '';
                        this.$refs.requirement_detail.requirement.referral_group =
                            response.referral_group;
                        this.$refs.requirement_detail.requirement.district_proposal =
                            response.district_proposal;
                        this.$refs.requirement_detail.requirement.district =
                            response.district;
                        this.$refs.requirement_detail.requirement.requirement_documents =
                            response.requirement_documents;
                        response.standard
                            ? $(
                                  this.$refs.requirement_detail.$refs
                                      .standard_req
                              )
                                  .val(response.standard_requirement)
                                  .trigger('change')
                            : '';
                        this.addRequirement();
                    },
                    (error) => {
                        console.log(error);
                    }
                );
        },
        updatedRequirements() {
            this.$refs.requirements_datatable.vmDataTable.ajax.reload();
        },
        eventListeners() {
            let vm = this;
            vm.$refs.requirements_datatable.vmDataTable.on(
                'click',
                '.deleteRequirement',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-id');
                    vm.removeRequirement(id);
                }
            );
            vm.$refs.requirements_datatable.vmDataTable.on(
                'click',
                '.editRequirement',
                function (e) {
                    e.preventDefault();
                    var id = $(this).attr('data-id');
                    vm.editRequirement(id);
                }
            );
        },
        sendDirection(req, direction) {
            let movement = direction == 'down' ? 'move_down' : 'move_up';
            helpers
                .fetchUrl(
                    helpers.add_endpoint_json(
                        api_endpoints.proposal_requirements,
                        req + '/' + movement
                    )
                )
                .then(
                    () => {},
                    (error) => {
                        console.log(error);
                    }
                );
        },
        moveUp(e) {
            // Move the row up
            let vm = this;
            e.preventDefault();
            var tr = $(e.target).parents('tr');
            vm.moveRow(tr, 'up');
            vm.sendDirection($(e.target).parent().data('id'), 'up');
        },
        moveDown(e) {
            // Move the row down
            e.preventDefault();
            let vm = this;
            var tr = $(e.target).parents('tr');
            vm.moveRow(tr, 'down');
            vm.sendDirection($(e.target).parent().data('id'), 'down');
        },
        moveRow(row, direction) {
            // Move up or down (depending...)
            var table = this.$refs.requirements_datatable.vmDataTable;
            // NOTE: It seems like the row.index is not the same as the position of the row in the table, e.g. row indexes may be [2, 0, 1] but the position, obviously, is 0, 1, 2
            // NOTE: I changed the logic here to first map row index to table position and to then swap the table positions of the two rows
            var index = table.row(row).index();

            // Get the indexes of the rows in the table
            const rowIndexes = table.rows().indexes();
            // The index of the row in the table
            const rowTablePosition = rowIndexes.indexOf(index);

            var order = -1;
            if (direction === 'down') {
                order = 1;
            }

            let targetIndex;
            rowIndexes.toArray().forEach((value, i) => {
                if (i === rowTablePosition + order) {
                    targetIndex = value;
                }
            });

            if (targetIndex === undefined) {
                console.warn('No target index found for row movement');
                return; // No target index found, do nothing
            }

            var data1 = table.row(index).data();
            data1.order += order;

            var data2 = table.row(targetIndex).data();
            data2.order += -order;

            table.row(index).data(data2);
            table.row(targetIndex).data(data1);

            table.draw('page');
        },
        setApplicationWorkflowState(bool) {
            let vm = this;
            vm.$emit('refreshRequirements', bool);
        },
        handleClick: function (value) {
            console.log('clicked', value);
        },
    },
};
</script>
<style scoped>
.dataTables_wrapper .dt-buttons {
    float: right;
}
</style>
