<template lang="html">
<div class="row" id="activityInfo">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Activity Details <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#activityInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    <div class="form-horizontal col-sm-12 borderDecoration">
                        
                        <div class="form-group">
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Event name</label>
                                </div>
                                <div class="col-sm-9">
                                    <!-- <input type="text" class="form-control" v-model="proposal.activities_event.event_name" name="event_name" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal"> -->
                                    <input type="text" class="form-control" name="event_name" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal">
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
                values:null
            }
        },
        methods:{
        }
    }
</script>

<style lang="css" scoped>
</style>

