<script>
import axios from 'axios';
import Searchbar from '@/components/Searchbar.vue';
import { RouterLink } from 'vue-router';

export default{

  name:'Udash',
  components:{
    Searchbar
  },
  data()
  {
    return{
    token:"",
    role:"",
    sections:[],
    latestbooks:[]
  };
  },
  methods:{
    logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},
  async autorevoke(){
    try{
        const response=await axios.get('http://localhost:5000/autorevoke',{
          headers:{
            'Authorization':`${this.token}`
          }
        });
        if (response.status==201){
            alert(response.data.message)
        }}   
    catch(error) {
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
}, async getsec(){
    try{
        const response=await axios.get('http://localhost:5000/secinfo',{
          headers:{
            'Authorization':`${this.token}`
          }
        });

        if (response.status==200){
          console.log(response.data.sec);
          this.sections=response.data.sec 
          this.latestbooks=response.data.latestbooks

        }}   
    catch(error) {
      const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';
      
        alert(`Error: ${errorMessage}`);
    }
}
  },
  created(){
    this.token = localStorage.getItem('token');
    this.role = localStorage.getItem('role');
    this.autorevoke();
    this.getsec();
  }}
</script>

<template>
  <div id="navbar">
    <h3 class="dashboard-title">Welcome to User Dashboard</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/userprofile">Profile</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
    </div>
  </div>

  <Searchbar />

  <div class="welcome-container">
    <h2>Sections</h2>
  </div>

  <div class="card-container">
    <div v-for="i in sections" :key="i.sid" class="card">
      <h3>
        <a :href="`/sdetails/${i.sid}`">{{ i.name }}</a>
      </h3>
    </div>
  </div>

  <div class="latest-releases">
    <h2>Latest Releases</h2>
    <table class="styled-table">
      <thead>
        <tr>
          <th>Book Name</th>
          <th>Author</th>
          <th>Date Uploaded</th>
          <th>Avg Rating</th>
          <th>TAP</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="i in latestbooks" :key="i.bid">
          <td>{{ i.bname }}</td>
          <td>{{ i.author }}</td>
          <td>{{ i.bdate }}</td>
          <td>{{ i.avgrev }}</td>
          <td><button @click="this.$router.push(`/book/${i.bid}`)">Explore</button></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
#navbar {
  width: 100%;
  background-color: #2c3e50;
  display: flex;
  justify-content: space-between;
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

.welcome-container {
  text-align: center;
  margin: 120px 0 40px; /* Adjusted for navbar space */
}

.welcome-container h1 {
  font-size: 2em;
  color: #2c3e50;
  margin-bottom: 10px;
}

.welcome-container h2 {
  font-size: 1.5em;
  color: #495057;
}

.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

.card {
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  width: 200px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.card h3 {
  margin: 0;
  font-size: 1.2em;
  color: #333;
}

.card a {
  text-decoration: none;
  color: #007BFF;
}

.card a:hover {
  text-decoration: underline;
}

/* Table Styles */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  margin: 25px 0;
  font-size: 18px;
  text-align: left;
  background-color: #ecf0f1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  overflow: hidden;
}

.styled-table thead tr {
  background-color: #2c3e50;
  color: #ffffff;
  text-align: left;
  font-weight: bold;
}

.styled-table th, 
.styled-table td {
  padding: 12px 15px;
}

.styled-table tbody tr {
  border-bottom: 1px solid #dddddd;
}

.styled-table tbody tr:nth-of-type(even) {
  background-color: #f3f3f3;
}

.styled-table tbody tr:last-of-type {
  border-bottom: 2px solid #2c3e50;
}

.styled-table tbody tr:hover {
  background-color: #ddd;
  cursor: pointer;
}

.styled-table tbody td {
  color: #2c3e50;
  font-weight: 500;
}

.latest-releases {
  margin-top: 50px;
  padding: 20px;
}

.latest-releases h2 {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
}
</style>
