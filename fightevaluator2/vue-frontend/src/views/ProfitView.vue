<script setup>
import { useMatchupStore } from '@/stores/matchupStore';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';


const route = useRoute();
const { event } = storeToRefs(useMatchupStore());

onMounted(() => {
    console.log(route);
})

</script>
<template>
    <h1>Profit, {{ event.id }}</h1>
    <table>
        <!--
            table of what?
        -->
        <thead></thead>
        <tbody>
            <!--have what here-->
        </tbody>
    </table>
</template>