import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import App from './App.vue'
//import posthogPlugin from "../plugins/posthog"; //import the plugin.
import router from './router'

// Import Vuetify styles and other dependencies
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import '@fortawesome/fontawesome-free/css/all.css'
import '@/assets/styles/colorVariables.css'
import '@/assets/styles/globalClasses.css'

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {
  faChevronDown,
  faChevronUp,
  faUserCircle,
  faGear,
  faRightFromBracket,
  faInfoCircle,
  faDownLeftAndUpRightToCenter,
  faArrowUp,
  faXmark,
  faHome,
  faMagnifyingGlass,
  faCircleInfo,
  faArrowsRotate,
  faHeart,
  faUpRightAndDownLeftFromCenter,
  faPlus,
  faStop,
  faFile,
  faTimes,
  faCopy,
  faCheck,
  faArrowRotateRight,
  faVolumeHigh,
  faVolumeXmark
} from '@fortawesome/free-solid-svg-icons'

library.add(
  faChevronDown,
  faChevronUp,
  faUserCircle,
  faGear,
  faRightFromBracket,
  faInfoCircle,
  faDownLeftAndUpRightToCenter,
  faArrowUp,
  faXmark,
  faHome,
  faMagnifyingGlass,
  faCircleInfo,
  faArrowsRotate,
  faHeart,
  faUpRightAndDownLeftFromCenter,
  faPlus,
  faStop,
  faFile,
  faTimes,
  faCopy,
  faCheck,
  faArrowRotateRight,
  faVolumeHigh,
  faVolumeXmark
)

// Import Vuetify components and directives
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// Create Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'dark'
  }
})

// Create Vue app instance
const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(vuetify)
app.use(router)

// Mount the app to the DOM
app.mount('#app')
