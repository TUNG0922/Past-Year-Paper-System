<template>
  <div id="app">
    <component :is="currentView" @switch-view="toggleView" @login-success="navigateToHome" />
  </div>
</template>

<script>
import LoginPage from './components/LoginPage.vue';
import RegisterPage from './components/RegisterPage.vue';
import StudentDashboard from './components/StudentDashboard.vue';
import LecturerDashboard from './components/LecturerDashboard.vue';

export default {
  name: 'App',
  components: {
    LoginPage,
    RegisterPage,
    StudentDashboard,
    LecturerDashboard,
  },
  data() {
    return {
      currentView: 'LoginPage', // Set the initial view to LoginPage
      role: '', // Store user role
    };
  },
  methods: {
    toggleView() {
      // Toggle between LoginPage and RegisterPage
      this.currentView = this.currentView === 'LoginPage' ? 'RegisterPage' : 'LoginPage';
    },
    navigateToHome(role) {
      // Set the role and navigate to the Home page (StudentDashboard or LecturerDashboard)
      this.role = role;
      this.currentView = role === 'student' ? 'StudentDashboard' : 'LecturerDashboard';
    },
  },
};
</script>

<style>
/* Prevent scrolling on the entire application */
html, body, #app {
  height: 100%; /* Full height */
  width: 100%; /* Full width */
  margin: 0; /* Remove default margin */
  overflow: hidden; /* Prevent scrolling */
}
</style>
