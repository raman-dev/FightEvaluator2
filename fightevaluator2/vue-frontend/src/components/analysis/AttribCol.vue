<script setup>
import { inject } from "vue";
defineProps({
  value: {
    type: [String, Number],
    required: true
  },
  side: {
    type: String,
    required: true, // "attrib-left" or "attrib-right"
  },
  attribName: {
    type: String,
    required: true,
  }
})


const attribInfoMap = inject('attribInfoMap');

</script>
<template>
  <div class="attrib-col" :class="side" :data-polarity="value">
    <div class="state-container">
      <h5>{{ attribInfoMap[attribName][value].state }}</h5>
    </div>
    <div class="attrib-description-container">
      <p>
        {{ attribInfoMap[attribName][value].description }}
      </p>
    </div>
  </div>
</template>



<style scoped lang="scss">

/*data-polarity color variables*/
$positiveBg: #0d6efd; 
$negativeBg: #dc3545;
$neutralBg: #ffc107; 


.attrib-col {
    border: 3px solid lavender;
    border-radius: 0.8rem;
    margin: 0.4rem;
    padding: 0.3rem;
}

div[data-polarity="positive"] {
    border-color: $positiveBg;
    h5 {
      background-color: $positiveBg;
    }
  }
  div[data-polarity="negative"] {
    border-color: $negativeBg;
    h5 {
      background-color: $negativeBg;
    }
  }
  div[data-polarity="neutral"] {
    border-color: $neutralBg;
    .state-container {
      background-color: $neutralBg;
      h5 {
        color: black;
      }
    }
  }

  div[data-polarity="null"] {
    .state-container {
      background-color: lightgray;
      h5 {
        color: darkslategray;
      }
    }
  }
</style>