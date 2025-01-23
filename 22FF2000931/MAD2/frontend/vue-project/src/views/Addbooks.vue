<template>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Add Book To Section</title>
</head>
<body>

    <div id="navbar">
    <h3 class="dashboard-title">Add books</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
      <RouterLink to="/adash">Admin Dashboard</RouterLink>
    </div>
    </div>

    <div id="upload-form">
        <h2><u>Add book to section</u></h2>
        <form enctype="multipart/form-data" @submit.prevent="addbooks">

            <label for="title">Title:</label>
            <input type="text" v-model="bname" required><br>
            
            <label for="author">Author:</label>
            <input type="text" v-model="author" required><br>

            <label for="description">Description:</label>
            <input type="text" v-model="bdescription" required><br>

            <label for="release_date">Release Date:</label>
            <input type="date" v-model="bdate" required><br>

            <label for="file">Upload Book:</label>
            <input type="file" @change="handlefile" required><br>
            
            <input type="submit" value="Upload">
        </form>
        <p> Go Back To Dashboard <a href="/adash"> Click Here </a></p>
    </div>
</body>
</html>
</template>


<script>

import axios from 'axios';
import { RouterLink } from 'vue-router';

export default{
    name:"Addbooks",
    data(){
        return{
        sid:parseInt(this.$route.params.sid),
        bname:"",
        author:"",
        bdate:"",
        bdescription:"",
        bookfile:null,
        role:""
        };
    },
    methods:{
        logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},

        handlefile(event){
            this.bookfile=event.target.files[0];
        },
        
        async addbooks(){
            const formData = new FormData();
                formData.append('bname', this.bname);
                formData.append('author', this.author);
                formData.append('bdescription', this.bdescription);
                formData.append('bdate', this.bdate);
                formData.append('bookfile', this.bookfile);
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`http://localhost:5000/addbooks/${this.sid}`,formData,
            {headers:{
                'Content-Type': 'multipart/form-data',
                'Authorization': token
            }});

            if (response.status==201){
                this.$router.push(`/sdetails/${this.sid}`)
                alert(response.data.message)
            }
            
         }  catch(error) {
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
            background-size: cover;
            background-repeat: no-repeat;
            margin: 0;
            padding: 0;
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
            color: black;
            font-weight: bold;
            font-size: 24px;
    }

    #upload-form {
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
            max-width: 600px;
            width: 80%;
            margin: 20px;
            margin-left: 28%;
        }

    h2 {
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
        input[type="date"],
        input[type="submit"] {
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

        input[type="file"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0 20px 0;
            border: none;
            font-family: 'Roboto', sans-serif;
            font-size: 14px;
            color: #555;
            font-weight: bold;
        }

        input[type="submit"] {
            background-color: #444554;
            color: #fff;
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
            font-weight:bold;
        }

        a:hover {
            text-decoration: underline;
        }

        #dashboard-link {
            display: block;
            text-align: center;
            margin-top: 20px;
            color: #3498db;
            text-decoration: none;
            font-weight: bold;
        }

        #dashboard-link:hover {
            text-decoration: underline;
        }

        div.flash{
            animation: fadeOut 4s forwards; /* 5s animation duration */
            font-size:larger;
            font-weight:bold;
            margin-top:45px;
            margin-left:4%;
            text-decoration: underline;
    
        }
        
        @keyframes fadeOut {
            to {
                opacity: 0;
            }
        }
</style>
