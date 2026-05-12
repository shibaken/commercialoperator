<template lang="html">
    <span v-if="help_text_url">
        <template v-if="!isForAssessor">
            <a :href="help_text_url" target="_blank"
                ><i class="fas fa-circle-question" style="color: blue"
                    >&nbsp;</i
                ></a
            >
        </template>

        <template v-else-if="assessorMode">
            <a :href="help_text_url" target="_blank"
                ><i class="fas fa-circle-question" style="color: green"
                    >&nbsp;</i
                ></a
            >
        </template>
    </span>
</template>

<script>
export default {
    props: ['help_text_url', 'assessorMode', 'isForAssessor'],
};
</script>

<style lang="css"></style>
