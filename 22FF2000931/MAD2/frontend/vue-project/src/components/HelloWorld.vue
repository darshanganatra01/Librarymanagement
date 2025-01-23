<script>
export default{
  name:'HelloWorld',
  props:{msg:String},
  methods:{
    alogout(){
      localStorage.clear;
    }
  },
  created(){
    this.alogout();
  }
}
</script>

<template>
  <h1> Library Management System V-2 </h1>
  <h2> Name : Ganatra Darshan </h2>
  <h3> Email : 22f2000931@ds.study.iitm.ac.in </h3>
  <h3> <button @click="this.$router.push('/login')">Click here to Login/Register as a User </button></h3>
  <h3> <button @click="this.$router.push('/liblogin')" >Click here to Login as an Admin </button></h3>
</template>





