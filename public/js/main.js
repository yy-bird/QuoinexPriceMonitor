const app  = new Vue({
    el: "#content",
    data: {
        price: {}
    },
    created: function(){
        setInterval(()=>{
            fetch('/price')
            .then(res => res.json())
            .then(json => this.price = json);
        }, 1000);
    }
})