Vue.component('bulma-card', {
    props: ['title'],
    template: `
<div class="card">
  <header class="card-header">
    <p class="card-header-title">
      {{ title }}
    </p>
    <slot name="header"></slot>
  </header>
  <div class="card-content">
    <div class="content">
      <slot></slot>
    </div>
  </div>
  <footer class="card-footer">
    <slot name="footer"></slot>
  </footer>
</div>
`
});

Vue.component('port-object', {
    props: ['port'],
    template: `
<bulma-card :title="'Port ' + port.id">
    Mode: 
    <button class="button" @click="$emit('changeMode', 'in')" :class="{'is-link': port.mode === 'in'}">Input</button>
    <button class="button" @click="$emit('changeMode', 'out')" :class="{'is-link': port.mode === 'out'}">Output</button>
    <template v-if="port.mode === 'in'">
        Default state: High
    </template>
    <br>
    Level: <a @click="$emit('changeLevel', !port.level)"><i class="fa fa-2x" :class="{'fa-toggle-on': port.level == 1, 'fa-toggle-off': port.level == 0}" aria-hidden="true"></i></a>
</bulma-card>
`,
});

Vue.component('port-list', {
    data () {
        return {
            'ports': [],
            'newPortNumber': null
        }
    },

    mounted () {
        this.refresh()
    },

    methods: {
        refresh () {
            axios.get('/ports').then(r => this.ports = r.data);
        },

        changeLevel (portId, level) {
            console.log(portId, level);
            axios.post('/ports/' + portId, {level: level}).then(this.refresh);
        },

        changeMode (portId, mode) {
            axios.post('/ports/' + portId, {mode: mode}).then(this.refresh);
        },

        addPort () {
            axios.put('/ports/' + this.newPortNumber, {}).then(this.refresh);
        }
    },
    template: `
<div>
    <port-object v-for="p in ports" @changeMode="m => changeMode(p.id, m)" @changeLevel="l => changeLevel(p.id, l)" :key="p.id" :port="p"></port-object>
    <br>
    <div class="field has-addons">
        <div class="control">
            <input class="input" type="number" v-model="newPortNumber" placeholder="Port Number">
        </div>
        <div class="control">
            <a @click="addPort" class="button is-info">
                Add
            </a>
        </div>
    </div>
</div>
`,
});

app = new Vue({
    el: '#app',
});