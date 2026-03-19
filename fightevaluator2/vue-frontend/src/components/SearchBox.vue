<script setup>
import { ref, defineModel } from 'vue';

const searchBoxInput = defineModel('searchBoxInput', {
    default: null,
    required: false,
});

const resultList = defineModel('resultList', {
    default: [],
    required: false,
});


const props = defineProps({ 
    placeholder: { default: '' }, 
    disabledText: { default: '' }, 
    searchOnInput: { default: true } 
});

const editModeEnabled = ref(false);
const emits = defineEmits(['selectResult'])

function onClickSearchResult(searchResult) {
    //clear 
    resultList.value = [];
    emits("selectResult", searchResult);
}

function toggleEditMode() {
    editModeEnabled.value = !editModeEnabled.value
}


</script>
<template>
    <div class="wrapper">
        <form class="d-flex" role="search">
            <div class="input-group">

                <template v-if="searchOnInput === true">
                    <input class="form-control" type="search" aria-label="Search" id="search-box"
                        :placeholder="placeholder" v-model="searchBoxInput" @blur="$emit('inputBoxDefocus')" />
                </template>
                <template v-else>
                    <input class="form-control" type="search" aria-label="Search" id="search-box"
                        :placeholder="placeholder" @blur="$emit('inputBoxDefocus')" />
                </template>

                <button class="btn btn-outline-secondary" type="button" @click="toggleEditMode">Search</button>
            </div>

        </form>
        <div class="result-list">
            <ul class="list-group hover">
                <li v-for="(result, index) in resultList" :key="result.id"
                    class="list-group-item list-group-item-action" @click="onClickSearchResult(resultList[index])">
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