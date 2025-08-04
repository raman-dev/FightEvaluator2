import { defineStore } from "pinia";
import { ref} from 'vue';

export const useMatchupActionMenuStore = defineStore('matchupActionMenuStore',()=>{
    const menuOpen = ref(false);
    const menuPosition = ref({x:-1,y:-1});
    return  { menuOpen,menuPosition };
});