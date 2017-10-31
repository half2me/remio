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
    props: ['id'],

    data () {
        return {
            port: {}
        };
    },

    mounted () {
        this.refresh();
    },

    methods: {
        refresh() {
            axios.get('/ports/' + this.id).then(r => this.port = r.data);
        },

        toggleLevel () {
            if (this.port.mode === 'output') {
                axios.post('/ports/' + this.id, {level: !this.port.level}).then(this.refresh());
            }
        },

        toggleMode () {
            axios.post('/ports/' + this.id, {
                mode: this.port.mode === 'input' ? 'output' : 'input'
            }).then(this.refresh);
        },

        toggleDefault () {
            axios.post('/ports/' + this.id, {
                default_level: !this.port.default_level
            }).then(this.refresh);
        },
    },
    template: `
<div>
    <bulma-card :title="'Port ' + id">
        <a slot="header" @click="$emit('remove')" class="card-header-icon" aria-label="more options">
            <span class="icon">
                <i class="fa fa-times-circle" aria-hidden="true"></i>
            </span>
        </a>
        <template v-if="port.mode === 'input'">
            <span class="icon" :class="{'has-text-danger': !port.default_level}"><i @click="toggleDefault" class="fa fa-2x fa-caret-square-o-down" aria-hidden="true"></i></span>
            <span class="icon" :class="{'has-text-danger': port.default_level}"><i @click="toggleDefault" class="fa fa-2x fa-caret-square-o-up" aria-hidden="true"></i></span>
        </template>
        <a @click="toggleLevel"><i class="fa fa-2x" :class="{'fa-toggle-on': port.level, 'fa-toggle-off': !port.level}" aria-hidden="true"></i></a>
        <br>
        <button slot="footer" class="button" @click="toggleMode" :class="{'is-link': port.mode === 'input'}">Input</button>
        <button slot="footer" class="button" @click="toggleMode" :class="{'is-link': port.mode === 'output'}">Output</button>
    </bulma-card>
    <br>
</div>
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

        removePort (portId) {
            axios.delete('/ports/' + portId).then(this.refresh)
        },

        addPort () {
            axios.put('/ports/' + this.newPortNumber, {}).then(this.refresh);
        }
    },
    template: `
<div>
    <port-object v-for="p in ports" @remove="removePort(p.id)" :key="p.id" :id="p.id"></port-object>
    <br>
    <div class="field has-addons">
        <div class="control">
            <input class="input" type="number" min="0" max="40" style="width: 10em" v-model="newPortNumber" placeholder="Port Number">
        </div>
        <div class="control">
            <a @click="addPort" class="button is-info">
                Add Port
            </a>
        </div>
    </div>
</div>
`,
});

app = new Vue({
    el: '#app',
});