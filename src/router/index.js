import {createRouter, createWebHistory} from 'vue-router'

import Home from "./../components/home.vue"
import properties from './../components/properties.vue'
`import SavedProperties from './../components/SavedProperties.vue'
import about from './../components/about.vue'
import support from './../components/support.vue'

const routes = [
  {
    path: "/",
    name: 'home',
    component: Home
  },
  {
    path: "/properties",
    name: 'properties',
    component: properties
  },
  {
    path: "/saved",
    name: 'saved',
    component: SavedProperties
  },
  {
    path: "/about",
    name: 'about',
    component: about
  },
  {
    path: "/support",
    name: 'support',
    component: support

  }
]
 const router = createRouter({
      history: createWebHistory(),
      routes, 
    })
    
    export default router