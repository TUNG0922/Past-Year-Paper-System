<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <h2>Login</h2>
      <div>
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="role">Role:</label>
        <select id="role" v-model="role" required>
          <option value="" disabled>Select your role</option>
          <option value="student">Student</option>
          <option value="lecturer">Lecturer</option>
        </select>
      </div>
      <button type="submit">Login</button>
      <button type="button" @click="switchToRegister">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'; // Import axios to make HTTP requests

export default {
  data() {
    return {
      username: '',
      password: '',
      role: '' // Data property for role
    };
  },
  methods: {
    async handleLogin() {
      try {
        // Send a POST request to the login endpoint
        const response = await axios.post('http://localhost:5000/login', {
          username: this.username,
          password: this.password,
          role: this.role, // Include role in the login request
        });
        
        // Handle successful login response
        console.log(response.data.message);
        alert('Login successful!'); // Notify user

        // Emit event with role for navigation
        this.$emit('login-success', response.data.role);
      } catch (error) {
        console.error('Error during login:', error);
        // Handle error response from the backend
        if (error.response && error.response.data) {
          alert(error.response.data.message || 'Login failed!'); // Show error message
        } else {
          alert('Login failed!'); // Generic error message
        }
      }
    },
    switchToRegister() {
      this.$emit('switch-view'); // Emit an event to switch views
    }
  }
};
</script>

<style scoped>
.login-container {
  background-image: url('@/assets/upm.png'); /* Replace with your image filename */
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

form {
  background: rgba(255, 255, 255, 0.8);
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

select {
  padding: 0.5rem;
  border-radius: 5px;
  border: 1px solid #ccc;
}

button {
  padding: 0.5rem;
  border-radius: 5px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #0056b3;
}
</style>
