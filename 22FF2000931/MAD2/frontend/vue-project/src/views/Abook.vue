<template>
  <div id="navbar">
    <h3 class="dashboard-title">Specific book details/Requests</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
      <RouterLink to="/adash">Admin dashboard</RouterLink>
    </div>
  </div>

  <Searchbar />

  <div class="book-details-container">
    <div class="book-info">
      <h2>Book Name: <span>{{ book.bname }}</span></h2>
      <h2>Description: <span>{{ book.bdescription }}</span></h2>
      <h2>Author: <span>{{ book.author }}</span></h2>
      <h2>Date Uploaded: <span>{{ book.bdate }}</span></h2>
      <h3>Average Reviews: <span>{{ getavg }}</span></h3>
    </div>

    <div class="book-actions">
      <button @click="getpdf(bid)" class="btn-primary">Open PDF</button>
      <h4><a :href="`/editbook/${bid}`" class="link-primary">Edit the book</a></h4>
      <button @click="deletebook(bid)" class="btn-danger">Delete this book</button>
    </div>

    <hr>

    <div v-for="i in bstatus" :key="i.iuid" class="status-card">
      <template v-if="i.status == 2">
        <h3>User: <span>{{ i.username }}</span></h3>
        <h3>Issue Date: <span>{{ i.idate }}</span></h3>
        <h3>Due Date: <span>{{ i.rdate }}</span></h3>
        <button @click="brevoke(i.iuid)" class="btn-warning">Revoke Access</button>
      </template>
      <template v-if="i.status == 1">
        <h3>User: <span>{{ i.username }}</span></h3>
        <h3>Applied Date: <span>{{ i.adate }}</span></h3>
        <button @click="baccept(i.iuid)" class="btn-success">Accept</button>
        <button @click="breject(i.iuid)" class="btn-danger">Reject</button>
      </template>
      <hr>
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

.dashboard-title {
  color: white;
}

#navbar a.active {
  background-color: #2980b9;
  color: white;
  border-radius: 4px;
}

.book-details-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.book-info h2 {
  font-size: 18px;
  color: #343a40;
  margin-bottom: 10px;
}

.book-info span {
  font-weight: bold;
  color: #007bff;
}

.book-actions {
  margin-top: 20px;
  margin-bottom: 30px;
}

.book-actions .btn-primary,
.book-actions .btn-danger {
  padding: 10px 15px;
  font-size: 16px;
  border-radius: 5px;
  margin-right: 10px;
}

.link-primary {
  color: #007bff;
  text-decoration: none;
}

.status-card {
  margin-top: 20px;
  padding: 15px;
  background-color: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
}

.status-card h3 {
  font-size: 16px;
  color: #495057;
}

.status-card span {
  font-weight: bold;
  color: #6c757d;
}

.status-card .btn-success,
.status-card .btn-danger,
.status-card .btn-warning {
  padding: 8px 12px;
  font-size: 14px;
  border-radius: 5px;
  margin-right: 10px;
}

.btn-primary {
  background-color: #007bff;
  color: #ffffff;
  border: none;
}

.btn-danger {
  background-color: #dc3545;
  color: #ffffff;
  border: none;
}

.btn-warning {
  background-color: #ffc107;
  color: #ffffff;
  border: none;
}

.btn-success {
  background-color: #28a745;
  color: #ffffff;
  border: none;
}

hr {
  border: 0;
  height: 1px;
  background: #dee2e6;
  margin: 20px 0;
}
</style>


<script>
import axios from 'axios';
import Searchbar from '@/components/Searchbar.vue';
import { RouterLink } from 'vue-router';

export default {
  name: "Abook",
  components:{
    Searchbar
  },
  data() {
    return {
      bid: parseInt(this.$route.params.bid),
      book: {},
      role: "",
      bstatus: [],
      getavg: "",
      token: localStorage.getItem('token')
    };
  },
  methods: {
    logout(){
      localStorage.clear();
      alert("Logged out Successfully");
      this.$router.push('/');
  },
    async bookinfo() {
      try {
        const response = await axios.get(`http://localhost:5000/bookinfo/${this.bid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 200) {
          this.book = response.data.book;
          console.log(response.data);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async getpdf(bid) {
      const URL = `http://localhost:5000/openbook/${this.bid}.pdf`;
      window.open(URL, '_blank');
    },
    async bookstatus() {
      try {
        const response = await axios.get(`http://localhost:5000/bstatus/${this.bid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 200) {
          this.bstatus = response.data.bstatus;
          console.log(response.data);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async brevoke(iuid) {
      try {
        const response = await axios.get(`http://localhost:5000/brevoke/${this.bid}/${iuid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 201) {
          this.bookstatus();
          alert(response.data.message);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async baccept(iuid) {
      try {
        const response = await axios.get(`http://localhost:5000/baccept/${this.bid}/${iuid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 201) {
          this.bookstatus();
          alert(response.data.message);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async breject(iuid) {
      try {
        const response = await axios.get(`http://localhost:5000/breject/${this.bid}/${iuid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 201) {
          this.bookstatus();
          alert(response.data.message);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async deletebook(bid) {
      try {
        const response = await axios.get(`http://localhost:5000/deletebook/${this.bid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 201) {
          alert(response.data.message);
          this.$router.push(`/sdetails/${this.book.sec}`);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    async getavgrev() {
      try {
        const response = await axios.get(`http://localhost:5000/bookreview/${this.bid}`, {
          headers: {
            'Authorization': this.token
          }
        });
        if (response.status == 200) {
          this.getavg = response.data.avgrev;
          console.log(response.data);
        }
      } catch (error) {
        this.handleError(error);
      }
    },
    handleError(error) {
      const errorMessage = error.response && error.response.data && error.response.data.message
        ? error.response.data.message
        : 'An error occurred';

      if (error.response.statusText == "UNAUTHORIZED") {
        alert("Token required for authentication, please login and come back!");
        this.$router.push('/liblogin');
      } else if (error.response.statusText == "FORBIDDEN") {
        alert("Imposter Imposter!");
        this.$router.push('/liblogin');
      } else {
        alert(`Error: ${errorMessage}`);
      }
    }
  },
  created() {
    this.role = localStorage.getItem("role");
    if (!this.token) {
      alert("Auth Token Required, Please Login");
      this.$router.push('/');
    } else if (this.role != "admin") {
      alert("You are not Admin :(");
      this.$router.push('/liblogin');
    } else {
      this.bookstatus();
      this.bookinfo();
      this.getavgrev();
    }
  }
}
</script>

