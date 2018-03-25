<template>
  <div>
    <h1>{{ title }}</h1>
    <ul>
      <li v-for="item in array">{{ item.state }}- {{ item.station_name }}</li>
    </ul>
  </div>
</template>

<script>
export default {
    name: 'ConnectedNodes',
    data () {
      return {
        title: 'Csatlakoztatotst mérőállomások:',
        array: []
      }
    },
    methods: {
      
    },
    created: function(){
      this.$http.get('http://localhost:3125/stations')
        .then(function(response){
          this.array = response.data.stations;
        });
    }
}
</script>

<style>

</style>
