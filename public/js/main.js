Vue.filter('reverse', function(value) {
    return value.slice().reverse();
});

const app  = new Vue({
    el: "#content",
    data: {
        price: { sell:[], buy:[]},
        account: {},
        orders: {live:[]}
    },
    methods: {
        reverse(items) {
            return items.slice().reverse();
      }     
    },
    created: function(){
        setInterval(()=>{
            fetch('/price').then(res => res.json())
            .then(json => this.price = json);
        }, 1000);

        setInterval(()=>{
            fetch('/account').then(res => res.json())
            .then(json => this.account = json);
        }, 1000);

        setInterval(()=>{
            fetch('/orders').then(res => res.json())
            .then(json => this.orders = json);
        });
    }
})