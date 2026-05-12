<template lang="html">
    <div>
        <div class="form-group">
            <label :id="id">{{ label }}</label>

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
            <div class="input-group date">
                <input
                    type="date"
                    :readonly="readonly"
                    :name="name"
                    class="form-control"
                    max="2999-12-31"
                    placeholder="DD/MM/YYYY"
                    :value="value"
                    :required="isRequired"
                />
                <span class="input-group-text">
                    <i class="fas fa-calendar-days"></i>
                </span>
            </div>
        </div>
        <Comment
            v-show="showingComment && assessorMode"
            :question="label"
            :readonly="assessor_readonly"
            :name="name + '-comment-field'"
            :value="comment_value"
        />
    </div>
</template>

<script>
import Comment from './comment.vue';
import HelpText from './help_text.vue';
import HelpTextUrl from './help_text_url.vue';
export default {
    components: { Comment, HelpText, HelpTextUrl },
    props: [
        // eslint-disable-next-line vue/require-prop-types
        'name',
        // eslint-disable-next-line vue/require-prop-types
        'label',
        // eslint-disable-next-line vue/require-prop-types
        'id',
        // eslint-disable-next-line vue/require-prop-types
        'readonly',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_assessor',
        // eslint-disable-next-line vue/require-prop-types
        'assessorMode',
        // eslint-disable-next-line vue/require-prop-types
        'value',
        // eslint-disable-next-line vue/require-prop-types
        'conditions',
        // eslint-disable-next-line vue/require-prop-types
        'handleChange',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'comment_value',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'assessor_readonly',
        // eslint-disable-next-line vue/require-prop-types
        'isRequired',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_url',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_assessor_url',
    ],
    data() {
        return {
            showingComment: false,
        };
    },
    computed: {
        isChecked: function () {
            return false;
        },
        options: function () {
            return JSON.stringify(this.conditions);
        },
    },
    mounted: function () {},
    methods: {
        toggleComment() {
            this.showingComment = !this.showingComment;
        },
    },
};
</script>

<style lang="css">
input {
    box-shadow: none;
}
</style>
