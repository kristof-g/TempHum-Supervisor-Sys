<template>
  <card-modal :visible="visible" @ok="close" @close="close" :cancelText="cancelText" :okText="okText" :title="title" transition="zoom">
    <p>
      <vb-switch type="success" size="large" :checked="swValue" v-model="swValue"></vb-switch>
    </p>
    <div class="tile is-ancestor">
      <div class="tile is-parent is-6">
        <article class="tile is-child box">
          <h5 class="title is-5">Minimális hőmérséklet</h5>
          <div class="block">
            <p>
              <slider type="success" size="small" :value="valueMin" :min="-50" :max="50" :step="1" is-fullwidth @change="updateMin"></slider>
            </p>
            <p class="control has-addons">
              <input class="input" type="number" v-model="valueMin" min="-50" max="50" number>
              <a class="button is-static"> °C</a>
            </p>
          </div>
        </article>
      </div>
      <div class="tile is-parent is-6">
        <article class="tile is-child box">
          <h1 class="title is-5">Maximális hőmérséklet</h1>
          <div class="block">
            <p>
              <slider type="success" size="small" :value="valueMax" :min="-50" :max="50" :step="1" is-fullwidth @change="updateMax"></slider>
            </p>
            <p class="control has-addons">
                <input class="input" type="number" v-model="valueMax" min="-50" max="50" number>
                <a class="button is-static"> °C</a>
            </p>
          </div>
        </article>
      </div>
    </div>

  </card-modal>
</template>

<script>
  import { CardModal } from 'vue-bulma-modal'
  import Tooltip from 'vue-bulma-tooltip'
  import Slider from 'vue-bulma-slider'
  import Cleave from 'vue-cleave'
  import 'cleave.js/dist/addons/cleave-phone.cn'
  import VbSwitch from 'vue-bulma-switch'

  export default {
    components: {
      VbSwitch,
      CardModal,
      Tooltip,
      Slider,
      Cleave
    },

    props: {
      visible: Boolean,
      title: String,
      url: String,
      item: Object
    },

    data () {
      return {
        src: require('assets/logo.svg'),
        okText: 'Modósítom!',
        cancelText: 'mégse',
        valueMin: this.item.min_temp,
        valueMax: this.item.max_temp,
        swValue: this.stateToValue(this.item.state),
        updateItem: null
      }
    },
    computed: {
    },
    methods: {
      stateToValue (state) {
        if (state === 'on') {
          return true
          }
        else if (state === 'off') {
          return false
          }
      },
      updateState () {
        this.updateItem.state = this.swValue ? 'on' : 'off'
        console.log('called...')
        console.log(this.updateItem.state)
      },
      updateMin (val) {
        this.valueMin = Number(val)
      },
      updateMax (val) {
        this.valueMax = Number(val)
      },
      open (url) {
        window.open(url)
      },

      close () {
        console.log(this.valueMin)
        this.$emit('close')
        this.title = '',
        this.item = null
      }
    },
    mounted: function () {
      
    }
  }

</script>

<style lang="scss" scoped>
  @import '~bulma/sass/utilities/mixins';
  p {
    margin-bottom: 20px;
  }
  .tooltip-value {
    width: 100%;
  }

.control.has-addons {
  @include mobile() {
    input {
      width: 100%;
    }

    input.is-expanded {
      flex-shrink: 1;
    }
  }
}
</style>
