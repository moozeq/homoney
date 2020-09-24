var date = {'month': 'JAN'};

var incomes = new Vue({
  el: '#incomes',
  data() {
    return {
      items: null
    }
  },
  mounted () {
    this.init();
  },
  methods: {
    init: function() {
        axios
          .get('/api/incomes')
          .then(response => {
            //console.log(response.data.items);
            this.items = response.data.items;
          });
    },
    rm_item: function(id) {
        axios
          .post('/api/rm', {
            'id': id,
            'type': 'in',
            'date': date
          })
          .then(response => {
            this.$delete(this.items, id);
            comes_stats.update();
          });
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
    this.init();
  },
  methods: {
    init: function() {
        axios
          .get('/api/outcomes')
          .then(response => {
            //console.log(response.data.items);
            this.items = response.data.items;
          });
    },
    rm_item: function(id) {
        axios
          .post('/api/rm', {
            'id': id,
            'type': 'out',
            'date': date
          })
          .then(response => {
            this.$delete(this.items, id);
            comes_stats.update();
          });
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
    this.init();
  },
  methods: {
    init: function() {
        axios
          .get('/api/available')
          .then(response => {
                this.incomes.options = this.incomes.options.concat(response.data.in);
                this.outcomes.options = this.outcomes.options.concat(response.data.out);
          });
    },
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
            comes_stats.update();
          });
    }
  },
  delimiters: ['[[', ']]']
})

var navbar = new Vue({
  el: '#navbar',
  methods: {
    refresh() {
        window.location.reload(true);
        //incomes.init();
        //outcomes.init();
        //comes_stats.update();
    },
    save() {
        axios
          .post('/api/save')
          .then(response => {
            this.$bvToast.toast(`Your data has been saved`, {
              title: 'Success',
              variant: 'success',
              toaster: 'b-toaster-bottom-left',
              autoHideDelay: 2000
            });
          });
    },
    load() {
        axios
          .post('/api/load')
          .then(response => {
            this.$bvToast.toast(`Saved data has been loaded`, {
              title: 'Success',
              variant: 'success',
              toaster: 'b-toaster-bottom-left',
              autoHideDelay: 2000
            });
          });
        this.refresh();
    },
    clear() {
        axios
          .post('/api/clear')
          .then(response => {
            this.$bvToast.toast(`All data has been cleared`, {
              title: 'Success',
              variant: 'success',
              toaster: 'b-toaster-bottom-left',
              autoHideDelay: 2000
            });
          });
        this.refresh();
    },
    logout() {
        console.log('Not implemented');
    }
  }
})

var comes_stats = new Vue({
  el: '#comes-stats',
  data() {
    return {
        summary: {
            income: null,
            outcome: null,
            balance: null,
            currency: null
        }
    }
  },
  methods: {
    update() {
        axios
          .get('/api/balance')
          .then(response => {
                this.summary.income = response.data.income;
                this.summary.outcome = response.data.outcome;
                this.summary.balance = response.data.balance;
                this.summary.currency = response.data.currency;
          });
    }
  },
  mounted: function() {
    this.update()
  },
  delimiters: ['[[', ']]']
})