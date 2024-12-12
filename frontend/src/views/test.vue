<template>
  <div class="container-fluid p-0 d-flex">
    <div class="left-element" :style="{ width: leftElementWidth, height: '100vh' }">
      Left Element
    </div>
    <div class="right-element" :style="{ width: rightElementWidth, height: '100vh' }">
      Right Element
    </div>
  </div>

  <!-- Button to trigger the transition -->
  <button class="btn btn-primary mt-3" @click="expandRight">Expand Right Element</button>
</template>

<script setup lang="ts">
import { ref } from 'vue';

// Define the reactive properties for the width of the elements
const rightElementWidth = ref('50%');
const leftElementWidth = ref('50%');

// Function to handle the expansion of the right element
const expandRight = () => {
  rightElementWidth.value = '100%';  // Set the right element to full width
  leftElementWidth.value = '0';      // Set the left element to 0 width
};
</script>

<style scoped>
/* Basic styles for the elements */
.left-element {
  background-color: lightblue;
  transition: width 0.5s ease;
}

.right-element {
  background-color: lightgreen;
  transition: width 0.5s ease;
}

button {
  margin-top: 20px;
}
</style>
