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


const props = defineProps({placeholder:{default:''},disabledText:{default:''}})

const editModeEnabled = ref(false);
const emits = defineEmits(['selectResult'])

function onClickSearchResult(searchResult) {
    //clear 
    resultList.value = [];
    emits("selectResult", searchResult);
}

function toggleEditMode() {
    editModeEnabled.value  = !editModeEnabled.value
}


</script>
<template>
    <div class="wrapper">
        <form class="d-flex" role="search">
            <div class="input-group">
                <span class="input-group-text">Current Event</span>
                <template v-if="editModeEnabled">
                    
                <input class="form-control" type="search"
                aria-label="Search" id="search-box" 
                :placeholder="placeholder"
                v-model="searchBoxInput" 
                @blur="$emit('inputBoxDefocus')"/>
                </template>
                <template v-else>
                    
                    <div class="search-box-disabled-text form-control">{{ disabledText }}</div>
                </template>

                <button  class="btn btn-outline-secondary" type="button" @click="toggleEditMode">edit</button>
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