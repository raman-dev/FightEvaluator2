<script setup>
import { ref } from 'vue';


const queryString = ref('');
const searchResults = ref([
    {name:'ufc 0'},
    {name:'ufc 1'},
    {name:'ufc fight night'}
]);

function onSearchBoxInput(event) {
    const inputValue = event.target.value.trim();
    if (inputValue.length == 0){
        return;
    }
    // console.log("Search box input:", event.target.value);
    queryString.value = inputValue;
    //drop down list?
    //or what
    //type name show list of what?
    // fighter name? 
    // show chronological list of last events
}

</script>
<template>
    <div class="wrapper border">
        <form class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" id="search-box" @input="onSearchBoxInput">
            <button class="btn btn-outline-success" type="submit" @click.prevent="submit" >Search</button>
        </form>
        <div class="result-list">
            <ul class="list-group hover">
                  <li v-for="result in searchResults" :key="result.id" class="list-group-item list-group-item-action">
                    {{ result.name }}
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