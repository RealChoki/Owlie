import { createApp } from 'vue'
import { createVuetify } from 'vuetify';
import App from './App.vue'
import posthogPlugin from "../plugins/posthog"; //import the plugin. 
import router from './router'

// Import Vuetify styles and other dependencies
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '@fortawesome/fontawesome-free/css/all.css';
import "@/assets/styles/colorVariables.css";
import "@/assets/styles/globalClasses.css";

// Create Vuetify instance
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'dark',
  },
});

// Create Vue app instance
const app = createApp(App);

// Use Vuetify, router, and mount the app
app.use(vuetify);
app.use(router);
app.use(posthogPlugin); //install the plugin

// Mount the app to the DOM
app.mount('#app');
