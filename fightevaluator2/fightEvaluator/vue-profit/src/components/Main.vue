<script setup>
import { onMounted } from 'vue';
import OddsTable from './event_likelihoods/OddsTable.vue';
import LinesTable from './lines/LinesTable.vue';


</script>
<template>
    <div class="main-container">
      <OddsTable/>
      <LinesTable/>
    </div>
    
</template>

<style lang="scss">

.likely-5 {
    background-color: #dc3545;
}

.likely-4 {
    background-color: #ed7b26;
}

.likely-3 {
    background-color: #ffc107;
}

.likely-2 {
    background-color: #80ff00;
}

.likely-1 {
    background-color: #00ff00;
}

.likely-0 {
    background-color: #52565a;
}

.likelihood {
    
    border-radius: 0.2rem;
    font-family: PoppinsSemiBold;
    width: 18ch;
    user-select: none;
    margin: 0.2rem;
    height: fit-content;

    span {
        color: black;
        padding: 1rem;
        padding-left: 0.6rem;
        text-transform: capitalize;
    }

    &.selected {
        outline: 2px solid whitesmoke;
        outline-offset: 1px;
    }

    &:hover {
        cursor: pointer;
    }

}


.main-container{
  height: 100%; 
  width: 70%;  
  
  margin: auto;
}

@media (max-width: 1400px) {
    .main-container{
        width: 75%;
    }
}

@media (max-width: 1200px) {
    .main-container{
        width: 82.5%;
    }
}

@media (max-width: 992px) {
    .main-container{
        width: 87%;
    }
}

@media (max-width: 768px) {
    .main-container{
        width: 92%;
    }
}

//no larger than
@media (max-width: 576px) {
    .main-container{
        width: 100%;
    }
}
    

</style>