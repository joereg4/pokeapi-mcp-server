# Installation Guide

This guide provides detailed step-by-step instructions for setting up the PokeAPI MCP Server.

## Prerequisites

Before you begin, ensure you have:

- **Docker Desktop** installed and running
- **Docker MCP CLI plugin** (`docker mcp` command available)
- **MCP-compatible client** (Claude Desktop, Cursor, etc.)

## Step-by-Step Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/pokeapi-mcp-server.git
cd pokeapi-mcp-server
```

### Step 2: Build the Docker Image

```bash
docker build -t pokeapi-mcp-server .
```

Verify the build was successful:
```bash
docker images | grep pokeapi-mcp-server
```

### Step 3: Set Up MCP Configuration

#### For Cursor Users

1. **Locate your Cursor MCP config file:**
   - macOS: `~/.cursor/mcp.json`
   - Windows: `%APPDATA%\Cursor\mcp.json`
   - Linux: `~/.config/cursor/mcp.json`

2. **Add the PokeAPI server configuration:**
   ```json
   {
     "mcpServers": {
       "pokeapi": {
         "command": "docker",
         "args": [
           "run", "-i", "--rm",
           "-v", "/var/run/docker.sock:/var/run/docker.sock",
           "-v", "/Users/yourusername/.docker/mcp:/mcp",
           "docker/mcp-gateway",
           "--catalog=/mcp/catalogs/docker-mcp.yaml",
           "--catalog=/mcp/catalogs/custom.yaml",
           "--config=/mcp/config.yaml",
           "--registry=/mcp/registry.yaml",
           "--tools-config=/mcp/tools.yaml",
           "--transport=stdio"
         ]
       }
     }
   }
   ```

   **Important:** Replace `/Users/yourusername` with your actual home directory path.

#### For Claude Desktop Users

1. **Locate your Claude Desktop config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
   - Linux: `~/.config/Claude/claude_desktop_config.json`

2. **Add the PokeAPI server configuration:**
   ```json
   {
     "mcpServers": {
       "pokeapi": {
         "command": "docker",
         "args": [
           "run", "-i", "--rm",
           "-v", "/var/run/docker.sock:/var/run/docker.sock",
           "-v", "/Users/yourusername/.docker/mcp:/mcp",
           "docker/mcp-gateway",
           "--catalog=/mcp/catalogs/docker-mcp.yaml",
           "--catalog=/mcp/catalogs/custom.yaml",
           "--config=/mcp/config.yaml",
           "--registry=/mcp/registry.yaml",
           "--tools-config=/mcp/tools.yaml",
           "--transport=stdio"
         ]
       }
     }
   }
   ```

### Step 4: Create MCP Catalog

1. **Create the catalogs directory:**
   ```bash
   mkdir -p ~/.docker/mcp/catalogs
   ```

2. **Create the custom catalog file:**
   ```bash
   cat > ~/.docker/mcp/catalogs/custom.yaml << 'EOF'
   version: 2
   name: custom
   displayName: Custom MCP Servers
   registry:
     pokeapi:
       description: "Access Pokémon data from PokeAPI"
       title: "PokeAPI"
       type: server
       dateAdded: "2025-01-27T00:00:00Z"
       image: pokeapi-mcp-server:latest
       ref: ""
       readme: ""
       toolsUrl: ""
       source: ""
       upstream: ""
       icon: ""
       tools:
         - name: get_pokemon
         - name: get_pokemon_species
         - name: get_evolution_chain
         - name: get_type
         - name: get_machine
         - name: get_pokedex
         - name: list_pokemon
         - name: list_types
         - name: search_pokemon_by_type
       secrets: []
       metadata:
         category: integration
         tags:
           - pokemon
           - gaming
           - api
         license: MIT
         owner: local
   EOF
   ```

### Step 5: Update MCP Registry

1. **Check if registry file exists:**
   ```bash
   ls -la ~/.docker/mcp/registry.yaml
   ```

2. **Create or update the registry file:**
   ```bash
   # If file doesn't exist, create it
   if [ ! -f ~/.docker/mcp/registry.yaml ]; then
     echo "registry:" > ~/.docker/mcp/registry.yaml
   fi
   
   # Add PokeAPI entry (avoid duplicates)
   if ! grep -q "pokeapi:" ~/.docker/mcp/registry.yaml; then
     echo "  pokeapi:" >> ~/.docker/mcp/registry.yaml
     echo "    ref: \"\"" >> ~/.docker/mcp/registry.yaml
   fi
   ```

### Step 6: Verify Installation

1. **Test the Docker image:**
   ```bash
   docker run --rm pokeapi-mcp-server python -c "
   import asyncio
   import sys
   sys.path.append('.')
   from pokeapi_server import get_pokemon
   print(asyncio.run(get_pokemon('pikachu')))
   "
   ```

2. **Check MCP server list:**
   ```bash
   docker mcp server list
   ```

### Step 7: Restart Your MCP Client

- **Cursor:** Quit and restart Cursor completely
- **Claude Desktop:** Quit and restart Claude Desktop completely

## Verification

After restarting your MCP client, you should be able to:

1. **See PokeAPI tools available** in your MCP client
2. **Use natural language queries** like:
   - "Get information about Pikachu"
   - "Show me all fire type Pokémon"
   - "What are the evolution chains for Eevee?"

## Troubleshooting

### Common Issues

#### "Docker command not found"
- Ensure Docker Desktop is installed and running
- Verify Docker is in your PATH

#### "MCP server not appearing"
- Check that all configuration files are in the correct locations
- Verify the Docker image built successfully
- Ensure your MCP client was restarted completely

#### "Permission denied" errors
- On macOS/Linux, ensure Docker has permission to access your home directory
- Check that the MCP directories are readable

#### "Tools not working"
- Verify the PokeAPI is accessible: `curl https://pokeapi.co/api/v2/pokemon/pikachu`
- Check Docker logs: `docker logs <container_name>`

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting section](README.md#-troubleshooting) in the main README
2. Search existing [GitHub Issues](https://github.com/yourusername/pokeapi-mcp-server/issues)
3. Create a new issue with:
   - Your operating system
   - MCP client being used
   - Error messages
   - Steps to reproduce

## Uninstallation

To remove the PokeAPI MCP Server:

1. **Remove from MCP configuration:**
   - Edit your MCP client config file
   - Remove the "pokeapi" server entry

2. **Remove Docker image:**
   ```bash
   docker rmi pokeapi-mcp-server
   ```

3. **Remove MCP catalog entry:**
   ```bash
   # Edit ~/.docker/mcp/catalogs/custom.yaml
   # Remove the pokeapi entry
   
   # Edit ~/.docker/mcp/registry.yaml
   # Remove the pokeapi entry
   ```

4. **Restart your MCP client**
