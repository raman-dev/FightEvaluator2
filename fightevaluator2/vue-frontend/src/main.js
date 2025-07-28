


import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router';

import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.bundle';



import App from './App.vue'

function getCookie(name) {
    let raw = document.cookie;
    let cookies = raw.split(';');
    let cookieMap = {};
    for (const rawCookie of cookies) {
        let [key,value] = rawCookie.split('=');
        cookieMap[key.trim()]=value.trim();
    }

    if (name in cookieMap) {
        return cookieMap[name];
    }
    return null;
}
//get csrf token from cookies


const app = createApp(App)

app.provide('csrftoken',getCookie('csrftoken'));
app.use(createPinia())
app.use(router);
app.mount('#app')
