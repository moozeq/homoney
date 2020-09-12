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
  delimiters: ['[[', ']]']
})
