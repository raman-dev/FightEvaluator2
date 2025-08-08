<script setup>

import NavBar from './components/NavBar.vue';
import MainContent from './components/MainContent.vue';
import { RouterLink, RouterView } from 'vue-router';


const links = [
    {
        name: "home",
        path: "/v-index"
    },
    {
        name: "events",
        path: "/v-events"
    },
    {
        name: "predictions",
        path: "/v-predictions"
    },
    {
        name: "profit",
        path: "/v-profit"
    },
];

const title = 'Fight Evaluator';

</script>

<template>
    <NavBar :links="links" :nav-title="title"></NavBar>
    <!-- <MainContent></MainContent> -->

    <RouterView />
</template>

<style lang="scss">
/* use font as variable */
$backgroundColor: #212529;


html,
body {
    height: 100%;
    width: 100%;
}

#app {
    width: 100% !important;

    display: flex;
    flex-direction: column;

    padding: 0rem;
    margin: 0rem;
}
</style>
