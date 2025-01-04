<template>
  <div
    class="container-fluid p-0 m-0"
    style="background-color: var(--color-background-dark)"
  >
    <RouterView />
  </div>
</template>

<script setup lang="ts"></script>
<style>
* {
  box-sizing: border-box;
}

.no-select {
  -webkit-touch-callout: none;
  /* iOS Safari */
  -webkit-user-select: none;
  /* Safari */
  -moz-user-select: none;
  /* Firefox */
  -ms-user-select: none;
  /* Internet Explorer/Edge */
  user-select: none;
  /* Non-prefixed version, currently supported by Chrome and Opera */
}

.btn-click:active {
  transform: scale(0.9);
}

html {
  background-color: var(--color-background-dark);
}
</style>
