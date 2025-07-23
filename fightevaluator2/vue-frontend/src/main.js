


import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter } from 'vue-router'

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle';



import App from './App.vue'

const app = createApp(App)

app.use(createPinia())
app.mount('#app')
