<template>
    <div>  
      <div class="black-box">
        <h1>Review This Book</h1>
        <form @submit.prevent="postreview">
          <div class="radio-box">
            <input type="radio" name="rev" value="1" v-model="review"> 1 : Did not meet expectations:(<br>
            <input type="radio" name="rev" value="2" v-model="review"> 2 : Not My Type!<br>
            <input type="radio" name="rev" value="3" v-model="review"> 3 : Okayish!<br>
            <input type="radio" name="rev" value="4" v-model="review"> 4 : Vibe Toh Hai;)<br>
            <input type="radio" name="rev" value="5" v-model="review"> 5 : Amazing!! <br>
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  </template>

<script>
import axios from 'axios';
    export default{
        name:"Review",
        data(){
            return{
                review:""
            };
        },
        props:{
            bid:Number,
        },
        methods: {
    async postreview() {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.post(`http://localhost:5000/breview/${this.bid}`, {
                review: this.review,
            }, {
                headers: {
                    'Authorization': token
                }
            });

            if (response.status == 201) {
                this.getreview();
                this.$router.push(`/book/${this.bid}`);
                alert(response.data.message);
            }
        } catch (error) {
            let errorMessage = 'An error occurred';
            if (error.response) {
                errorMessage = error.response.data && error.response.data.message
                    ? error.response.data.message
                    : error.response.statusText;
                
                if (error.response.status == 401) {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/liblogin');
                    return;
                }
                
                if (error.response.status == 403) {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                    return;
                }
            }
            alert(`Error: ${errorMessage}`);
        }
    },
    async getreview() {
        try {
            const token = localStorage.getItem('token');
            const response = await axios.get(`http://localhost:5000/breview/${this.bid}`, {
                headers: {
                    'Authorization': token
                }
            });
            if (response.status == 200) {
                this.review = parseInt(response.data.stars);
            }
        } catch (error) {
            let errorMessage = 'An error occurred';
            if (error.response) {
                errorMessage = error.response.data && error.response.data.message
                    ? error.response.data.message
                    : 'An error occurred';
                
                if (error.response.status == 401) {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/liblogin');
                    return;
                } else if (error.response.status == 403) {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                    return;
                }
            }
            alert(`Error: ${errorMessage}`);
        }
    }
},
created() {
    this.token = localStorage.getItem('token');
    this.role = localStorage.getItem('role');
    this.getreview();
}

    }
</script>

<style scoped>
        .black-box {
            margin:auto;
            padding: 35px;
            border:solid;
            border-radius: 15px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center; 
            width:450px;
            border-color:black;
            margin-top: 90px;

        }

        h1 {
            font-size: 28px;
            margin-bottom: 60px;
            background-color: #444554;
            color:white;
            margin-top: 0;
            margin:0;
            padding:14px 10px;
        }
        

        form {
            width: 300px;
            margin: 0 auto; /* Center the form */
            text-align: center;

        }

        .radio-box {
            margin-top: 50px;
            font-size: 20px;
            margin-bottom: 30px;
            text-align: left;
        }

        input[type="radio"] {
            margin-bottom: 10px;
        }

        button {
            margin-top: 30px;
            padding: 13px 25px;
            background-color: #444554;
            color: #fff;
            border: none;
            border-radius: 3px;
            cursor: pointer;
            transition: background-color 0.3s;
            font-size: 16px;

        }

        button:hover {
            background-color: #333;
        }
    </style>
