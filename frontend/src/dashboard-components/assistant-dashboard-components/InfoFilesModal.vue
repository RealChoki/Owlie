<template>
  <div class="modal fade" id="infoFilesModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header d-flex justify-content-between align-items-center">
          <h5 class="modal-title"><b>Accepted Formats</b></h5>
          <font-awesome-icon
            class="fa-2x cursor-pointer text-white"
            :icon="['fas', 'xmark']"
            data-bs-dismiss="modal"
            aria-label="Close"
          />
        </div>
        <div class="modal-body pb-3 pt-2">
          <table class="table-sm text-white">
            <thead>
              <tr>
                <th>Extension</th>
                <th>Mime Type</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in combinedData" :key="index">
                <td>{{ item.extension }}</td>
                <td>{{ item.mime }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { defineProps, computed } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faXmark } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'

library.add(faXmark)

// Define props for acceptedFileTypes and acceptedMimeTypes
const props = defineProps({
  acceptedFileTypes: {
    type: Array as () => string[],
    required: true
  },
  acceptedMimeTypes: {
    type: Array as () => string[],
    required: true
  }
})

const combinedData = computed(() => {
  const maxLen = Math.max(props.acceptedFileTypes.length, props.acceptedMimeTypes.length)
  const result = []
  for (let i = 0; i < maxLen; i++) {
    result.push({
      extension: props.acceptedFileTypes[i] || '',
      mime: props.acceptedMimeTypes[i] || ''
    })
  }
  return result
})
</script>

<style scoped>
.modal-content {
  background-color: var(--color-gray-medium);
  border: 1px solid var(--color-gray-shadow);
  border-radius: 8px;
}

.modal-header {
  border-bottom: 1px solid var(--color-gray-shadow);
}

.modal-title {
  color: var(--text-color);
}

.modal-body {
  color: var(--text-color);
  padding-bottom: 0;
}

.modal-body p {
  margin-bottom: 0;
}

/* Table styles  */
table {
  border-collapse: collapse;
  background-color: var(--color-gray-medium);
  width: 100%;
}

table thead th,
table tbody td {
  border-left: 1px solid #333; /* Border only between columns */
  border-top: 1px solid #333; /* Border only between rows */
  color: var(--text-color);
}

table tbody td:first-child,
table thead th:first-child {
  border-left: none; /* Remove left border for the first column */
}

table tbody tr:first-child td {
  border-top: none; /* Remove top border for the first row */
}

table thead th {
  border-top: none;
  border-bottom: 1px solid #333; /* Add bottom border to the header */
}
</style>
