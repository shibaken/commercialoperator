<template lang="html">
    <div>
        <Treeselect
            ref="treeselect"
            v-model="localValue"
            :model-value="localValue"
            :value="localValue"
            :options="options"
            :open-on-click="true"
            :multiple="multiple"
            :max-height="max_height"
            :value-consists-of="value_consists_of"
            :clearable="clearable"
            :flat="flat"
            :default-expand-level="default_expand_level"
            :normalizer="normalizer"
            :open-direction="open_direction"
            :disabled="disabled"
            :open-on-focus="true"
            :limit="localLimit"
            :close-on-select="closeOnSelect"
            :disable-branch-nodes="disableBranchNodes"
            :z-index="zIndex"
            @update:modelValue="localValue = $event"
        >
            <template #option-label="{ node, labelClassName }">
                <div class="row" :class="labelClassName">
                    <div class="col-sm-8 text-nowrap">
                        <!-- NOTE: NOTE: Added ? to to all instances of node.raw deal with undefined error -->
                        {{ node.raw.name }}
                    </div>
                    <!-- NOTE: NOTE: Added ? to to all instances of node.raw deal with undefined error -->
                    <div
                        v-if="node.raw.can_edit"
                        class="col-sm-4 option-label-container"
                    >
                        <!-- Note: I changed the listener from click to mousedown, because when opening the multiselect list, click would deselect/select a list option item before opening the modal -->
                        <div class="text-nowrap pull-right">
                            <a
                                v-if="is_checked(node)"
                                @mousedown.stop="edit_activities($event, node)"
                                >{{ edit_display_text(node) }}
                                <i class="fas fa-pen-to-square"></i
                            ></a>
                            <a v-else style="color: grey">
                                {{ edit_display_text(node) }}
                                <i class="fas fa-pen-to-square"></i>
                            </a>
                        </div>
                    </div>
                </div>
            </template>

            <template #value-label="{ node }">
                <div v-if="allow_edit">
                    <a
                        :disabled="!is_checked(node)"
                        :title="edit_display_text(node)"
                        @mousedown.stop="edit_activities($event, node)"
                    >
                        <!-- NOTE: Added ? to deal with undefined error -->
                        {{ node.label }}
                    </a>
                </div>
                <div v-else>
                    <!-- NOTE: Added ? to deal with undefined error -->
                    <a> {{ node.label }} </a>
                </div>
            </template>
        </Treeselect>
    </div>
</template>

<script>
import Treeselect from '@sookoll/vue-treeselect';
import '@sookoll/vue-treeselect/dist/vue3-treeselect.css';

export default {
    name: 'TreeSelect',
    components: {
        Treeselect,
    },
    props: {
        proposal: {
            type: Object,
            required: true,
        },
        modelValue: {
            type: Array,
            required: false,
            default: () => [],
        },
        // eslint-disable-next-line vue/require-default-prop
        options: {
            type: Array,
            required: false,
        },
        flat: {
            type: Boolean,
            default: false,
        },
        // eslint-disable-next-line vue/prop-name-casing
        always_open: {
            type: Boolean,
            default: true,
        },
        clearable: {
            type: Boolean,
            default: false,
        },
        multiple: {
            type: Boolean,
            default: true,
        },
        // eslint-disable-next-line vue/prop-name-casing
        max_height: {
            type: Number,
            default: 350,
        },
        // eslint-disable-next-line vue/prop-name-casing
        default_expand_level: {
            type: Number,
            default: 0,
        },
        // eslint-disable-next-line vue/prop-name-casing
        value_consists_of: {
            type: String,
            default: 'LEAF_PRIORITY', // last leaf nodes get pushed to selected_items array
        },
        // eslint-disable-next-line vue/prop-name-casing
        open_direction: {
            type: String,
            default: 'bottom',
        },
        // eslint-disable-next-line vue/prop-name-casing
        allow_edit: {
            type: Boolean,
            default: false,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        limit: {
            type: Number,
            default: Infinity,
        },
        closeOnSelect: {
            type: Boolean,
            default: false,
        },
        disableBranchNodes: {
            type: Boolean,
            default: false,
        },
        zIndex: {
            type: Number,
            default: 999,
        },
    },
    emits: ['update:modelValue'],
    data() {
        return {
            normalizer(node) {
                return {
                    id: node.last_leaf ? node.id : node.name,
                    // eslint-disable-next-line no-prototype-builtins
                    label: node.hasOwnProperty('label')
                        ? node.label
                        : node.name,
                    children: node.children,
                    isDisabled: node.is_disabled,
                };
            },
            // Note: I changed from using the prop `value` (props should not be mutated) to using a `localValue` data property
            // NOTE: I changed `value` to `modelValue` as per vue3 v-model convention
            localValue: this.modelValue,
            // Note: I changed from using the prop `limit` (props should not be mutated) to using a `localLimit` data property
            localLimit: this.limit,
        };
    },
    watch: {
        localValue: {
            handler: function (newValue) {
                this.$emit('update:modelValue', newValue);
            },
            deep: true,
        },
    },

    updated: function () {},

    mounted: function () {
        if (!this.disabled) {
            this.localLimit = 20;
        }
    },

    methods: {
        get_node_id: function (node) {
            //id: node.last_leaf ? node.id : (node.hasOwnProperty('node_id') : node.node_id ? node.name), // this is a nested if statement
            if (node.last_leaf) {
                return node.id;
                // eslint-disable-next-line no-prototype-builtins
            } else if (node.hasOwnProperty('node_id')) {
                return node.node_id;
            } else {
                return node.name;
            }
        },
        edit_display_text: function (node) {
            // NOTE: <!-- NOTE: Added ? to to all instances of node.raw deal with undefined error -->
            // eslint-disable-next-line no-prototype-builtins
            if (node.raw.hasOwnProperty('sections')) {
                return 'Edit sections and activities';
            } else {
                return 'Edit access and activities';
            }
        },
        edit_activities: function (event, node) {
            event.stopPropagation();
            // NOTE: <!-- NOTE: Added ? to to all instances of node.raw deal with undefined error -->
            // eslint-disable-next-line no-prototype-builtins
            if (node.raw.hasOwnProperty('sections')) {
                this.$parent.$parent.edit_sections(node);
                // NOTE: <!-- NOTE: Added ? to to all instances of node.raw deal with undefined error -->
                // eslint-disable-next-line no-prototype-builtins
            } else if (node.raw.hasOwnProperty('allowed_zone_activities')) {
                this.$parent.$parent.edit_activities(node);
            } else {
                this.$parent.$parent.edit_activities(node);
            }
        },
        is_checked: function (node) {
            // NOTE: Added ? to deal with undefined error
            return this.modelValue.includes(node.id);
        },
    },
};
</script>

<style lang="css" scoped>
.option-label-container {
    z-index: 999;
}
</style>
