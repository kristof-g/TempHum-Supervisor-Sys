<template>
  <b-container>
      <b-card>
          <form method="POST" class="form-signin">
              <i class="fa fa-lock fa-5x"></i>
              <hr>
          <h1 class="lead">A mérőállomásokhoz való hozzáféréshez kérlek jelentkezz be!</h1>
          <label for="inputPassword" class="sr-only">Password</label>
          <b-form-input v-model="text1" type="password"></b-form-input>
          <button class="btn btn-lg btn-primary btn-block" type="submit">Belépés!</button>
          </form>
      </b-card>
  </b-container>
</template>

<script>
export default {
  name: 'Login',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
