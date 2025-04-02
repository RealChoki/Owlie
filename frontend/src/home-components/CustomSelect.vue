<template>
  <div
    class="custom-select"
    tabindex="0"
    @click="handleClick"
    @keydown="onKeydown"
    role="combobox"
    aria-expanded="open"
  >
    <div class="selected-option">{{ selectedOptionLabel }}</div>
    <font-awesome-icon
      :icon="open ? ['fas', 'chevron-up'] : ['fas', 'chevron-down']"
      class="chevron-icon"
    />
    <ul v-if="open" class="options-list">
      <li
        v-for="(option, index) in options"
        :key="index"
        @click.stop="selectOption(option)"
        :class="{ active: index === highlightedIndex }"
      >
        {{ option.label }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, defineEmits, watch } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array as () => { value: string; label: string }[], required: true },
  // Controlled open state from parent:
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'opened', 'closed'])

const open = ref(props.isOpen)

const highlightedIndex = ref(-1)

// Keep local open in sync with parent's prop:
watch(
  () => props.isOpen,
  (newVal) => {
    open.value = newVal
  }
)

function handleClick() {
  if (!open.value) {
    open.value = true
    emit('opened')
  } else {
    open.value = false
    emit('closed')
  }
}

function onKeydown(event: KeyboardEvent) {
  if (!open.value) {
    if (event.key === 'Enter' || event.key === ' ') {
      handleClick()
    }
    return
  }

  // When menu is open:
  switch (event.key) {
    case 'ArrowDown':
      highlightedIndex.value = (highlightedIndex.value + 1) % props.options.length
      break
    case 'ArrowUp':
      highlightedIndex.value =
        (highlightedIndex.value - 1 + props.options.length) % props.options.length
      break
    case 'Enter':
      if (highlightedIndex.value >= 0) {
        selectOption(props.options[highlightedIndex.value])
      }
      break
  }
}

function selectOption(option: { value: string; label: string }) {
  emit('update:modelValue', option.value)
  open.value = false
  emit('closed')
}

const selectedOptionLabel = computed(() => {
  const found = props.options.find((o) => o.value === props.modelValue)
  return found ? found.label : ''
})
</script>

<style scoped>
.custom-select {
position: relative;
display: inline-block;
border: 1px solid var(--color-gray-light);
border-radius: 6px;
padding: 5px 10px;
cursor: pointer;
}

.custom-select:hover {
background-color: var(--color-gray-light);
}

.selected-option {
display: inline-block;
color: var(--color-white);
}

.chevron-icon {
color: var(--color-white);
margin-left: 5px;
font-size: 0.8em;
}

.options-list {
list-style: none;
padding: 0;
margin: 0;
position: absolute;
top: calc(100% + 5px);
left: 0;
right: 0;
background: var(--color-gray-medium);
border: 1px solid var(--color-gray-light);
border-radius: 6px;
max-height: 200px;
overflow-y: auto;
z-index: 100;     
color: var(--color-white);
}

.options-list li {
padding: 5px 10px;
cursor: pointer;
}

.options-list li:hover {
background-color: var(--color-gray-light);
}

.options-list li:nth-child(n+1):hover,
.options-list li.active {
background-color: var(--color-gray-light);
}
</style>
