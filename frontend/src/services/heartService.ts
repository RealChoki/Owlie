import { computed } from 'vue'
import { heartCount, userMessageTokens } from '../services/chatService'
import { getHeartCountLS, setHeartCountLS, setUserMessageTokensLS } from '../services/localStorageService'

const LAST_REGEN_TIME_KEY = 'lastRegenTime'
const REGEN_INTERVAL_MS = 3 * 60 * 1000 // 3 minutes in milliseconds
const HEARTS_PER_INTERVAL = 0.5
const totalHearts = 5

function handleStorageChange(event: StorageEvent) {
    if (event.key === 'heartCount') {
        const newHeartCount = parseFloat(event.newValue || '')
        if (!isNaN(newHeartCount)) {
            heartCount.value = newHeartCount
        }
    }
}

function initializeHeartCount() {
    heartCount.value = getHeartCountLS()
}

function setupHeartRegeneration() {
    const lastRegenTime = getLastRegenTime()
    const currentTime = Date.now()
    const intervalsPassed = calculateIntervalsPassed(lastRegenTime, currentTime, REGEN_INTERVAL_MS)

    if (intervalsPassed > 0 && heartCount.value < totalHearts) {
        regenerateHearts(intervalsPassed * HEARTS_PER_INTERVAL)
    }

    updateLastRegenTime(currentTime)

    const regenInterval = setInterval(() => {
        if (heartCount.value < totalHearts) {
            regenerateHearts(HEARTS_PER_INTERVAL)
            updateLastRegenTime(Date.now())
        }
    }, REGEN_INTERVAL_MS)

    return regenInterval

    // Helper Functions
    function getLastRegenTime() {
        return parseInt(localStorage.getItem(LAST_REGEN_TIME_KEY) || '0', 10)
    }

    function calculateIntervalsPassed(lastTime: number, currentTime: number, interval: number) {
        return Math.floor((currentTime - lastTime) / interval)
    }

    function regenerateHearts(amount: number) {
        const newHeartCount = Math.min(heartCount.value + amount, totalHearts);
        const heartsHealed = newHeartCount - heartCount.value; // How many hearts were restored

        if (heartsHealed > 0) {
            heartCount.value = newHeartCount;
            setHeartCountLS(heartCount.value);

            // Restore tokens (1,000 per half-heart)
            const tokensToRestore = heartsHealed * 1000;
            userMessageTokens.value = Math.min(userMessageTokens.value + tokensToRestore, 10000);
            setUserMessageTokensLS(userMessageTokens.value);

            console.log(`Regenerated ${heartsHealed} hearts and restored ${tokensToRestore} tokens.`);
        }
    }

    function updateLastRegenTime(time: number) {
        localStorage.setItem(LAST_REGEN_TIME_KEY, time.toString())
    }
}

const heartClasses = computed(() => {
    const classes = [];
    const halvesRemaining = heartCount.value * 2; // Convert heartCount to halves
  
    for (let index = 1; index <= totalHearts; index++) {
      const heartPosition = index * 2; // Positions 2, 4, 6, 8, 10
      if (heartPosition - 1 < halvesRemaining) {
        classes.push("heart-filled");
      } else if (heartPosition - 2 < halvesRemaining) {
        classes.push("heart-half-filled");
      } else {
        classes.push("heart-empty");
      }
    }
    return classes;
  });

export {
    totalHearts,
    heartClasses,
    initializeHeartCount,
    setupHeartRegeneration,
    handleStorageChange
}
