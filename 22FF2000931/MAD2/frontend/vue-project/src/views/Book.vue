<template>
    <div id="navbar">
        <h3 class="dashboard-title">Book Details</h3>
        <div class="right-links">
            <RouterLink to="/">Home</RouterLink>
            <RouterLink to="/udash">User Dashboard</RouterLink>
            <a href="#" @click.prevent="logout">Logout</a>
        </div>
  </div>
    <div class="book-container">
      <div class="book-card">
        <h2>Book Name: <span>{{ this.book.bname }}</span></h2>
        <h2>Description: <span>{{ this.book.bdescription }}</span></h2>
        <h2>Author: <span>{{ this.book.author }}</span></h2>

        <div v-if="this.bstatus.status == 2" class="status-card issued">
          <h4>Issued Date: <span>{{ this.bstatus.idate }}</span></h4>
          <h4>Return By: <span>{{ this.bstatus.rdate }}</span></h4>
          <button @click="getpdf(this.bid)" class="btn btn-primary">Open PDF</button>
          <button @click="breturn(this.bid)" class="btn btn-success">Return Book</button>
        </div>
        

        <div v-if="this.bstatus.status == 1" class="status-card pending">
          <h3>Request Still Pending</h3>
          <h4>Applied Date: <span>{{ this.bstatus.adate }}</span></h4>
        </div>
        

        <div v-if="this.bstatus.status == 0" class="status-card rejected">
          <h4>Request Rejected, Request Again</h4>
          <button @click="brequest(this.bid)" class="btn btn-warning">Request Book</button>
        </div>

        <div v-if="this.bstatus.status == -1" class="status-card available">
          <h4>You Can Request This Book</h4>
          <button @click="brequest(this.bid)" class="btn btn-primary">Request Book</button>
        </div>
        
        <Review v-if="this.bstatus.status==2" :bid="this.bid" />
      </div>
    </div>
  </template>

  
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


.book-container {
      max-width: 800px;
      margin: 125px auto;
      padding: 20px;
      background-color: #f8f9fa;
      border-radius: 8px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    .book-card h2 {
      font-size: 18px;
      color: #343a40;
      margin-bottom: 10px;
    }

    .book-card h2 span {
      font-weight: bold;
      color: #007bff;
    }

    hr {
      border: 0;
      height: 1px;
      background: #dee2e6;
      margin: 20px 0;
    }

    .status-card {
      margin-top: 20px;
      padding: 15px;
      background-color: #ffffff;
      border: 1px solid #dee2e6;
      border-radius: 8px;
    }

    .status-card h3,
    .status-card h4 {
      font-size: 16px;
      color: #495057;
    }

    .status-card h4 span {
      font-weight: bold;
      color: #6c757d;
    }

    .btn {
      padding: 10px 15px;
      font-size: 16px;
      border-radius: 5px;
      margin-right: 10px;
      border: none;
      cursor: pointer;
    }

    .btn-primary {
      background-color: #007bff;
      color: #ffffff;
    }

    .btn-success {
      background-color: #28a745;
      color: #ffffff;
    }

    .btn-warning {
      background-color: #ffc107;
      color: #ffffff;
    }

</style>

<script>
import axios from 'axios';
import Review from "../components/Reviews.vue";
import { RouterLink } from 'vue-router';

export default {
    name: "Book",
    components: { Review },
    data() {
        return {
            bid: parseInt(this.$route.params.bid),
            book: {},
            role: "",
            bstatus: {},
        };
    },
    methods: {
        logout(){
    localStorage.clear();
    this.$router.push('/liblogin')
    alert("Logged out successfully")
},
        async bookinfo() {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`http://localhost:5000/bookinfo/${this.bid}`, {
                    headers: {
                        'Authorization': token
                    }
                });
                if (response.status == 200) {
                    this.book = response.data.book;
                    console.log(response.data);
                }
            } catch (error) {
                const errorMessage = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : 'An error occurred';

                if (error.response.statusText == "UNAUTHORIZED") {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/apilogin');
                } else if (error.response.statusText == "FORBIDDEN") {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                } else {
                    alert(`Error: ${errorMessage}`);
                }
            }
        },
        async getpdf(bid) {
            const URL = `http://localhost:5000/openbook/${this.bid}.pdf`;
            window.open(URL, '_blank');
        },
        async bookstatus() {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`http://localhost:5000/bstatus/${this.bid}`, {
                    headers: {
                        'Authorization': token
                    }
                });
                if (response.status == 200) {
                    this.bstatus = response.data.bstatus;
                    console.log(response.data);
                }
            } catch (error) {
                const errorMessage = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : 'An error occurred';

                if (error.response.statusText == "UNAUTHORIZED") {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/apilogin');
                } else if (error.response.statusText == "FORBIDDEN") {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                } else {
                    alert(`Error: ${errorMessage}`);
                }
            }
        },
        async brequest() {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`http://localhost:5000/brequest/${this.bid}`, {
                    headers: {
                        'Authorization': token
                    }
                });
                if (response.status == 201) {
                    this.bookstatus();
                    alert(response.data.message);
                }
            } catch (error) {
                const errorMessage = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : 'An error occurred';

                if (error.response.statusText == "UNAUTHORIZED") {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/apilogin');
                } else if (error.response.statusText == "FORBIDDEN") {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                } else {
                    alert(`Error: ${errorMessage}`);
                }
            }
        },
        async breturn() {
            try {
                const token = localStorage.getItem('token');
                const response = await axios.get(`http://localhost:5000/breturn/${this.bid}`, {
                    headers: {
                        'Authorization': token
                    }
                });
                if (response.status == 201) {
                    this.bookstatus();
                    alert(response.data.message);
                }
            } catch (error) {
                const errorMessage = error.response && error.response.data && error.response.data.message
                    ? error.response.data.message
                    : 'An error occurred';

                if (error.response.statusText == "UNAUTHORIZED") {
                    alert("Token required for authentication, please login and come back!");
                    this.$router.push('/apilogin');
                } else if (error.response.statusText == "FORBIDDEN") {
                    alert("Imposter Imposter!");
                    this.$router.push('/liblogin');
                } else {
                    alert(`Error: ${errorMessage}`);
                }
            }
        }
    },
    created() {
        this.token = localStorage.getItem('token');
        this.role = localStorage.getItem("role");
        if (!this.token) {
            alert("Auth Token Required Please Login");
            this.$router.push('/');
        } else {
            this.bookstatus();
            this.bookinfo();
        }
    },
}
</script>

