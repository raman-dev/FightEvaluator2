<script setup>
const props = defineProps(['event', 'fighter','label']);

</script>
<template>
    <option style="text-transform: capitalize;" :value="{event:props.event,fighter:props.fighter.id}" v-if="props.event === 'WIN'" >
        {{ props.fighter.last_name }} wins
    </option>
    <option style="text-transform: capitalize;" :value="{event:props.event,fighter:null}" v-else>
        {{ props.label }}
    </option>
</template>