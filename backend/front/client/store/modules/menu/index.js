import * as types from '../../mutation-types'
import lazyLoading from './lazyLoading'
import charts from './charts'
import uifeatures from './uifeatures'
import components from './components'
// show: meta.label -> name
// name: component name
// meta.label: display label

const state = {
  items: [
    {
      name: 'Állomások',
      path: '/connectednodes',
      meta: {
        auth: true,
        icon: 'fa-list-ul',
        link: 'connectednodes/index.vue'
      },
      component: lazyLoading('connectednodes', true)
    },
    {
      name: 'Test-Állomás',
      path: '/station',
      meta: {
        auth: true,
        icon: 'fa-cog',
        link: 'station/index.vue'
      },
      component: lazyLoading('station', true)
    },
    charts,
    uifeatures,
    components
  ]
}

const mutations = {
  [types.EXPAND_MENU] (state, menuItem) {
    if (menuItem.index > -1) {
      if (state.items[menuItem.index] && state.items[menuItem.index].meta) {
        state.items[menuItem.index].meta.expanded = menuItem.expanded
      }
    } else if (menuItem.item && 'expanded' in menuItem.item.meta) {
      menuItem.item.meta.expanded = menuItem.expanded
    }
  }
}

export default {
  state,
  mutations
}
