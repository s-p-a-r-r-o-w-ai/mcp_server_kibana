# MCP Server for Kibana

MCP server providing tools for Kibana REST API endpoints using FastMCP and Pydantic.

## Features

### 🔐 Authentication
- **Reverse Proxy Authentication**: Production-ready authentication via Caddy reverse proxy
- **API Key Support**: Secure access using `X-API-Key` header
- **Kibana Integration**: Supports `KIBANA_API_KEY` for Kibana authentication

### 🌐 Spaces Support
All tools support an optional `space` argument to target specific Kibana Spaces (e.g., `default`, `marketing`).

### 📊 Data Views
- `get_all_data_views(space)` - Get all data views
- `get_data_view(id, space)` - Get specific data view
- `create_data_view(data_view, override, space)` - Create new data view
- `update_data_view(id, data_view, override, space)` - Update data view

### 💾 Saved Objects
- `find_saved_objects(..., space)` - Search saved objects with filters
- `create_saved_object(type, attributes, id, references, space)` - Create saved object
- `get_saved_object(type, id, space)` - Get saved object
- `update_saved_object(type, id, attributes, references, space)` - Update saved object

## Quick Start

### Using Docker Compose (Recommended)

1. **Copy environment file**:
```bash
cp .env.example .env
```

2. **Edit `.env` with your configuration**:
```bash
KIBANA_URL=https://your-kibana-instance.com
KIBANA_API_KEY=your-kibana-api-key
MCP_API_KEY=your-secret-mcp-key  # Used for client authentication
```

3. **Start the services**:
```bash
docker compose up -d
```

The setup includes:
- **MCP Kibana Server**: Internal service running in SSE mode
- **Caddy Reverse Proxy**: Handles authentication and SSL termination

4. **Verify the setup**:
```bash
# Test 1: Without auth (should return 401)
curl http://localhost:8080/sse
# Expected: HTTP/1.1 401 Unauthorized

# Test 2: With correct API key (should return 200)
curl -H "X-API-Key: your-secret-mcp-key" http://localhost:8080/sse
# Expected: HTTP/1.1 200 OK

# Test 3: Health check (no auth required)
curl http://localhost:8080/health
# Expected: OK
```

5. **View logs**:
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f caddy
docker compose logs -f mcp-server
```

### Architecture

```
Client (with X-API-Key) 
    ↓
Caddy Reverse Proxy (validates API key)
    ↓
MCP Kibana Server (internal, SSE mode)
    ↓
Kibana API
```

## Local Development

### Without Docker

1. **Install dependencies**:
```bash
pip install uv
uv sync
```

2. **Create `.env` file**:
```bash
KIBANA_URL=http://localhost:5601
KIBANA_API_KEY=your-api-key-here
```

3. **Run in stdio mode** (no auth needed for local development):
```bash
python -m mcp_server_kibana.server stdio
```

### With MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

Then connect to:
- **With Docker**: `http://localhost:8080/sse` (requires `X-API-Key` header)
- **Local stdio**: Use the inspector's stdio connection mode

## Production Deployment

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `KIBANA_URL` | Yes | Your Kibana instance URL |
| `KIBANA_API_KEY` | Yes | API key for Kibana authentication |
| `MCP_API_KEY` | Yes | Secret key for MCP client authentication |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

### Security Best Practices

1. **Use Strong API Keys**: Generate cryptographically secure keys
   ```bash
   # Generate a secure key
   openssl rand -base64 32
   ```

2. **Enable HTTPS in Production**: Uncomment HTTPS section in `Caddyfile` and `docker-compose.yml`

3. **Rotate Keys Regularly**: Update `MCP_API_KEY` periodically

4. **Network Isolation**: Use Docker networks to isolate services

### HTTPS Configuration

For production with automatic HTTPS:

1. Update `Caddyfile` - uncomment the HTTPS section
2. Update `docker-compose.yml` - uncomment port 443 and TLS_EMAIL
3. Set `TLS_EMAIL` in `.env` for Let's Encrypt notifications
4. Ensure your domain points to your server

## Client Configuration

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "kibana": {
      "url": "http://localhost:8080/sse",
      "headers": {
        "X-API-Key": "your-secret-mcp-key"
      }
    }
  }
}
```

### Cursor / Other MCP Clients

Configure with:
- **Endpoint**: `http://localhost:8080/sse`
- **Header**: `X-API-Key: your-secret-mcp-key`

## Docker Management

### Common Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View running containers
docker compose ps

# View logs
docker compose logs -f

# Rebuild and restart
docker compose up -d --build

# Remove all containers and volumes
docker compose down -v
```

## Testing

### Authentication Tests

```bash
# Test 1: No authentication (should fail with 401)
curl -v http://localhost:8080/sse
# Expected: HTTP/1.1 401 Unauthorized
# Response: "Unauthorized: Valid X-API-Key header required"

# Test 2: Valid API key (should succeed with 200)
curl -v -H "X-API-Key: your-secret-mcp-key" http://localhost:8080/sse
# Expected: HTTP/1.1 200 OK
# Response: SSE stream with session endpoint

# Test 3: Invalid API key (should fail with 401)
curl -v -H "X-API-Key: wrong-key" http://localhost:8080/sse
# Expected: HTTP/1.1 401 Unauthorized

# Test 4: Health check (no auth required)
curl http://localhost:8080/health
# Expected: OK
```

### MCP Protocol Tests

```bash
# Initialize session (requires auth)
curl -X POST "http://localhost:8080/sse" \
  -H "X-API-Key: your-secret-mcp-key" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}'
```

## Troubleshooting

### Connection Refused
**Symptoms**: `curl: (7) Failed to connect`

**Solutions**:
- Check if containers are running: `docker compose ps`
- Verify port 8080 is not in use: `lsof -i :8080` or `netstat -tuln | grep 8080`
- Check Docker logs: `docker compose logs -f`
- Restart services: `docker compose restart`

### 401 Unauthorized
**Symptoms**: `HTTP/1.1 401 Unauthorized`

**Solutions**:
- Verify `X-API-Key` header is included in request
- Check that header value matches `MCP_API_KEY` in `.env` file
- View Caddy logs for auth failures: `docker compose logs caddy`
- Ensure no extra spaces in API key value

### Kibana Connection Issues
**Symptoms**: Errors when calling Kibana tools

**Solutions**:
- Verify `KIBANA_URL` is correct and accessible
- Test Kibana API key: `curl -H "Authorization: ApiKey YOUR_KEY" https://your-kibana/api/status`
- Ensure `KIBANA_API_KEY` has proper permissions
- Check MCP server logs: `docker compose logs mcp-server`
- Verify network connectivity from container to Kibana

### Container Won't Start
**Symptoms**: Container exits immediately

**Solutions**:
- Check logs: `docker compose logs mcp-server`
- Verify environment variables in `.env`
- Ensure no syntax errors in `docker-compose.yml`
- Try rebuilding: `docker compose up -d --build`

### Port Already in Use
**Symptoms**: `Bind for 0.0.0.0:8080 failed: port is already allocated`

**Solutions**:
- Stop conflicting services: `docker ps` and `docker stop <container>`
- Change port in `docker-compose.yml` (e.g., `8081:80`)
- Kill process using port: `lsof -ti:8080 | xargs kill -9`

## Project Structure

```
mcp_server_kibana/
├── src/mcp_server_kibana/
│   ├── clients/          # Kibana HTTP client
│   ├── config/           # Configuration settings
│   ├── prompts/          # Lens visualization prompts
│   ├── tools/            # MCP tool implementations
│   ├── utils/            # Utility modules
│   ├── models.py         # Pydantic models
│   └── server.py         # Main server entry point
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
├── Caddyfile            # Reverse proxy config
├── .env.example         # Environment template
└── README.md            # This file
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

Apache 2.0