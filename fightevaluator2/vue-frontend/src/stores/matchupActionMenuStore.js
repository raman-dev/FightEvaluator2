import { defineStore } from "pinia";
import { ref} from 'vue';

export const useMatchupActionMenuStore = defineStore('matchupActionMenuStore',()=>{
    const menuOpen = ref(false);
    const menuPosition = ref({
        x:-1,
        y:-1,
        tablePctX:-1,//should be a percentage of table width
        tablePctY:-1 //should be a percentage of table height
        //on resize map tableRelative position to page relative and move menu to that position
    });
    const menuLimitRect = ref(null);

    /*
        what is the position of the cursor relative to the table?

        relX = pageX - tablePageX
        relY = pageY - tablePageY

        pctX = relX/tableWidth
        pctY = relY/tableHeight

        pctX -> pageX
        pctX * tableWidth + tablePageX
        pctY * tableHeight + tablePageY
    */
       //use to maintain relative position on resize
    function getPagePositionFromPercent(width,height,tablePageX,tablePageY){
        return {
            x : menuPosition.value.tablePctX * width + tablePageX,
            y : menuPosition.value.tablePctY * height + tablePageY
        }
    }
    return  { menuOpen,menuPosition, menuLimitRect, getPagePositionFromPercent };
});