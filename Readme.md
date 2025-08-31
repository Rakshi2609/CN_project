# Node.js Round Robin Load Balancer

This project demonstrates a simple **Round Robin Load Balancer** implemented in Node.js. It distributes incoming HTTP requests across three backend servers (`server1.js`, `server2.js`, and `server3.js`) to balance the load and improve reliability.

## Use Case

A load balancer is used to distribute client requests across multiple backend servers. This helps:
- Prevent any single server from becoming a bottleneck.
- Increase the availability and reliability of your service.
- Scale your application horizontally by adding more servers.

This example is ideal for learning and experimenting with basic load balancing concepts in a local environment.

## How It Works

- **Backend Servers:**  
  - `server1.js` listens on port 3001 and responds with "Response from Server 1!"
  - `server2.js` listens on port 3002 and responds with "Response from Server 2!"
  - `server3.js` listens on port 3003 and responds with "Response from Server 3!"

- **Load Balancer (`loadBalancer.js`):**  
  - Listens on port 8000.
  - Forwards each incoming request to one of the backend servers using the Round Robin algorithm.
  - Uses the `http-proxy` library to proxy requests.

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/) installed on your system.
- Install the `http-proxy` package:
  ```
  npm install http-proxy
  ```

### Running the Servers

1. **Start the backend servers** (in separate terminals or using background processes):

   ```
   node server1.js
   node server2.js
   node server3.js
   ```

2. **Start the load balancer:**

   ```
   node loadBalancer.js
   ```

3. **Send requests to the load balancer:**

   Open your browser or use `curl` to access `http://localhost:8000`.  
   Each request will be forwarded to a different backend server in a round robin fashion.

   Example using `curl`:
   ```
   curl http://localhost:8000
   ```

   You should see responses alternating between:
   - "Response from Server 1!"
   - "Response from Server 2!"
   - "Response from Server 3!"

## Files

- `loadBalancer.js` - The load balancer implementation.
- `server1.js` - Backend server 1.
- `server2.js` - Backend server 2.
- `server3.js` - Backend server