<template>
  <nav class="navbar navbar-expand-lg navbar-light sticky-top pb-4">
    <div
      class="container-fluid d-flex justify-content-between align-items-center"
    >
      <img
        src="../icons/MenuOpen.png"
        style="cursor: pointer"
        ref="menuToggleRef"
        @click="toggleBurgerMenu"
      />
      <div class="d-flex flex-column align-items-center position-relative w-50">
        <div class="hearts-container">
          <span
            v-for="(heartClass, index) in heartClasses"
            :key="index"
            :class="['heart-icon', { 'blur-effect': isOpenBurgerMenu }]"
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
        <p :class="['assistant-title', { 'blur-effect': isOpenBurgerMenu }]">
          {{ props.selectedModule }}
        </p>      
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
import { ref, defineEmits, computed, onMounted, onUnmounted, watch } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faPenToSquare,
  faCalendarDays,
  faHeart,
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

library.add(faPenToSquare, faCalendarDays, faHeart);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
  selectedModule: String,
});

const menuToggleRef = ref(null);
const emit = defineEmits(["toggleBurgerMenu"]);

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

const toggleBurgerMenu = () => {
  emit("toggleBurgerMenu", !props.isOpenBurgerMenu);
};

const handlePenClick = async () => {
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

watch(heartCount, (newValue) => {
  setHeartCountLS(newValue);
});

watch(messageCount, (newValue) => {
  setMessageCountLS(newValue);
});

heartCount.value = getHeartCountLS();
messageCount.value = getMessageCountLS();

onMounted(() => {
  const lastRegenTimeKey = 'lastRegenTime';
  const regenIntervalMs = 3 * 60 * 1000; // 3 minutes in milliseconds

  // Retrieve the last regeneration timestamp from localStorage
  const lastRegenTime = parseInt(localStorage.getItem(lastRegenTimeKey) || '0', 10);
  const currentTime = Date.now();

  // Calculate the number of intervals that have passed
  let intervalsPassed = Math.floor((currentTime - lastRegenTime) / regenIntervalMs);

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
  bottom: -18px;
  font-weight: bold;
  white-space: nowrap;
}
</style>
