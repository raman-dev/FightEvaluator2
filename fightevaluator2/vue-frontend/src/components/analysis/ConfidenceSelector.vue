<script setup>
import { ref, useTemplateRef, watch } from "vue";

const props = defineProps({
  modelValue: {
    type: Number,
    default: 3, // neutral by default
  },
});

const emit = defineEmits(["update:modelValue"]);
const likelihood = ref(props.modelValue);
const showConfidenceList = ref(false);

const wrapperRef = useTemplateRef('wrapperRef');
const confidenceSelectorRef = useTemplateRef('confidenceSelectorRef');
const confidenceListRef=  useTemplateRef('confidenceListRef');

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

// function showConfidenceList() {
/*
    animating what?
      confidence list needs to un collapse itself
      
      list   -> 0px height
        items
      
      on click show do what 
        set list height to its scroll height
      
      list container should have what 
      overflow visible and a fixed height just before animating and while open
*/
// }
function toggleList() {
  showConfidenceList.value = !showConfidenceList.value;
}
function onBeforeEnter(confidenceList) {
  const wrapper = wrapperRef.value;
  const container = confidenceSelectorRef.value;
  
  //measure wrapper height then set it 
  const wrapperHeight = wrapper.offsetHeight;
  const containerHeight = container.offsetHeight;
  console.log('onBeforeEnter.wrapperHeight',wrapperHeight);
  
  wrapper.style.height = `${wrapperHeight}px`;

  //container height needs to be fixed 
  container.style.height = `${containerHeight}px`;
  //overflow hidden
  confidenceList.style.height = '0px';
  // console.log (containerHeight);
}

function onEnter(confidenceList) {
  const container = confidenceSelectorRef.value;
  const scrollHeight = confidenceList.scrollHeight;
  const containerHeight = container.offsetHeight;

  confidenceList.style.height = `${scrollHeight}px`;
  container.style.height=`${scrollHeight + containerHeight}px`;
}

function onBeforeLeave(confidenceList) {
  
}

function onLeave(confidenceList) {
  const container = confidenceSelectorRef.value;
  const containerHeight = container.offsetHeight;
  const listHeight = confidenceList.offsetHeight;

  container.style.height = `${containerHeight - listHeight}px`;
  confidenceList.style.height = '0px';
}

function onAfterLeave(confidenceList) {
  const container = confidenceSelectorRef.value;
  const wrapper = wrapperRef.value;
  //height needs to be auto again
  container.style.height = `auto`;
  wrapper.style.height = `auto`;
  confidenceList.style.height='0px';
}


</script>

<template>
  <!--wrapper needs fixed height and confidence selector needs to change its height-->
  <div class="confidence-selector-wrapper" ref="wrapperRef">

   
      <div class="confidence-selector" ref="confidenceSelectorRef">

        <div class="current-confidence d-flex align-items-center" :data-likelihood="likelihood">
          <p class="confidence my-0 w-100" :class="'likely-' + likelihood" style="color:black;">
            {{ labels[likelihood] }}
          </p>
          <button class="btn show-confidence-list-btn w-0" @click="toggleList">
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
              <path fill="white" d="M480-345 240-585l56-56 184 184 184-184 56 56-240 240Z" />
            </svg>
          </button>
        </div>
      <Transition 
        @before-enter="onBeforeEnter" 
        @enter="onEnter" 
        @before-leave="onBeforeLeave" 
        @leave="onLeave"
        @after-leave="onAfterLeave">
        <ul class="confidence-list" v-if="showConfidenceList">
          <li v-for="n in 5" :key="n" :class="{ active: likelihood === n }" :data-likelihood="n"
            @click="selectLikelihood(n)">
            <div :class="'likelihood likely-' + n">{{ labels[n] }}</div>
          </li>
        </ul>
      </Transition>
      </div>

    
  </div>

</template>

<style scoped lang="scss">


.confidence-selector-wrapper {
  overflow: visible;
  height: auto;
  position: relative;
  z-index: 1000;
}

.confidence-selector {
  background-color: #12161A;
  border: 1px solid lavender;
  border-radius: 0.4rem;
  padding: 0.3rem;
  height: auto;
  transition: all 0.3s ease-in-out;

  .current-confidence {
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
  // position: relative;
  // z-index: 100;
  list-style-type: none;

  padding: 0px;
  margin-bottom: 0rem;
  height: 0px;
  transition: all 0.3s ease-in-out;


  overflow: hidden;
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

  li.active .likelihood {
    outline: 2px solid white;
    outline-offset: 2px;
  }
}
</style>
