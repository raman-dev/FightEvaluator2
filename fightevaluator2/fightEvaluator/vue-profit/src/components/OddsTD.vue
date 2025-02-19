<script setup>

const props = defineProps(['event','odd']);

function oddClick(index){
    if (index != -1){
        //we know its a win event and we clicked one of the two td's controlled by us
    }
}

</script>

<template>
    
    <td @click="oddClick(-1)" v-if="props.event != 'win'">
        <strong>
            {{ props.odd }}
        </strong>
    </td>
    <td v-else v-for="(winOdd,index) in props.odd" @click="oddClick(index)" :key="index">
        <strong>
            {{ winOdd }}
        </strong>
    </td>
</template>

<style scoped>
    :hover{
        cursor: pointer;
    }
</style>