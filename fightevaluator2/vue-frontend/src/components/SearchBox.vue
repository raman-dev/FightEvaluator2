<script setup>
import { ref,defineModel } from 'vue';

const searchBoxInput = defineModel('searchBoxInput',{
    default: '',
    required: false,
});

const resultList = defineModel('resultList',{
    default: [],
    required: false,
});


</script>
<template>
    <div class="wrapper border">
        <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" id="search-box" v-model="searchBoxInput">
            <button class="btn btn-outline-success" type="submit" @click.prevent="submit" >Search</button>
        </form>
        <div class="result-list">
            <ul class="list-group hover">
                  <li v-for="result in resultList" :key="result.id" class="list-group-item list-group-item-action">
                    {{ result.title }}
                  </li>
            </ul>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .wrapper{
        form {
            margin: 0px;
        }
    }
</style>