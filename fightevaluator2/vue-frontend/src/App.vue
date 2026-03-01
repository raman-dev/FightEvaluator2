<script setup>

import NavBar from './components/NavBar.vue';


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

    <!-- <div class="xcontent-wrapper"> -->
        <RouterView v-slot="{ Component, route }">
            <Transition name="fade" mode="out-in">
                <component :is="Component" :key="route.path" />
            </Transition>
        </RouterView>
    <!-- </div> -->


    <!-- <RouterView></RouterView> -->
</template>

<style lang="scss">
.fade-enter-active,
.fade-leave-active {
    transition: all 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
    transform: translateY(1%);
    opacity: 0;
}

/* use font as variable */
$backgroundColor: #212529;


html,
body {
    height: 100%;
    width: 100%;
}

#app {
    height: 100%;
    width: 100% !important;

    display: flex;
    flex-direction: column;

    padding: 0rem;
    margin: 0rem;
    overflow: auto;
    overflow-y: hidden;

    // .xcontent-wrapper{
    //     height: 100%;
    //     width: 100%;
    //     overflow: auto;
    // }
    // .xcontent-wrapper > :first-child{
    //     padding-top: 0.5rem;
    // }
}
</style>
