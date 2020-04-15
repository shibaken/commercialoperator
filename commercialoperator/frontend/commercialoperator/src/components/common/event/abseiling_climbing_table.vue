<template id="abseiling_climbing_table">
    <div class="row">
        <div class="col-sm-12"> 
            <div class="row" >
                <div class="col-md-3" v-if="!proposal.readonly">
                            <!-- <button style="margin-top:25px;" class="btn btn-primary pull-right">New Application</button> -->
                            <input type="button" style="margin-top:25px;" @click.prevent="newVehicle" class="btn btn-primary" value="Add new abseiling_climbing" />
                </div>
            </div>

            <div class="row">
                <div class="col-lg-12" style="margin-top:25px;">
                    <datatable ref="abseiling_climbing_datatable" :id="datatable_id" :dtOptions="abseiling_climbing_options" :dtHeaders="abseiling_climbing_headers"/>
                </div>
            </div>
        </div>
        <!-- <editActivity ref="edit_abseiling_climbing" :abseiling_climbing_id="abseiling_climbing_id"  @refreshFromResponse="refreshFromResponse"></editActivity> -->
    </div>
</template>
<script>
import datatable from '@/utils/vue/datatable.vue'
//import editVehicle from './edit_abseiling_climbing.vue'
import {
    api_endpoints,
    helpers
}from '@/utils/hooks'
export default {
    name: 'AbseilingClimbingTableDash',
    props: {
        // level:{
        //     type: String,
        //     required: true,
        //     validator:function(val) {
        //         let options = ['internal','referral','external'];
        //         return options.indexOf(val) != -1 ? true: false;
        //     }
        // },
        proposal:{
                type: Object,
                required:true
        },
        url:{
            type: String,
            required: true
        },
    },
    data() {
        let vm = this;
        return {
            new_abseiling_climbing:{
                leader:'',
                rego_number:'',
                expiry_date:null,
                proposal: vm.proposal.id
            },
            pBody: 'pBody' + vm._uid,
            datatable_id: 'abseiling_climbing-datatable-'+vm._uid,
            // Filters for Vehicles
            external_status:[
                'Due',
                'Future',
                'Under Review',
                'Approved',
            ],
            internal_status:[
                'Due',
                'Future',
                'With Assessor',
                'Approved',
            ],
            abseiling_climbing_headers:["Leader","NOLRS registration no.","Expiry Date","Action"],
            abseiling_climbing_options:{
                language: {
                    processing: "<i class='fa fa-4x fa-spinner fa-spin'></i>"
                },
                responsive: true,
                //serverSide: true,
                //lengthMenu: [ [10, 25, 50, 100, -1], [10, 25, 50, 100, "All"] ],
                ajax: {
                    "url": vm.url,
                    "dataSrc": '',

                    // adding extra GET params for Custom filtering
                    // "data": function ( d ) {
                    //     //d.regions = vm.filterVehicleRegion.join();
                    //     d.date_from = vm.filterComplianceDueFrom != '' && vm.filterComplianceDueFrom != null ? moment(vm.filterComplianceDueFrom, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    //     d.date_to = vm.filterComplianceDueTo != '' && vm.filterComplianceDueTo != null ? moment(vm.filterComplianceDueTo, 'DD/MM/YYYY').format('YYYY-MM-DD'): '';
                    // }

                },
                dom: 'lBfrtip',
                buttons:[
                'excel', 'csv', ],
                columns: [
                    
                    {
                        data: "leader",
                        mRender:function (data,type,full) {
                            //return `C${data}`;
                            return data;
                        },
                        //name: "abseiling_climbing__region__name" // will be use like: Approval.objects.filter(abseiling_climbing__region__name='Kimberley')
                    },
                    {
                        data: "rego_number",

                        //name: "abseiling_climbing__activity",
                    },
                    {
                        data: "expiry_date",
                        //name: "abseiling_climbing__title",
                    },
                    {
                        data: '',
                        mRender:function (data,type,full) {
                            let links = '';
                            if(!vm.proposal.readonly){
                            links +=  `<a href='#${full.id}' data-edit-abseiling_climbing='${full.id}'>Edit Vehicle</a><br/>`;
                            links +=  `<a href='#${full.id}' data-discard-abseiling_climbing='${full.id}'>Discard</a><br/>`;
                        }
                        //     if (!vm.is_external){
                        //         if (full.can_user_view) {
                        //             links +=  `<a href='/internal/compliance/${full.id}'>Process</a><br/>`;
                                    
                        //         }
                        //         else {
                        //             links +=  `<a href='/internal/compliance/${full.id}'>View</a><br/>`;
                        //         }
                        //     }
                        //     else{
                        //         if (full.can_user_view) {
                        //             links +=  `<a href='/external/compliance/${full.id}'>View</a><br/>`;
                                    
                        //         }
                        //         else {
                        //             links +=  `<a href='/external/compliance/${full.id}'>Submit</a><br/>`;
                        //         }
                        //     }
                            return links;
                        },
                        // name: ''  
                    },
                    // {data: "reference", visible: false},
                    // {data: "customer_status", visible: false},
                    // {data: "can_user_view", visible: false},

                ],
                processing: true,
                /*
                initComplete: function () {
                    // Grab Regions from the data in the table
                    var regionColumn = vm.$refs.abseiling_climbing_datatable.vmDataTable.columns(1);
                    regionColumn.data().unique().sort().each( function ( d, j ) {
                        let regionTitles = [];
                        $.each(d,(index,a) => {
                            // Split region string to array
                            if (a != null){
                                $.each(a.split(','),(i,r) => {
                                    r != null && regionTitles.indexOf(r) < 0 ? regionTitles.push(r): '';
                                });
                            }
                        })
                        vm.abseiling_climbing_regions = regionTitles;
                    });
                    // Grab Activity from the data in the table
                    var titleColumn = vm.$refs.abseiling_climbing_datatable.vmDataTable.columns(2);
                    titleColumn.data().unique().sort().each( function ( d, j ) {
                        let activityTitles = [];
                        $.each(d,(index,a) => {
                            a != null && activityTitles.indexOf(a) < 0 ? activityTitles.push(a): '';
                        })
                        vm.abseiling_climbing_activityTitles = activityTitles;
                    });

                    // Grab Status from the data in the table
                    var statusColumn = vm.$refs.abseiling_climbing_datatable.vmDataTable.columns(6);
                    statusColumn.data().unique().sort().each( function ( d, j ) {
                        let statusTitles = [];
                        $.each(d,(index,a) => {
                            a != null && statusTitles.indexOf(a) < 0 ? statusTitles.push(a): '';
                        })
                        vm.status = statusTitles;
                    });
                }
                */
            }
        }
    },
    components:{
        datatable,
        //editVehicle
    },
    watch:{
    },
    computed: {
       /* status: function(){
            return this.is_external ? this.external_status : this.internal_status;
            //return [];
        }, */
        is_external: function(){
            return this.level == 'external';
        },
    },
    methods:{
        fetchFilterLists: function(){
            let vm = this;

            // vm.$http.get(api_endpoints.filter_list_compliances).then((response) => {
            //     vm.abseiling_climbing_regions = response.body.regions;
            //     vm.abseiling_climbing_activityTitles = response.body.activities;
            //     vm.status = vm.level == 'external' ? vm.external_status: vm.internal_status;
            // },(error) => {
            //     console.log(error);
            // })
            //console.log(vm.regions);
        },
        newVehicle: function(){
            let vm=this;
            this.$refs.edit_abseiling_climbing.abseiling_climbing_id = null;
            //this.$refs.edit_abseiling_climbing.fetchVehicle(id);
            var new_abseiling_climbing_another={
                access_type: null,
                capacity:'',
                rego:'',
                rego_expiry:null,
                license:'',
                proposal: vm.proposal.id
            }
            //this.$refs.edit_abseiling_climbing.abseiling_climbing=this.new_abseiling_climbing;
            this.$refs.edit_abseiling_climbing.abseiling_climbing=new_abseiling_climbing_another;
            this.$refs.edit_abseiling_climbing.abseiling_climbing_action='add'
            this.$refs.edit_abseiling_climbing.isModalOpen = true;
        },
        editVehicle: function(id){
            this.$refs.edit_abseiling_climbing.abseiling_climbing_id = id;
            this.$refs.edit_abseiling_climbing.fetchVehicle(id);
            this.$refs.edit_abseiling_climbing.isModalOpen = true;
        },
        discardVehicle:function (abseiling_climbing_id) {
            let vm = this;
            swal({
                title: "Discard Vehicle",
                text: "Are you sure you want to discard this abseiling_climbing?",
                type: "warning",
                showCancelButton: true,
                confirmButtonText: 'Discard Vehicle',
                confirmButtonColor:'#d9534f'
            }).then(() => {
                vm.$http.delete(api_endpoints.discard_abseiling_climbing(abseiling_climbing_id))
                .then((response) => {
                    swal(
                        'Discarded',
                        'Your abseiling_climbing has been discarded',
                        'success'
                    )
                    vm.$refs.abseiling_climbing_datatable.vmDataTable.ajax.reload();
                }, (error) => {
                    console.log(error);
                });
            },(error) => {

            });
        },
        addEventListeners: function(){
            let vm = this;
            vm.$refs.abseiling_climbing_datatable.vmDataTable.on('click', 'a[data-edit-abseiling_climbing]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-edit-abseiling_climbing');
                vm.editVehicle(id);
            });
            // External Discard listener
            vm.$refs.abseiling_climbing_datatable.vmDataTable.on('click', 'a[data-discard-abseiling_climbing]', function(e) {
                e.preventDefault();
                var id = $(this).attr('data-discard-abseiling_climbing');
                vm.discardVehicle(id);
            });
        },
        refreshFromResponse: function(){
            this.$refs.abseiling_climbing_datatable.vmDataTable.ajax.reload();
        },
        initialiseSearch:function(){
            
        }, 
    },
    mounted: function(){
        let vm = this;
        vm.fetchFilterLists();
        this.$nextTick(() => {
            vm.addEventListeners();
            vm.initialiseSearch();
        });
        if(vm.is_external){
            var column = vm.$refs.abseiling_climbing_datatable.vmDataTable.columns(8); //Hide 'Assigned To column for external'
            column.visible(false);
        }
        
    }
}
</script>
<style scoped>
</style>
