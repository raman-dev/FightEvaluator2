<script setup>
import { onMounted, useTemplateRef, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useMediaQuery } from '@vueuse/core';


const props = defineProps(['links', 'navTitle'])

const navbarTogglerRef = useTemplateRef('navbarToggler');
const navbarCollapseRef = useTemplateRef('navbarCollapse');
const linkUlTemplateRef = useTemplateRef('linksUlRef');

function onNavbarLinkClick() {
    const navbarToggler = navbarTogglerRef.value;
    const navbarCollapse = navbarCollapseRef.value;
    if (navbarCollapse.classList.contains('show')) {
        navbarToggler.click();
    }
}

const isLarge = useMediaQuery('(min-width: 992px)');
function onNavItemClick(event){
    if ((!isLarge.value)){
        //click on descendant nav-item
        const li = event.currentTarget;
        li.querySelector("a").click();
    }
}

</script>

<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary mb-3">
        <div class="container-fluid">
            <RouterLink class="navbar-brand" :to="{ name: 'home' }">{{ navTitle }}</RouterLink>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" ref="navbarToggler"
                data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
                aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarSupportedContent" ref="navbarCollapse">
                <!--implement current link status-->
                <ul class="navbar-nav me-auto mb-2 mb-lg-0" ref="linksUlRef">
                    <li class="nav-item" v-for="linkObj in links" :class="{ 'nav-collapsed': !isLarge }" @click="onNavItemClick">
                        <!-- <a class="nav-link" href="#">{{ linkObj.name }}</a> -->
                        
                        <template v-if="isLarge">
                            <RouterLink @click="onNavbarLinkClick" class="nav-link" active-class="active" :to=linkObj.path>
                            {{ linkObj.name }}</RouterLink>
                            <div class="active-underline"></div>
                        </template>
                        <div v-if="!isLarge" class="nav-link-wrapper">
                            <RouterLink @click="onNavbarLinkClick" class="nav-link" active-class="active" :to=linkObj.path>
                            {{ linkObj.name }}</RouterLink>
                            <div class="active-underline"></div>
                        </div>
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
.nav-item .nav-link {
    text-transform: capitalize;
}

.nav-item {
    width: 100%;
    padding: 0.5rem;
    a {
        padding: 0px !important;
    }

    .nav-item-wrapper {
        max-width: fit-content;
    }

    //style the sibling immediatly after nav-link.active
    .nav-link.active + .active-underline {
        background-color: whitesmoke;
        height: 1px;
        width: 100%;
    }
}
.nav-item.nav-collapsed{
    &:hover{
        cursor: pointer;
        a {
            color: rgba(255, 255, 255, .8) !important; 
        }
    }
    .nav-link-wrapper {
        width: fit-content;
    }
}

</style>