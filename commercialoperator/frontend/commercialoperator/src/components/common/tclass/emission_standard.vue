<template lang="html" :id="id">
<div>
    <div class="row">
                <fieldset class="scheduler-border">
                    <legend class="scheduler-border">{{emission_standard.emission_standard_type_value}}</legend>
                    <div class="form-group">
                        <!-- <div class="row">
                            <div class="col-sm-3">
                                <label class="control-label pull-right"  for="Name">Expiry Date</label>
                            </div>
                            <div class="col-sm-9">
                                <div class="input-group date" ref="emission_standard_expiry" style="width: 70%;">
                                    <input type="text" class="form-control" v-model="emission_standard.emission_standard_expiry" name="emission_standard_expiry" placeholder="DD/MM/YYYY" :disabled="readonly">
                                    <span class="input-group-addon">
                                        <i class="fas fa-calendar-days"></i>
                                    </span>
                                </div>
                            </div>
                        </div> -->
                        <div class="row">
                            <div class="col-sm-3">
                                <label class="control-label pull-right"  for="Name">Attach documents</label>
                            </div>
                            <div class="col-sm-9">
                                <FileField :proposal_id="proposal_id" :isRepeatable="false" :name="'emission_standard'+emission_standard.emission_standard_type" :id="'emission_standard'+emission_standard.emission_standard_type+proposal_id" :readonly="!canEditActivities" ref="emission_standard_file"></FileField>
                            </div>
                        </div>
                        <div  class="row">
                            <div class="col-sm-3">
                                <label class="control-label pull-right"  for="Name">Details</label>
                            </div>
                            <div class="col-sm-9">
                                <div class="" ref="emission_comments" style="width: 70%;">
                                    <textarea class="form-control" v-model="emission_standard.emission_comments" name="emission_standard_comments" :disabled="readonly"></textarea>        
                                </div>
                            </div>
                        </div>
                    </div>
                </fieldset>
            </div>  
</div>
</template>

<script>
import FileField from '@/components/forms/filefield.vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'

export default {
    name:"emission_standard",
    props:{
        proposal_id: null,
        emission_standard: {
                type: Object,
                required:true
            },
        id:String,
        assessor_readonly: Boolean,
        assessorMode:{
            default:function(){
                return false;
            }
        },
        value:{
            default:function () {
                return null;
            }
        },
        readonly:Boolean,
        canEditActivities:{
              type: Boolean,
              default: true
            }
    },
    components: {
        FileField,
    },
    data:function(){
        return {
            repeat:1,
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
        }
    },

    computed: {
        // typeOther: function(){
        //     return this.accreditation && this.accreditation.accreditation_type=='other' ? true: false;
        // }
    },

    methods:{
        eventListeners:function (){
            let vm=this;
                // $(vm.$refs.accreditation_expiry).datetimepicker(vm.datepickerOptions);
                // $(vm.$refs.accreditation_expiry).on('dp.change', function(e){
                //     if ($(vm.$refs.accreditation_expiry).data('DateTimePicker').date()) {
                //         vm.accreditation.accreditation_expiry =  e.date.format('DD/MM/YYYY');
                //     }
                //     else if ($(vm.$refs.accreditation_expiry).data('date') === "") {
                //         vm.accreditation.accreditation_expiry = null;
                //     }
                //  });
        },
    },
    mounted:function () {
        let vm = this;
        this.$nextTick(()=>{
                vm.eventListeners();
            });
    }
}

</script>

<style lang="css">
    fieldset.scheduler-border {
        border: 1px groove #ddd !important;
        padding: 0 1.4em 1.4em 1.4em !important;
        margin: 0 0 1.5em 0 !important;
        -webkit-box-shadow:  0px 0px 0px 0px #000;
                box-shadow:  0px 0px 0px 0px #000;
    }
    legend.scheduler-border {
        width:inherit; /* Or auto */
        padding:0 10px; /* To give a bit of padding on the left and right */
        border-bottom:none;
    }
</style>
