<template>
  <card-modal :visible="visible" @ok="close" @close="close" :cancelText="cancelText" :okText="okText" :title="title" transition="zoom">
    <a @click="open(url)">Vue Admin on GitHub</a>
  </card-modal>
</template>

<script>
import { CardModal } from 'vue-bulma-modal'

export default {
  components: {
    CardModal
  },

  props: {
    visible: Boolean,
    title: String,
    url: String
  },

  data () {
    return {
      src: require('assets/logo.svg'),
      okText: 'Modósítom!',
      cancelText: 'mégse'
    }
  },

  methods: {
    open (url) {
      window.open(url)
    },

    close () {
      this.$emit('close')
      this.title = ''
    }
  }
}
</script>
