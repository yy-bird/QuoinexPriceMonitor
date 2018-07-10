const request = require("request");
const jwt = require('jwt-simple');

function getPublicHeader(path){
    return {
        url: `https://api.quoine.com${path}`,
        headers: {
            "X-Quoine-API-Version": 2
        }
    }
}

function getPrivateHeader(path){
    return {
        url:`https://api.quoine.com${path}`,
        headers: {
            "X-Quoine-API-Version": 2,
            "x-Quoine-Auth": getToken(path)
        }
    }
}

function getToken(path){
    return jwt.encode({path: path, nonce: (new Date()).getTime()*1000, token_id: 288106}, 
    'WXgmqJSaO9kc6+XkW/vcypujwU/xCeQKO4TtO2EfCU/hZ+Od1OqrkULHmwPD+/TucygWraQJ6zpR9KmZQtI3hg==', 
    "HS256");
}

function getPrice(price){
    request(getPublicHeader("/products/57/price_levels"), (error, resp, body) => {
        price.sell = JSON.parse(body).sell_price_levels.slice(0, 10);
        price.buy = JSON.parse(body).buy_price_levels.slice(0, 10);
    });
}

function getAccount(account){
    request(getPrivateHeader("/fiat_accounts"), (error, resp, body) => {
        account.usd = JSON.parse(body).find(x => x.currency == 'USD').balance;
    });
    request(getPrivateHeader("/crypto_accounts"), (error, resp, body) => {
        account.qash = JSON.parse(body).find(x => x.currency == 'QASH').balance;
    })
}

function getOrders(orders){
    request(getPrivateHeader("/orders?product_id=57&status=live&with_details=1"), (error, resp, body) => {
        orders.live = JSON.parse(body).models;
    })
}

module.exports = {
    getPrice: getPrice,
    getAccount: getAccount,
    getOrders: getOrders
}