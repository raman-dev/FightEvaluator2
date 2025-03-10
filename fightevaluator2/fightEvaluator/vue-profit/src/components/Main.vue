<script setup>
import OddsTable from './OddsTable.vue';

</script>
<template>
    <OddsTable />
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
    color: black;
}

.likelihood {
  border-radius: 0.2rem;
  width: 18ch;
  user-select: none;
  margin: 0.2rem;
  height: fit-content;

  span {
    color: black;
    padding: 1rem;
    padding-left: 0.6rem;
  }

  &.selected {
    outline: 2px solid whitesmoke;
    outline-offset: 1px;
  }

  &:hover {
    cursor: pointer;
  }

  .justification{
    overflow: hidden;
    height: 0px;
  }

}
</style>