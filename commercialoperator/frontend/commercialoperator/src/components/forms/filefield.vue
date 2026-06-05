<template lang="html">
    <div>
        <div class="form-group">
            <!-- using num_files to determine if files have been uploaded for this question/label (used in commercialoperator/frontend/commercialoperator/src/components/external/proposal.vue) -->
            <label v-if="label" :id="id" :num_files="num_documents()">{{
                label
            }}</label>
            <div v-if="files">
                <div v-for="v in documents" :key="v.name" class="col-sm-12">
                    <p>
                        File:
                        <a :href="v.file" target="_blank">{{ v.name }}</a>
                        &nbsp;
                        <span v-if="!readonly && v.can_delete">
                            <a
                                class="fas fa-trash"
                                title="Remove file"
                                :filename="v.name"
                                style="cursor: pointer; color: red"
                                @click="delete_document(v)"
                            ></a>
                        </span>
                        <span
                            v-else-if="!readonly && !v.can_delete && v.can_hide"
                        >
                            <a
                                class="fas fa-trash"
                                title="Remove file"
                                :filename="v.name"
                                style="cursor: pointer; color: blue"
                                @click="hide_document(v)"
                            ></a>
                        </span>
                        <span v-else>
                            <span v-if="!assessorMode">
                                <i
                                    class="fas fa-circle-info"
                                    aria-hidden="true"
                                    title="Previously submitted documents cannot be deleted"
                                    style="cursor: pointer"
                                ></i>
                            </span>
                        </span>
                    </p>
                </div>
            </div>
            <template v-if="!readonly">
                <div v-for="n in repeat" :key="n">
                    <div
                        v-if="
                            isRepeatable ||
                            (!isRepeatable && num_documents() == 0)
                        "
                    >
                        <span class="btn btn-link btn-file"
                            ><u>Attach Document</u>
                            <input
                                :name="name"
                                type="file"
                                class="form-control"
                                :data-que="n"
                                :accept="fileTypes"
                                :required="isRequired"
                                @change="handleChange($event)"
                        /></span>
                    </div>
                </div>
            </template>
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
    name: 'FileFieldComponent',
    components: {},
    props: {
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        proposal_id: null,
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        required_doc_id: null,
        // eslint-disable-next-line vue/require-default-prop
        name: String,
        // eslint-disable-next-line vue/require-default-prop
        label: String,
        // eslint-disable-next-line vue/require-default-prop
        id: String,
        // eslint-disable-next-line vue/require-default-prop
        isRequired: String,
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        comment_value: String,
        // eslint-disable-next-line vue/prop-name-casing
        assessor_readonly: Boolean,
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        help_text: String,
        // eslint-disable-next-line vue/prop-name-casing, vue/require-default-prop
        help_text_assessor: String,
        // eslint-disable-next-line vue/require-prop-types
        assessorMode: {
            default: function () {
                return false;
            },
        },
        // eslint-disable-next-line vue/require-prop-types
        value: {
            default: function () {
                return null;
            },
        },
        // eslint-disable-next-line vue/require-prop-types
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
        // eslint-disable-next-line vue/require-default-prop
        docsUrl: String,
    },
    data: function () {
        return {
            repeat: 1,
            files: [
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
        proposal_document_action: function () {
            return this.proposal_id
                ? `/api/proposal/${this.proposal_id}/process_document/`
                : '';
        },
    },
    mounted: function () {
        let vm = this;
        vm.documents = vm.get_documents();
        if (vm.value) {
            if (Array.isArray(vm.value)) {
                vm.value;
            } else {
                var file_names = vm.value.replace(/ /g, '_').split(',');
                vm.files = file_names.map(function (file_name) {
                    return { name: file_name };
                });
            }
        }
    },

    methods: {
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
            vm.files.push(e.target.files[0]);

            if (e.target.files.length > 0) {
                vm.save_document(e);
            }
        },
        get_documents: function () {
            let vm = this;
            vm.show_spinner = true;

            var formData = new FormData();
            formData.append('action', 'list');
            formData.append('input_name', vm.name);
            helpers
                .fetchUrl(vm.proposal_document_action, {
                    method: 'POST',
                    body: formData,
                })
                .then((res) => {
                    vm.documents = res;
                    vm.show_spinner = false;
                });
        },

        delete_document: function (file) {
            let vm = this;
            vm.show_spinner = true;

            var formData = new FormData();
            formData.append('action', 'delete');
            formData.append('document_id', file.id);

            helpers
                .fetchUrl(vm.proposal_document_action, {
                    method: 'POST',
                    body: formData,
                })
                .then(() => {
                    vm.documents = vm.get_documents();
                    vm.show_spinner = false;
                });
        },
        hide_document: function (file) {
            let vm = this;
            vm.show_spinner = true;
            var formData = new FormData();
            formData.append('action', 'hide');
            formData.append('document_id', file.id);
            formData.append('csrfmiddlewaretoken', vm.csrf_token);
            helpers
                .fetchUrl(vm.proposal_document_action, {
                    method: 'POST',
                    body: formData,
                })
                .then(() => {
                    vm.documents = vm.get_documents();
                    vm.show_spinner = false;
                });
        },

        uploadFile(e) {
            let vm = this;
            vm.show_spinner = true;
            let _file = null;

            if (e.target.files && e.target.files[0]) {
                var reader = new FileReader();
                reader.readAsDataURL(e.target.files[0]);
                reader.onload = function (e) {
                    _file = e.target.result;
                };
                _file = e.target.files[0];
            }
            return _file;
        },

        save_document: function (e) {
            let vm = this;

            var formData = new FormData();
            formData.append('action', 'save');
            formData.append('proposal_id', vm.proposal_id);
            formData.append('input_name', vm.name);
            formData.append('filename', e.target.files[0].name);
            formData.append('_file', vm.uploadFile(e));

            helpers
                .fetchUrl(vm.proposal_document_action, {
                    method: 'POST',
                    body: formData,
                })
                .then(
                    (res) => {
                        vm.documents = res;
                        vm.show_spinner = false;
                    },
                    () => {}
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
