<template>
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
</head>
<body>
    <div id="navbar">
      <h3 class="dashboard-title">Welcome to Librarian Dashboard</h3>
      <div class="right-links">
        <RouterLink to="/">Home</RouterLink>
      </div>
    </div>
    <div id="signup-form">
        <h2>Sign Up</h2>
        <form @submit.prevent="signup">
            <label for="name">Name:</label>
            <input type="text" v-model="this.name" required><br>

            <label for="state">State:</label>
            <input type="text" v-model="this.state"><br>

            <label for="email">Email:</label>
            <input type="email" v-model="this.email" required><br>
            
            <label for="password">Password:</label>
            <input type="password" v-model="this.password" required><br>

            <input type="submit" value="Sign Up"/>
        </form>
        <p> Already have an account? <a href="/login">Sign In</a></p>
    </div>
</body>
</html>

</template>

<script>
import axios from 'axios';

export default{
    name:"SignupForm",
    data(){return{
        name:"",
        state:"",
        email:"",
        password:"",
    };
},
    methods:{
    async signup() {
      try {
        const response = await axios.post('http://localhost:5000/signup', {
          name:this.name,
          state:this.state,
          email: this.email,
          password: this.password
        });
        if (response.status==201){
          this.$router.push('/login')
          alert(response.data.message)
        }
      } catch(error) {
        const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      alert(`Error: ${errorMessage}`);
    }
  }
}

}
    
</script>


<style scoped>
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
  
        body {
            font-family: 'Open Sans', sans-serif;
            background-size: cover;
            background-repeat: no-repeat;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }

        #top-right {
            position: absolute;
            top: 10px;
            right: 10px;
        }

        #top-right a {
            text-decoration: none;
            color: black; /* Change color to black */
            font-weight: bold;
            font-size: 24px; /* Increase font size */
        }

        #signup-form {
            background-color:whitesmoke;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            max-width: 600px;
            width: 80%;
            margin: 40px auto;
        }

        h2 {
            font-family: Georgia, 'Times New Roman', Times, serif;
            font-size: 24px;
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
            color: #333;
            font-weight: bold;
        }

        input[type="text"],
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 5px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #555;
            font-weight: bold;
        }

        input[type="submit"] {
            background-color: #3498db;
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            margin: 10px auto;
            display: block;
        }

        input[type="submit"]:hover {
            background-color: #1e75c9;
        }

        a {
            color: #3498db;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        .uniquemail{
            font-family: 'Roboto', sans-serif;
            font-size: 16px;
            font-weight: bold;
            animation: fadeOut 4s forwards; /* 5s animation duration */
        }

        div.logo{
            margin:0;
            text-align:center;
            margin-right:0;
            margin-top:0;
        }

           
</style>