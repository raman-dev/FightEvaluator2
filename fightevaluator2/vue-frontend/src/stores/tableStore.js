import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useTableStore = defineStore('table', () => {
  //3 tables
  //only show 1 action menu when right clicked 
  //right click only possible after row is active 
  const actionMenuOpen = ref(false);
  return { actionMenuOpen }
  
})
