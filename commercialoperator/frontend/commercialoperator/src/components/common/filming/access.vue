<template lang="html">
<div class="row" id="accessInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Access Requirements <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#accessInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <ParkTable :url="parks_url" :proposal="proposal"  ref="parks_table"></ParkTable>
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">List all parks, terrestrial and/or marine ...</label>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div>
                </div>
            </div>                

        </div>
    </div>

</div>
</template>

<script>
import ParkTable from './parks_table.vue'
    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            }
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                values:null,
                parks_url: '/api/proposal_filming_parks.json'
            }
        },
        components:{
            ParkTable
        },
        methods:{
        }
    }
</script>

<style lang="css" scoped>
</style>

