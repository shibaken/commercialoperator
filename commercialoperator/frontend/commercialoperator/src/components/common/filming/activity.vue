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
                                    <div class="input-group date" ref="completion_date" style="width: 70%;">
                                        <input type="text" class="form-control" v-model="proposal.filming_activity.completion_date" name="completion_date" placeholder="Completion date" :disabled="proposal.readonly || proposal.pending_amendment_request || proposal.is_amendment_proposal">
                                        <span class="input-group-addon">
                                            <span class="glyphicon glyphicon-calendar"></span>
                                        </span>
                                    </div>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Title of film/ name of program/ name of product</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <input type="text" class="form-control" name="Activity title" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_activity.activity_title">
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Previous contact person in the Department</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <input type="text" class="form-control" name="Previous contact Person" placeholder="" :disabled="proposal.readonly" v-model="proposal.filming_activity.previous_contact_person">
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Type of film to be undertaken</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <ul class="list-inline"  >
                                        <li v-for="f in film_type_choices" class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Checkbox" type="checkbox" @click="selectFilmType($event, f)" v-model="proposal.filming_activity.film_type" :value="f.key" data-parsley-required :disabled="proposal.readonly" />
                                            {{ f.value }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Purpose of still or motion film</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <ul class="list-inline"  >
                                        <li v-for="p in purpose_choices" class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Checkbox_purpose" type="checkbox" @click="selectFilmType($event, p)" v-model="proposal.filming_activity.film_purpose" :value="p.key" data-parsley-required :disabled="proposal.readonly"/>
                                            {{ p.value }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="row" v-if="proposal.filming_activity.film_purpose=='other'">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Details</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <textarea class="form-control" v-model="proposal.filming_activity.film_purpose_details" :disabled="proposal.readonly" style="width: 80%"></textarea>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Does the film have Tourism WA sponsorship</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <ul class="list-inline"  >
                                        <li v-for="s in sponsorship_choices" class="form-check list-inline-item">
                                            <input  class="form-check-input" ref="Radio" type="radio" @click="selectFilmType($event, s)" v-model="proposal.filming_activity.sponsorship" :value="s.key" data-parsley-required :disabled="proposal.readonly" name="sponsorship"/>
                                            {{ s.value }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">How will the still or motion film be used or shown</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <ul class="list-inline"  >
                                        <li v-for="u in film_usage_choices" class="form-check list-inline-item border-0">
                                            <input  class="form-check-input" ref="Checkbox" type="checkbox" @click="selectFilmType($event, u)" v-model="proposal.filming_activity.film_usage" :value="u.key" data-parsley-required :disabled="proposal.readonly" />
                                            {{ u.value }}
                                        </li>
                                    </ul>
                                </div>
                            </div>
                            <div class="row">&nbsp;</div>
                            <div class="row">
                                <div class="col-sm-3">
                                    <label class="control-label pull-left"  for="Name">Description of production</label>
                                </div>
                                <div class="col-sm-9" style="margin-bottom: 5px">
                                    <textarea class="form-control" v-model="proposal.filming_activity.production_description" :disabled="proposal.readonly" style="width: 80%"></textarea>
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
                values:null,
                film_type_choices:[],
                sponsorship_choices:[],
                film_usage_choices:[],
                purpose_choices:[],
                datepickerOptions:{
                    format: 'DD/MM/YYYY',
                    showClear:true,
                    useCurrent:false,
                    keepInvalid:true,
                    allowInputToggle:true,
                },
            }
        },
        methods:{
            fetchActivityTabData: function(){
                let vm = this;
                vm.$http.get('/api/filming_activity_tab').then((response) => {
                    console.log(response.body);
                    vm.film_type_choices=response.body.film_type_choices;
                    vm.sponsorship_choices= response.body.sponsorship_choices;
                    vm.film_usage_choices=response.body.film_usage_choices;
                    vm.purpose_choices=response.body.purpose_choices;
                },(error) => {
                    console.log(error);
                } );
            },
            selectFilmType:function(){

            },
            eventListeners:function (){
                let vm=this;

                var date= new Date()
                var today= new Date(date.getFullYear(), date.getMonth(), date.getDate());

                $(vm.$refs.commencement_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.commencement_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.commencement_date).on('dp.change', function(e){
                    if ($(vm.$refs.commencement_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.filming_activity.commencement_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.commencement_date).data('date') === "") {
                        vm.proposal.filming_activity.commencement_date = "";
                    }
                 });

                $(vm.$refs.completion_date).datetimepicker(vm.datepickerOptions);
                //Set minimum date on datetimepicker so that nominated
                //start date cannot be selected prior to today
                $(vm.$refs.completion_date).data("DateTimePicker").minDate(today);
                $(vm.$refs.completion_date).on('dp.change', function(e){
                    if ($(vm.$refs.completion_date).data('DateTimePicker').date()) {
                        

                        vm.proposal.filming_activity.completion_date =  e.date.format('DD/MM/YYYY');
                    }
                    else if ($(vm.$refs.completion_date).data('date') === "") {
                        vm.proposal.filming_activity.completion_date = "";
                    }
                 });

            },
        },
        mounted: function(){
            let vm=this;
            this.fetchActivityTabData();
            this.$nextTick(()=>{
                vm.eventListeners();
            });
        }
    }
</script>

<style lang="css" scoped>
</style>

