<template>
  <div
    ref="popoverRef"
    class="popover position-absolute z-50"
    :style="{ ...positionStyle }"
    :class="{ 'popover-nav': props.origin === 'Nav', 'popover-burger': props.origin === 'BurgerMenu' }"
  >
    <nav class="p-2 text-white">
      <div ref="popoverUniversityRef" class="p-2">
        Hochschule für Technik und Wirtschaft Berlin
      </div>
      <hr class="my-1" />
      <a
        href="#"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="['fas', 'user-circle']" /> Profile
      </a>
      <a
        href="#"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="['fas', 'gear']" /> Settings
      </a>
      <a
        href="#"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="['fas', 'info-circle']" /> About Us
      </a>
      <a
        href="#"
        class="d-flex align-items-center gap-2 text-decoration-none text-white p-2 rounded"
      >
        <font-awesome-icon :icon="['fas', 'right-from-bracket']" /> Log Out
      </a>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, nextTick, PropType } from "vue";
import type { Ref } from "vue";
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { library } from "@fortawesome/fontawesome-svg-core";
import {
  faUserCircle,
  faGear,
  faRightFromBracket,
  faInfoCircle,
} from "@fortawesome/free-solid-svg-icons";

// Add icons to library
library.add(faUserCircle, faGear, faRightFromBracket, faInfoCircle);

// Props
const props = defineProps({
  origin: {
    type: String as PropType<"BurgerMenu" | "Nav">,
    required: true,
  },
  togglePopover: {
      type: Function,
      required: false,
  },
});

// Refs
const emit = defineEmits(["togglePopover"]);

const popoverRef: Ref<HTMLElement | null> = ref(null);
const popoverUniversityRef: Ref<HTMLElement | null> = ref(null);
const positionStyle = ref<Partial<CSSStyleDeclaration>>(null);
const isFirstClick = ref(true);

// Function to update popover position based on height
function updatePopoverPosition() {
  if (props.origin !== "BurgerMenu") return;
  const universityHeight = popoverUniversityRef.value?.offsetHeight || 0;

  positionStyle.value = {
    top:
      universityHeight > 63
        ? "-175px"
        : universityHeight > 42
        ? "-155px"
        : "-135px",
  };
}

// ResizeObserver handler
function handleHeightChange(entries: ResizeObserverEntry[]) {
    updatePopoverPosition();
}
function handleClickOutside(event: MouseEvent) {
  if (isFirstClick.value) {
    isFirstClick.value = false;
    return;
  }
  if (popoverRef.value && !popoverRef.value.contains(event.target as Node)) {
    emit("togglePopover");
  }
}

let resizeObserver: ResizeObserver | null = null;

// Lifecycle hooks
onMounted(() => {
  document.addEventListener("click", handleClickOutside);
  if (popoverUniversityRef.value) {
    resizeObserver = new ResizeObserver(handleHeightChange);
    resizeObserver.observe(popoverUniversityRef.value);
  }
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
  if (resizeObserver && popoverUniversityRef.value) {
    resizeObserver.unobserve(popoverUniversityRef.value);
  }
  resizeObserver?.disconnect();
});
</script>

<style scoped>
.popover {
  z-index: 9999;
  width: 100%;
  background-color: var(--color-gray-medium);
  border-color: var(--color-gray-light);
  border-width: 1px;
}

.popover nav a:hover {
  background-color: var(--color-gray-light);
}

/* from burger-menu */
.popover-burger {
  top: -135px;
  left: transformX(-50%);
  max-width: 450px;
}

/* from nav */
.popover-nav {
  top: 4.5em;
  right: 0;
}
</style>
