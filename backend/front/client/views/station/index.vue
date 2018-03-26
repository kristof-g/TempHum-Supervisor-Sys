<template>
  <article class="tile is-child box">
          <h1 class="title">Kérlek válasz ki egy ídősávot az adatok megjelenítéséhez!</h1>
          <p class="control">
            <datepicker placeholder="válaszd ki az ídősávot" :config="{ mode: 'range', locale: l10n }"></datepicker>
          </p>
        </article>
</template>

<script>
import Datepicker from 'vue-bulma-datepicker'

export default {
  components: {
    Datepicker
  },

  data () {
    return {
      value: '2016-12-12'
    }
  },

  mounted () {
    const { checkIn, checkOut } = this.$refs
    checkIn.datepicker.set('onChange', (selectedDates, dateStr, instance) => {
      checkOut.datepicker.set('minDate', selectedDates[0].fp_incr(1))
    })

    checkOut.datepicker.set('onChange', (selectedDates, dateStr, instance) => {
      checkIn.datepicker.set('maxDate', dateStr)
    })
  },

  computed: {
    today () {
      return new Date()
    },
    maxDate () {
      let d = new Date()
      d.setDate(32)
      return d
    },
    placeholder () {
      return `minDate: today, maxDate: ${this.maxDate.getFullYear()}-${this.maxDate.getMonth() + 1}-${this.maxDate.getDate()}`
    },
    // https://github.com/chmln/flatpickr/blob/gh-pages/src/flatpickr.l10n.zh.js
    l10n () {
      return {
        firstDayOfWeek: 1,
        weekdays: {
          shorthand: ['HÉ', 'KE', 'SZE', 'CSÜ', 'PÉ', 'SZO', 'VA'],
          longhand: ['Hétfő', 'Kedd', 'Szerda', 'Csütörtök', 'Péntek', 'Szombat', 'Vasárnap']
        },
        months: {
          shorthand: ['jan', 'feb', 'már', 'ápr', 'máj', 'jún', 'júl', 'aug', 'szept', 'okt', 'nov', 'dec'],
          longhand: ['január', 'február', 'március', 'április', 'május', 'június', 'július', 'augusztus', 'szeptember', 'október', 'november', 'december']
        }
      }
    }
  },

  watch: {
    value (newVal, oldVal) {
      console.log(newVal, oldVal)
    }
  }
}
</script>

<style lang="scss" scoped>
.tile.is-parent {
  min-width: 50%;
}
</style>
