<template>
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Editbook</title>
    </head>
    <body>
        <div id="navbar">
        <h3 class="dashboard-title">Edit Book</h3>
        <div class="right-links">
            <RouterLink to="/">Home</RouterLink>
            <RouterLink to="/adash">Admin Dashboard</RouterLink>
            <a href="#" @click.prevent="logout">Logout</a>
        </div>
        </div>

        <div id="upload-form">
            <h2><u>Edit the book</u></h2>
            <form enctype="multipart/form-data" @submit.prevent="editbook">
    
                <label for="title">Title:</label>
                <input type="text" v-model="bname" required><br>
                
                <label for="author">Author:</label>
                <input type="text" v-model="author" required><br>
    
                <label for="description">Description:</label>
                <input type="text" v-model="bdescription" required><br>
    
                <label for="release_date">Release Date:</label>
                <input type="date" v-model="bdate" required><br>
    
                <label for="file">Edit Book file (will be same otherwise):</label>
                <input type="file" @change="handlefile"><br>
                
                
                <input type="submit" value="Edit">
            </form>
            <p> Go Back To Dashboard <a href="/adash"> Click Here </a></p>
        </div>
    </body>
    </html>
    </template>
    
    
    <script>
    
    import axios from 'axios';
    
    export default{
        name:"Editbook",
        data(){
            return{
            bid:parseInt(this.$route.params.bid),
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
            
            async editbook(){
                const edformData = new FormData();
                    edformData.append('bname', this.bname);
                    edformData.append('author', this.author);
                    edformData.append('bdescription', this.bdescription);
                    edformData.append('bdate', this.bdate);
                    edformData.append('bookfile', this.bookfile);
            try {
                const token = localStorage.getItem('token');
                const response = await axios.post(`http://localhost:5000/editbook/${this.bid}`,edformData,
                {headers:{
                    'Content-Type': 'multipart/form-data',
                    'Authorization': token
                }});
    
                if (response.status==201){
                    this.$router.push(`/abook/${this.bid}`)
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
      },
    async getbook(){
        try{
        const token = localStorage.getItem('token');
        const response=await axios.get(`http://localhost:5000/bookinfo/${this.bid}`,{
          headers:{
            'Authorization':token
          }
        });
        if (response.status==200){
            this.bname=response.data.book.bname,
            this.author=response.data.book.author,
            this.bdate=response.data.book.bdate,
            this.bdescription=response.data.book.bdescription
           }
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
            else{
                this.getbook();
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
        background-image: url("road-220058_1920.jpg");
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
        font-weight: bold;
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