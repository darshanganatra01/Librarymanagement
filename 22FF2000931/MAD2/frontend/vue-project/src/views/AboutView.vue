<template>
    <div id="navbar">
    <h3 class="dashboard-title">Welcome to Librarian Dashboard</h3>
    <div class="right-links">
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="">Logout</RouterLink>
    </div>
  </div>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>

<style>

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

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>
