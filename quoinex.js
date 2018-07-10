const Pusher = require('pusher-js');
const request = require("request");
const api = require('./api');

const price = {sell: [], buy: []};
const account = {usd: -1, qash: -1};
const orders = {live:[]};

api.getPrice(price);
api.getAccount(account);
api.getOrders(orders);

const pusher = new Pusher('2ff981bb060680b5ce97', {
    wsHost: 'ws.pusherapp.com',
    wsPort: 80,
    enabledTransports: ["ws", "flash", "wss"],
    disabledTransports: ["flash"]
});

pusher.subscribe("price_ladders_cash_qashusd_sell")
    .bind("updated", (data) => {
        price.sell = data.slice(0, 10);
});

pusher.subscribe("price_ladders_cash_qashusd_buy")
    .bind("updated", function(data){
        price.buy = data.slice(0, 10);
});

pusher.subscribe("user_57134_account_usd")
    .bind("updated", function(data){
        account.usd = data.balance
});

pusher.subscribe("user_57134_account_qash")
    .bind("updated", function(data){
        account.qash = data.balance
});

module.exports = class Quoinex {
    constructor(){
        this.price = price;
        this.account = account;
        this.orders = orders;
    }
};