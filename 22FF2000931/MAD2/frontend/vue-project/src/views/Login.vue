<script>
import axios from 'axios';

export default {
  name: 'LoginForm',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://localhost:5000/apilogin', {
          email: this.email,
          password: this.password
        });
        if (response.status==200){
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('role',response.data.role)
          this.$router.push('/udash')}
          
      } catch (error) {
        const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      alert(`Error: ${errorMessage}`);
    }
  },autologout(){
    localStorage.clear();
  }
},
created(){
  this.autologout();
}
}
</script>



<template>

  <div id="navbar">
      <h3 class="dashboard-title">Welcome to User Login</h3>
      <div class="right-links">
        <RouterLink to="/">Home</RouterLink>
      </div>
    </div>
    <div>
      <title>Music Streaming App</title>
      <div id="top-right">
      </div>
  
      <div id="signin-form">
        <h2>LOGIN</h2>
        <form @submit.prevent="login">
          <label for="email">Email:</label>
          <input type="email" v-model="this.email" required /><br />
          <label for="password">Password:</label>
          <input type="password" v-model="this.password" required /><br />
          <div style="text-align: center;">
            <input type="submit" value="Login" />
          </div>
        </form>
        <p>Don't have an account? <a href="/signup">Sign Up</a></p>
      </div>
    </div>
  </template>
  
  <style scoped>
  body {
    font-family: 'Open Sans', sans-serif;
    background-size: cover;
    background-repeat: no-repeat;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
  }
  
  #top-right {
    position: absolute;
    top: 10px;
    right: 10px;
  }
  
  #top-right a {
    text-decoration: none;
    color: black;
    font-weight: bold;
    font-size: 24px;
    padding: 5px 10px;
  }
  
  #top-right a[href="/admin"] {
    color: #3498db;
  }
  
  #signin-form {
    margin-top: 500px; /* Increased margin */
    background-color: whitesmoke;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    max-width: 600px;
    width: 80%;
    margin: 110px auto; /* Increased margin */
  }
  
  .title {
    font-size: 28px;
    font-weight: bold;
    color: #333;
  }
  
  form {
    margin: 20px 0;
    text-align: left;
  }
  
  label {
    display: block;
    margin: 10px 0;
    color: #555;
    font-weight: bold;
  }
  
  input[type='email'],
  input[type='password'] {
    width: 100%;
    padding: 5px;
    margin: 10px 0;
    border: 2px solid #ccc;
    border-radius: 10px;
    font-family: 'Roboto', sans-serif;
    font-size: 14px;
    color: #333;
  }
  
  input[type='submit'] {
    background-color: #3498db;
    color: #fff;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    cursor: pointer;
    transition: background-color 0.3s;
    font-family: 'Roboto', sans-serif;
    font-size: 16px;
    margin-top: 10px;
  }
  
  input[type='submit']:hover {
    background-color: #1e75c9;
  }
  
  a {
    color: #3498db;
    text-decoration: none;
  }
  
  a:hover {
    text-decoration: underline;
  }
  
  .flash {
    font-family: 'Roboto', sans-serif;
    font-size: 16px;
    font-weight: bold;
    animation: fadeOut 4s forwards;
  }
  
  @keyframes fadeOut {
    to {
      opacity: 0;
    }
  }
  
  .logo {
    margin: 0;
    text-align: center;
    margin-right: 0;
    margin-top: 0;
  }
  
  #navbar {
    width: 100%;
    background-color: #2c3e50;
    display: flex;
    justify-content: space-between; /* Aligns title to the left and links to the right */
    align-items: center;
    padding: 15px 30px;
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1000;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    margin-bottom: 40px; /* Added margin-bottom */
  }
  
  #navbar .right-links {
    display: flex;
    align-items: center;
    margin-right: 35px;
  }
  
  #navbar .right-links a {
    color: #ecf0f1;
    padding: 8px 15px;
    text-decoration: none;
    font-size: 16px;
    transition: background-color 0.3s ease, color 0.3s ease;
  }
  
  #navbar a:hover {
    background-color: #34495e;
    color: #ecf0f1;
  }
  
  #navbar a.active {
    background-color: #2980b9;
    color: white;
    border-radius: 4px;
  }
  
  .dashboard-title {
    color: white;
  }
  
  </style>
  