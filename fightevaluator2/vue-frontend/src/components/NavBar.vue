<script setup>
import { useTemplateRef } from 'vue';


const props = defineProps(['links','navTitle'])

const navbarTogglerRef = useTemplateRef('navbarToggler');
const navbarCollapseRef = useTemplateRef('navbarCollapse');


function onNavbarLinkClick(){
    const navbarToggler = navbarTogglerRef.value;
    const navbarCollapse = navbarCollapseRef.value;
    if (navbarCollapse.classList.contains ('show')){
        navbarToggler.click();
    }
}

</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary mb-3">
        <div class="container-fluid">
            <RouterLink class="navbar-brand" :to="{name:'home'}">{{ navTitle }}</RouterLink>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" ref="navbarToggler"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent" ref="navbarCollapse">
                <!--implement current link status-->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" >
                    <li class="nav-item" v-for="linkObj in links">
                        <!-- <a class="nav-link" href="#">{{ linkObj.name }}</a> -->
                        <RouterLink @click="onNavbarLinkClick" class="nav-link" :to=linkObj.path> {{ linkObj.name }}</RouterLink>
                    </li>
                </ul>
                <form class="d-flex" role="search">
                    <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
                    <button class="btn btn-outline-success" type="submit">Search</button>
                </form>
            </div>
        </div>
    </nav>
</template>

<style lang="scss">
    .nav-item .nav-link{
        text-transform: capitalize;
    }
</style>