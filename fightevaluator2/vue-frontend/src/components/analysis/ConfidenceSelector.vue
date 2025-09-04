<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Number,
    default: 3, // neutral by default
  },
});

const emit = defineEmits(["update:modelValue"]);
const likelihood = ref(props.modelValue);

watch(
  () => props.modelValue,
  (val) => {
    likelihood.value = val;
  }
);

function selectLikelihood(n) {
  likelihood.value = n;
  emit("update:modelValue", n);
}

const labels = {
  1: "very likely",
  2: "somewhat likely",
  3: "neutral",
  4: "somewhat unlikely",
  5: "very unlikely",
};
</script>

<template>
  <div class="confidence-selector">
    <div class="current-confidence d-flex align-items-center" :data-likelihood="likelihood">
      <p class="confidence my-0 w-100" :class="'likely-' + likelihood" style="color:black;">
        {{ labels[likelihood] }}
      </p>
      <button class="btn show-confidence-list-btn w-0">
        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
          <path fill="white" d="M480-345 240-585l56-56 184 184 184-184 56 56-240 240Z" />
        </svg>
      </button>
    </div>

    <ul class="confidence-list">
      <li v-for="n in 5" :key="n" :class="{ active: likelihood === n }" :data-likelihood="n"
        @click="selectLikelihood(n)">
        <div :class="'likelihood likely-' + n">{{ labels[n] }}</div>
      </li>
    </ul>
  </div>
</template>

<style scoped lang="scss">
.confidence-selector{
  border: 1px solid lavender;
  border-radius: 0.4rem;
  padding: 0.3rem;

  .current-confidence{
    margin-bottom: 0.1rem;
    margin-top: 0.1rem;
  }
}

.confidence {
  min-width: fit-content;
  border-radius: 0.4rem;
  padding: 0.3rem;
  text-align: center;
  text-transform: capitalize;
  font-family: PoppinsSemiBold;
}

ul.confidence-list {
  list-style-type: none;
  
  padding: 0px;
  margin-bottom: 0rem;
  height: 0px;

  overflow: hidden;
  
  transition: all 0.3s ease-in-out;
  font-family: PoppinsSemiBold;

  li {
    padding: 0.3rem;
    margin-bottom: 0.1rem;
    color: black;
  }

  li .likelihood {
    border-radius: 0.4rem;
    padding: 0.3rem;
    text-align: center;
    text-transform: capitalize;
  }

  li:hover {
    cursor: pointer;
  }

  li.active .likelihood{
    outline: 2px solid white;
    outline-offset: 2px;
  }
}

.likely-1 {
  color: green;
}

.likely-2 {
  color: limegreen;
}

.likely-3 {
  color: black;
}

.likely-4 {
  color: orange;
}

.likely-5 {
  color: red;
}
</style>
