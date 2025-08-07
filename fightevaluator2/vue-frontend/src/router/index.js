import { createRouter, createWebHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import AllEventsView from "@/views/AllEventsView.vue";

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
            path:'/v-events', name:'events',
            component: AllEventsView
        },
        
    ]
})

export default router;