<script setup>
import { ref, defineModel } from 'vue';

const searchBoxInput = defineModel('searchBoxInput', {
    default: '',
    required: false,
});

const resultList = defineModel('resultList', {
    default: [],
    required: false,
});


const emits = defineEmits(['selectResult'])

function onClickSearchResult(searchResult) {
    //clear 
    resultList.value = [];
    emits("selectResult", searchResult);
}


</script>
<template>
    <div class="wrapper">
        <form class="d-flex" role="search">
            <div class="input-group">
                <input class="form-control" type="search"
                aria-label="Search" id="search-box" 
                
                v-model="searchBoxInput" 
                @blur="$emit('inputBoxDefocus')" />
                <button  class="btn btn-outline-danger" type="button" @click.prevent="submit">Clear</button>
            </div>
        </form>
        <div class="result-list">
            <ul class="list-group hover">
                <li v-for="(result, index) in resultList" :key="result.id" class="list-group-item list-group-item-action"
                    @click="onClickSearchResult(resultList[index])">
                    {{ result.title }}
                </li>
            </ul>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.wrapper {
    form {
        margin: 0px;
    }

    .result-list {
        ul {
            li:hover {
                cursor: pointer;
            }
        }
    }
}
</style>