<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
      <div
        class="container-fluid d-flex justify-content-between align-items-center"
      >
        <!-- Burger icon -->
        <img src="../components/icons/Menu.png" />
        
        <div class="calendar-days-background">
          <font-awesome-icon :icon="['fas', 'calendar-days']"
          class="calendar-days" 
          />
        </div>

        <!-- Action buttons -->
        <font-awesome-icon :icon="['fas', 'pen-to-square']" 
        class="pen-to-square"
        style="color: #5b5b5b;"
        />
        
      </div>
    </nav>

    <div class="container my-4 logo-container">
      <img class="original-logo" src="../components/icons/ChatGPT.png" />
      <div class="arrow-container">
        <div class="arrow-text">don't sue</div>
        <font-awesome-icon :icon="['fas', 'arrow-right-long']" class="arrow" />
      </div>
    </div>

    <!-- Sticky input bar at the bottom -->
    <div class="d-flex gap-2 sticky-footer mb-3">
      <!-- Plus icon button with circular style -->
      <font-awesome-icon
        :icon="['fas', 'plus']"
        class="cursor-pointer btn-circle"
        style="background-color: #5b5b5b;"
      />

      <!-- Message input -->
      <input
        type="text"
        class="custom-input"
        placeholder="Type a message..."
        aria-label="Message input"
        v-model="message"
      />

      <!-- Conditional Send/Voice icon with circular style -->
      <font-awesome-icon
        v-if="message"
        :icon="['fas', 'arrow-up']"
        class="cursor-pointer btn-circle bg-light"
      />
      <font-awesome-icon
        v-else
        :icon="['fas', 'volume-high']"
        class="cursor-pointer btn-circle bg-light"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faBars,
  faPlus,
  faArrowUp,
  faLeaf,
  faVolumeHigh,
  faPenToSquare,
  faArrowRightLong,
  faCalendarDays
} from "@fortawesome/free-solid-svg-icons";

// Add icons to the library
library.add(faBars, faPlus, faArrowUp, faLeaf, faVolumeHigh, faPenToSquare, faArrowRightLong, faCalendarDays);

// Reactive state for message input
const message = ref("");
</script>

<style scoped>
/* Optional: Additional styling for specific components */
.container {
  max-width: 800px;
  position: relative;
}

.custom-input {
  width: 80%;
  background-color: #232323;
  border: none;
  color: white;
  border-radius: 25px;
  height: 45px;
}

.custom-input::placeholder {
  padding-left: 15px;
}

.custom-input:focus {
  outline: none;
}

.btn-input-group {
  font-size: 2rem;
}

.btn-circle {
  border-radius: 50%;
  width: 25px;
  height: 25px;
  max-width: 25px;
  max-height: 25px;
  min-width: 25px;
  min-height: 25px;
  padding: 0.5em;
}

.btn-circle font-awesome-icon {
  font-size: 1rem;
}

.logo-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 60vh;
  position: relative;
}

.original-logo {
  width: 50px;
  height: 50px;
}

.sticky-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 100%;           
  padding: 1rem;           
  z-index: 1000;
}

.sticky-footer .input-container {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.arrow-container {
  position: absolute;
  top: 43%; /* Adjust as needed */
  left: 40%; /* Adjust as needed */
  transform: translate(-50%, -50%); /* Adjust as needed */
  display: flex;
  align-items: center;
}

.arrow {
  color: white;
  font-size: 24px; /* Adjust as needed */
  margin-right: 10px;
  rotate: 45deg;
}

.arrow-text {
  color: white;
  font-size: 14px;
  margin-top: -25px;
  margin-right: 3px;
}

.pen-to-square {
  font-size: 1.8rem;
}

.calendar-days {
  font-size: 1.8rem;
  color: #717171;
}

.calendar-days-background{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 5.5em;
  height: 2.6em;
  background: linear-gradient(90deg, white, #5b5b5b);
  border-radius: 20px;
  cursor: pointer;
}
</style>