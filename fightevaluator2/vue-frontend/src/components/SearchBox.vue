<script setup>
import { defineModel } from 'vue';

const searchBoxInput = defineModel('searchBoxInput', {
    default: null,
    required: false,
});


const props = defineProps({ 
    placeholder: { default: '' }, 
    disabledText: { default: '' }, 
});


</script>
<template>
    <div class="wrapper">
        <form class="d-flex" role="search">
            <div class="input-group">
                <input class="form-control" type="search" aria-label="Search" id="search-box" 
                v-model="searchBoxInput" 
                :placeholder="placeholder"
                 @blur="$emit('inputBoxDefocus')" />
                <button class="btn btn-outline-secondary" type="button" @click="$emit('searchClick')">Search</button>
            </div>
        </form>
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