<template>
  <div>
    <h1>{{ title }}</h1>
    <table class="table table-striped">
      <thead>
        <tr>
          <th>név</th>
          <th>állapot</th>
          <th>utolsó mérés</th>
          <th>utolsó mérés időpontja</th>
          <th>maximum</th>
          <th>minimum</th>
          <th>müveletek</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in array">
          <td>{{item.station_name}}</td>
          <td>{{item.state}}</td>
          <td>{{item.last_temp}} °C | {{item.last_hum}} %</td>
          <td>{{item.last_data_date}}</td>
          <td>{{item.min_temp}} °C</td>
          <td>{{item.max_temp}} °C</td>
          <td>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
  export default {
    data () {
      return {
        title: 'Csatlakoztatotst mérőállomások:',
        array: []
      }
    },
    methods: {
      loadData () {
        this.isloading = true
        this.$http({
          headers: {
            'Authorization': 'Bearer ' + this.$auth.token()
          },
          url: 'http://localhost:3125/stations',
          transformResponse: [(data) => {
            return JSON.parse(data.replace(/T00:00:00/g, ''))
          }]
        }).then((response) => {
          this.array = response.data.stations
          this.isloading = false
        }).catch((error) => {
          console.log(error)
        })
      }
    },
    created: function () {
      this.loadData()
      console.log('crweafr')
    }
  }
</script>

<style>
  
</style>
