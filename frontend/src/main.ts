import './assets/main.css'

import { createApp } from 'vue'
import { createVuetify } from 'vuetify';
import App from './App.vue'
import router from './router'

// Import Vuetify styles and other dependencies
import 'vuetify/styles';
import '@mdi/font/css/materialdesignicons.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import '@fortawesome/fontawesome-free/css/all.css';

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

// Mount the app to the DOM
app.mount('#app');
