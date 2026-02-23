<script setup>
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();


onMounted(() => {
    console.log('profitView.route:',route);
})

</script>
<template>
    <h1>Profit</h1>
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