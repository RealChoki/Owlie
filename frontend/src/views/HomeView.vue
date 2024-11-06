<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
      <div
        class="container-fluid d-flex justify-content-between align-items-center"
      >
        <!-- Burger icon -->
        <button class="btn btn-outline-secondary me-2">
          <font-awesome-icon :icon="['fas', 'bars']" />
        </button>
        <!-- Action buttons -->
        <div class="d-flex align-items-start">
          <button class="btn btn-primary mb-2">
            <font-awesome-icon :icon="['fas', 'pen-to-square']" />
          </button>
          <button class="btn btn-outline-primary">
            <font-awesome-icon :icon="['fas', 'leaf']" />
          </button>
        </div>
      </div>
    </nav>

    <div class="container my-4" style="height: 60vh; overflow-y: auto">
      <img class="origial-logo" src="../components/icons/ChatGPT.png" />
    </div>

    <!-- Sticky input bar at the bottom -->
    <div class="d-flex gap-2 sticky-footer mb-3">
      <!-- Plus icon button with circular style -->
      <font-awesome-icon
        :icon="['fas', 'plus']"
        class="cursor-pointer btn-circle"
        style="background-color: #858585;"
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
} from "@fortawesome/free-solid-svg-icons";

// Add icons to the library
library.add(faBars, faPlus, faArrowUp, faLeaf, faVolumeHigh, faPenToSquare);

// Reactive state for message input
const message = ref("");
</script>

<style scoped>
/* Optional: Additional styling for specific components */
.container {
  max-width: 800px;
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

.origial-logo {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  margin: auto;
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
</style>
