const express = require('express');
const path = require('path');
const Quoinex = require('./quoinex');

const app = express();
const quoinex = new Quoinex();

app.use('/static', express.static('public'));

app.get('/', (req, res) => res.sendFile(path.join(__dirname + '/index.html')));

app.get('/price', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(quoinex.price));
});

app.get('/account', (req, res) => {
    res.setHeader('Content-Type', 'application/json');  
    res.send(JSON.stringify(quoinex.account));  
})

app.get('/orders', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(quoinex.orders));
})

app.listen(3000, () => console.log("listening on port 3000"));


