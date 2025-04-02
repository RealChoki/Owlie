<template>
  <div
    ref="ProfileMenuRef"
    class="popover profile-menu position-absolute z-50"
    :style="{ ...positionStyle }"
    :class="{
      'profile-menu-nav': props.origin === 'Nav',
      'profile-menu-burger': props.origin === 'BurgerMenu',
      'profile-menu-nav-edit-quiz': props.origin === 'Nav-EditQuiz'
    }"
  >
    <nav class="p-2 text-white">
      <div ref="ProfileMenuUniversityRef" class="p-2">Hochschule für Technik und Wirtschaft Berlin</div>
      <hr class="my-1" />
      <a
        href="#"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
        @click="navigateToProfile"
      >
        <font-awesome-icon :icon="['fas', 'user-circle']" /> Profile
      </a>
      <a
        @click="emit('openSettings')"
        class="cursor-pointer d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="['fas', 'gear']" /> Settings
      </a>
      <a
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded cursor-pointer"
        @click="navigateToAboutUs"
      >
        <font-awesome-icon :icon="['fas', 'info-circle']" /> About Us
      </a>
      <a class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded cursor-pointer" @click="logout">
        <font-awesome-icon :icon="['fas', 'right-from-bracket']" /> Log Out
      </a>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, PropType } from 'vue'
import type { Ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserCircle, faGear, faRightFromBracket, faInfoCircle } from '@fortawesome/free-solid-svg-icons'
import { useRouter } from 'vue-router'

// Add icons to library
library.add(faUserCircle, faGear, faRightFromBracket, faInfoCircle)
const router = useRouter()

// Props
const props = defineProps({
  origin: {
    type: String as PropType<'BurgerMenu' | 'Nav' | 'Nav-EditQuiz'>,
    required: true
  },
  toggleProfileMenu: {
    type: Function,
    required: false
  }
})

// Refs
const emit = defineEmits(['toggleProfileMenu'])

const ProfileMenuRef: Ref<HTMLElement | null> = ref(null)
const ProfileMenuUniversityRef: Ref<HTMLElement | null> = ref(null)
const positionStyle = ref<Partial<CSSStyleDeclaration>>(null)
const isFirstClick = ref(true)

// Function to update ProfileMenu position based on height
function updateProfileMenuPosition() {
  if (props.origin !== 'BurgerMenu') return
  const universityHeight = ProfileMenuUniversityRef.value?.offsetHeight || 0

  positionStyle.value = {
    top: universityHeight > 63 ? '-175px' : universityHeight > 42 ? '-155px' : '-135px'
  }
}

function logout() {
  router.push('/login')
}

function navigateToAboutUs() {
  router.push('/about')
}

function navigateToProfile() {
  router.push('/profile')
}

// ResizeObserver handler
function handleHeightChange(entries: ResizeObserverEntry[]) {
  updateProfileMenuPosition()
}
function handleClickOutside(event: MouseEvent) {
  if (isFirstClick.value) {
    isFirstClick.value = false
    return
  }
  if (ProfileMenuRef.value && !ProfileMenuRef.value.contains(event.target as Node)) {
    emit('toggleProfileMenu')
  }
}

let resizeObserver: ResizeObserver | null = null

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  if (ProfileMenuUniversityRef.value) {
    resizeObserver = new ResizeObserver(handleHeightChange)
    resizeObserver.observe(ProfileMenuUniversityRef.value)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (resizeObserver && ProfileMenuUniversityRef.value) {
    resizeObserver.unobserve(ProfileMenuUniversityRef.value)
  }
  resizeObserver?.disconnect()
})
</script>

<style scoped>
.profile-menu {
  z-index: 9999;
  width: 100%;
  background-color: var(--color-gray-medium);
  border-color: var(--color-gray-light);
  border-width: 1px;
}

.profile-menu nav a:hover {
  background-color: var(--color-gray-light);
}

/* from burger-menu */
.profile-menu-burger {
  top: -135px;
  left: transformX(-50%);
  max-width: 450px;
}

/* from nav */
.profile-menu-nav {
  top: 4.5em;
  right: 0;
}

.profile-menu-nav-edit-quiz {
  top: 3.5em;
  right: 0;
}
</style>
