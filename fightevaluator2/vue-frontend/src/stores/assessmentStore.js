import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const useAssessmentStore = defineStore('assessment', () => {
    const server = inject('server');

    const sampleFetchResult = { 
        "fighter": { "id": 1226, "first_name": "davey", "middle_name": null, "last_name": "grant", "nick_name": "N/A", "weight_class": "bantamweight", "height": 68, "reach": 69, "wins": 15, "losses": 7, "draws": 0, "stance": "Orthodox", "date_of_birth": "1985-12-18", "data_api_link": "https://www.tapology.com/fightcenter/fighters/18815-david-grant", "img_link": "https://images.tapology.com/headshot_images/18815/large/Davey-Grant-hs.jpg?1389648532", "name_index": "davey-grant" }, 
        "assessment": { "id": 1225, "fighter": 1226, "head_movement": 3, "gas_tank": 0, "aggression": 3, "desire_to_win": 3, "striking": 3, "chinny": 0, "grappling_offense": 0, "grappling_defense": 0 }, 
        "notes": [
            { "data": "Good striking volume, always throwing strikes.", "createdAt": "2025-04-03T22:28:19.111Z", "id": 876 }, 
            { "data": "Doesn't switch up into grappling or clinching.", "createdAt": "2025-04-04T15:32:51.721Z", "id": 877 }, 
            { "data": "hello", "createdAt": "2025-08-26T21:02:40.922Z", "id": 959 }] }

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
        server.get_assessment(fighterId, onReceiveAssessment);
        // onReceiveAssessment(sampleFetchResult);
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