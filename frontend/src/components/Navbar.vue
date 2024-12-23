<template>
  <nav class="navbar navbar-expand-lg navbar-light pb-4">
    <div
      class="container-fluid"
    >
      <img
      v-if="!isWideScreen"
        class="mt-3 icon-click-effect"
        src="../icons/MenuOpen.png"
        style="cursor: pointer"
        @click="toggleBurgerMenu"
      />
      <img
      v-else-if="isWideScreen && !isOpenSidebar"
        class="mt-3 icon-click-effect"
        src="../icons/MenuOpen.png"
        style="cursor: pointer"
        @click="toggleSidebar"
      />
      <div v-else class="icon-holder mt-3"> 
        <font-awesome-icon
          class="icon-click-effect"
          :icon="['fas', 'arrows-rotate']"
          :class="{ 'arrows-rotate': true}"
          style="color: #5b5b5b; cursor: pointer"
          @click="handleRefreshClick"
        />
      </div>
      <div class="d-flex flex-column align-items-center position-relative w-50"
        
      >

        <div class="hearts-container">
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
                    <stop offset="100%" stop-color="#5b5b5b" />
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
                    <stop offset="100%" stop-color="#5b5b5b" />
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
                    <stop offset="100%" stop-color="#5b5b5b" />
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
      <div class="icon-holder mt-3">
      <!-- if user doesnt have pfp -->
        <!-- <font-awesome-icon
          class="arrows-rotate icon-click-effect"
          v-if="isWideScreen && isOpenSidebar"
          :icon="['fas', 'user-circle']"
          style="color: #5b5b5b; cursor: pointer"
        /> -->
        <div 
        v-if="isWideScreen && isOpenSidebar"
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle icon-click-effect"
            style="width: 32px; height: 32px"
          >
            <img
              alt="User"
              src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
              class="img-fluid rounded-circle"
              style="width: 100%; height: 100%"
              @click="togglePopover"
            />
          </div>
        <font-awesome-icon
        v-else
          class="icon-click-effect arrows-rotate"
          :icon="['fas', 'arrows-rotate']"
          style="color: #5b5b5b; cursor: pointer"
          @click="handleRefreshClick"
        />
      </div>
    </div>
      <ProfileMenus
        v-if="isPopoverVisible"
        :origin="'Nav'"
        @togglePopover="togglePopover"
       />
  </nav>
</template>

<script setup lang="ts">
import { ref, defineEmits, computed, onMounted, onUnmounted, watch } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faArrowsRotate,
  faHeart,
  faUser
} from "@fortawesome/free-solid-svg-icons";
import { useThread } from "../hooks/useThread";
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
import { useScreenWidth } from "../utils/useScreenWidth";
import { navbarCourseTitle } from "../services/homeService";
import ProfileMenus from "@/widgets/ProfileMenus.vue";

library.add(faArrowsRotate, faHeart, faUser);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
  isOpenSidebar: Boolean
});

const isPopoverVisible = ref(false);
const togglePopover = () => {
  isPopoverVisible.value = !isPopoverVisible.value;
};

const emit = defineEmits(["toggleBurgerMenu", "toggleSidebar"]);

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

const toggleBurgerMenu = () => {
  emit("toggleBurgerMenu", !props.isOpenBurgerMenu);
};

const toggleSidebar = () => {
  emit("toggleSidebar", !props.isOpenSidebar);
};

const handleRefreshClick = async () => {
  if (!props.isOpenBurgerMenu) {
    clearMessages(false); // Do not reset heartCount
    clearThread();
    await initializeThread();
  }
};

const totalHearts = 5;

const heartClasses = computed(() => {
  const classes = [];
  const halvesRemaining = heartCount.value * 2; // Convert heartCount to halves

  for (let index = 1; index <= totalHearts; index++) {
    const heartPosition = index * 2; // Positions 2, 4, 6, 8, 10
    if (heartPosition - 1 < halvesRemaining) {
      classes.push("heart-filled");
    } else if (heartPosition - 2 < halvesRemaining) {
      classes.push("heart-half-filled");
    } else {
      classes.push("heart-empty");
    }
  }
  return classes;
});

function handleResize() {
  if (window.innerWidth <= 768) {
    isPopoverVisible.value = false;
  }
}

const handleStorageChange = (event: StorageEvent) => {
  if (event.key === 'heartCount') {
    const newHeartCount = parseFloat(event.newValue || '');
    if (!isNaN(newHeartCount)) {
      heartCount.value = newHeartCount;
    }
  }
};

watch(heartCount, (newValue) => {
  setHeartCountLS(newValue);
});

watch(messageCount, (newValue) => {
  setMessageCountLS(newValue);
});

heartCount.value = getHeartCountLS();
messageCount.value = getMessageCountLS();

const { isWideScreen } = useScreenWidth();

onMounted(() => {
  window.addEventListener("resize", handleResize);
  handleResize();
  const lastRegenTimeKey = "lastRegenTime";
  const regenIntervalMs = 3 * 60 * 1000; // 3 minutes in milliseconds

  // Retrieve the last regeneration timestamp from localStorage
  const lastRegenTime = parseInt(
    localStorage.getItem(lastRegenTimeKey) || "0",
    10
  );
  const currentTime = Date.now();

  // Calculate the number of intervals that have passed
  let intervalsPassed = Math.floor(
    (currentTime - lastRegenTime) / regenIntervalMs
  );

  // Update the heart count based on the intervals passed
  if (intervalsPassed > 0 && heartCount.value < totalHearts) {
    let heartsToAdd = intervalsPassed * 0.5; // Each interval adds 0.5 heart
    heartCount.value += heartsToAdd;
    if (heartCount.value > totalHearts) {
      heartCount.value = totalHearts; // Cap at totalHearts
    }
    setHeartCountLS(heartCount.value);
  }

  // Update the last regeneration time
  localStorage.setItem(lastRegenTimeKey, currentTime.toString());
  window.addEventListener('storage', handleStorageChange);
  // Start the interval for future regeneration
  const regenInterval = setInterval(() => {
    if (heartCount.value < totalHearts) {
      heartCount.value += 0.5; // Regenerate half a heart
      if (heartCount.value > totalHearts) {
        heartCount.value = totalHearts; // Cap at totalHearts
      }
      setHeartCountLS(heartCount.value);

      // Update the last regeneration time
      localStorage.setItem(lastRegenTimeKey, Date.now().toString());
    }
  }, regenIntervalMs);

  onUnmounted(() => {
    window.removeEventListener("resize", handleResize);
    window.removeEventListener('storage', handleStorageChange);
    clearInterval(regenInterval);
  });
});
</script>
<style scoped>
.navbar {
  background-color: #131213;
}

.hearts-container {
  display: flex;
  align-items: center;
  gap: 0.1em;
}

.heart-icon svg {
  transition: transform 0.3s ease;
}

.heart-icon svg:hover {
  transform: scale(1.1);
}

.arrows-rotate {
  font-size: 1.8rem;
}

.icon-holder {
  width: 29px;
}

.assistant-title {
  background: linear-gradient(90deg, white, #5b5b5b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 12px;
  margin: 0;
  position: absolute;
  bottom: -18px;
  font-weight: bold;
  white-space: nowrap;
}

.icon-click-effect {
  cursor: pointer;
  display: inline-block;
  transition: transform 0.2s ease;
}

.icon-click-effect:active {
  transform: scale(0.9);
}

.popover {
  width: 100%;
  top: 4.5em;
  right: 0;
  background-color: #2a2a2a;
  border-color: #414141;
  border-width: 1px;
}

.popover nav a:hover {
  background-color: #414141;
}
</style>
