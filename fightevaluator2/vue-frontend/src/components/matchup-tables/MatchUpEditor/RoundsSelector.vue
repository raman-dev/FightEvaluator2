<script setup>
const rounds = defineModel('rounds',{default:3,required:true});
</script>

<template>
    <!--rounds-->
    <div class="rounds-radio-group border rounded-2 p-1 px-3">
        <p class="radio-group-title">Rounds</p>
        <div class="form-check mx-3">
            <input class="form-check-input" type="radio" name="rounds" value="3" id="rounds-radio-3" v-model="rounds">
            <label class="form-check-label" for="rounds-radio-3">
                3
            </label>
        </div>
        <div class="form-check">
            <input class="form-check-input" type="radio" name="rounds" value="5" id="rounds-radio-5" v-model="rounds">
            <label class="form-check-label" for="rounds-radio-5">
                5
            </label>
        </div>
    </div>
</template>

<style scoped lang="scss">

.rounds-radio-group {
    width: fit-content;
    display: flex;

    .radio-group-title {
      margin: 0px;
    }
  }

</style>