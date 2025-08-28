import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import AllEventsView from "@/views/AllEventsView.vue";
import AnalysisView from "@/views/AnalysisView.vue";
import AssessmentView from "@/views/AssessmentView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes:[//route objects
        {
            path:'/v-events/:eventId', name:'event-specific',
            component: HomeView
        },
        {
            path:'/v-index',name:'home',
            component : HomeView
        },
        {
            path:'/',
            redirect:'/v-assessment/3604'
            // redirect:'/v-index'
        },
        {
            path:'/v-events', name:'events',
            component: AllEventsView
        },
        {
            path:'/v-matchup/:matchupId', name:'analyze',props:true,
            component: AnalysisView
        },
        {
            path:'/v-assessment/:fighterId', name:'assessment',
            component: AssessmentView
        }
        
    ]
})

export default router;