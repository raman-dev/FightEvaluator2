<script setup>
import Main from './components/Main.vue';

</script>

<template>
  <Main></Main>
</template>

<style lang="scss">
@import url('@/assets/css/fonts.scss');
  
  html, body {p
      height: 100% !important;
      min-height: 800px;
      font-family: PoppinsLight !important;
      font-size: 16px; 
      overflow: hidden;
  }
  
  body{
      display: flex;
      flex-direction: column;
  }
  
  h1,
  h2,
  h3 {
      font-family: PoppinsBold;
  }
  
  h4{
      font-family: PoppinsSemiBold;
  }
   
  h5,
  h6 {
      font-family: PoppinsMedium;
  }

  #app{
    height: 100%;
  }
</style>
