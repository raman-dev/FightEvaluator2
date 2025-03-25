import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import "bootstrap"
import "bootstrap/dist/css/bootstrap.css"
import { useEventLikelihoodsStore } from './stores/event_likelihoods'


const matchupData = {
     1: {
      title: "Fighter A vs Fighter B",
      events: {
        win: [
          {
            likelihood: "somewhat likely",
            likelihood_val: 2,
            justification: "Fighter A has a strong takedown defense and striking advantage.",
            fighter: "Fighter A"
          },
          {
            likelihood: "somewhat unlikely",
            likelihood_val: 4,
            justification: "Fighter B has shown weakness against similar opponents.",
            fighter: "Fighter B"
          }
        ],
        rounds_geq_one_half: {
          likelihood: "very likely",
          likelihood_val: 1,
          justification: "Both fighters are known for cautious first rounds."
        },
        does_not_go_the_distance: {
          likelihood: "somewhat likely",
          likelihood_val: 2,
          justification: "High knockout rates on both sides indicate early finish potential."
        }
      }
    },
    
    2:{
      title: "Fighter C vs Fighter D",
      events: {
        win: [
          {
            likelihood: "neutral",
            likelihood_val: 3,
            justification: "Both fighters have similar skill levels and fight records.",
            fighter: "Fighter C"
          },
          {
            likelihood: "neutral",
            likelihood_val: 3,
            justification: "Both fighters have similar skill levels and fight records.",
            fighter: "Fighter D"
          }
        ],
        rounds_geq_one_half: {
          likelihood: "somewhat likely",
          likelihood_val: 2,
          justification: "Both tend to pace themselves in earlier rounds."
        },
        does_not_go_the_distance: {
          likelihood: "somewhat unlikely",
          likelihood_val: 4,
          justification: "Neither fighter has a high finish rate in recent fights."
        }
      }
    },
    
    3 : {
      title: "Fighter E vs Fighter F",
      events: {
        win: [
          {
            likelihood: "very likely",
            likelihood_val: 1,
            justification: "Fighter E's grappling dominance is expected to control the match.",
            fighter: "Fighter E"
          },
          {
            likelihood: "very unlikely",
            likelihood_val: 5,
            justification: "Fighter F lacks tools to counter Fighter E's ground game.",
            fighter: "Fighter F"
          }
        ],
        rounds_geq_one_half: {
          likelihood: "neutral",
          likelihood_val: 3,
          justification: "If Fighter E gets an early takedown, a quick finish is possible."
        },
        does_not_go_the_distance: {
          likelihood: "very likely",
          likelihood_val: 1,
          justification: "Fighter E typically finishes fights within the first round."
        }
      }
    }
};

function getPredictionData(urlIn,eventId){
  let url = urlIn;
  if (eventId != undefined){
    url = `${urlIn}/${eventId}`;
  }
  fetch (url,{
    method:'GET'
  })
  .then((response) => response.json())
  .then((data) => {
      console.log(data);
      //populate eventLilelihoodStore

  });
}

const app = createApp(App)
const pinia = createPinia();
app.use(pinia);

const eventLikelihoodStore = useEventLikelihoodsStore();
//fetch here
const testUrl = '/test-data';
const predictionUrl = '/profit-data';
const eventId = 103

getPredictionData(predictionUrl,eventId);
// fetch (testUrl,{method:'GET'})
// .then((response) => response.json())
// .then((data) => {
//     console.log(data)
// });



eventLikelihoodStore.populateData(matchupData);
app.mount('#app')
