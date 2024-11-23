<template>
  <nav class="navbar navbar-expand-lg navbar-light sticky-top">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <img src="../components/icons/Menu.png" style="cursor: pointer" ref="menuToggleRef" @click="toggleBurgerMenu" />
      <div class="d-flex flex-column align-items-center position-relative w-50">
        <div class="calendar-days-background">
          <font-awesome-icon :icon="['fas', 'calendar-days']" class="calendar-days" />
        </div>
        <p class="assistant-title">{{ props.selectedModule }}</p>
      </div>
      <font-awesome-icon
        :icon="['fas', 'pen-to-square']"
        :class="{ 'pen-to-square': true, 'blur-effect': isOpenBurgerMenu }"
        style="color: #5b5b5b; cursor: pointer"
        @click="handlePenClick"
      />
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPenToSquare, faCalendarDays } from '@fortawesome/free-solid-svg-icons'
import { useThread } from './hooks/useThread' // Adjust the import path accordingly

library.add(faPenToSquare, faCalendarDays)

const props = defineProps({
  isOpenBurgerMenu: Boolean,
  selectedModule: String  // Add selectedModule prop
})

const menuToggleRef = ref(null)
const emit = defineEmits(['toggleBurgerMenu'])

const { clearThread } = useThread(ref(undefined), () => {})

const toggleBurgerMenu = () => {
  emit('toggleBurgerMenu', !props.isOpenBurgerMenu)
}

const handlePenClick = () => {
  if (!props.isOpenBurgerMenu) {
    localStorage.removeItem('newThreadData')
    clearThread()
  }
}

</script>

<style scoped>
.navbar {
  background-color: #131213;
}

.calendar-days-background {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 5.5em;
  height: 2.3em;
  background: linear-gradient(90deg, white, #5b5b5b);
  border-radius: 20px;
  cursor: pointer;
}

.calendar-days {
  font-size: 1.8rem;
  color: #4f4f4f;
}

.pen-to-square {
  font-size: 1.8rem;
}

.blur-effect {
  filter: blur(1.5px);
  cursor: default !important;
  pointer-events: none;
}

.assistant-title {
  background: linear-gradient(90deg, white, #5b5b5b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 12px;
  margin: 0;
  position: absolute;
  bottom: -23px;
  font-weight: bold;
  white-space: nowrap;
}
</style>
