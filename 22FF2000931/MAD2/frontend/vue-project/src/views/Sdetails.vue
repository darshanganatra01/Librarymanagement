
<script>
import axios from 'axios';
import { RouterLink } from 'vue-router';

export default{

  name:'Sdetails',
  data(){
    return{
        sid:parseInt(this.$route.params.id, 10),
        books:[],
        section:{},
        role:""
    };
  },
  methods:{
    logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},

    async sbooks(){
    try{
        const token = localStorage.getItem('token');
        const response=await axios.get(`http://localhost:5000/sbooks/${this.sid}`,{
          headers:{
            'Authorization':token
          }
        });
        if (response.status==200){
            this.books=response.data.rlist,
            this.section=response.data.sec}
           

    }   
    catch(error) {
      const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      if(error.response.statusText=="UNAUTHORIZED"){
          alert("Token requred for authentication please login and come back!")
          this.$router.push('/liblogin')}
      
      else{alert(`Error: ${errorMessage}`);}
    }
  },async deletesec(sid){
    try{
        const token = localStorage.getItem('token');
        const response=await axios.get(`http://localhost:5000/deletesec/${this.sid}`,{
            headers:{
                'Authorization':token
            }
        });
        if (response.status==201){
            alert(response.data.message)
            this.$router.push(`/adash`)

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
  },
},
  created(){
        this.token = localStorage.getItem('token')
        this.role = localStorage.getItem('role')
        if(!this.token){
          alert("Auth Token Required Please Login") 
          this.$router.push('/')
        }
        else{
            this.sbooks();
        }
      }
    }


</script>


<template>
  <div id="navbar">
    <h3 class="dashboard-title">Details for Particular Section</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink v-if="this.role=='user'" to="/udash">User Dashboard</RouterLink>
      <RouterLink v-if="this.role=='admin'" to="/adash">Admin Dashboard</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
    </div>
  </div>  

  <div class="section-details-container">
    <h1 class="section-title">Book Details for Section</h1>
    <h2 class="section-name">Section Name: <span>{{ this.section.sname }}</span></h2>
    <h2 class="section-description">Description: <span>{{ this.section.description }}</span></h2>

    <div v-if="this.role == 'user'" class="user-books">
      <h3 v-for="i in books" :key="i.bid" class="book-item">
        <a :href="`/book/${i.bid}`" class="book-link"><h3>{{ i.bname }}</h3>by {{ i.author }}</a>
      </h3>
    </div>

    <div v-if="this.role == 'admin'" class="admin-section">
      <h3 v-for="i in books" :key="i.bid" class="book-item">
        <h4><a :href="`/abook/${i.bid}`" class="book-link"><h3>{{ i.bname }} </h3>by {{ i.author }}</a></h4>
      </h3>

      <div class="admin-controls">
        <button @click="this.$router.push(`/editsection/${this.sid}`)" class="btn btn-primary">Edit Section</button>
        <button @click="deletesec(this.sid)" class="btn btn-warning">Delete Section</button>
        <button @click="this.$router.push(`/addbooks/${this.sid}`)" class="btn btn-success">Add Books</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Navbar Styles */
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

/* Section Details Container Styles */
.section-details-container {
  max-width: 1100px;
  margin: 120px auto 20px;
  padding: 50px;
  background-color: #ffffff;
  border-radius: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.section-title {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 25px;
  font-weight: bold;
}

.section-name,
.section-description {
  font-size: 22px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.section-name span,
.section-description span {
  color: #2980b9;
  font-weight: 600;
}

/* User Books List Styles */
.user-books,
.admin-section {
  margin-top: 40px;
}

.book-item {
  margin-bottom: 15px;
  font-size: 20px;
  color: #2c3e50;
  background-color: #f8f9fa;
  padding: 14px 25px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.book-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.book-link {
  color: #2980b9;
  text-decoration: none;
  transition: color 0.3s ease;
  font-size: 20px;
}

.book-link:hover {
  color: #1b73a1;
  text-decoration: underline;
}

/* Admin Controls Styles */
.admin-controls {
  margin-top: 30px;
  display: flex;
  justify-content: center;
  gap: 20px;
}

.btn {
  padding: 14px 25px;
  font-size: 18px;
  border-radius: 30px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-primary {
  background-color: #3498db;
  color: #ffffff;
}

.btn-warning {
  background-color: #f39c12;
  color: #ffffff;
}

.btn-success {
  background-color: #2ecc71;
  color: #ffffff;
}

.btn-primary:hover,
.btn-warning:hover,
.btn-success:hover {
  transform: scale(1.05);
  opacity: 0.9;
}
</style>
