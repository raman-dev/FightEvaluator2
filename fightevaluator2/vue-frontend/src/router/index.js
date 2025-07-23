import { createRouter,createMemoryHistory } from "vue-router";

import HomeView from "@/views/HomeView.vue";

const router = createRouter({
    history: createMemoryHistory(),
    routes:[
        //route objects
        {
            path:'/',
            name:'home',
            component : HomeView
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