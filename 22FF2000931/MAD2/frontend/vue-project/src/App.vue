<script setup>
import { RouterLink, RouterView } from 'vue-router';
import HelloWorld from './components/HelloWorld.vue';
</script>

<template>
  <div class="mid">
    <RouterView />
  </div>
</template>

<style scoped>

/* Adjust the margin-top for the content to avoid overlap with the navbar */
body, #app {
  margin: 0;
  padding: 0;
}

.mid {
  margin-top: 75px; /* Adjust this value to match the height of the navbar */
  padding: 20px; /* Add padding if necessary */
}
</style>
