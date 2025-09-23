<script setup>
import { inject } from "vue";
import AttribCol from "./AttribCol.vue"


defineProps({'attribComparison': {required: true, type: Array}});
const rmscores = inject('replaceUnderscoreSpace');
const attribValueLabelMap = inject('attribValueLabelMap');

</script>

<template>
    <div class="attrib-compare-table">
        <div v-for="(item, index) in attribComparison" :key="index" class="attrib-row" :data-name="item.attribName">
            <h3>{{ rmscores(item[0]) }}</h3>

            <!-- Reusable AttribCol components -->
            <AttribCol :value="attribValueLabelMap[item[1]]" side="attrib-left" :attribName="item[0]" />
            <AttribCol :value="attribValueLabelMap[item[2]]" side="attrib-right" :attribName="item[0]"/>
        </div>
    </div>
</template>

<style scoped lang="scss">

.attrib-row {
  display: grid;
  grid-template-columns: 1fr 1fr;

  h3 {
    text-transform: capitalize;
    text-align: center;
    grid-column: span 2;
  }

  .attrib-left {
    text-align: end;
  }
  
}
</style>
