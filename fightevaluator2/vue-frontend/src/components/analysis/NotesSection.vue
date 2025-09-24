<script setup>
import NoteItem from "./NoteItem.vue"

defineProps({
  fighter: {
    type: Object,
    required: true
    // expected: { first_name: string, last_name: string }
  },
  notes: {
    type: Array,
    required: true
    // expected: [ { data: string, tag: string }, ... ]
  }
})
</script>

<template>
  <div class="notes-section notes-left">
    <h3 class="fighter-name">
      {{ fighter.first_name }} {{ fighter.last_name }} - Notes
    </h3>

    <div class="notes-container">
      <ul class="notes">
        <NoteItem v-for="(note, index) in notes" :key="index" :text="note.data" :tag="note.tag" />
      </ul>
    </div>
  </div>
</template>

<style scoped lang="scss">
.notes-section {
  .fighter-name {
    text-transform: capitalize;
  }

  .notes {
    border-radius: 0.4rem;
    list-style: none;
    padding: 0.5rem;
    background-color: #12161A;

    li p {
      max-width: 36ch;
    }

    
  }
}
</style>
