<template>
  <div class="search-container">
    <form>
      <span class="search">Search</span> : <input type="text" v-model="query" @input="search" class="search-input">
    </form>

    <!-- For admin -->
    <div v-if="this.role=='admin'" class="search-results">
      <h3 v-if="sresults?.book?.length">Matched books</h3>
      <h4 v-for="i in sresults.book" :key="i.bid">
        <a :href="'/Abook/' + i.bid">{{ i.bname }}</a>
      </h4>
      <h3 v-if="sresults?.section?.length">Matched sections</h3>
      <h4 v-for="i in sresults.section" :key="i.sid">
        <a :href="'/sdetails/' + i.sid">{{ i.sname }}</a>
      </h4>
      <h3 v-if="sresults?.author?.length">Matched authors</h3>
      <h4 v-for="i in sresults.author" :key="i.author">
        <a :href="'/Abook/' + i.bid">{{ i.author }}</a>
      </h4>
    </div>

    <!-- for user -->
    <div v-if="this.role=='user'" class="search-results">
      <h3 v-if="sresults?.book?.length">Matched books</h3>
      <h4 v-for="i in sresults.book" :key="i.bid">
        <a :href="'/book/' + i.bid">{{ i.bname }}</a>
      </h4>
      <h3 v-if="sresults?.section?.length">Matched sections</h3>
      <h4 v-for="i in sresults.section" :key="i.sid">
        <a :href="'/sdetails/' + i.sid">{{ i.sname }}</a>
      </h4>
      <h3 v-if="sresults?.author?.length">Matched authors</h3>
      <h4 v-for="i in sresults.author" :key="i.author">
        <a :href="'/book/' + i.bid">{{ i.author }}</a>
      </h4>
    </div>
  </div>
</template>

<style scoped>

.search{
  font-size: large;
  color: white;
}
.search-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 30px;
  background-color: #2c3e50;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin-top: 15px;
  border-radius: 8px;
}

.search-input {
  padding: 10px;
  width: 400px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 16px;
  margin-bottom: 20px;
}

.search-input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5);
}

.search-results {
  width: 100%;
  max-width: 500px;
}

h3, h4 {
  color:whitesmoke;
  margin-bottom: 10px;
}

a {
  color: white;
  text-decoration: none;
}

a:hover {
  color: #0056b3;
  text-decoration: underline;
}
</style>


<script>
import axios from 'axios';
    export default{
        name:"Search",
        data(){
            return {
               sresults:{},
               query:"",
               token:"",
               role:""
            };
        },
        methods:{
            async search(){
    try{
        const response=await axios.get(`http://localhost:5000/search/${this.query}+ing`,{
          headers:{
            'Authorization':`${this.token}`
          }
        });
        if (response.status==200){
            this.sresults=response.data
            console.log(response.data)
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
        }
    },
    created(){
        this.token =localStorage.getItem('token')
        this.role=localStorage.getItem('role')
    }}
</script>


