const http = require('http');
http.createServer((req, res) => {
  res.writeHead(200);
  res.end('Response from Server 3!');
}).listen(3003, () => console.log('Server 3 running on port 3003'));