<template>
  <div v-if="isOpenBurgerMenu" ref="burgerMenuRef" class="burger-menu-open p-3 bg-black rounded shadow-sm">
    <div class="search-container">
      <input
        type="text"
        v-model="searchQuery"
        class="burger-menu-search-bar w-100"
        placeholder="Search modules..."
        @focus="isSearchFocused = true"
        @blur="isSearchFocused = false"
      />
      <font-awesome-icon
        :icon="['fas', 'magnifying-glass']"
        class="magnifying-glass"
        style="color: #5b5b5b"
        :class="{ 'text-white': isSearchFocused }"
      />
      <img
        src="../components/icons/Menu gray.png"
        style="cursor: pointer"
        class="ms-3"
        @click="toggleBurgerMenu"
      />
    </div>
    <ul class="p-0 mt-3">
      <li
        v-for="(module, index) in filteredModules"
        :key="index"
        class="list-item-hover rounded text-white py-1"
      >
        <p class="m-0 py-2 px-2">{{ module }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

// State
const isOpenBurgerMenu = ref(false)
const searchQuery = ref('')
const isSearchFocused = ref(false)

// Mock data for modules
const modules = ref(['Module 1', 'Module 2', 'Module 3'])

// Computed property for filtered module list
const filteredModules = computed(() =>
  modules.value.filter((module) =>
    module.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
)

// Method to toggle burger menu
function toggleBurgerMenu() {
  isOpenBurgerMenu.value = !isOpenBurgerMenu.value
}
</script>

<style scoped>
.burger-menu-open {
  position: fixed;
  top: 50px;
  right: 20px;
  width: 250px;
  z-index: 1050;
}

.burger-menu-search-bar {
  background-color: #2a2a2a;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 0.5rem;
}

.magnifying-glass {
  position: absolute;
  right: 20px;
  top: 13px;
  font-size: 1.2rem;
}

.list-item-hover:hover {
  background-color: #414141;
}
</style>
