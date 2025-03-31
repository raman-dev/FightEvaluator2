import { defineStore } from "pinia";
import { ref } from "vue";

export const useGraphStore = defineStore('graph',()=>{
    const show = ref(true);

    function toggleGraph(){
        show.value = !show.value;

        return show.value;
    }

    return  { show,toggleGraph }
});