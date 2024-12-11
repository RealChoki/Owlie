import { ref, onMounted, onBeforeUnmount } from "vue";

// Function to check screen width
export function useScreenWidth() {
  const isWideScreen = ref(false);

  function checkScreenWidth() {
    isWideScreen.value = window.innerWidth > 768; // You can change the threshold here
  }

  onMounted(() => {
    checkScreenWidth();
    window.addEventListener("resize", checkScreenWidth);
  });

  onBeforeUnmount(() => {
    window.removeEventListener("resize", checkScreenWidth);
  });

  return { isWideScreen };
}
