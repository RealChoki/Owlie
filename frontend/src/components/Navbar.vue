<template>
  <nav class="navbar navbar-expand-lg navbar-light sticky-top">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <img src="../icons/MenuOpen.png" style="cursor: pointer" ref="menuToggleRef" @click="toggleBurgerMenu" />
      <div class="d-flex flex-column align-items-center position-relative w-50">
        <div class="hearts-container">
          <span
            v-for="(heartClass, index) in heartClasses"
            :key="index"
            :class="['heart-icon', heartClass]"
          >
            ♥
          </span>
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
import { ref, defineEmits, computed, onMounted, onUnmounted, watch } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faPenToSquare, faCalendarDays, faHeart } from '@fortawesome/free-solid-svg-icons';
import { useThread } from '../hooks/useThread';
import { heartCount, messageCount, clearMessages } from '../services/chatService';
import { 
  getHeartCountLS, 
  setHeartCountLS, 
  getMessageCountLS, 
  setMessageCountLS 
} from '../services/localStorageService';

library.add(faPenToSquare, faCalendarDays, faHeart);

const props = defineProps({
  isOpenBurgerMenu: Boolean,
  selectedModule: String,
});

const menuToggleRef = ref(null);
const emit = defineEmits(['toggleBurgerMenu']);

const { clearThread, initializeThread } = useThread(ref(undefined), () => {});

const toggleBurgerMenu = () => {
  emit('toggleBurgerMenu', !props.isOpenBurgerMenu);
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
    const heartPosition = index * 2; // Positions 2,4,6,8,10
    if (heartPosition - 1 < halvesRemaining) {
      classes.push('heart-filled');
    } else if (heartPosition - 2 < halvesRemaining) {
      classes.push('heart-half-filled');
    } else {
      classes.push('heart-empty');
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
  const regenInterval = setInterval(() => {
    if (heartCount.value < totalHearts) {
      heartCount.value += 0.5; // Regenerate half a heart
      if (heartCount.value > totalHearts) {
        heartCount.value = totalHearts; // Cap at totalHearts
      }
      console.log(`[Navbar.vue] Regenerated half a heart. New heartCount: ${heartCount.value}`);
    }
  }, 3 * 60 * 1000); // Every 3 minutes

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
}

.heart-icon {
  font-size: 2rem;
  padding: 0;
  margin: 0 2px;
  line-height: 1; /* Ensure no extra space around the icon */
}

.heart-filled {
  background: linear-gradient(to right, white, #5b5b5b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.heart-half-filled {
  background: linear-gradient(to right, white, #5b5b5b);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  position: relative;
}

.heart-half-filled::after {
  content: '';
  position: absolute;
  top: 0;
  right: 0;
  width: 50%;
  height: 100%;
  background-color: #131213; /* Match the background color */
}

.heart-empty {
  color: #131213; 
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
