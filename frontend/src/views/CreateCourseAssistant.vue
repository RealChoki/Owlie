<template>
  <div
    class="d-flex flex-column vh-100"
    style="background-color: var(--color-black)"
  >
    <!-- Navbar -->
    <div class="container-fluid navbar-container">
      <nav class="py-2 px-3 d-flex align-items-center justify-content-between">
        <!-- Home Icon -->
        <button
          class="btn btn-link p-0 d-flex align-items-center"
          @click="handleHomeClick"
          aria-label="Home"
        >
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
        <Profilemenu
          v-if="isProfileMenuVisible"
          :origin="'Nav-EditQuiz'"
          @toggleProfileMenu="toggleProfileMenu"
        />
      </nav>
    </div>

    <!-- Content Container -->
    <div
      class="d-flex flex-grow-1 p-1"
      style="background-color: var(--color-black)"
    >
      <div
        class="w-100 rounded text-white p-4"
        style="
          background-color: var(--color-background-dark);
          border: 1px solid var(--color-gray-shadow);
          margin: 5px;
          overflow-y: auto;
          max-height: calc(100vh - 60px);
        "
      >
        <h3 class="text-center mb-5 mt-4">Create an Assistant</h3>
        <div class="form-container d-flex justify-content-center">
          <form @submit.prevent="submitForm">
            <div class="mb-3">
              <label for="subjectSelect" class="form-label">Subject</label>
              <select
                id="subjectSelect"
                v-model="subject"
                class="login-input w-100"
                required
              >
                <option value="Wirtschaftsinformatik">
                  Wirtschaftsinformatik
                </option>
                <option value="Medieninformatik">Medieninformatik</option>
              </select>
            </div>

            <div class="mb-3">
              <label for="courseNameInput" class="form-label"
                >Course Name</label
              >
              <input
                type="text"
                id="courseNameInput"
                v-model="courseName"
                class="login-input w-100"
                placeholder="Enter course name"
                required
              />
            </div>

            <div class="mb-3">
              <label for="courseIdInput" class="form-label">Course ID</label>
              <input
                type="text"
                id="courseIdInput"
                v-model="courseId"
                class="login-input w-100"
                placeholder="Enter course ID"
                required
              />
            </div>

            <button type="submit" class="btn btn-action w-100">Submit</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import { faHome } from "@fortawesome/free-solid-svg-icons";

library.add(faHome);

const isProfileMenuVisible = ref(false);
const isWideScreen = ref(window.innerWidth > 768);
const isSidebarOpen = ref(false);
const router = useRouter();

const subject = ref("Wirtschaftsinformatik");
const courseName = ref("");
const courseId = ref("");

const submitForm = () => {
  const formData = {
    subject: subject.value,
    courseName: courseName.value,
    courseId: courseId.value,
  };

  console.log("Form submitted with data:", formData);

};

const handleHomeClick = () => {
  router.push("/");
};

const toggleProfileMenu = () => {
  isProfileMenuVisible.value = !isProfileMenuVisible.value;
};
</script>

<style scoped>
.navbar-container {
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
