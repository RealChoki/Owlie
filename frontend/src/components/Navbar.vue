<template>
  <nav class="navbar navbar-expand-lg navbar-light pb-4">
    <div class="container-fluid">
      <img
        v-if="!isWideScreen"
        class="mt-3 icon-click-effect cursor-pointer"
        src="../assets/icons/MenuOpen.png"
        @click="toggleBurgerMenu"
      />
      <img
        v-else-if="isWideScreen && !isSidebarOpen"
        class="mt-3 icon-click-effect cursor-pointer"
        src="../assets/icons/MenuOpen.png"
        @click="toggleSidebar"
      />
      <div v-else class="nav-icon-holder mt-3">
        <font-awesome-icon
          class="icon-click-effect cursor-pointer nav-icon"
          :icon="['fas', 'arrows-rotate']"
          @click="handleRefreshClick"
          style="color: var(--color-white); opacity: 0.85;"
        />
      </div>
      <div class="d-flex flex-column align-items-center position-relative w-50">
        <div class="hearts-container d-flex align-items-center gap-0.5">
          <span
            v-for="(heartClass, index) in heartClasses"
            :key="index"
            class="heart-icon"
          >
            <template v-if="heartClass === 'heart-filled'">
              <!-- Full Heart -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="30"
                height="30"
              >
                <defs>
                  <linearGradient
                    id="heartGradient"
                    gradientUnits="userSpaceOnUse"
                    x1="0"
                    y1="0"
                    x2="24"
                    y2="0"
                  >
                    <stop offset="0%" stop-color="white" />
                    <stop offset="100%" stop-color="var(--color-gray-shadow)" />
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="30"
                height="30"
              >
                <defs>
                  <linearGradient
                    id="halfHeartGradient"
                    gradientUnits="userSpaceOnUse"
                    x1="0"
                    y1="0"
                    x2="24"
                    y2="0"
                  >
                    <stop offset="0%" stop-color="white" />
                    <stop offset="100%" stop-color="var(--color-gray-shadow)" />
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
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="30"
                height="30"
              >
                <defs>
                  <linearGradient
                    id="emptyHeartGradient"
                    gradientUnits="userSpaceOnUse"
                    x1="0"
                    y1="0"
                    x2="24"
                    y2="0"
                  >
                    <stop offset="0%" stop-color="white" />
                    <stop offset="100%" stop-color="var(--color-gray-shadow)" />
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
        </div>
        <p class="assistant-title">
          {{ navbarCourseTitle }}
        </p>
      </div>
      <div class="nav-icon-holder mt-3">
        <div
          v-if="isWideScreen && isSidebarOpen"
          class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle icon-click-effect cursor-pointer pfp-container"
        >
          <img
            alt="User"
            src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
            class="img-fluid rounded-circle"
            @click="toggleProfileMenu"
          />
        </div>
        <font-awesome-icon
          v-else
          class="nav-icon"
          :class="{ 'cursor-pointer icon-click-effect': !isBurgerMenuOpen }"
          :icon="['fas', 'arrows-rotate']"
          @click="handleRefreshClick"
        />
      </div>
    </div>
    <Profilemenu
      v-if="isProfileMenuVisible"
      :origin="'Nav'"
      @toggleProfileMenu="toggleProfileMenu"
    />
  </nav>
</template>

<script setup lang="ts">
import {
  ref,
  computed,
  watch,
  onMounted,
  onUnmounted,
} from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faArrowsRotate,
  faHeart,
  faUserCircle,
} from "@fortawesome/free-solid-svg-icons";
import { useThread } from "../hooks/useThread";
import { useScreenWidth } from "../utils/useScreenWidth";
import Profilemenu from "@/widgets/Profilemenu.vue";
import {
  heartCount,
  messageCount,
  clearMessages,
} from "../services/chatService";
import {
  getHeartCountLS,
  setHeartCountLS,
  getMessageCountLS,
  setMessageCountLS,
} from "../services/localStorageService";
import { navbarCourseTitle } from "../services/homeService";
import {
  totalHearts,
  initializeHeartCount,
  setupHeartRegeneration,
  handleStorageChange,
  heartClasses,
} from "../services/heartService";

// FontAwesome library setup
library.add(faArrowsRotate, faHeart, faUserCircle);

// Props and emits
const props = defineProps({
  isBurgerMenuOpen: Boolean,
  isSidebarOpen: Boolean,
});
const emit = defineEmits(["toggleBurgerMenu", "toggleSidebar"]);

const isProfileMenuVisible = ref(false);
const { isWideScreen } = useScreenWidth();

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
};

const toggleBurgerMenu = () => {
  emit("toggleBurgerMenu", !props.isBurgerMenuOpen);
};

const toggleSidebar = () => {
  emit("toggleSidebar", !props.isSidebarOpen);
};

const handleRefreshClick = async () => {
  if (!props.isBurgerMenuOpen) {
    clearMessages(false);
    clearThread();
    await initializeThread();
  }
};

function handleResize() {
  if (window.innerWidth <= 768) {
    isProfileMenuVisible.value = false;
  }
}

watch(heartCount, (newValue) => {
  setHeartCountLS(newValue);
});

watch(messageCount, (newValue) => {
  setMessageCountLS(newValue);
});

onMounted(() => {
  window.addEventListener("resize", handleResize);
  window.addEventListener("storage", handleStorageChange);
  handleResize();
  initializeHeartCount();
  const regenInterval = setupHeartRegeneration();

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
    window.removeEventListener("storage", handleStorageChange);
    clearInterval(regenInterval);
  });
});
</script>


<style scoped>
.nav-icon {
  color: var(--color-gray-shadow);
  font-size: 1.8rem;
}

.heart-icon svg {
  transition: transform 0.3s ease;
}

.heart-icon svg:hover {
  transform: scale(1.1);
}

.assistant-title {
  background: linear-gradient(90deg, white, var(--color-gray-shadow));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 12px;
  margin: 0;
  position: absolute;
  bottom: -18px;
  font-weight: bold;
  white-space: nowrap;
}





</style>
