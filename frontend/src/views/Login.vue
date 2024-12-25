<template>
  <div class="container-fluid vh-100 d-flex p-2 py-4">
   <!-- Left Section -->
<div class="login-left d-flex align-items-center justify-content-center">
  <div class="p-4 w-100">
    <h1 class="text-center mb-4">Login</h1>
    <form @submit.prevent="onSubmit">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
          type="email"
          id="email"
          v-model="email"
          class="login-input w-100"
          placeholder="Enter your email"
          required
        />
      </div>
      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
          type="password"
          id="password"
          v-model="password"
          class="login-input w-100"
          placeholder="Enter your password"
          required
        />
      </div>
      
      <!-- Text and Login Button Container -->
      <div class="d-flex justify-content-between align-items-center mb-4 gap-3">
        <span class="small text-start" style="width: 50%; cursor: pointer;">Don't have an account? <strong>Register</strong></span>

        <button
          type="submit"
          class="btn btn-action"
          style="width: 50%;"
        >
          Login
        </button>
      </div>
    </form>
  </div>
</div>

    <!-- Right Section -->
    <div class="login-right">
      <div class="container h-100">
        <video
          class="image_preview_container"
          src="https://chatki.htw-berlin.de/public/img/HAWKIBG-DM.m4v"
          type="video/m4v"
          preload="auto"
          autoplay
          loop
          muted
          style="
            opacity: 1;
            width: 100%;
            height: 100%;
            object-fit: cover;
            border-radius: 20px;
          "
        ></video>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const email = ref("");
const password = ref("");

const router = useRouter(); 

const onSubmit = () => {
  if (!email.value || !password.value) {
    alert("Please fill in all fields.");
    return;
  }

  console.log("Email:", email.value);
  console.log("Password:", password.value);

  router.push("/");
};
</script>


<style scoped>
.container-fluid {
  background-color: var(--color-black);
}
.login-left {
  min-width: 420px;
  background-color: var(--color-black);
  color: var(--color-white);
}

.login-right {
  flex-grow: 1;
  background-color: var(--color-black);
}

.btn-action {
  background-color: var(--color-white);
  color: var(--color-black);
  border-color: var(--color-gray-light);
}

.btn-action:hover {
  background-color: #e0e0e0;
  color: var(--color-black);
  border-color: var(--color-gray-light);
}

.btn-action:focus {
  background-color: #e0e0e0;
  color: var(--color-black);
  border-color: var(--color-gray-light);
}

.btn-action:active {
  background-color: #d1d1d1;
  color: var(--color-black);
  border-color: var(--color-gray-light);
}

.btn-action:disabled {
  background-color: var(--color-disabled);
  border-color: var(--color-disabled);
}

.login-input {
  background-color: var(--color-gray-medium);
  color: var(--color-white);
  padding: 0.5rem;
  padding-left: 1rem;
  border: 1px solid var(--color-gray-light);
  border-radius: 6px;
}

.login-input:focus {
  outline: none;
}

.login-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
  transition: color 0.2s ease;
}
</style>
