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
    <div class="notes-container">
      <div class="title-wrapper d-flex justify-content-between">

        <h4 class="fighter-name">
          {{ fighter.first_name }} {{ fighter.last_name }}
        </h4>
        <h4> Notes</h4>
      </div>
      <ul class="notes">
        <NoteItem v-if="notes.length === 0" text="No notes taken" tag="info" empty="true" />
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

  .notes-container{  
    padding: 0.5rem;
    background-color: #12161A;
    .notes {
      border-radius: 0.4rem;
      list-style: none;
      padding: 0rem;
      
      padding-left: 0.4rem;
      padding-right: 0.4rem;
      li p {
        max-width: 36ch;
      }
    }
  }

}
</style>
