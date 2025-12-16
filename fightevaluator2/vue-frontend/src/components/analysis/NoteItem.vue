<script setup>
import { inject } from 'vue';

defineProps({
  text: {
    type: String,
    required: true
  },
  tag: {
    type: Number,
    required: false
  },
  createdAt:{
    type: String,
    required: false,
    default: ""
  },
  empty: {
    type: Boolean,
    required: false,
    default: false
  }
})

const formatDateShort = inject('formatDateShort');
</script>

<template>
  <li class="note" :data-tag="tag" :class="{'empty-note':empty}">
    <span class="timestamp" v-if="createdAt.length > 0">{{ formatDateShort(createdAt) }}</span>
    <p>{{ text }}</p>
  </li>
</template>

<style scoped lang="scss">
/*data-polarity color variables*/
$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;

.note {
  background-color: #212529;
  // border: 1px solid lavender;
  border-radius: 0.6rem;
  list-style: None;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  padding-top: 0.6rem;
  margin: 0.6rem;

  .timestamp{
    font-size: 0.7rem;
    opacity: 0.7;
    margin-bottom: 0.2rem;
    text-align: end;
  }

  p {
    word-break: break-word;
    text-wrap: wrap;
    max-width: 32ch;
    margin: 0px;
  }
}

.note.empty-note{
  border-color: #42464a;
  background-color: #212328;
}

.note[data-tag="positive"] {
  border: 3px solid $positiveBg;
}

.note[data-tag="negative"] {
  border: 3px solid $negativeBg;
}
</style>
