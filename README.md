# MCP Server for Kibana

MCP server providing tools for Kibana REST API endpoints using FastMCP and Pydantic.

## Features

### 🔐 Authentication
- **Bearer Token Authentication**: Built-in FastMCP token verification
- **API Key Support**: Secure access using `Authorization: Bearer <token>` header
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

### 🏢 Spaces Management
- `get_all_spaces()` - Get all Kibana spaces
- `get_space(id)` - Get specific space
- `create_space(id, name, ...)` - Create new space
- `update_space(id, name, ...)` - Update space

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
# MCP_API_KEY=optional-bearer-token  # If not set, auto-generated on startup
```

3. **Start the services**:
```bash
docker compose up -d
```

The setup includes:
- **MCP Kibana Server**: Direct service with built-in token verification

4. **Verify the setup**:
```bash
# Check server logs for auto-generated token
docker compose logs mcp-server

# Test 1: Without auth (should return 401)
curl http://localhost:8080/mcp
# Expected: HTTP/1.1 401 Unauthorized

# Test 2: With bearer token from logs (should return 200)
curl -H "Authorization: Bearer <token-from-logs>" http://localhost:8080/mcp
# Expected: HTTP/1.1 200 OK
```

5. **View logs**:
```bash
# View server logs
docker compose logs -f mcp-server
```

### Architecture

```
Client (with Bearer token) 
    ↓
MCP Kibana Server (/mcp endpoint)
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
- **With Docker**: `http://localhost:8080/mcp` (requires `Authorization: Bearer <token>` header)
- **Local stdio**: Use the inspector's stdio connection mode

## Production Deployment

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `KIBANA_URL` | Yes | Your Kibana instance URL |
| `KIBANA_API_KEY` | Yes | API key for Kibana authentication |
| `MCP_API_KEY` | No | Bearer token (auto-generated if not set) |
| `LOG_LEVEL` | No | Logging level (default: INFO) |

### Deployment Modes

**1. Production (Docker Compose):**
- HTTP server with /mcp endpoint
- Auto-generated bearer tokens
- Built-in authentication

**2. Development (Local):**
- Direct stdio mode (no auth)
- HTTP mode with auto-generated tokens
- MCP Inspector compatible

**3. ASGI Production:**
- Use with Uvicorn/Gunicorn
- `uvicorn mcp_server_kibana.server:app`
- Full ASGI middleware support

### Security Best Practices

1. **Use Strong API Keys**: Tokens are auto-generated securely on startup

2. **Rotate Keys Regularly**: Update `MCP_API_KEY` periodically

3. **Use HTTPS in Production**: Deploy behind a reverse proxy with SSL

### HTTPS Configuration

For production HTTPS, deploy behind a reverse proxy (nginx, Caddy, etc.) that handles SSL termination and forwards requests to the MCP server on port 8080.

## Client Configuration

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "kibana": {
      "url": "http://localhost:8080/mcp",
      "headers": {
        "Authorization": "Bearer <token-from-server-logs>"
      }
    }
  }
}
```

### Cursor / Other MCP Clients

Configure with:
- **Endpoint**: `http://localhost:8080/mcp`
- **Header**: `Authorization: Bearer <token-from-server-logs>`

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
curl -v http://localhost:8080/mcp
# Expected: HTTP/1.1 401 Unauthorized

# Test 2: Valid bearer token (should succeed with 200)
curl -v -H "Authorization: Bearer <token-from-logs>" http://localhost:8080/mcp
# Expected: HTTP/1.1 200 OK

# Test 3: Invalid bearer token (should fail with 401)
curl -v -H "Authorization: Bearer wrong-key" http://localhost:8080/mcp
# Expected: HTTP/1.1 401 Unauthorized
```

### MCP Protocol Tests

```bash
# Initialize session (requires auth)
curl -X POST "http://localhost:8080/mcp" \
  -H "Authorization: Bearer <token-from-logs>" \
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
- Verify `Authorization: Bearer <token>` header is included in request
- Check that token value matches `MCP_API_KEY` in `.env` file
- View server logs for auth failures: `docker compose logs mcp-server`
- Ensure no extra spaces in token value

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
- Change port in `docker-compose.yml` (e.g., `8081:8080`)
- Kill process using port: `lsof -ti:8080 | xargs kill -9`

## ASGI Production Deployment

```bash
# Install production server
pip install uvicorn[standard]

# Run with Uvicorn
uvicorn mcp_server_kibana.server:app --host 0.0.0.0 --port 8080

# Run with Gunicorn
gunicorn mcp_server_kibana.server:app -k uvicorn.workers.UvicornWorker
```

## Project Structure

```
mcp_server_kibana/
├── src/mcp_server_kibana/
│   ├── clients/          # Kibana HTTP client
│   ├── config/           # Configuration settings
│   ├── tools/            # MCP tool implementations
│   ├── utils/            # Utility modules
│   ├── models.py         # Pydantic models
│   └── server.py         # Main server + ASGI app
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Container setup

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