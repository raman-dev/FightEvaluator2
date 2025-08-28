import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const useAssessmentStore = defineStore('assessment', () => {
    const server = inject('server');

    const sampleFetchResult = {"fighter":{"id":3604,"first_name":"fares","middle_name":null,"last_name":"ziam","nick_name":"N/A","weight_class":"lightweight","height":73,"reach":75,"wins":16,"losses":4,"draws":0,"stance":"orthodox","date_of_birth":"1997-03-21","data_api_link":null,"img_link":"https://images.tapology.com/headshot_images/119061/large/Fares_Ziam-hs.jpg?1667400450","name_index":"fares-ziam"},"assessment":{"id":3603,"fighter":3604,"head_movement":3,"gas_tank":3,"aggression":2,"desire_to_win":3,"striking":3,"chinny":0,"grappling_offense":0,"grappling_defense":3},"notes":[{"data":"Leans over lead leg, susceptible to leg kicks or overhands.","createdAt":"2024-09-26T18:48:44.959Z","id":625},{"data":"Backs up against the cage against aggressive opponents.","createdAt":"2024-09-26T18:52:02.751Z","id":626},{"data":"Knows when to be aggressive and tries to finish his opponents.","createdAt":"2025-01-31T19:50:45.475Z","id":762}]}

    const assessment = ref({});
    const fighter = ref({});
    const notes = ref([]);

    function onReceiveAssessment(data) {
        console.log('Received assessment.data => ', data);
        assessment.value = data.assessment;
        fighter.value = data.fighter;
        notes.value = data.notes;
    }

    function onDeleteNote(deletedNote) {
        // ('Deleted => ',deletedNote);
        //search the list for the corresponding note and delete
        notes.value = notes.value.filter((note) => note.id != deletedNote.noteId);
    }

    function onAddNote(note) {
        //('Added note',note);

        notes.value.push(note);
    }

    function resetData() {
        assessment.value = {};
        fighter.value = {};
        notes.value = [];
    }

    async function fetchAssessment(fighterId) {
        resetData();
        console.log('Fetching => assessment.fighterId.',fighterId);
        // server.get_assessment(fighterId, onReceiveAssessment);
        onReceiveAssessment(sampleFetchResult);
    }

    async function addNote(noteText) {
        server.send_note({
            assessment_id: assessment.value.id,
            data: noteText,
            tag: 'NEUTRAL'
        }, onAddNote);
    }

    async function deleteNote(noteId) {
        server.delete_note(noteId, onDeleteNote);
        // onDeleteNote(noteId);
    }
    /*
    
        data
            assessment
                
            notes

            fighter
                name
                ...
    
    */

    return { assessment, fighter, notes, fetchAssessment, deleteNote, addNote };
});