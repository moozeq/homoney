var date = {'month': 'JAN'};

var incomes = new Vue({
  el: '#incomes',
  data() {
    return {
      items: null
    }
  },
  mounted () {
    axios
      .get('/api/incomes')
      .then(response => {
        this.items = response.data.items;
      })
  },
  methods: {
    rm_item: function(id) {
        axios
          .post('/api/rm', {
            'id': id,
            'type': 'in',
            'date': date
          })
          .then(response => {
            this.$delete(this.items, id);
          })
    }
  },
  delimiters: ['[[', ']]']
})

var outcomes = new Vue({
  el: '#outcomes',
  data() {
    return {
      items: null
    }
  },
  mounted () {
    axios
      .get('/api/outcomes')
      .then(response => {
        this.items = response.data.items;
      })
  },
  methods: {
    rm_item: function(id) {
        axios
          .post('/api/rm', {
            'id': id,
            'type': 'out',
            'date': date
          })
          .then(response => {
            this.$delete(this.items, id);
          })
    }
  },
  delimiters: ['[[', ']]']
})

var incomes_menu = new Vue({
  el: '#comes-menu',
   data() {
     return {
       incomes: {
           options: [
            { value: null, text: 'Select new income type' },
           ],
           selected: null,
           value: 0
       },
       outcomes: {
           options: [
            { value: null, text: 'Select new outcome type' },
           ],
           selected: null,
           value: 0
       },
     }
  },
  mounted () {
    axios
      .get('/api/available')
      .then(response => {
            this.incomes.options = this.incomes.options.concat(response.data.in);
            this.outcomes.options = this.outcomes.options.concat(response.data.out);
      })
  },
  methods: {
    add_item: function(type) {
        if (type == 'in') {
            data = incomes;
            type_str = 'income';
            container = this.incomes;
        }
        else if (type == 'out') {
            data = outcomes;
            type_str = 'outcome';
            container = this.outcomes;
        }
        else {
            this.$bvToast.toast(`Wrong ${type_str} item type!`, {
              title: 'Error',
              variant: 'danger',
              autoHideDelay: 2000
            });
            return;
        }

        if (!container.selected) {
            this.$bvToast.toast(`Type of ${type_str} not selected!`, {
              title: 'Error',
              variant: 'danger',
              autoHideDelay: 2000
            });
            return;
        }
        if (!container.value || container.value < 0) {
            this.$bvToast.toast(`Wrong ${type_str} value!`, {
              title: 'Error',
              variant: 'danger',
              autoHideDelay: 2000
            });
            return;
        }
        axios
          .post('/api/add', {
            'name': container.selected,
            'item_type': type,
            'value': parseInt(container.value),
            'date': date
          })
          .then(response => {
            data.$set(data.items, response.data.id, response.data)
            this.$nextTick(() => {
                data.$el.scrollTop = data.$el.scrollHeight;
            });
          })
    }
  },
  delimiters: ['[[', ']]']
})
