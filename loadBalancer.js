const http = require('http');
const httpProxy = require('http-proxy');

// List of backend servers
const servers = [
    { host: 'localhost', port: 3001 },
    { host: 'localhost', port: 3002 },
    { host: 'localhost', port: 3003 }
];

const proxy = httpProxy.createProxyServer({});

let currentServerIndex = 0;

const loadBalancer = http.createServer((req, res) => {
    // Select a server using Round Robin
    const target = servers[currentServerIndex];
    console.log(`Forwarding request to: ${target.host}:${target.port}`);
    
    // Forward the request
    proxy.web(req, res, { target: `http://${target.host}:${target.port}` }, (err) => {
        console.error(`Error connecting to ${target.host}:${target.port}`, err.message);
        res.writeHead(502);
        res.end('Bad Gateway: Could not connect to the upstream server.');
    });

    // Update the index for the next request
    currentServerIndex = (currentServerIndex + 1) % servers.length;
});

const PORT = 8000;
loadBalancer.listen(PORT, () => {
    console.log(`Load Balancer running on port ${PORT}`);
});