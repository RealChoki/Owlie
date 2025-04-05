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
        Creating an AI Assistant that Empowers Independent Problem-Solving
      </h1>
      <p class="w-75 paragraph-desktop" style="color: var(--text-color)">
        Welcome! We are a passionate team of 2 business informatics students (<a
          href="https://github.com/RealChoki"
          style="color: var(--text-color)"
          >Choki's GitHub</a
        >
        and <a href="https://github.com/davidcraccer" style="color: var(--text-color)">David's GitHub</a>) from HTW
        Berlin with a dream. Meet Owlie – our innovative AI teaching assistant. Unlike traditional AI tools that often
        provide immediate answers, Owlie encourages students to think critically and solve problems independently by
        offering hints, guidance, and personalized feedback.
      </p>
      <p class="w-75 paragraph-desktop" style="color: var(--text-color)">
        Our goal is to address the challenges AI faces in education, such as promoting critical thinking over quick
        solutions, and fostering a deeper understanding of concepts. By helping students develop problem-solving skills,
        we believe AI can truly empower learners.
      </p>
      <p class="w-75 paragraph-mobile" style="color: var(--text-color)">
        We are two business informatics students (<a
          href="https://github.com/RealChoki"
          style="color: var(--text-color)"
          >Choki</a
        >
        and <a href="https://github.com/davidcraccer" style="color: var(--text-color)">David</a>) from HTW Berlin,
        passionate about AI in education. Meet Owlie – an innovative AI teaching assistant designed to encourage
        critical thinking. Instead of simply providing answers, Owlie offers hints, guidance, and personalized feedback
        to help students develop problem-solving skills while maintaining academic integrity.
      </p>
      <img class="owl-logo w-25 mt-4" src="../assets/icons/owl.svg" alt="Owl Logo" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
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
