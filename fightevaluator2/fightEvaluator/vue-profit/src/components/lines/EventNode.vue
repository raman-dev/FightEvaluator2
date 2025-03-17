<script setup>
import { ref,onMounted } from 'vue';


const props = defineProps(['likelihood','likelihood_val','fighter','type','justification']);

const typeReadable = ref('');

onMounted(() => {

    console.log(props);
    
    if (props.type == 'WIN'){
        typeReadable.value = props.type;
    }else if (props.type == 'ROUNDS_GEQ_ONE_HALF'){
        typeReadable.value = 'rounds >= 1.5';
    }else{
        typeReadable.value = 'fight does not go the distance';
    }
});

</script>

<template>
    <div class="event-node border d-flex flex-column">
        <div class="likelihood" :class='["likely-"+props.likelihood_val]'>
            <span>
                {{ props.likelihood }}
            </span>
        </div>
        <span v-if="props.type == 'win'">{{ props.fighter }}</span>
        <span v-else>
            {{ typeReadable }}
        </span>
    </div>
</template>

<style scoped lang="scss">
    .event-node{
        padding: 0.4rem;
        margin: 0.2rem;

        span {
            text-transform: capitalize;
        }
    }
</style>