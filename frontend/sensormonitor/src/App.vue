<template>
  <div id="app">
    <navbar-view/> 
    <router-view/>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar'
export default {
  name: 'App',
  components: {
            'navbar-view': Navbar
        }
}
</script>

<style>

</style>
