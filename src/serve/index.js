const http = require('http');
const fs = require('fs')

const PORT=8080;

var server = http.createServer(function (req, resp) {
    if (req.url == '/') {
        resp.writeHead(200, { 'Content-Type': 'text/html' });
        fs.createReadStream('test.html').pipe(resp);
    } else if (req.url == '/about') {
        resp.writeHead(200, { 'Content-Type': 'text/html' });
        fs.createReadStream('about.html').pipe(resp);
    } else {
        resp.end('error 404!');
    }
})

server.listen(process.env.PORT || PORT);
console.log('Server running at http://127.0.0.1:'+PORT);
