<script setup>

import NavBar from './components/NavBar.vue';
import MainContent from './components/MainContent.vue';


const links = [
    "home",
    "events",
    "predictions",
    "profit"
];

const title = 'Fight Evaluator';

</script>

<template>
    <NavBar :links="links" :nav-title="title"></NavBar>
    <MainContent></MainContent>
</template>

<style lang="scss">
    html, body{
        height: 100%;
        width: 100%;
    }
    #app{
        width: 100% !important;

        display: flex;
        flex-direction: column;
       
        padding: 0rem;
        margin: 0rem;
    }

</style>
