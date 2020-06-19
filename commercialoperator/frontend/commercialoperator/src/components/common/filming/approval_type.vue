p<template lang="html">
<div class="row" id="approvalType">
    <div class="col-sm-12">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Approval Type <small></small>
                <a class="panelClicker" :href="'#'+lBody" data-toggle="collapse"  data-parent="#accessInfo" expanded="true" :aria-controls="lBody">
                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                </a>
                </h3>
            </div>
            <div class="panel-body collapse in" :id="lBody">
                <div class="" >                        
                    

                    <div class="form-horizontal col-sm-12">
                        
                        <div class="form-group">
                            <div class="">    
                                <div class="col-sm-6">
                                    <label class="control-label pull-left"  for="Name">
                                    This Application should result in a </label>
                                    
                                </div>
                                <div class="col-sm-6">
                                    <ul class="list-inline"  >
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_approval_type" value="lawful_authority" data-parsley-required :disabled="readonly" name="filming_approval_type"/>
                                            Lawful Authority
                                        </li>
                                        <li class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio"  v-model="proposal.filming_approval_type" value="licence" data-parsley-required :disabled="readonly" name="filming_approval_type"/>
                                            Licence
                                        </li>
                                    </ul>      
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

    export default {
        props:{
            proposal:{
                type: Object,
                required:true
            },
            hasAssessorMode:{
                type:Boolean,
                default: false
            },
        },
        data:function () {
            let vm = this;
            return{
                lBody: 'lBody'+vm._uid,
                values:null,
                selected_approval_type:'',
            }
        },
        computed:{
            readonly: function(){
                return !this.hasAssessorMode ? true : false;
            }
        },
        components:{
        },
        methods:{
        },
        mounted: function(){
            this.selected_approval_type=this.proposal.filming_approval_type;
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

