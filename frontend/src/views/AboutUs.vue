<template>
  <button @click="handleHomeClick" class="position-absolute mt-3">
    <font-awesome-icon
      class="icon-click-effect nav-icon-holder cursor-pointer"
      :icon="['fas', 'home']"
      style="color: var(--color-gray-shadow); margin-left: 1.9em"
    />
  </button>
  <div class="d-flex justify-content-center container">
    <div class="d-flex flex-column justify-content-center align-items-center text-center vh-100 w-75">
      <h1 class="fw-bold mb-4" style="color: var(--color-white">
        Creating an AI Assistant that Empowers Independent Problem-Solving
      </h1>
      <p class="w-75 paragraph-desktop" style="color: var(--color-white">
        Welcome! We are a passionate team of 2 business informatics students (<a
          href="https://github.com/RealChoki"
          style="color: var(--color-white"
          >Choki's GitHub</a
        >
        and <a href="https://github.com/davidcraccer" style="color: var(--color-white">David's GitHub</a>) from HTW
        Berlin with a dream. Meet Owlie – our innovative AI teaching assistant. Unlike traditional AI tools that often
        provide immediate answers, Owlie encourages students to think critically and solve problems independently by
        offering hints, guidance, and personalized feedback.
      </p>
      <p class="w-75 paragraph-desktop" style="color: var(--color-white">
        Our goal is to address the challenges AI faces in education, such as promoting critical thinking over quick
        solutions, and fostering a deeper understanding of concepts. By helping students develop problem-solving skills,
        we believe AI can truly empower learners.
      </p>
      <p class="w-75 paragraph-mobile" style="color: var(--color-white">
        We are two business informatics students (<a
          href="https://github.com/RealChoki"
          style="color: var(--color-white"
          >Choki</a
        >
        and <a href="https://github.com/davidcraccer" style="color: var(--text-color)">David</a>) from HTW Berlin,
        passionate about AI in education. Meet Owlie – an innovative AI teaching assistant designed to encourage
        critical thinking. Instead of simply providing answers, Owlie offers hints, guidance, and personalized feedback
        to help students develop problem-solving skills while maintaining academic integrity.
      </p>
      <img class="owl-logo w-25 mt-4" src="../assets/icons/OwlLogo.png" alt="Owl Logo" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faHome } from '@fortawesome/free-solid-svg-icons'
import { useRouter } from 'vue-router'

const router = useRouter()

library.add(faHome)

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
