<script setup>
import { ref,watch } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { storeToRefs } from 'pinia';


const { matchup } = storeToRefs(useMatchupDetailStore());
const analysisComplete = ref(false);


watch (matchup,(newMatchupVal,oldMatchupVal) => {
    analysisComplete.value = newMatchupVal.analysisComplete;
});

</script>
<template>

    <div class="analysis-check-container d-flex justify-content-center" :class="{'checked':analysisComplete}">
        <input class="form-check-input" type="checkbox" v-model="analysisComplete" id="flexCheckDefault">
        <label class="form-check-label mx-2" for="flexCheckDefault">
        Analysis Complete
        </label>
  </div>

</template>
<style lang="scss" scoped>

.analysis-check-container{
  margin: auto;
  width: fit-content;
  padding: 0.4rem;
  padding-left: 0.6rem;
  padding-right: 0.6rem;
  outline: 2px solid #e6e6fa22;
  border-radius: 0.4rem;
  user-select: none;

  transition: outline 0.15s ease-in;
  * {
    cursor: pointer;
  }
}

.analysis-check-container:hover{
  cursor: pointer;
}

.analysis-check-container.checked{
  // outline-width: 3px;
  outline-color: #00FF00;
}

</style>