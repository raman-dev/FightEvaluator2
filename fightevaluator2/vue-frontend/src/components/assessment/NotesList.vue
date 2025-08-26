<script setup>

const notes = defineModel('notes');

</script>

<template>
    <ul>
        <template v-for="note in notes">
            <li>
                {{ note.data }}
            </li>
        </template>
    </ul>
</template>