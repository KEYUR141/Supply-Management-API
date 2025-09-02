// import { createApp } from 'vue'
// import App from './App.vue'

// createApp(App).mount('#app')

import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";   // ⬅️ import router
import './assets/tailwind.css'


const app = createApp(App);
app.use(router);                 // ⬅️ tell Vue to use router
app.mount("#app");
