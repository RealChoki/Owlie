<template>
  <div class="vh-100 d-flex p-2 py-4" style="color: var(--text-color)">
    <img src="../assets/icons/htw.png" alt="" style="position: fixed; top: 20px; left: 30px; width: 50px" />
    <div class="login-left d-flex align-items-center justify-content-center">
      <div class="p-4 w-100">
        <h1 class="text-center mb-4">{{ $t('login.title') }}</h1>
        <form @submit.prevent="onSubmit">
          <div class="mb-3">
            <label for="username" class="form-label">{{ $t('login.username.label') }}</label>
            <input
              type="text"
              id="username"
              v-model="username"
              class="login-input w-100"
              :placeholder="$t('login.username.placeholder')"
              required
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">{{ $t('login.password.label') }}</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="login-input w-100"
              :placeholder="$t('login.password.placeholder')"
              required
            />
          </div>

          <!-- Text and Login Button Container -->
          <div class="d-flex justify-content-between align-items-center mb-4 gap-3">
            <span class="small text-start" style="width: 50%"
              >{{ $t('login.register.title') }}
              <strong class="cursor-pointer">{{ $t('login.register.link') }}</strong></span
            >

            <button type="submit" class="btn btn-action" style="width: 50%">Login</button>
          </div>
        </form>
      </div>
    </div>
    <div class="login-right">
      <div class="pe-3 h-100 rm-0">
        <video
          v-if="isDarkMode"
          class="image_preview_container"
          type="video/m4v"
          preload="auto"
          src="@/assets/videos/dark_sky.mp4"
          autoplay
          loop
          muted
          style="opacity: 1; width: 100%; height: 100%; object-fit: cover; border-radius: 20px"
        ></video>
        <video
          v-else
          class="image_preview_container"
          type="video/m4v"
          preload="auto"
          src="@/assets/videos/blue_sky.mp4"
          autoplay
          loop
          muted
          style="opacity: 1; width: 100%; height: 100%; object-fit: cover; border-radius: 20px"
        ></video>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { isDarkMode } from '@/services/themeService'

const username = ref('')
const password = ref('')

const router = useRouter()

// Store the token in sessionStorage after login
const onSubmit = async () => {
  if (!username.value || !password.value) {
    alert('Please fill in all fields.')
    return
  }

  try {
    const response = await fetch('https://moodle.htw-berlin.de/login/token.php', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams({
        username: username.value,
        password: password.value,
        service: 'moodle_mobile_app'
      })
    })

    const data = await response.json()

    if (data.token) {
      // Store token in sessionStorage
      sessionStorage.setItem('auth_token', data.token)
      console.log('Token stored in sessionStorage:', data.token)
      router.push('/')
    } else {
      alert('Login failed. Please check your credentials.')
    }
  } catch (error) {
    console.error('Error during login:', error)
  }
}
</script>

<style scoped>
/*
.logo {
  width: 30px;
}
*/

.container-fluid {
  background-color: var(--background);
}

.login-left {
  min-width: 420px;
  background-color: var(--background);
  color: var(--text-color);
}

.login-right {
  flex-grow: 1;
  background-color: var(--background);
}

.btn-action {
  background-color: var(--login-button-bg);
  color: var(--login-button-color);
}

.btn-action:hover {
  background-color: var(--login-button-bg-hover);
  color: var(--login-button-color);
}

.btn-action:focus {
  background-color: var(--login-button-bg-hover);
  color: var(--login-button-color);
}

.btn-action:active {
  background-color: var(--login-button-bg-active);
  color: var(--login-button-color);
}

.btn-action:disabled {
  background-color: var(--color-disabled);
}

.login-input {
  background-color: var(--login-input-bg);
  color: var(--text-color);
  padding: 0.5rem;
  padding-left: 1rem;
  border: 1px solid var(--login-input-border-color);
  border-radius: 6px;
}

.login-input:focus {
  outline: none;
}
</style>
