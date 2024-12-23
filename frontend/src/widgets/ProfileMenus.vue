<template>
  <div
    ref="popoverRef"
    v-if="isVisible"
    class="popover position-absolute z-50"
    :style="{ ...popoverStyle, }"
  >
    <nav class="p-2 text-white">
      <div ref="popoverUniversityRef" class="p-2">
        {{ universityName }}
      </div>
      <hr class="my-1" />
      <a
        v-for="item in menuItems"
        :key="item.label"
        :href="item.href"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="item.icon" /> {{ item.label }}
      </a>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, onMounted, computed } from "vue";
import type { Ref } from "vue";

// Props
const props = defineProps({
  isVisible: Boolean,
  universityName: {
    type: String,
    default: "Hochschule für Technik und Wirtschaft Berlin",
  },
  menuItems: {
    type: Array as () => { label: string; href: string; icon: string[] }[],
    required: true,
  },
  position: {
    type: Object as () => Partial<CSSStyleDeclaration>,
    default: () => ({}),
  },
  width: {
    type: [String, Number],
    default: "100%",
  },
  maxWidth: {
    type: String,
    default: "450px",
  },
});

// Refs
const popoverRef: Ref<HTMLElement | null> = ref(null);
const popoverUniversityRef: Ref<HTMLElement | null> = ref(null);

// Computed styles
const popoverStyle = computed(() => {
  const { width, maxWidth } = props;
  return {
    width: typeof width === "number" ? `${width}px` : width,
    maxWidth,
    backgroundColor: "#2a2a2a",
    borderColor: "#414141",
    borderWidth: "1px",
  };
});

const positionStyle = ref<Partial<CSSStyleDeclaration>>(props.position);

// Methods
onMounted(() => {
  updatePopoverPosition();
});

watch(() => props.isVisible, (newVal) => {
  if (newVal) {
    nextTick(() => {
      updatePopoverPosition();
    });
  }
});

function updatePopoverPosition() {
  const universityHeight = popoverUniversityRef.value?.offsetHeight || 0;

  let calculatedTop;
  if (universityHeight > 63) {
    calculatedTop = "-175px";
  } else if (universityHeight > 42) {
    calculatedTop = "-155px";
  } else {
    calculatedTop = "-135px";
  }

  positionStyle.value = { ...props.position, top: calculatedTop };
};

</script>

<style scoped>
.popover {
  position: absolute;
  z-index: 50;
}

.popover nav a:hover {
  background-color: #414141;
}
</style>
