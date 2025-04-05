<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light pb-4">
      <div class="container-fluid">
        <svg
          v-if="!isWideScreen"
          width="27"
          height="27"
          viewBox="0 0 100 100"
          xmlns="http://www.w3.org/2000/svg"
          class="mt-3 icon-click-effect cursor-pointer"
          @click="toggleBurgerMenu"
        >
          <rect x="0" y="15" width="100" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
          <rect x="0" y="44" width="66" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
          <rect x="0" y="73" width="33" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
        </svg>

        <svg
          v-else-if="isWideScreen && !isSidebarOpen"
          width="27"
          height="27"
          viewBox="0 0 100 100"
          xmlns="http://www.w3.org/2000/svg"
          class="mt-3 icon-click-effect cursor-pointer"
          @click="toggleSidebar"
        >
          <rect x="0" y="15" width="100" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
          <rect x="0" y="44" width="66" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
          <rect x="0" y="73" width="33" height="12" rx="4" fill="var(--buger-menu-icon-open)" />
        </svg>
        <div v-else class="nav-icon-holder mt-3">
          <font-awesome-icon
            class="icon-click-effect cursor-pointer nav-icon"
            :icon="['fas', 'arrows-rotate']"
            @click="handleRefreshClick"
            style="color: var(--reload-icon-left); opacity: 0.85"
          />
        </div>
        <div class="d-flex flex-column align-items-center position-relative w-50">
          <div class="hearts-container d-flex align-items-center gap-0.5">
            <span
              v-for="(heartClass, index) in heartClasses"
              :key="index"
              class="heart-icon"
              @mouseenter="showTooltip"
              @mousemove="moveTooltip"
              @mouseleave="hideTooltip"
            >
              <template v-if="heartClass === 'heart-filled'">
                <!-- Full Heart -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30">
                  <defs>
                    <linearGradient id="heartGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="24" y2="0">
                      <stop offset="0%" stop-color="var(--hearts-bg-start)" />
                      <stop offset="100%" stop-color="var(--hearts-bg-end)" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M16.4,4C14.6,4,13,4.9,12,6.3C11,4.9,9.4,4,7.6,4C4.5,4,2,6.5,2,9.6C2,14,12,22,12,22s10-8,10-12.4C22,6.5,19.5,4,16.4,4z"
                    fill="url(#heartGradient)"
                    stroke="url(#heartGradient)"
                    stroke-width="2"
                  />
                </svg>
              </template>

              <template v-else-if="heartClass === 'heart-half-filled'">
                <!-- Half-Filled Heart -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30">
                  <defs>
                    <linearGradient id="halfHeartGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="24" y2="0">
                      <stop offset="0%" stop-color="var(--hearts-bg-start)" />
                      <stop offset="100%" stop-color="var(--hearts-bg-end)" />
                    </linearGradient>
                    <clipPath id="leftHalf">
                      <rect x="0" y="0" width="12" height="24"></rect>
                    </clipPath>
                  </defs>
                  <path
                    d="M16.4,4C14.6,4,13,4.9,12,6.3C11,4.9,9.4,4,7.6,4C4.5,4,2,6.5,2,9.6C2,14,12,22,12,22s10-8,10-12.4C22,6.5,19.5,4,16.4,4z"
                    fill="url(#halfHeartGradient)"
                    clip-path="url(#leftHalf)"
                    stroke="url(#halfHeartGradient)"
                    stroke-width="2"
                  />
                  <!-- Border for the Right Side -->
                  <path
                    d="M16.4,4C14.6,4,13,4.9,12,6.3C11,4.9,9.4,4,7.6,4C4.5,4,2,6.5,2,9.6C2,14,12,22,12,22s10-8,10-12.4C22,6.5,19.5,4,16.4,4z"
                    fill="none"
                    stroke="url(#halfHeartGradient)"
                    stroke-width="2"
                  />
                </svg>
              </template>

              <template v-else>
                <!-- Empty Heart -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30">
                  <defs>
                    <linearGradient id="emptyHeartGradient" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="24" y2="0">
                      <stop offset="0%" stop-color="var(--hearts-bg-start)" />
                      <stop offset="100%" stop-color="var(--hearts-bg-end)" />
                    </linearGradient>
                  </defs>
                  <path
                    d="M16.4,4C14.6,4,13,4.9,12,6.3C11,4.9,9.4,4,7.6,4C4.5,4,2,6.5,2,9.6C2,14,12,22,12,22s10-8,10-12.4C22,6.5,19.5,4,16.4,4z"
                    fill="none"
                    stroke="url(#emptyHeartGradient)"
                    stroke-width="2"
                  />
                </svg>
              </template>
            </span>
            <div v-if="tooltipVisible" class="tooltip" :style="tooltipStyle">Tokens: {{ userMessageTokens }}</div>
          </div>
          <p class="assistant-title">
            {{ navbarCourseTitle }}
          </p>
        </div>
        <div class="nav-icon-holder mt-3">
          <font-awesome-icon
            v-if="isWideScreen && isSidebarOpen"
            class="nav-icon cursor-pointer icon-click-effect"
            :icon="['fas', 'user-circle']"
            @click="toggleProfileMenu"
            style="color: var(--profile-icon-navbar);"
          />
          <font-awesome-icon
            v-else
            class="nav-icon"
            :class="{ 'cursor-pointer icon-click-effect': !isBurgerMenuOpen }"
            :icon="['fas', 'arrows-rotate']"
            @click="handleRefreshClick"
            style="color: var(--reload-icon-right);"
          />
        </div>
      </div>
      <Profilemenu
        v-if="isProfileMenuVisible"
        :origin="'Nav'"
        @toggleProfileMenu="toggleProfileMenu"
        @openSettings="openSettings"
      />
    </nav>
    <SettingsMenuModal />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useThread } from '../hooks/useThread'
import { useScreenWidth } from '../utils/useScreenWidth'
import Profilemenu from '@/widgets/Profilemenu.vue'
import SettingsMenuModal from '@/home-components/SettingsMenuModal.vue'
import { heartCount, clearMessages, userMessageTokens } from '../services/chatService'
import { getHeartCountLS, setHeartCountLS } from '../services/localStorageService'
import { navbarCourseTitle } from '../services/homeService'
import {
  totalHearts,
  initializeHeartCount,
  setupHeartRegeneration,
  handleStorageChange,
  heartClasses
} from '../services/heartService'
import * as bootstrap from 'bootstrap'

// FontAwesome library setup

// Props and emits
const props = defineProps({
  isBurgerMenuOpen: Boolean,
  isSidebarOpen: Boolean
})
const emit = defineEmits(['toggleBurgerMenu', 'toggleSidebar'])

const isProfileMenuVisible = ref(false)
const showSettings = ref(false)

const { isWideScreen } = useScreenWidth()

const { clearThread, initializeThread } = useThread(ref(undefined), () => {})

const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value
}

function openModal(modalId: string) {
  const modalElement = document.getElementById(modalId)
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement)
    modal.show()
  }
}

function openSettings() {
  showSettings.value = true
  isProfileMenuVisible.value = false // ensure the profile menu closes
  openModal('settingsModal')
}

const tooltipVisible = ref(false)
const tooltipStyle = ref({ top: '0px', left: '0px' })

const showTooltip = () => {
  tooltipVisible.value = true
}

const hideTooltip = () => {
  tooltipVisible.value = false
}

const moveTooltip = (event) => {
  tooltipStyle.value = {
    top: `${event.clientY + 10}px`, // Add 10px to avoid overlap
    left: `${event.clientX + 10}px` // Add 10px to avoid overlap
  }
}

const toggleBurgerMenu = () => {
  emit('toggleBurgerMenu', !props.isBurgerMenuOpen)
}

const toggleSidebar = () => {
  emit('toggleSidebar', !props.isSidebarOpen)
}

const handleRefreshClick = async () => {
  if (!props.isBurgerMenuOpen) {
    clearMessages(false)
    clearThread()
    await initializeThread()
  }
}

function handleResize() {
  if (window.innerWidth <= 768) {
    isProfileMenuVisible.value = false
  }
}

watch(heartCount, (newValue) => {
  setHeartCountLS(newValue)
})

onMounted(() => {
  window.addEventListener('resize', handleResize)
  window.addEventListener('storage', handleStorageChange)
  handleResize()
  initializeHeartCount()
  const regenInterval = setupHeartRegeneration()

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    window.removeEventListener('storage', handleStorageChange)
    clearInterval(regenInterval)
  })
})
</script>

<style scoped>
.nav-icon {
  font-size: 1.8rem;
}

.heart-icon svg {
  transition: transform 0.3s ease;
}

.heart-icon svg:hover {
  transform: scale(1.1);
}

.assistant-title {
  background: var(--assistant-title-gradient);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 12px;
  margin: 0;
  position: absolute;
  bottom: -18px;
  font-weight: bold;
  white-space: nowrap;
}

.tooltip {
  position: fixed;
  background-color: #333;
  color: white;
  padding: 5px 8px;
  border-radius: 4px;
  font-size: 12px;
  white-space: nowrap;
  z-index: 10;
  pointer-events: none;
  opacity: 0.9;
  transition: opacity 0.2s;
}
</style>
