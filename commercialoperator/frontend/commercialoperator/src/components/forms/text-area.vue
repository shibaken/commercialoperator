<template lang="html">
    <form class="needs-validation form-horizontal" name="textAreaForm">
        <div class="form-group row">
            <div class="input-group">
                <template v-if="help_text">
                    <HelpText :help_text="help_text" />
                </template>
                <template v-if="help_text_assessor && assessorMode">
                    <HelpText
                        :help_text="help_text_assessor"
                        assessor-mode="{assessorMode}"
                        is-for-assessor="{true}"
                    />
                </template>

                <template v-if="help_text_url">
                    <HelpTextUrl :help_text_url="help_text_url" />
                </template>
                <template v-if="help_text_assessor_url && assessorMode">
                    <HelpTextUrl
                        :help_text_url="help_text_assessor_url"
                        assessor-mode="{assessorMode}"
                        is-for-assessor="{true}"
                    />
                </template>

                <template v-if="assessorMode && !assessor_readonly">
                    <template v-if="!showingComment">
                        <a
                            v-if="
                                comment_value != null &&
                                comment_value != undefined &&
                                comment_value != ''
                            "
                            href=""
                            @click.prevent="toggleComment"
                            ><i style="color: red" class="far fa-comment"
                                >&nbsp;</i
                            ></a
                        >
                        <a v-else href="" @click.prevent="toggleComment"
                            ><i class="far fa-comment">&nbsp;</i></a
                        >
                    </template>
                    <a v-else href="" @click.prevent="toggleComment"
                        ><i class="fas fa-ban">&nbsp;</i></a
                    >
                </template>
                <label
                    :id="id"
                    :for="name"
                    class="col-sm-12 control-label inline"
                    >{{ label }}</label
                >
                <div class="col-sm-12">
                    <textarea
                        :id="textAreaId"
                        v-model="localValue"
                        :readonly="readonly"
                        class="form-control"
                        rows="5"
                        :name="name"
                        :required="isRequired"
                    ></textarea>
                    <div class="invalid-feedback">
                        Please provide a response.
                    </div>
                </div>
                <br />
            </div>
            <Comment
                v-show="showingComment && assessorMode"
                :question="label"
                :readonly="assessor_readonly"
                :name="name + '-comment-field'"
                :value="comment_value"
            />
        </div>
    </form>
</template>

<script>
import Comment from './comment.vue';
import HelpText from './help_text.vue';
import HelpTextUrl from './help_text_url.vue';
import $ from 'jquery'
export default {
    components: { Comment, HelpText, HelpTextUrl },
    props: {
        name: {
            type: String,
            default: null,
        },
        value: {
            type: String,
            default: '',
        },
        id: {
            type: String,
            default: null,
        },
        isRequired: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        help_text: {
            type: String,
            default: null,
        },
        // eslint-disable-next-line vue/prop-name-casing
        help_text_assessor: {
            type: String,
            default: null,
        },
        assessorMode: {
            type: Boolean,
            default: false,
        },
        label: {
            type: String,
            default: null,
        },
        readonly: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        comment_value: {
            type: String,
            default: null,
        },
        // eslint-disable-next-line vue/prop-name-casing
        assessor_readonly: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        help_text_url: {
            type: String,
            default: null,
        },
        // eslint-disable-next-line vue/prop-name-casing
        help_text_assessor_url: {
            type: String,
            default: null,
        },
    },
    data() {
        return {
            showingComment: false,
            localValue: JSON.parse(JSON.stringify(this.value)),
        };
    },
    computed: {
        textAreaId: function () {
            return `${this.id}-text-area`;
        },
    },
    watch: {
        value: {
            handler: function (value) {
                this.localValue = value;
            },
            deep: true,
        },
    },
    methods: {
        toggleComment() {
            this.showingComment = !this.showingComment;
        },
        /**
         * Checks if the comments text field is not empty if the field is required to check for validity
         */
        isValid() {
            if (!this.isRequired) {
                return true;
            }
            const form = document.forms.textAreaForm;
            const textArea = document.getElementById(this.textAreaId);

            const isValid =
                this.isRequired &&
                [null, undefined, ''].includes(this.localValue) === false;
            console.log(`Text-area is ${isValid ? 'valid' : 'not valid'}`);

            if (!isValid) {
                form.classList.add('was-validated');
                textArea.classList.add('is-invalid');
                $(form).find(':invalid').first().focus();
                return false;
            }
            textArea.classList.remove('is-invalid');
            form.classList.remove('was-validated');

            return true;
        },
    },
};
</script>

<style lang="css">
input {
    box-shadow: none;
}
</style>
