
import { createApp } from 'vue'
//vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
//mdb
import 'mdb-vue-ui-kit/css/mdb.min.css';
//components
import App from './App.vue'
import router from './router'


const  vuetify = createVuetify({
    components,
    directives,
})
createApp(App)
.use(router)
.use(vuetify)
.mount('#app')
