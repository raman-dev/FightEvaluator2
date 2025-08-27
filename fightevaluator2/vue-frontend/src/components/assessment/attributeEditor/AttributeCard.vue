<script setup>
import { inject,onMounted,ref,watch } from 'vue';

const attribLabelValueMap = inject('attribValueMap');
const attribValueLabelMap = inject('attribValueLabelMap');
const attribCardOrder = inject('attribCardOrder');
const attribInfoMap = inject('attribInfoMap');


const rmscores = (val) => {
    if (!val) return "";
    return val.replace(/_/g, " ").trim();
};

const editModeEnabled = ref(false);
const attributeValue = defineModel('attributeValue');

const attrib_value = ref('');
const props = defineProps(['attrib_name']);

onMounted(()=>{
    attrib_value.value = attribValueLabelMap[attributeValue.value];
    console.log (props.attrib_name,attrib_value.value);
})

watch(attributeValue,(newVal,oldVal) => {
    attrib_value.value = attribValueLabelMap[newVal];
});

</script>
<template>
     <div class="attrib-card" :data-edit-mode-enabled="editModeEnabled" :data-attrib-state="attrib_value" :data-attrib-name="props.attrib_name">
        <div class="card-header">
            <div class="state-container">
                <h4>{{ rmscores(props.attrib_name) }}</h4>
                <svg class="arrow" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 -960 960 960" width="24">
                    <path fill="white" d="m560-240-56-58 142-142H160v-80h486L504-662l56-58 240 240-240 240Z" />
                </svg>
                <div class="card-state">{{ attrib_value }}</div>
            </div>
            <div class="button-container">
                <button class="attrib-edit-button btn btn-outline-light">edit</button>
                <button class="attrib-commit-button btn btn-outline-info">commit</button>
            </div>
        </div>
        <div class="card-body">
            attribute state options container
            <div class="attrib-option" :data-option-state="positive" :selected="attrib_value=='positive'">
                <h5 class="option">Option 0</h5>
                <p class="description"></p>
            </div>
            <div class="attrib-option" :data-option-state="neutral" :selected="attrib_value=='neutral'" v-if="props.attrib_name != 'grappling_offense' && props.attrib_name != 'grappling_defense'">
                <h5 class="option">Option 0</h5>
                <p class="description"></p>
            </div>
            <div class="attrib-option" :data-option-state="negative" :selected="attrib_value=='negative'">
                <h5 class="option">Option 0</h5>
                <p class="description">{{ attribInfoMap[props.attrib_name]["negative"] }}</p>
            </div>
            <div class="attrib-option" :data-option-state="untested" :selected="attrib_value=='untested'">
                <h5 class="option">Option 0</h5>
                <p class="description">"untested"</p>
            </div>
        </div>
        <div class="card-footer">
            <div class="card-state-description" :data-option-state="attrib_value">
                <p>{{ attribInfoMap[props.attrib_name][attrib_value].description }}</p>
            </div>
        </div> 
    </div> 
</template>
<style lang="scss" scoped>
$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;
$outlineColor : #3d7efd;

$backgroundColor: #212529;
// $cardColor: #242a34;
$cardBorderColor: #131b23;
$cardColor: #12161A;

$color-0: #01161E; 
$color-1: #124559;
$color-2: #598392;
$color-3: #AEC3B0;
$color-4: #EFF6E0;

// $backgroundColor: #01121E;
// $cardColor: #124554;

$btnBackgroundColor: #598392;
$btnBorderColor: black;
$btnBorderRadius: 0.6rem;
$btnClickBackground: #5983928f;

$cardPadding: 1.2rem;
$cardStatePadding: 0.3rem;
$optionPadding: 0.8rem;
$descriptionPadding: 0.5rem;
$borderRadius: 0.5rem;
$flickerDuration: 400ms;

@mixin button-active{
  box-shadow: black 2px 2px 0 0;
  // background-color: $btnClickBackground;
}

.attrib-card[data-attrib-state="positive"]{
  .card-state{
    background-color: $positiveBg;
  }
}

.attrib-card[data-attrib-state="neutral"]{
  .card-state{
    background-color: $neutralBg;
    // color: whitesmoke;
    color:#12161A; 
  }
}

.attrib-card[data-attrib-state="negative"]{
  .card-state{
    background-color: $negativeBg;
    color: whitesmoke;
  }
}


.fighter-attrib-list{
  padding: 0.5rem;
}

.attrib-card{
  background-color: $cardColor;
  
  // border: 2px solid $cardBorderColor;
  border-radius: $borderRadius;

  outline: 0px solid transparent;
  outline-offset: 2px;
  
  padding: $cardPadding;
  margin-bottom: 0.7rem;

  transition: outline 0.12s ease-out;

  p{
    margin: 0px;
  }
  .card-header{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
    .state-container{
      display: flex;
      align-items: center;
      text-transform: capitalize;
      h4 {
        margin: 0px;
      }

      .card-state{
        display: flex;
        align-items: center;

        border-radius: 0.4rem;
        // border: 2px solid lavender;
        border: 1px solid transparent;
        padding: $cardStatePadding;

        font-family: PoppinsSemiBold;
      }
    }
    .button-container{
      display: flex;
    }
  }
  .card-body{
    // display: flex;
    // justify-content: space-evenly;
    
    height: 0px;
    opacity: 0;
    
    overflow: hidden;
    transition: all 0.3s cubic-bezier(.58,-0.02,.19,.85);
  
    .attrib-option{
      display: flex;
      align-items: center;

      // padding: $optionPadding;
      margin: $optionPadding;
      cursor: pointer;

      font-family: PoppinsSemiBold;
      text-transform: uppercase;

      .option{
        margin: 0px;  
        margin-right: 0.5rem;
        padding: $optionPadding;

        border-radius: $borderRadius;
        border: 2px solid lavender;
      }

      .description{
        padding: $optionPadding;
        border-radius: $borderRadius;
        border: 2px solid lavender;
        text-transform: capitalize;
      }
    }

    .attrib-option[data-option-state="positive"]{
        .option, .description{
          border-color: $positiveBg;
        }
        .option{
          color: $positiveBg;
        }
    }
    .attrib-option[data-option-state="neutral"]{
      .option, .description{
        border-color: $neutralBg;
      }
      .option{
        color: $neutralBg;
      }
    }

    .attrib-option[data-option-state="negative"]{
      .option, .description{
        border-color: $negativeBg;
      }
      .option{
        color: $negativeBg;
      }
    }
    
    .attrib-option[data-option-state="positive"][selected]{
      border-color: whitesmoke;
      color: whitesmoke;
      background-color: $positiveBg;
    }
    .attrib-option[data-option-state="neutral"][selected]{
      border-color: whitesmoke;
      color: whitesmoke;
      background-color: $neutralBg;
    }
    .attrib-option[data-option-state="negative"][selected]{
      border-color: whitesmoke;
      color: whitesmoke;
      background-color: $negativeBg;
    }

    .attrib-option[selected]{
      border-color: whitesmoke;
      color: whitesmoke;
      .option{
        border-color: whitesmoke;
        color: whitesmoke;
      }
    }

    .attrib-option[data-option-state="untested"]{
      display: none; 
    }
  }

  .card-footer{
    margin-top: 0.4rem;
    .card-state-description{
      
      border: 2px solid lavender;
      border-radius: $borderRadius;

      padding: $descriptionPadding;
    }
    .card-state-description[data-option-state="positive"]{
      border-color: $positiveBg !important;
    }
    
    .card-state-description[data-option-state="neutral"]{
      border-color: $neutralBg !important;
    }
    
    .card-state-description[data-option-state="negative"]{
      border-color: $negativeBg !important;
    }
    // .card-state-description[data-option-state="untested"]{
    //   display: none;
    // }
  }
}

//disable button click on attrib options when card edit mode disabled
.attrib-card[data-edit-mode-enabled="false"]{
   //reset outling color for animation
   outline-color: transparent !important;
   animation-play-state: paused;
  .card-body{
    .attrib-option{
      pointer-events: none;
    }
  }
}
.attrib-card[data-edit-mode-enabled="true"]{
  // outline-color: lavender !important;
  
  outline: 3px solid lavender !important;

  animation-play-state: running;
  margin-bottom: 0.85rem;

  .card-state{
    background-color: transparent;
  }
  .attrib-edit-button{
    @include button-active;
  }
}

.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="positive"]{
  .card-state{
    border-color: $positiveBg;
    color: $positiveBg;
  }
}
  
.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="neutral"]{
  .card-state{
    border-color: $neutralBg;
    color: $neutralBg;
  }
}

.attrib-card[data-edit-mode-enabled="true"][data-attrib-state="negative"]{
  .card-state{
    border-color: $negativeBg;
    color: $negativeBg;
  }
}
</style>