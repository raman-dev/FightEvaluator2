import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const useAssessmentStore = defineStore('assessment', () => {
    const server = inject('server');

    const sampleFetchResult = {
        "fighter": {
            "id": 1226,
            "first_name": "davey",
            "middle_name": null,
            "last_name": "grant",
            "nick_name": "N/A",
            "weight_class": "bantamweight",
            "height": 68,
            "reach": 69,
            "wins": 15,
            "losses": 7,
            "draws": 0,
            "stance": "Orthodox",
            "date_of_birth": "1985-12-18",
            "data_api_link": "https://www.tapology.com/fightcenter/fighters/18815-david-grant",
            "img_link": "https://images.tapology.com/headshot_images/18815/large/Davey-Grant-hs.jpg?1389648532",
            "name_index": "davey-grant"
        },
        "assessment": {
            "id": 1225,
            "fighter": 1226,
            "head_movement": 3,
            "gas_tank": 0,
            "aggression": 3,
            "desire_to_win": 3,
            "striking": 3,
            "chinny": 0,
            "grappling_offense": 0,
            "grappling_defense": 0
        },
        "notes": [
            {
                "data": "Good striking volume, always throwing strikes.",
                "createdAt": "2025-04-03T22:28:19.111Z"
            },
            {
                "data": "Doesn't switch up into grappling or clinching.",
                "createdAt": "2025-04-04T15:32:51.721Z"
            }
        ]
    }

    const assessment = ref({});
    const fighter = ref({});
    const notes = ref([]);

    function onReceiveAssessment(data) {
        console.log('Received data => ', data);
        assessment.value = data.assessment;
        fighter.value = data.fighter;
        notes.value = data.notes;
    }

    function resetData() {
        assessment.value = {};
        fighter.value = {};
        notes.value = [];
    }

    async function fetchAssessment(fighterId) {
        resetData();
        // server.get_assessment(fighterId, onReceiveAssessment);
        onReceiveAssessment(sampleFetchResult);
    }
    /*
    
        data
            assessment
                
            notes

            fighter
                name
                ...
    
    */

    return { assessment, fighter,notes, fetchAssessment };
});