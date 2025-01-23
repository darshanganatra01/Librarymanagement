

<script>
import Search from "../components/Searchbar.vue";
import axios from 'axios';

export default {
  name: 'Adash',
  components: {
    Search
  },
  data() {
    return {
      sections: [],
      token: "",
      role: "",
      query: "",
      sresults: {},
      totalsecs: "",
      totalbooks: "",
      totalusers: "",
      topbooks: [],
      allrequests: [] // Added to capture all requests data
    };
  },
  methods: {
    logout() {
      localStorage.clear();
      this.$router.push('/liblogin');
      alert("Logged out successfully");
    },
    async allsections() {
      try {
        const response = await axios.get('http://localhost:5000/addsection', {
          headers: {
            'Authorization': `${this.token}`
          }
        });
        if (response.status == 200) {
          this.sections = response.data;
          console.log(response.data);
        }
      } catch (error) {
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
    async autorevoke() {
      try {
        const response = await axios.get('http://localhost:5000/autorevoke', {
          headers: {
            'Authorization': `${this.token}`
          }
        });
        if (response.status == 201) {
          alert(response.data.message);
        }
      } catch (error) {
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
    async stats() {
      try {
        const response = await axios.get('http://localhost:5000/stats', {
          headers: {
            'Authorization': `${this.token}`
          }
        });
        if (response.status == 200) {
          this.totalsecs = response.data.totalsecs;
          this.totalbooks = response.data.totalbooks;
          this.totalusers = response.data.totalusers;
          this.topbooks = response.data.topbooks;
          this.allrequests = response.data.allrequests;

          console.log(response.data);
        }
      } catch (error) {
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
    async triggerexport() {
      try {
        const response = await axios.get('http://localhost:5000/triggerexport', {
          headers: {
            'Authorization': `${this.token}`
          }
        });
        if (response.status == 200) {
          alert(response.data.message);
        }
      } catch (error) {
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
    }
  },
  created() {
    this.token = localStorage.getItem('token');
    this.role = localStorage.getItem('role');
    if (!this.token) {
      alert("Auth Token Required Please Login");
      this.$router.push('/');
    } else if (this.role != "admin") {
      alert("You are not Admin:(");
      this.$router.push('/liblogin');
    } else {
      this.autorevoke();
      this.allsections();
      this.stats();
    }
  }
}
</script>

<template>
  <div id="navbar">
    <h3 class="dashboard-title">Welcome to Librarian Dashboard</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <a href="#" @click.prevent="logout">Logout</a>
    </div>
  </div>

  <Search />

  <div class="stats-container">
    <h3>Total Number of Users : {{ this.totalusers }}</h3>
    <h3>Total Number of Books : {{ this.totalbooks }}</h3>
    <h3>Total Number of Sections : {{ this.totalsecs }}</h3>
  </div>

  <div class="dashboard-container">
    <h2 class="list-title">List of Sections</h2>
    <div class="section-list">
      <div class="section-items">
        <h3 v-for="i in sections" :key="i.sid" class="section-item">
          <a :href="`/sdetails/${i.sid}`" class="section-link">{{ i.name }}</a>
        </h3>
      </div>
      <div class="button-container">
        <RouterLink to="/addsection" class="btn btn-primary">Add a Section</RouterLink>
        <button @click="triggerexport" class="btn btn-warning">Export CSV</button>
      </div>
    </div>
  </div>

  <div class="top3">
    <h3 v-if="this.topbooks?.length">Some of the Best Sellers!</h3>
    <div v-for="i in this.topbooks" :key="i.bid" class="top3-item">
      <span>{{ i.bname }}</span>
      <button @click="this.$router.push(`/abook/${i.bid}`)">Explore</button>
    </div>
  </div>

  <!-- Statistics Graphs Section -->
  <div class="graphs-container">
    <h2 class="graphs-heading">Statistics</h2>
    <div class="graphs-row">
      <img src="../assets/pie.png" alt="Section Books Pie Chart" class="graph-image"/>
      <img src="../assets/behaviour.png" alt="User Request Behavior" class="graph-image"/>
    </div>
    <div class="graphs-row">
      <img src="../assets/histo.png" alt="Requests Histogram" class="graph-image"/>
      <img src="../assets/bar.png" alt="Interesting Plot" class="graph-image"/>
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

/* Stats Container Styles */
.stats-container {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
}

.stats-container h3 {
  background-color: #ecf0f1;
  border-radius: 15px;
  padding: 20px;
  font-size: 20px;
  color: #2c3e50;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stats-container h3:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

/* Dashboard Container Styles */
.dashboard-container {
  margin-top: 80px;
  padding: 20px;
  text-align: center;
}

.list-title {
  font-size: 24px;
  margin-bottom: 20px;
}

.section-list {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section-items {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.section-item {
  background-color: #ecf0f1;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  font-size: 18px;
}

.section-link {
  text-decoration: none;
  color: #2c3e50;
}

.button-container {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn-primary {
  background-color: #2980b9;
  color: white;
}

.btn-primary:hover {
  background-color: #1c6ea4;
}

.btn-warning {
  background-color: #f39c12;
  color: white;
}

.btn-warning:hover {
  background-color: #e08e0b;
}

/* Top3 Section Styles */
.top3 {
  margin-top: 30px;
}

.top3-item {
  background-color: #ecf0f1;
  border-radius: 10px;
  padding: 15px;
  margin: 10px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.top3-item span {
  font-size: 18px;
}

.top3-item button {
  background-color: #2980b9;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
}

.top3-item button:hover {
  background-color: #1c6ea4;
}

/* Graphs Section Styles */
.graphs-container {
  margin-top: 50px;
  text-align: center;
}

.graphs-heading {
  font-size: 24px;
  color: #2c3e50;
  margin-bottom: 20px;
}

.graphs-row {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 30px;
}

.graph-image {
  max-width: 45%;
  height: auto;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
