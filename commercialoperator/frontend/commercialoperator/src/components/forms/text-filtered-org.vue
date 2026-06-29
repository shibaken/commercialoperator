<template lang="html">
    <div>
        <div class="form-group">
            <label v-if="label" :id="org_id" for="label" class="inline">{{
                label
            }}</label>
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

            <template v-if="readonly">
                <input
                    :readonly="readonly"
                    :type="type"
                    class="form-control"
                    :name="name"
                    :value="value"
                    :required="isRequired"
                />
            </template>
            <template v-else>
                <v-select
                    label="name"
                    name="name"
                    :filterable="false"
                    :options="options"
                    placeholder="Start typing to search for an organisation"
                    @search="onSearch"
                >
                    <template #no-options
                        >Search for name, trading name or ABN</template
                    >
                    <template #option="option = { option }">
                        <div class="d-center">
                            {{ option.name }}
                            <span v-if="option.trading_name">
                                ({{ option.trading_name }})
                            </span>
                        </div>
                    </template>

                    <template #selected-option="option = { option }">
                        <div class="selected d-center" :org_id="option.org_id">
                            <input
                                type="hidden"
                                class="form-control"
                                :name="name + '-selected'"
                                :value="option.org_id"
                            />
                            <input
                                type="hidden"
                                class="form-control"
                                :name="name + '-selected-ledger'"
                                :value="option.organisation_id || option.id"
                            />
                            <span>
                                {{ option.name }}
                                <span v-if="option.trading_name">
                                    ({{ option.trading_name }})
                                </span>
                            </span>
                        </div>
                    </template>
                </v-select>
            </template>
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

import { helpers } from '@/utils/hooks';
import _ from 'lodash';

export default {
    // components: { Comment, HelpText, HelpTextUrl, VueSelect },
    components: { Comment, HelpText, HelpTextUrl },
    props: [
        // eslint-disable-next-line vue/require-prop-types
        'url',
        // eslint-disable-next-line vue/require-prop-types
        'type',
        // eslint-disable-next-line vue/require-prop-types
        'name',
        // eslint-disable-next-line vue/require-prop-types
        'id',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'comment_value',
        // eslint-disable-next-line vue/require-prop-types
        'value',
        // eslint-disable-next-line vue/require-prop-types
        'isRequired',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_assessor',
        // eslint-disable-next-line vue/require-prop-types
        'assessorMode',
        // eslint-disable-next-line vue/require-prop-types
        'label',
        // eslint-disable-next-line vue/require-prop-types
        'readonly',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'assessor_readonly',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_url',
        // eslint-disable-next-line vue/prop-name-casing, vue/require-prop-types
        'help_text_assessor_url',
    ],
    data() {
        return {
            showingComment: false,
            options: [],
            fullname: null,
        };
    },
    methods: {
        toggleComment() {
            this.showingComment = !this.showingComment;
        },
        onSearch(search, loading) {
            loading(true);
            this.search(loading, search, this);
        },
        search: _.debounce((loading, search, vm) => {
            helpers
                .fetchUrl(vm.url + escape(search), {
                    emulateJSON: true,
                })
                .then((res) => {
                    vm.options = res;
                    loading(false);
                });
        }, 350),
    },
};
</script>

<style lang="css">
@import 'vue-select/dist/vue-select.css';

input {
    box-shadow: none;
}

.v-select {
    color: #147688;
    background-color: white;
    border-color: #91ddec;
}
</style>
