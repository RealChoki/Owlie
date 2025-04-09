import { createApp } from 'vue'
import { createVuetify } from 'vuetify'
import i18n from '@/i18n'
import App from './App.vue'
//import posthogPlugin from "../plugins/posthog"; //import the plugin.
import router from './router'

// Import Vuetify styles and other dependencies
import 'vuetify/styles'
import { VBtn, VBtnToggle } from 'vuetify/components'
import 'bootstrap/dist/css/bootstrap.min.css'
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

const vuetify = createVuetify({
  components: {
    VBtn,
    VBtnToggle,
  },
  theme: {
    defaultTheme: 'dark',
  },
})

// Create Vue app instance
const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)
app.use(vuetify)
app.use(router)
app.use(i18n)

// Mount the app to the DOM
app.mount('#app')
