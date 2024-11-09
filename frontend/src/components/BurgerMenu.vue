<template>
  <div ref="burgerMenuRef" class="burger-menu-open p-3 bg-black rounded shadow-sm">
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
      <!-- Add event to close the burger menu -->
      <img 
        src="../components/icons/Menu gray.png" 
        style="cursor: pointer" 
        class="ms-3" 
        @click="closeBurgerMenu" 
      />
    </div>
    <ul class="p-0 mt-3">
      <li v-for="(module, index) in filteredModules" :key="index" class="list-item-hover rounded text-white py-1">
        <p class="m-0 py-2 px-2">{{ module }}</p>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'
library.add(faMagnifyingGlass)

// Props for burger menu visibility (received from the parent)
const props = defineProps({
  isOpenBurgerMenu: Boolean
})

const emit = defineEmits(['closeBurgerMenu'])

const searchQuery = ref('')
const isSearchFocused = ref(false)

const modules = ref([
  'Grundlagen der Programmierung',
  'Statistik',
  'Unternehmenssoftware',
  'Datenbanktechnologien',
  'Webentwicklung',
  'Betriebssysteme'
])

const filteredModules = computed(() =>
  modules.value.filter((module) => module.toLowerCase().includes(searchQuery.value.toLowerCase()))
)

function closeBurgerMenu() {
  emit('closeBurgerMenu')
}
</script>

<style scoped>
.burger-menu-open {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  width: 80vw;
  z-index: 9999;
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

.list-item-hover {
  list-style-type: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}
</style>
