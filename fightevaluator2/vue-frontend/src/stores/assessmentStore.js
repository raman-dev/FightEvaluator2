import { defineStore } from "pinia";

export const useAssessmentStore = defineStore('assessment', () =>{
    const server = inject('server');

    const assessment = ref({});
    const bio = ref({});
    const notes = ref({});

    function onReceiveAssessment(data){
        assessment.value = data.assessment;
        bio.value = data.bio;    
        notes.value = data.notes;
         
    }

    function resetData(){
        assessment.value = {};
        bio.value = {};
        notes.value = {};
    }

    async function fetchAssessment(fighterId){
        resetData();
        server.get_assessment(fighterId,onReceiveAssessment);
    }
    /*
    
        data
            assessment
                
            notes

            bio
                name
                ...
    
    */

    return { assessment,bio,fetchAssessment };
});