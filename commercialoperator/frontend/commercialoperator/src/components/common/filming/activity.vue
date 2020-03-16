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
                                    <label class="control-label pull-left"  for="Name">Period of proposed filming/ photography</label>
                                </div>
                                <div class="col-sm-4">
                                    <div class="input-group date" ref="commencement_date" style="width: 70%;">
                                        <input type="text" class="form-control" v-model="proposal.filming_activity.commencement_date" name="commencement_date" placeholder="Commencement date" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                                <div class="col-sm-4">
                                    <div class="input-group date" ref="nominated_start_date" style="width: 70%;">
                                        <input type="text" class="form-control" v-model="proposal.filming_activity.commencement_date" name="commencement_date" placeholder="Commencement date" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
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
            fetchData: function(){
            let vm = this;
            vm.$http.get('/api/filming_activity_tab').then((response) => {
                console.log(response.body);
            },(error) => {
                console.log(error);
            } );
        },
        },
        mounted: function(){
            this.fetchData()
        }
    }
</script>

<style lang="css" scoped>
</style>

