<script setup>
import { inject, onMounted, ref, watch } from 'vue';
import AttributeOption from './AttributeOption.vue';

const attribLabelValueMap = inject('attribLabelValueMap');
const attribValueLabelMap = inject('attribValueLabelMap');
const attribInfoMap = inject('attribInfoMap');

const rmscores = (val) => {
  if (!val) return "";
  return val.replace(/_/g, " ").trim();
};

const editModeEnabled = ref(false);
const attributeValue = defineModel('attributeValue');

const attrib_value = ref('');
const props = defineProps(['attrib_name']);

onMounted(() => {
  attrib_value.value = attribValueLabelMap[attributeValue.value];
  // console.log(props.attrib_name, attrib_value.value);
})

watch(attributeValue, (newVal, oldVal) => {
  attrib_value.value = attribValueLabelMap[newVal];
});

function onClickEdit(){
    editModeEnabled.value = !editModeEnabled.value
    attrib_value.value = attribValueLabelMap[attributeValue.value];
}

//called before element is in the dom no heights and dimensions
function onBeforeEnterCardBodyTransition(cardBody){
  // console.log('onBeforeEnterCardBodyTransition!');
  cardBody.style.height = `0px`;
}

//called one frame after element is in the dom
function onEnterCardBodyTransition(cardBody){
  // console.log('onEnterCardBodyTransition! scrollHeight => ',cardBody.scrollHeight);
  cardBody.style.height = `${cardBody.scrollHeight}px`;
}

function onAfterEnterCardBodyTransition(cardBody) {
  cardBody.style.height='auto';
}

function onBeforeLeaveCardBodyTransition(cardBody) {
  cardBody.style.height=`${cardBody.scrollHeight}px`;
}

function onLeaveCardBodyTransition(cardBody) {
  // console.log('onLeaveCardBodyTransition!');
  cardBody.style.height = '0px';
}

function onClickAttribOption(value,attribOption){
  console.log('onClickAttribOption!',attribOption);
  attrib_value.value=value;
}

</script>
<template>
  <div class="attrib-card" :data-edit-mode-enabled="editModeEnabled" :data-attrib-state="attribValueLabelMap[attributeValue]"
    :data-attrib-name="props.attrib_name">
    <div class="card-header">
      <div class="state-container">
        <h4>{{ rmscores(props.attrib_name) }}</h4>
        <svg class="arrow" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
          <path fill="white" d="m560-240-56-58 142-142H160v-80h486L504-662l56-58 240 240-240 240Z" />
        </svg>
        <div class="card-state">{{ attribInfoMap[props.attrib_name][attribValueLabelMap[attributeValue]].state }}</div>
      </div>
      <div class="button-container">
        <button class="attrib-edit-button btn btn-outline-light" @click="onClickEdit">edit</button>
        <button class="attrib-commit-button btn btn-outline-info">commit</button>
      </div>

    </div>

    <Transition 
      @before-enter="onBeforeEnterCardBodyTransition"
      @enter="onEnterCardBodyTransition"
      @after-enter="onAfterEnterCardBodyTransition"

      @before-leave="onBeforeLeaveCardBodyTransition"
      @leave="onLeaveCardBodyTransition"
    >
      <div class="card-body" v-if="editModeEnabled">
        <template v-for="value, key in attribInfoMap[props.attrib_name]">
          <template v-if="props.attrib_name !== 'grappling_defense' && props.attrib_name != 'grappling_offense'">
            <AttributeOption :optionState="key" :description="value.description" :state="value['state']"
              :selected="attrib_value === key" @click="onClickAttribOption(key,value)">
            </AttributeOption>
          </template>
          <template v-else>
            <AttributeOption :optionState="key" :description="value['description']" :state="value['state']"
              :selected="attrib_value === key" v-if="key !== 'neutral'" @click="onClickAttribOption(key,value)">
            </AttributeOption>
          </template>
        </template>
      </div>
    </Transition>

    <div class="card-footer">
      <div class="card-state-description" :data-option-state="attribValueLabelMap[attributeValue]">
        <p >{{ attribInfoMap[props.attrib_name][attribValueLabelMap[attributeValue]]['description'] }}</p>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>

.v-enter-active,.v-leave-active{
  transition: all 0.3s cubic-bezier(.58, -0.02, .19, .85);
}

.v-enter-from,.v-leave-to{
  opacity: 0;
}

.v-enter-to,.v-leave-from {
  opacity: 1;
}

$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;

$cardColor: #12161A;

$cardPadding: 1.2rem;
$cardStatePadding: 0.3rem;
$optionPadding: 0.8rem;
$descriptionPadding: 0.5rem;
$borderRadius: 0.5rem;

@mixin button-active {
  box-shadow: black 2px 2px 0 0;
  // background-color: $btnClickBackground;
}

.attrib-card[data-attrib-state="positive"] {
  .card-state {
    background-color: $positiveBg;
  }
}

.attrib-card[data-attrib-state="neutral"] {
  .card-state {
    background-color: $neutralBg;
    // color: whitesmoke;
    color: #12161A;
  }
}

.attrib-card[data-attrib-state="negative"] {
  .card-state {
    background-color: $negativeBg;
    color: whitesmoke;
  }
}

.attrib-card {
  background-color: $cardColor;

  // border: 2px solid $cardBorderColor;
  border-radius: $borderRadius;

  outline: 0px solid transparent;
  outline-offset: 2px;

  padding: $cardPadding;
  margin-bottom: 0.7rem;

  transition: outline 0.12s ease-out;

  p {
    margin: 0px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;

    .state-container {
      display: flex;
      align-items: center;
      text-transform: capitalize;

      h4 {
        margin: 0px;
      }

      .card-state {
        display: flex;
        align-items: center;

        border-radius: 0.4rem;
        // border: 2px solid lavender;
        border: 1px solid transparent;
        padding: $cardStatePadding;

        font-family: PoppinsSemiBold;
      }
    }

    .button-container {
      display: flex;
    }
  }

  .card-body {
    // display: flex;
    // justify-content: space-evenly;

    height: 0px;
    overflow: hidden;

    //keep for any visual state changes
    transition: all 0.3s cubic-bezier(.58, -0.02, .19, .85);
  }

  .card-footer {
    margin-top: 0.4rem;

    .card-state-description {

      border: 2px solid lavender;
      border-radius: $borderRadius;

      padding: $descriptionPadding;
    }

    .card-state-description[data-option-state="positive"] {
      border-color: $positiveBg !important;
    }

    .card-state-description[data-option-state="neutral"] {
      border-color: $neutralBg !important;
    }

    .card-state-description[data-option-state="negative"] {
      border-color: $negativeBg !important;
    }

    // .card-state-description[data-option-state="untested"]{
    //   display: none;
    // }
  }
}

//disable button click on attrib options when card edit mode disabled
.attrib-card[data-edit-mode-enabled="false"] {
  //reset outling color for animation
  outline-color: transparent !important;
  animation-play-state: paused;

  .card-body {
    .attrib-option {
      pointer-events: none;
    }
  }
}

.attrib-card[data-edit-mode-enabled="true"] {
  // outline-color: lavender !important;

  outline: 3px solid lavender !important;

  animation-play-state: running;
  margin-bottom: 0.85rem;

  .card-state {
    background-color: transparent;
  }

  .attrib-edit-button {
    @include button-active;
  }
}

.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="positive"] {
  .card-state {
    border-color: $positiveBg;
    color: $positiveBg;
  }
}

.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="neutral"] {
  .card-state {
    border-color: $neutralBg;
    color: $neutralBg;
  }
}

.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="negative"] {
  .card-state {
    border-color: $negativeBg;
    color: $negativeBg;
  }
}
</style>