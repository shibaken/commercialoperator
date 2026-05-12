<template lang="html">
    <div>
        <div class="col-sm-12">
            <div v-if="has_uploaded_docs" class="form-group">
                <div class="row">
                    <div class="col-sm-6">
                        <label class="control-label pull-left" for="Name"
                            >Uploaded Documents</label
                        >
                    </div>
                    <div class="col-sm-6">
                        <div
                            ref="due_date"
                            class="input-group date"
                            style="width: 70%"
                        >
                            <div
                                v-for="v in uploaded_documents"
                                :key="v.name"
                                class="row"
                            >
                                <span>
                                    <a :href="v._file" target="_blank">{{
                                        v.name
                                    }}</a>
                                    &nbsp;
                                    <a
                                        class="fas fa-trash"
                                        title="Remove file"
                                        :filename="v.name"
                                        style="cursor: pointer; color: red"
                                        @click="delete_document(v)"
                                    ></a>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-sm-12">
                        <div v-for="n in repeat" :key="n">
                            <div
                                v-if="
                                    isRepeatable ||
                                    (!isRepeatable && num_documents() == 0)
                                "
                            >
                                <span class="btn btn-link btn-file">
                                    <input
                                        :name="name"
                                        type="file"
                                        class="form-control"
                                        :data-que="n"
                                        :accept="fileTypes"
                                        :required="isRequired"
                                        @change="handleChange($event)"
                                    />
                                    <u>Attach Document</u>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <div class="row">
                    <div class="col-sm-9">
                        <div v-if="files">
                            <div v-for="v in files" :key="v.name">
                                <p>
                                    File:{{ v.name }} &nbsp;
                                    <a
                                        class="fas fa-trash"
                                        title="Remove file"
                                        :filename="v.name"
                                        style="cursor: pointer; color: red"
                                        @click="pop_file(v)"
                                    ></a>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <span v-if="show_spinner"
                ><i class="fas fa-2x fa-spinner fa-spin"></i
            ></span>
        </div>
    </div>
</template>

<script>
import { helpers } from '@/utils/hooks';
import $ from 'jquery'
export default {
    name: 'FileField2',
    components: {},
    props: {
        proposal_id: null,
        required_doc_id: null,
        name: String,
        label: String,
        id: String,
        isRequired: String,
        value: {
            default: function () {
                return null;
            },
        },
        fileTypes: {
            default: function () {
                var file_types =
                    'image/*,' +
                    'video/*,' +
                    'audio/*,' +
                    'application/pdf,text/csv,application/msword,application/vnd.ms-excel,application/x-msaccess,' +
                    'application/x-7z-compressed,application/x-bzip,application/x-bzip2,application/zip,' +
                    '.dbf,.gdb,.gpx,.prj,.shp,.shx,' +
                    '.json,.kml,.gpx';
                return file_types;
            },
        },
        isRepeatable: Boolean,
        readonly: Boolean,
        delete_url: String,
        uploaded_documents: Array,
    },
    data: function () {
        return {
            repeat: 1,
            files: [],
            // eslint-disable-next-line vue/no-reserved-keys
            _files: [
                {
                    file: null,
                    name: '',
                },
            ],
            showingComment: false,
            show_spinner: false,
            documents: [],
            filename: null,
        };
    },
    computed: {
        csrf_token: function () {
            return helpers.getCookie('csrftoken');
        },
        has_uploaded_docs: function () {
            return this.uploaded_documents ? true : false;
        },
    },
    mounted: function () {},

    methods: {
        reset_files() {
            this.files = [];
        },
        toggleComment() {
            this.showingComment = !this.showingComment;
        },
        handleChange: function (e) {
            let vm = this;
            if (vm.isRepeatable) {
                let el = $(e.target).attr('data-que');
                let avail = $('input[name=' + e.target.name + ']');

                avail = [
                    ...avail.map((id) => {
                        return $(avail[id]).attr('data-que');
                    }),
                ];
                avail.pop();
                if (vm.repeat == 1) {
                    vm.repeat += 1;
                } else {
                    if (avail.indexOf(el) < 0) {
                        vm.repeat += 1;
                    }
                }
                $(e.target).css({ display: 'none' });
                $(e.target.parentElement).css({ display: 'none' }); //to hide <span> element btn-link
            } else {
                vm.files = [];
            }
            vm.add_file(e);
        },
        add_file(e) {
            let vm = this;
            var file_updated = false;
            for (var idx in vm.files) {
                for (var key in vm.files[idx]) {
                    var name = vm.files[idx][key];
                    if (name == e.target.files[0].name) {
                        // replace the file with new one with same name
                        vm.files[idx]['file'] = e.target.files[0];
                        file_updated = true;
                    }
                }
            }

            if (!file_updated) {
                vm.files.push({
                    name: e.target.files[0].name,
                    file: e.target.files[0],
                });
            }
        },
        pop_file(v) {
            /* pops file from the local files array - client side (before it has been saved to the server) */
            let vm = this;
            for (var idx in vm.files) {
                for (var key in vm.files[idx]) {
                    var name = vm.files[idx][key];
                    if (name == v.name) {
                        // Remove the file from the array
                        vm.files.splice(idx, 1);
                        return;
                    }
                }
            }

            // Adding these variables here just in case. This part has likely been copied from elsewhere. Don't know what it is supposed to do.
            let file_updated, e;
            if (!file_updated) {
                vm.files.push({
                    name: e.target.files[0].name,
                    file: e.target.files[0],
                });
            }
        },
        delete_document: function (file) {
            /* deletes, previously saved file, from the server */
            let vm = this;
            vm.show_spinner = true;
            var data = { id: file.id, name: file.name };

            swal.fire({
                title: 'Delete Document',
                text: 'Are you sure you want to delete this document?',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Delete Document',
                confirmButtonColor: '#d9534f',
            }).then(
                (swalresult) => {
                    if (swalresult.isConfirmed) {
                        helpers.fetchUrl(vm.delete_url, {
                            method: 'POST',
                            body: JSON.stringify(data),
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        })
                        .then(
                            (response) => {
                                vm.uploaded_documents = response;
                                vm.$emit('refreshFromResponse', response);
                                vm.show_spinner = false;
                            },
                            (err) => {
                                console.log(err);
                            }
                        );
                    }
                },
            );
        },
        num_documents: function () {
            let vm = this;
            if (vm.documents) {
                return vm.documents.length;
            }
            return 0;
        },
    },
};
</script>

<style lang="css">
input {
    box-shadow: none;
}
.btn-file {
    position: relative;
    overflow: hidden;
}
.btn-file input[type='file'] {
    position: absolute;
    top: 0;
    right: 0;
    min-width: 100%;
    min-height: 100%;
    font-size: 100px;
    text-align: right;
    filter: alpha(opacity=0);
    opacity: 0;
    outline: none;
    background: white;
    cursor: inherit;
    display: block;
}
</style>
