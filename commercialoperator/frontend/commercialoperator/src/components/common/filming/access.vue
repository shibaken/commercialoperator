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
                            <div class="">
                                
                                <div class="col-sm-12">
                                    <label class="control-label pull-left"  for="Name">List all parks, terrestrial and/or marine ...</label>
                                    <ParkTable :url="parks_url" :proposal="proposal"  ref="parks_table"></ParkTable>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                        </div> 
                    </div>

                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you intend to use the Munda Bidi or Bibbulmun Track?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.track_use" :value="true" data-parsley-required :disabled="proposal.readonly" name="track_use"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.track_use" :value="false" data-parsley-required :disabled="proposal.readonly" name="track_use"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you intend to conduct any off-road/ track driving/ walking?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.off_road" :value="true" data-parsley-required :disabled="proposal.readonly" name="off_road"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.off_road" :value="false" data-parsley-required :disabled="proposal.readonly" name="off_road"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.off_road" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Details (when/ where/ how long)</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="off_road_details" placeholder="" v-model="proposal.filming_access.off_road_details"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you require roads or car packs to be closed during filming?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.road_closure" :value="true" data-parsley-required :disabled="proposal.readonly" name="road_closure"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.road_closure" :value="false" data-parsley-required :disabled="proposal.readonly" name="road_closure"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.road_closure" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Details</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="road_closure_details" placeholder="" v-model="proposal.filming_access.road_closure_details"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div  class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Number of people in filming party</label>
                                    
                                </div>
                                <div class="col-sm-6" style="margin-bottom: 5px">
                                      <input type="text" class="form-control" name="no_of_people" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_access.no_of_people">   
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Do you intend to camp on CALM Land?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.camp_on_land" :value="true" data-parsley-required :disabled="proposal.readonly" name="camp_on_land"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.camp_on_land" :value="false" data-parsley-required :disabled="proposal.readonly" name="camp_on_land"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.camp_on_land" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Where?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.camp_location"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Will you need assistance from Department staff? <small> (Supervision fees may apply)</small> </label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_assistance" :value="true" data-parsley-required :disabled="proposal.readonly" name="staff_assistance"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_assistance" :value="false" data-parsley-required :disabled="proposal.readonly" name="staff_assistance"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.staff_assistance" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    In what capacity and for how long?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.assistance_staff_capacity"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Will you need Department staff to Film? <small> (Supervision fees may apply)</small> </label>
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_to_film" :value="true" data-parsley-required :disabled="proposal.readonly" name="staff_to_film"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.staff_to_film" :value="false" data-parsley-required :disabled="proposal.readonly" name="staff_to_film"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.staff_to_film" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    In what capacity and for how long?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.film_staff_capacity"></textarea>    
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">Will you be featuring Aboriginal people/ items/ area of cultural significance?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.cultural_significance" :value="true" data-parsley-required :disabled="proposal.readonly" name="cultural_significance"/>
                                            Yes
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_access.cultural_significance" :value="false" data-parsley-required :disabled="proposal.readonly" name="cultural_significance"/>
                                            No
                                        </li>
                                    </ul>      
                                </div>
                            </div>
                            <!-- <div class="row">&nbsp;</div> -->
                            <div v-if="proposal.filming_access.cultural_significance" class="">
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    Where?</label>
                                    
                                </div>
                                <div class="col-sm-6">
                                      <textarea :disabled="readonly" class="form-control" name="camp_location" placeholder="" v-model="proposal.filming_access.cultural_significance_details"></textarea>    
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

</div>
</template>

<script>
import ParkTable from './parks_table.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
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
                parks_url: helpers.add_endpoint_json(api_endpoints.proposals,vm.$route.params.proposal_id+'/filming_parks'),
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
.borderDecoration {
    border: 1px solid;
    border-radius: 5px;
    padding: 5px;
    margin-top: 5px;
}
</style>

