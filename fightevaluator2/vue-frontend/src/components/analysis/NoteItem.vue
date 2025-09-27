<script setup>
defineProps({
  text: {
    type: String,
    required: true
  },
  tag: {
    type: Number,
    required: false
  }
})
</script>

<template>
  <li class="note" :data-tag="tag">
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
  border: 2px solid lavender;
  border-radius: 0.6rem;
  list-style: None;
  display: flex;
  padding: 1rem;
  margin: 0.6rem;

  p {
    word-break: break-word;
    text-wrap: wrap;
    max-width: 32ch;
    margin: 0px;
  }
}

.note[data-tag="positive"] {
  border: 3px solid $positiveBg;
}

.note[data-tag="negative"] {
  border: 3px solid $negativeBg;
}
</style>
