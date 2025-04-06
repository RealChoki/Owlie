<template>
  <div
    class="custom-select"
    :class="{ 'custom-select-active': open }"
    tabindex="0"
    @click="handleClick"
    @keydown="onKeydown"
    role="combobox"
    aria-expanded="open"
  >
    <div class="selected-option">{{ selectedOptionLabel }}</div>
    <font-awesome-icon :icon="open ? ['fas', 'chevron-up'] : ['fas', 'chevron-down']" class="chevron-icon" />
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

const props = defineProps({
  modelValue: { type: String, required: true },
  options: { type: Array as () => { value: string; label: string }[], required: true },
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['update:modelValue', 'opened', 'closed'])

const open = ref(props.isOpen)
const highlightedIndex = ref(-1)

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

  switch (event.key) {
    case 'ArrowDown':
      highlightedIndex.value = (highlightedIndex.value + 1) % props.options.length
      break
    case 'ArrowUp':
      highlightedIndex.value = (highlightedIndex.value - 1 + props.options.length) % props.options.length
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
  border: 1px solid var(--custom-select-border-color);
  border-radius: 6px;
  padding: 5px 10px;
  cursor: pointer;
  background: var(--custom-select-bg);
  transition: background-color 0.3s ease;
}

.custom-select:hover {
  background-color: var(--custom-select-hover-bg);
  border: 1px solid var(--custom-select-border-color);
}

/* New style to persist the active state background */
.custom-select-active {
  background-color: var(--custom-select-active-bg);
}

.selected-option {
  display: inline-block;
  color: var(--text-color);
}

.chevron-icon {
  color: var(--text-color);
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
  background: var(--custom-select-option-bg);
  border: 1px solid var(--custom-select-option-border-color);
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
  z-index: 100;
  color: var(--text-color);
}

.options-list li {
  padding: 5px 10px;
  cursor: pointer;
}

.options-list li:hover {
  background-color: var(--custom-select-option-bg-hover);
}

.options-list li:nth-child(n + 1):hover,
.options-list li.active {
  background-color: var(--custom-select-option-bg-active);
}
</style>
```
