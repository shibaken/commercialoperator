<template id="district_proposal_table">
    <div class="row">
        <div class="col-sm-12">
                <FormSection
                    :form-collapse="false"
                    label="District Applications"
                    index="district_applications"
                    subtitle=""
                >
                    <div class="row">
                        <div class="col-lg-12" style="margin-top: 25px">
                            <datatable
                                :id="datatable_id"
                                ref="district_proposal_datatable"
                                :dt-options="district_proposal_options"
                                :dt-headers="district_proposal_headers"
                            />
                        </div>
                    </div>
                </FormSection>
        </div>
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue';
import FormSection from '@/components/forms/section_toggle.vue';
import { constants } from '@/utils/hooks';
import { v4 as uuid } from 'uuid';

export default {
    name: 'FilmingDistrictProposalTableDash',
    components: {
        datatable,
        FormSection,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        url: {
            type: String,
            required: true,
        },
    },
    data() {
        let vm = this;
        return {
            pBody: 'pBody' + uuid(),
            datatable_id: 'district-proposal-datatable-' + uuid(),

            district_proposal_headers: [
                'District',
                'Status',
                'Assigned Officer',
                'Action',
            ],
            district_proposal_options: {
                language: {
                    processing: constants.DATATABLE_PROCESSING_HTML,
                },
                columnDefs: [
                    { responsivePriority: 1, targets: 0 },
                    {
                        responsivePriority: 2,
                        targets: -1,
                    },
                ],
                responsive: true,
                ajax: {
                    url: vm.url,
                    dataSrc: '',
                },
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
                        data: 'district_name',
                    },
                    {
                        data: 'processing_status',
                    },
                    {
                        data: 'assigned_officer',
                    },
                    {
                        data: 'id',
                        mRender: function (data, type, full) {
                            let links = '';

                            links += full.district_assessor_can_assess
                                ? `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>Process</a><br/>`
                                : `<a href='/internal/proposal/${full.proposal}/district_proposal/${full.id}'>View</a><br/>`;

                            return links;
                        },
                        // name: ''
                    },
                ],
                processing: true,
            },
        };
    },
    computed: {
        is_external: function () {
            return this.level == 'external';
        },
    },
    watch: {},
    mounted: function () {
        let vm = this;
        vm.fetchFilterLists();
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
        });
    },
    methods: {
        fetchFilterLists: function () {},
        addEventListeners: function () {},
        refreshFromResponse: function () {
            this.$refs.district_proposal_datatable.vmDataTable.ajax.reload();
        },
        initialiseSearch: function () {},
    },
};
</script>
<style scoped></style>
