import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import AllEventsView from "@/views/AllEventsView.vue";
import AnalysisView from "@/views/AnalysisView.vue";
import AssessmentView from "@/views/AssessmentView.vue";
import ProfitView from "@/views/ProfitView.vue";

const router = createRouter({
    history: createWebHistory(),
    routes:[//route objects
        {
            path:'/',
            // redirect:'/v-matchup/1470'
            redirect:'/v-index'
        },
        {
            path:'/v-index',name:'home',
            component : HomeView
        },
        {
            path:'/v-events/:eventId', name:'event-specific',
            component: HomeView
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
        },
        {
            path:'/v-profit',name:'profit',
            component: ProfitView,
        }
        // Prediction route is now added in src/main.js to enable pre-loading data
        // {
        //     path:'/v-predictions',name:'predictions',
        //     component: PredictionsView, 
        // }
        
    ]
})

export default router;