<template>
    <div class="register-container">
      <form @submit.prevent="handleRegister">
        <h2>Register</h2>
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
        <button type="submit">Register</button> <!-- Register button -->
        <button type="button" @click="switchToLogin">Back to Login</button> <!-- Back to Login button -->
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
        role: ''
      };
    },
    methods: {
      async handleRegister() {
        try {
          // Make the registration request
          const response = await axios.post('http://localhost:5000/register', {
            username: this.username,
            password: this.password,
            role: this.role
          });
  
          // Handle successful registration response
          console.log(response.data.message);
          alert('Registration successful!'); // Notify user
          this.switchToLogin(); // Optionally switch to login view
        } catch (error) {
          // Handle error response
          console.error('Error during registration:', error);
          if (error.response && error.response.data) {
            alert(error.response.data.message || 'Registration failed!'); // Show error message
          } else {
            alert('Registration failed! Please check the console for more details.'); // Generic error message
          }
        }
      },
      switchToLogin() {
        this.$emit('switch-view'); // Emit an event to switch views
      }
    }
  };
  </script>
  
  <style scoped>
  .register-container {
    background-image: url('@/assets/upm.png'); /* Replace with your image filename */
    background-size: cover; /* Cover the entire container */
    background-repeat: no-repeat; /* Prevent repeating of the image */
    background-position: center; /* Center the image */
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh; /* Full height of the viewport */
    width: 100vw; /* Full width of the viewport */
    overflow: hidden; /* Prevent scrolling */
  }
  
  form {
    background: rgba(255, 255, 255, 0.8); /* Optional: Semi-transparent background for form */
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    display: flex;
    flex-direction: column;
    gap: 1rem; /* Space between form elements */
  }
  
  select {
    padding: 0.5rem; /* Add some padding to the select box */
    border-radius: 5px; /* Rounded corners for the select box */
    border: 1px solid #ccc; /* Border for the select box */
  }
  
  button {
    padding: 0.5rem; /* Padding for buttons */
    border-radius: 5px; /* Rounded corners for buttons */
    border: none; /* Remove default border */
    background-color: #007bff; /* Button background color */
    color: white; /* Button text color */
    cursor: pointer; /* Cursor pointer on hover */
    transition: background-color 0.3s; /* Smooth transition for background color */
  }
  
  button:hover {
    background-color: #0056b3; /* Darker color on hover */
  }
  </style>  