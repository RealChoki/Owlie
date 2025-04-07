<template>
  <button @click="handleHomeClick" class="position-absolute mt-3">
    <font-awesome-icon
      class="icon-click-effect nav-icon-holder cursor-pointer"
      :icon="['fas', 'home']"
      style="color: var(--home-icon); margin-left: 1.9em"
    />
  </button>
  <div class="d-flex justify-content-center container">
    <div class="d-flex flex-column justify-content-center align-items-center text-center vh-100 w-75">
      <h1 class="fw-bold mb-4" style="color: var(--text-color)">
        {{ $t('aboutUs.title') }}
      </h1>
      <p class="w-75 paragraph-desktop" style="color: var(--text-color)">
        {{ $t('aboutUs.description1.beforeLinks') }}
        <a href="https://github.com/RealChoki" target="_blank" style="color: var(--text-color)">
          {{ $t('aboutUs.description1.linkChoki') }}
        </a>
        {{ $t('aboutUs.description1.and') }}
        <a href="https://github.com/davidcraccer" target="_blank" style="color: var(--text-color)">
          {{ $t('aboutUs.description1.linkDavid') }}
        </a>
        {{ $t('aboutUs.description1.afterLinks') }}
      </p>
      <p class="w-75 paragraph-desktop" style="color: var(--text-color)">
        {{ $t('aboutUs.description2') }}
      </p>
      <p class="w-75 paragraph-mobile" style="color: var(--text-color)">
        {{ $t('aboutUs.mobile.beforeLinks') }}
        <a href="https://github.com/RealChoki" target="_blank" style="color: var(--text-color)">
          {{ $t('aboutUs.mobile.linkChoki') }}
        </a>
        {{ $t('aboutUs.mobile.and') }}
        <a href="https://github.com/davidcraccer" target="_blank" style="color: var(--text-color)">
          {{ $t('aboutUs.mobile.linkDavid') }}
        </a>
        {{ $t('aboutUs.mobile.afterLinks') }}
      </p>
      <img class="owl-logo w-25 mt-4" src="../assets/icons/owl-filled-white.png" alt="Owl Logo" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { isDarkMode } from '@/services/themeService'

const router = useRouter()

const handleHomeClick = () => {
  router.push('/')
}
</script>

<style scoped>
.container {
  max-width: 1190px;
  min-width: 500px;
}

/* Hide long text on small screens */
.paragraph-mobile {
  display: none;
}

/* Show short text on small screens, hide long text */
@media (max-width: 768px) {
  .paragraph-desktop {
    display: none;
  }
  .paragraph-mobile {
    display: block;
  }
}

.owl-logo {
  user-drag: none;
  -webkit-user-drag: none;
  user-select: none;
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
}
</style>
