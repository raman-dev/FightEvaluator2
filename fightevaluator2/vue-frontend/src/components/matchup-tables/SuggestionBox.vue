<script setup>

import { ref,defineModel } from 'vue';

const fighters = defineModel('fighters', { default: [] });
const selectedFighter = defineModel ('selectedFighter', { default: null });

function selectFighter(fighter){
    // selectedFighter.value = {
    //     id: fighter.id,
    //     first_name: fighter.first_name,
    //     last_name: fighter.last_name
    // };
    selectedFighter.value = fighter;
    fighters.value = [];//clear suggestion box
}

</script>
<template>
    <ul class="suggestion-box list-group" >
        <li class="list-group-item list-group-item-action" v-for="fighter in fighters" :key="fighter.id" @click="selectFighter(fighter)">
          <div class="suggestion">
            <p class="name">{{fighter.first_name}} {{fighter.last_name}}</p>
          </div>
        </li>
    </ul>
</template>