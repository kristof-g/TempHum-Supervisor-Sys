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
        <tr v-for="item in array" @click="openModalCard(item)" >
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
  import Vue from 'vue'
  import CardModal from './CardModal'
  const CardModalComponent = Vue.extend(CardModal)

  const openCardModal = (propsData = {
    visible: true
  }) => {
    return new CardModalComponent({
      el: document.createElement('div'),
      propsData
    })
  }

  export default {
    data () {
      return {
        title: 'Csatlakoztatotst mérőállomások:',
        array: [],
        cardModal: null
      }
    },
    methods: {
      loadData () {
        this.isloading = true
        this.$http({
          headers: {
            'Authorization': 'Bearer ' + this.$auth.token()
          },
          url: this.$api_url + '/stations',
          transformResponse: [(data) => {
            return JSON.parse(data.replace(/T00:00:00/g, ''))
          }]
        }).then((response) => {
          this.array = response.data.stations
          this.isloading = false
        }).catch((error) => {
          console.log(error)
        })
      },
      openModalCard (item) {
        const cardModal = this.cardModal = openCardModal({
          title: item.station_name + ' állomás szerkesztése',
          item: item,
          url: this.$store.state.pkg.homepage
        })
        cardModal.$children[0].active()
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
