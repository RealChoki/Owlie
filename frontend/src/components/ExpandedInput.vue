<template>
  <div class="full-screen-overlay">
    <div class="h-100 p-2" style="background-color: #232323">
      <div class="container h-100 d-flex flex-column">
        <div class="d-flex justify-content-end mt-2 mb-3">
          <font-awesome-icon
            :icon="['fas', 'down-left-and-up-right-to-center']"
            @click.stop="closeExpandedInput"
            class="collapse-icon"
          />
        </div>
        <textarea
          class="full-screen-textarea"
          style="background-color: #232323"
          placeholder="Type a message..."
          aria-label="Message input"
          v-model="message"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faDownLeftAndUpRightToCenter } from '@fortawesome/free-solid-svg-icons'
library.add(faDownLeftAndUpRightToCenter)

const props = defineProps({
  isExpandedInput: Boolean
})

const emit = defineEmits(['closeExpandedInput'])

const message = ref('')

function closeExpandedInput() {
  emit('closeExpandedInput')
}
</script>

<style scoped>
.full-screen-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.8);
  z-index: 1020;
}

.collapse-icon {
  color: #ffffff;
  cursor: pointer;
  font-size: 1.5rem;
}

.full-screen-textarea {
  flex: 1;
  width: 100%;
  height: 100%;
  border: none;
  outline: none;
  color: #ffffff;
  padding: 1rem;
  font-size: 1rem;
  resize: none;
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}

/* Hide scrollbar for Chrome, Safari and Opera */
.full-screen-textarea::-webkit-scrollbar {
  display: none;
}

</style>
