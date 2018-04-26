const Pusher = require('pusher-js');
const request = require("request");

const price = {sell: [], buy: []};

let options = {
    url: "https://api.quoine.com/products/57/price_levels",
    headers: {
        "X-Quoine-API-Version": 2
    }
}

request(options, (error, resp, body) => {
    price.sell = JSON.parse(body).sell_price_levels[0];
    price.buy = JSON.parse(body).buy_price_levels[0];
})

const pusher = new Pusher('2ff981bb060680b5ce97', {
    wsHost: 'ws.pusherapp.com',
    wsPort: 80,
    enabledTransports: ["ws", "flash", "wss"],
    disabledTransports: ["flash"]
});

pusher.subscribe("price_ladders_cash_qashusd_sell")
    .bind("updated", (data) => {
        price.sell = data[0];
});

pusher.subscribe("price_ladders_cash_qashusd_buy")
    .bind("updated", function(data){
        price.buy = data[0];
});

module.exports = class Quoinex {
    constructor(){
        this.price = price;
    }
};