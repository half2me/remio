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
    <button class="button" @click="$emit('changeMode', 'out')" :class="{{'is-link': port.mode === 'out'}}">Output</button>
    <template v-if="ok">
        Default state: High
    </template>
    <br>
    Level: <a @click="$emit('changeState')"><i class="fa fa-2x" :class="{'fa-toggle-on': port.level == 1, 'fa-toggle-off': port.level == 0}" aria-hidden="true"></i></a>
</bulma-card>
`,
});

Vue.component('port-list', {
    props: ['ports'],
    template: `
<template>
    <port-object v-for="p in ports" :key="p.id" :port="p"></port-object>
    <br>
    <div class="field has-addons">
        <div class="control">
            <input class="input" type="number" placeholder="Port Number">
        </div>
        <div class="control">
            <a class="button is-info">
                Add
            </a>
        </div>
    </div>
</template>
`,
});