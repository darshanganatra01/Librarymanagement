<template>
  <div id="navbar">
    <h3 class="dashboard-title">Welcome to User Profile</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/udash">User Dashboard</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
    </div>
  </div>

  <div class="user-info">
    <p><strong>Username:</strong> {{ cuser.username }}</p>
    <p><strong>Email:</strong> {{ cuser.email }}</p>
  </div>

  <div class="book-collection">
    <h3 v-if="this.abooks.length">Your Book Collection</h3>
    <h3 v-else>You don't have any books to read. Want to explore? Go to the dashboard.</h3>
    <div v-for="i in abooks" :key="i.bid" class="book-item">
      <p><strong>Book:</strong> {{ i.bname }}</p>
      <button @click="this.$router.push(`/book/${i.bid}`)" class="btn btn-primary">Explore</button>
    </div>
  </div>

  <div class="pending-requests">
    <h3 v-if="this.pbooks.length">Your Pending Requests</h3>
    <h3 v-else>You don't have any pending requests.</h3>
    <div v-for="i in pbooks" :key="i.bid" class="book-item">
      <p><strong>Book:</strong> {{ i.bname }}</p>
      <button @click="this.$router.push(`/book/${i.bid}`)" class="btn btn-primary">Explore</button>
    </div>
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

.user-info {
  margin: 100px auto 20px;
  padding: 20px;
  max-width: 800px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.user-info p {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 10px;
}

.book-collection,
.pending-requests {
  margin: 20px auto;
  padding: 20px;
  max-width: 800px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.book-item {
  margin-bottom: 20px;
}

.book-item p {
  font-size: 18px;
  color: #2c3e50;
  margin-bottom: 5px;
}

.btn {
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.btn-primary {
  background-color: #2980b9;
  color: #ffffff;
}

.btn-primary:hover {
  transform: scale(1.05);
  opacity: 0.9;
}
</style>

<script>
import axios from 'axios';
import { RouterLink } from 'vue-router';

    export default{
        name:"Profile",
        data(){
            return{
                abooks:[],
                pbooks:[],
                cuser:{},
                token:""
            };
        },
    methods:{
      logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},
        async getprofile(){
            try{
        const response=await axios.get('http://localhost:5000/getprofile',{
          headers:{
            'Authorization':`${this.token}`
          }
        });
        if (response.status==200){
            this.abooks=response.data.abooks;
            this.pbooks=response.data.pbooks;
            this.cuser=response.data.cuser
        }}   
    catch(error) {
      const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      if(error.response.statusText=="UNAUTHORIZED"){
          alert("Token requred for authentication please login and come back!")
          this.$router.push('/login')}
      
      else{alert(`Error: ${errorMessage}`);}
    }
            }
        },
        created(){
            this.token=localStorage.getItem("token")
            this.getprofile();
        }
    }
</script>
