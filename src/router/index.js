import {createRouter, createWebHistory} from 'vue-router'

import Home from "./../components/home.vue"
import properties from './../components/properties.vue'
import SavedProperties from './../components/SavedProperties.vue'
import about from './../components/about.vue'
import support from './../components/support.vue'
import login from './../components/login.vue'
import register from './../components/register.vue'
import agents from './../components/agents.vue'
import settings from './../components/settings.vue'

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

  },
  {
    path: "/login",
    name: 'login',
    component: login
  },
  {
    path: "/register",
    name: 'register',
    component: register
  },
  {
    path: "/agents",
    name: 'agents',
    component: agents
  },
  {
    path: "/settings",
    name: 'settings',
    component: settings
  }

]
 const router = createRouter({
      history: createWebHistory(),
      routes, 
    })
    
    export default router