<template>
  <div class="container-fluid vh-100 d-flex p-2 py-4">
    <!-- Left Section -->
    <!-- <div
      class="logo-container d-flex align-items-center px-4 mt-3 position-fixed"
    >
      <img src="../assets/icons/OwlLogo.png" alt="Logo" class="logo" />
      <div class="text-white">
        <span class="fw-bold ms-2">Owlie</span>
        <span class="fst-italic"> - personal student assistant</span>
      </div>
    </div> -->
    <div class="login-left d-flex align-items-center justify-content-center">
      <div class="p-4 w-100">
        <h1 class="text-center mb-4">Login</h1>
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              v-model="username"
              class="login-input w-100"
              placeholder="Enter your username"
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
          <div
            class="d-flex justify-content-between align-items-center mb-4 gap-3"
          >
            <span class="small text-start cursor-pointer" style="width: 50%"
              >Don't have an account? <strong>Register</strong></span
            >

            <button type="submit" class="btn btn-action" style="width: 50%">
              Login
            </button>
          </div>
        </form>
      </div>
    </div>
    <!-- Right Section -->
    <!-- src="../assets/videos/vecteezy_abstract-grey-and-black-professional-motion-background_34700930.mp4" -->
    <div class="login-right">
      <div class="container h-100">
        <video
          class="image_preview_container"
          type="video/m4v"
          preload="auto"
          src="https://videos.pexels.com/video-files/1877846/1877846-hd_1920_1080_30fps.mp4"
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

const username = ref("");
const password = ref("");

const router = useRouter();

// Store the token in sessionStorage after login
const onSubmit = async () => {
  if (!username.value || !password.value) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const response = await fetch(
      "https://moodle.htw-berlin.de/login/token.php",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username.value,
          password: password.value,
          service: "moodle_mobile_app",
        }),
      }
    );

    const data = await response.json();

    if (data.token) {
      // Store token in sessionStorage
      sessionStorage.setItem("auth_token", data.token);
      console.log("Token stored in sessionStorage:", data.token);
      router.push("/");
    } else {
      alert("Login failed. Please check your credentials.");
    }
  } catch (error) {
    console.error("Error during login:", error);
  }
};
</script>

<style scoped>
/*
.logo {
  width: 30px;
}
*/

.container-fluid {
  background-color: var(--color-black);
}
.login-left {
  min-width: 420px;
  background-color: var(--color-black);
  color: var(--text-color);
}

.login-right {
  flex-grow: 1;
  background-color: var(--color-black);
}

.btn-action {
  background-color: var(--text-color);
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
  color: var(--text-color);
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
