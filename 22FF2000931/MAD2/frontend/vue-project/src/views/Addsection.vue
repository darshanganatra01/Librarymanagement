<template>
    <div>
   
      <div id="navbar">
    <h3 class="dashboard-title">Add Section</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
      <RouterLink to="/adash">Admin Dashboard</RouterLink>
    </div>
    </div>
      <title>Music Streaming App</title>
      <div id="signin-form">
        <h2>ADD SECTION</h2>
        <form @submit.prevent="addsection">
          <label for="name">Name:</label>
          <input type="name" v-model="this.name" required /><br />
          <label for="date">Date:</label>
          <input type="date" v-model="this.date" required /><br />
          <label for="description">Description:</label>
          <input type="description" v-model="this.description" required /><br />
          <div style="text-align: center;">
            <input type="submit" value="Add" />
          </div>
        </form>
      </div>
    </div>
</template>


<script>

import axios from 'axios';

export default{
    name:"Addsection",
    data(){
        return{
            name:"",
            date:"",
            description:"",
            role:""
        };
    },
    methods:{
      logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},
    async addsection() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://localhost:5000/addsection', {
          name:this.name,
          date:this.date,
          description: this.description
        },
        {
          headers:{
          'Authorization':token

        }});
        if (response.status==201){
          this.$router.push('/adash')
          alert(response.data.message)
        }
      } catch(error) {
      const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      if(error.response.statusText=="UNAUTHORIZED"){
          alert("Token requred for authentication please login and come back!")
          this.$router.push('/liblogin')}
      
      else if(error.response.statusText=="FORBIDDEN"){
            alert("Imposter Imposter!")
            this.$router.push('/liblogin')
      }
      
      else{alert(`Error: ${errorMessage}`);}
    }
  }},
  created(){
        this.token = localStorage.getItem('token')
        this.role = localStorage.getItem('role')
        if(!this.token){
          alert("Auth Token Required Please Login") 
          this.$router.push('/')
        }
        else if(this.role!="admin"){
          alert("You are not Admin:(") 
          this.$router.push('/liblogin')
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
  background-color: whitesmoke;
  border-radius: 10px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
  max-width: 600px;
  width: 80%;
  margin: 85px auto;
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

input[type='name'],
input[type='date'],
input[type='description'] {
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


.logo {
  margin: 0;
  text-align: center;
  margin-right: 0;
  margin-top: 0;
}
</style>

