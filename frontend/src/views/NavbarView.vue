<script setup lang="ts"></script>

<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light sticky-top">
      <div
        class="container-fluid d-flex justify-content-between align-items-center"
      >
        <button class="btn btn-outline-secondary me-2">
          <i class="fas fa-bars"></i>
        </button>
        <div class="d-flex align-items-start">
          <button class="btn btn-primary mb-2">
            <i class="fas fa-plus-circle me-1"></i>
          </button>
          <button class="btn btn-outline-primary">
            <i class="fas fa-leaf me-1"></i>
          </button>
        </div>
      </div>
    </nav>

    <div class="container my-4" style="height: 60vh; overflow-y: auto">
      <!-- Chat messages go here -->
    </div>

    <div class="container-fluid p-3 border-top">
      <div class="input-group">
        <button class="btn btn-outline-secondary">
          <i class="fas fa-plus"></i>
        </button>
        <input
          type="text"
          class="custom-input"
          placeholder="Type a message..."
          aria-label="Message input"
        />
        <button class="btn btn-outline-primary">
          <i class="fas fa-paper-plane"></i>
          <!-- Send icon -->
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Optional: Additional styling for specific components */
.container {
  max-width: 800px;
}

.custom-input {
  width: 80%;
}
</style>
