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
        :class="{ 'input-focused': isSearchFocused }"
        ref="searchInput"
      />
      <font-awesome-icon
        :icon="['fas', 'magnifying-glass']"
        class="magnifying-glass"
        :class="{ 'text-white': isSearchFocused }"
        @click="focusInput"
        style="cursor: pointer" 
      />
      <!-- Add event to close the burger menu -->
      <img 
        src="../components/icons/Menu gray.png" 
        style="cursor: pointer" 
        class="ms-3" 
        @click="closeBurgerMenu" 
      />
    </div>
    <ul class="p-0 mt-3" style="cursor: pointer">
      <li
        v-for="(module, index) in filteredModules"
        :key="index"
        class="list-item-hover rounded text-white py-1"
        @click="selectModule(module)"
        >
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
const searchInput = ref<HTMLInputElement | null>(null)

const modules = ref([
  'Grundlagen der Programmierung',
  'Statistik',
  'Unternehmenssoftware',
  'Datenbanktechnologien',
  'Webentwicklung',
  'Betriebssysteme'
])

function selectModule(module: string) {
  emit('moduleSelected', module)  // Emit the selected module to the parent
  closeBurgerMenu()  // Close the menu after selecting the module
}

const filteredModules = computed(() =>
  modules.value.filter((module) => module.toLowerCase().includes(searchQuery.value.toLowerCase()))
)

function closeBurgerMenu() {
  emit('closeBurgerMenu')
}

function focusInput() {
  if (searchInput.value) {
    searchInput.value.focus()
  }
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
  padding-left: 2.6rem;
}

.burger-menu-search-bar:focus {
  outline: none;
}

.burger-menu-search-bar::placeholder {
  transition: color 0.1s ease; /* Smooth transition */
}

.search-container {
  display: flex;
  align-items: center;
  position: relative;
}

.magnifying-glass {
  position: absolute;
  font-size: 1.2rem;
  left: 15px;
  color: #5b5b5b; /* Default color */
  transition: color 0.1s ease; /* Smooth transition */
}

.text-white {
  color: white !important;
}

.input-focused::placeholder {
  color: white !important;
}

.list-item-hover {
  list-style-type: none;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.list-item-hover:hover {
  background-color: #414141;
}

ul.p-0 {
  padding-left: 0 !important;
  padding-right: 0 !important;
}
</style>