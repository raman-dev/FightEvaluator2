<script>

const notes = defineModel(['notes']);

</script>

<template>
    <ul>
        <template v-for="note in notes">
            <li>
                {{ note }}
            </li>
        </template>
    </ul>
</template>