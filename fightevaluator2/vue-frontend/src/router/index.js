import { createRouter,createMemoryHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";
import AllEventsView from "@/views/AllEventsView.vue";

const router = createRouter({
    history: createMemoryHistory(),
    routes:[
        //route objects
        {
            path:'/',
            name:'home',
            component : HomeView
        },
        {
            path:'/events',
            name:'events',
            component: AllEventsView
        }
    ]
    //when building prepend index-vue to all links
    // routes:[
    //     //route objects
    //     {
    //         path:'/index-vue',
    //         name:'home',
    //         component : HomeView
    //     }
    // ]
})

export default router;