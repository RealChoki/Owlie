<!-- filepath: vsls:/frontend/src/views/CourseDashboard.vue -->
<template>
  <div class="d-flex flex-column vh-100" style="background-color: var(--color-black)">
    <!-- Navbar -->
    <div class="container-fluid navbar-container">
      <nav class="py-2 px-3 d-flex align-items-center justify-content-between">
        <!-- Home Icon -->
        <button class="btn btn-link p-0 d-flex align-items-center" @click="handleHomeClick" aria-label="Home">
          <font-awesome-icon
            class="icon-click-effect nav-icon-holder"
            :icon="['fas', 'home']"
            style="color: var(--color-gray-shadow)"
          />
        </button>
        <div class="nav-icon-holder">
          <div
            class="d-flex align-items-center justify-content-center overflow-hidden rounded-circle icon-click-effect pfp-container"
          >
            <img
              alt="User"
              src="https://s.gravatar.com/avatar/6276a6c42e2f0f22bb0a96c4b1f2bd32?s=480&amp;r=pg&amp;d=https%3A%2F%2Fcdn.auth0.com%2Favatars%2Fsh.png"
              class="img-fluid rounded-circle"
              @click="toggleProfileMenu"
            />
          </div>
        </div>
        <Profilemenu v-if="isProfileMenuVisible" :origin="'Nav-EditQuiz'" @toggleProfileMenu="toggleProfileMenu" />
      </nav>
    </div>

    <!-- Main Content -->
    <div class="d-flex flex-grow-1">
      <!-- Sidebar -->
      <div class="sidebar py-3 px-3">
        <h3>Dashboard</h3>
        <!-- Vertical Tabs Navigation -->
        <div class="tabs-container text-white mb-3">
          <ul class="p-0 mt-1">
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'assistants' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'assistants'"
            >
              Assistants
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'usage' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'usage'"
            >
              Usage
            </li>
            <li
              :class="{ 'selected-sidebar-item': activeTab === 'stats' }"
              class="list-item-hover py-2 rounded text-white cursor-pointer"
              @click="activeTab = 'stats'"
            >
              Stats
            </li>
          </ul>
        </div>
      </div>

      <!-- Right Content -->
      <div class="right-side w-100 rounded px-3">
        <!-- Assistants Tab -->
        <AssistantDashboard v-if="activeTab === 'assistants'" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import {  faHome } from '@fortawesome/free-solid-svg-icons'
import Profilemenu from '../widgets/Profilemenu.vue'
import AssistantDashboard from '../dashboard-components/AssistantDashboard.vue'
import axios from 'axios'

library.add( faHome )

const router = useRouter()
// Sidebar Tabs
const activeTab = ref<'assistants' | 'usage' | 'stats'>('assistants')

// Profile Menu and Navbar handlers
const isProfileMenuVisible = ref(false)
function toggleProfileMenu() {
  isProfileMenuVisible.value = !isProfileMenuVisible.value
}
function handleHomeClick() {
  router.push('/')
}
</script>

<style scoped>
/* Navbar */
.navbar-container {
  background-color: var(--color-black);
}

/* Sidebar */
.sidebar {
  background-color: var(--color-black);
  min-width: 225px;
  max-width: 225px;
  padding: 1rem;
  color: white;
  padding-right: 10px !important;
}

/* Sidebar Items */
.list-item-hover {
  position: relative;
  list-style-type: none;
  transition: background-color 0.5s ease, color 0.5s ease;
  padding-left: 0.8em !important;
}

.list-item-hover:hover {
  background-color: var(--color-gray-light);
}

.list-item-hover::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 100%;
  background: linear-gradient(to bottom, white, var(--color-gray-shadow));
  transition: width 0.5s ease, opacity 0.5s ease;
  opacity: 0;
}

/* Sidebar item when selected */
.selected-sidebar-item {
  background-color: var(--color-gray-medium);
  position: relative;
  overflow: hidden;
  transition: background-color 0.5s ease, color 0.5s ease;
}

.selected-sidebar-item::before {
  width: 5px;
  opacity: 1;
}

/* Tabs */
.tabs-container ul {
  padding: 0;
  margin: 0;
  list-style: none;
}

.tabs-container li {
  cursor: pointer;
  padding: 0.5rem;
}

/* Right Content */
.right-side {
  background-color: var(--color-background-dark);
  border: 1px solid var(--color-gray-shadow);
  margin: 5px;
  height: calc(100vh - 60px);
  overflow: auto; /* Make the container scrollable */
}
</style>
