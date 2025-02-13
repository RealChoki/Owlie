<template>
    <div class="profile-page">
      <!-- Header: Profile Info -->
      <div class="profile-header">
        <img :src="user.profilePic" alt="Profile Picture" class="profile-pic" />
        <div>
          <h1>{{ user.name }}</h1>
          <p>{{ user.university }} - {{ user.subject }}</p>
        </div>
      </div>
  
      <!-- Usage Stats: Assistant Modes -->
      <div class="usage-stats">
        <h2>Assistant Modes Usage</h2>
        <table>
          <thead>
            <tr>
              <th>Mode</th>
              <th>Usage Count</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="([mode, count], index) in sortedModesArray" 
              :key="index"
            >
              <td>{{ mode }}</td>
              <td>{{ count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- Usage Stats: Courses -->
      <div class="course-stats">
        <h2>Most Used Courses</h2>
        <table>
          <thead>
            <tr>
              <th>Course</th>
              <th>Usage Count</th>
            </tr>
          </thead>
          <tbody>
            <tr 
              v-for="([course, count], index) in sortedCoursesArray" 
              :key="index"
            >
              <td>{{ course }}</td>
              <td>{{ count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue'
  
  // 1) Mock user profile data
  const user = ref({
    name: 'John Doe',
    university: 'Some University',
    subject: 'Computer Science',
    profilePic: 'https://via.placeholder.com/150'
  })
  
  // 2) Mock usage data for assistant modes
  //    (Replace with real data from your backend or store)
  const modeUsage = ref({
    exam: 10,
    quiz: 5,
    general: 20
  })
  
  // 3) Mock usage data for courses
  const courseUsage = ref({
    'Math 101': 15,
    'CS 202': 20,
    'History 303': 5
  })
  
  // 4) Convert mode usage object into an array, then sort by usage (descending)
  const sortedModesArray = computed(() => {
    return Object.entries(modeUsage.value)
      .sort((a, b) => b[1] - a[1]) // sort by usage count descending
  })
  
  // 5) Convert course usage object into an array, then sort by usage (descending)
  const sortedCoursesArray = computed(() => {
    return Object.entries(courseUsage.value)
      .sort((a, b) => b[1] - a[1])
  })
  
  // 6) Fetch user & usage data on mount (if needed)
  //    (This is where you'd call your API, e.g., fetch('/api/profile')...)
  //    For demo, we're just using the hardcoded data above
  onMounted(() => {
    // Example:
    // fetch('/api/profile')
    //   .then(res => res.json())
    //   .then(data => {
    //     user.value = data.user
    //     modeUsage.value = data.modeUsage
    //     courseUsage.value = data.courseUsage
    //   })
  })
  </script>
  
  <style scoped>
  .profile-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 24px;
    font-family: Arial, sans-serif;
  }
  
  .profile-header {
    display: flex;
    align-items: center;
    margin-bottom: 24px;
  }
  
  .profile-pic {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 16px;
  }
  
  /* Basic table styling */
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    margin-bottom: 24px;
  }
  
  table th,
  table td {
    border: 1px solid #ddd;
    padding: 8px 12px;
    text-align: left;
  }
  
  table thead {
    background-color: #f9f9f9;
  }
  </style>
  