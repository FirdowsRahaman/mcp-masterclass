# Chapter 10: Deployment & Scale

## Objective
In 10 minutes, you will understand:
- How to transition an MCP server from local `stdio` development to production.
- Hosting MCP servers in the cloud using SSE transport.
- Scaling strategies for high-traffic MCP architectures.

## The Concept
Building an MCP server locally is easy. Deploying it to production so that thousands of distributed AI agents can query it simultaneously requires traditional web-scale engineering.

### The "Restaurant Franchise" Analogy
**Scaling an MCP Server is like moving from a Food Truck to a Restaurant Franchise.**
- A local `stdio` server is a **Food Truck**: It's simple, runs on one machine, and one person (the Host) talks directly to it.
- Scaling to the cloud (SSE) is building a **Franchise**: You need identical, containerized kitchens (Docker), someone standing outside directing customer traffic (Load Balancers), and you suddenly have to worry about people stealing the recipes (Authentication).

## How It Works

### 1. Containerization (Docker)
The first step to deployment is containerizing your server. Because FastMCP seamlessly switches to an ASGI app (like FastAPI) when using SSE, your Dockerfile looks just like a standard web app.

```dockerfile
# Example Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY server.py .

# Expose the SSE port
EXPOSE 8000

# Run the server using an ASGI server like Uvicorn (FastMCP handles this internally when mcp.run(transport="sse") is called)
CMD ["python", "server.py"]
```

### 2. Cloud Hosting (AWS, GCP, Render)
Deploy your containerized server to a cloud provider. Because SSE maintains long-lived HTTP connections, you must ensure your load balancers are configured to support long timeouts and HTTP/2.

- **AWS**: Use ECS/Fargate with an Application Load Balancer (ALB).
- **GCP**: Use Cloud Run (ensure "Session Affinity" is enabled if state is required).

### 3. Scaling Considerations
- **Statelessness**: Try to keep your MCP servers stateless. If a server maintains local memory between the `initialize` and `tools/call` steps, a load balancer might route the second request to a different container, breaking the workflow. Use external databases (Redis, Postgres) for state.
- **Authentication**: When moving from `stdio` (implicitly secure) to `SSE` (public internet), you *must* implement authentication middleware (e.g., Bearer tokens in headers) to prevent unauthorized agents from executing your tools.

## Try It Yourself
1. Take your Lab 2 "Weather Server".
2. Change the `mcp.run()` call to use `transport="sse"`.
3. Write a Dockerfile for it.
4. Build and run the Docker container locally, exposing port 8000.
5. Connect the MCP inspector to your containerized, "cloud-ready" server!

## Checkpoint
1. Why does moving from `stdio` to SSE suddenly require you to think about Authentication?
2. What happens if a load balancer routes an MCP request to a different container midway through a session?
