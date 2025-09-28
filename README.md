# PokeAPI MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![Verified on MseeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/9b3b2fab-52ee-431d-b263-74a438783b08)

A Model Context Protocol (MCP) server that provides comprehensive access to Pokémon data from the [PokeAPI](https://pokeapi.co/). Perfect for AI assistants, chatbots, and applications that need rich Pokémon information.

## 🚀 Features

- **9 Comprehensive Tools** for accessing Pokémon data
- **LLM-Optimized Responses** with clean formatting and emojis
- **Smart Data Processing** handling PokeAPI gotchas
- **Docker Ready** with secure containerization
- **No Authentication Required** - works out of the box
- **Error Handling** with user-friendly messages

## 🛠️ Available Tools

| Tool | Description | Example |
|------|-------------|---------|
| `get_pokemon` | Get detailed Pokémon info (stats, types, abilities, sprites) | `get_pokemon("pikachu")` |
| `get_pokemon_species` | Get species data (flavor text, evolution info, capture rate) | `get_pokemon_species("pikachu")` |
| `get_evolution_chain` | Get evolution chain by ID | `get_evolution_chain("10")` |
| `get_type` | Get type effectiveness and damage relations | `get_type("electric")` |
| `get_machine` | Get TM/HM/TR information | `get_machine("1")` |
| `get_pokedex` | Get Pokédex entries and descriptions | `get_pokedex("national")` |
| `list_pokemon` | List Pokémon with pagination | `list_pokemon("20", "0")` |
| `list_types` | List all Pokémon types | `list_types("20", "0")` |
| `search_pokemon_by_type` | Find Pokémon of specific type | `search_pokemon_by_type("fire", "10")` |

## 📋 Prerequisites

- **Docker Desktop** with MCP Toolkit enabled
- **Docker MCP CLI plugin** (`docker mcp` command)
- **MCP-compatible client** (Claude Desktop, Cursor, etc.)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/joereg4/pokeapi-mcp-server.git
cd pokeapi-mcp-server
```

### 2. Pull the Docker Image
```bash
docker pull joereg4/pokeapi-mcp-server:latest
```

### 3. Set Up MCP Configuration

#### For Cursor:
Add to your `~/.cursor/mcp.json`:
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

#### For Claude Desktop:
Add to your Claude Desktop config:
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

### 4. Create MCP Catalog
```bash
mkdir -p ~/.docker/mcp/catalogs
cat > ~/.docker/mcp/catalogs/custom.yaml << EOF
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

### 5. Update Registry
```bash
echo "registry:" >> ~/.docker/mcp/registry.yaml
echo "  pokeapi:" >> ~/.docker/mcp/registry.yaml
echo "    ref: \"\"" >> ~/.docker/mcp/registry.yaml
```

### 6. Restart Your MCP Client
Restart Cursor, Claude Desktop, or your MCP client to load the new server.

## 💡 Usage Examples

Once configured, you can use natural language queries:

### Basic Pokémon Information
- "Get information about Pikachu"
- "Show me Charizard's stats and abilities"
- "What are Mewtwo's base stats?"

### Evolution and Species Data
- "What are the evolution chains for Eevee?"
- "Get species information for Bulbasaur"
- "Show me Pikachu's evolution chain"

### Type Effectiveness
- "What are the damage relations for electric type?"
- "Show me all fire type Pokémon"
- "What types are weak to water?"

### Pokédex and Lists
- "List the first 50 Pokémon"
- "Get the National Pokédex information"
- "Show me all available Pokémon types"

### Technical Information
- "What machine teaches Thunderbolt?"
- "Get machine information for TM01"

## 🏗️ Architecture

```
Your MCP Client → MCP Gateway → PokeAPI MCP Server → PokeAPI
```

The server acts as a bridge between your MCP client and the PokeAPI, providing:
- **Formatted responses** optimized for LLM consumption
- **Error handling** with user-friendly messages
- **Data processing** to handle PokeAPI quirks
- **Pagination support** for large datasets

## 🧪 Testing

### Test the Server Directly
```bash
# Test MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | docker run -i --rm pokeapi-mcp-server python pokeapi_server.py

# Test a specific tool
docker run --rm pokeapi-mcp-server python -c "
import asyncio
import sys
sys.path.append('.')
from pokeapi_server import get_pokemon
print(asyncio.run(get_pokemon('pikachu')))
"
```

### Verify MCP Integration
```bash
# Check if server appears in MCP list
docker mcp server list
```

## 🔧 Development

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run server directly
python pokeapi_server.py

# Test with MCP protocol
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python pokeapi_server.py
```

### Adding New Tools
1. Add function to `pokeapi_server.py` with `@mcp.tool()` decorator
2. Update the catalog entry with new tool name
3. Rebuild Docker image: `docker build -t pokeapi-mcp-server .`
4. Restart your MCP client

## 🐛 Troubleshooting

### Tools Not Appearing
- ✅ Verify Docker image built successfully
- ✅ Check catalog and registry files exist
- ✅ Ensure MCP client configuration is correct
- ✅ Restart your MCP client completely

### API Errors
- ✅ PokeAPI is free with no rate limits
- ✅ Server includes 10-second timeout handling
- ✅ Check network connectivity if requests fail
- ✅ Verify Pokémon names/IDs are correct

### Common Issues
- **"Resource not found"**: Check spelling of Pokémon names (use lowercase)
- **"Network error"**: Verify internet connection and PokeAPI availability
- **"Tools not loading"**: Ensure Docker is running and MCP configuration is correct

## 📊 Data Processing Features

The server intelligently processes PokeAPI data:

- **🖼️ Sprite Handling**: Extracts and formats sprite URLs, handles missing sprites gracefully
- **🌐 Language Filtering**: Automatically filters flavor text to English
- **🔄 Evolution Chain Flattening**: Converts complex evolution data to readable trees
- **⚔️ Move Data Processing**: Shows version group details and limits results for readability
- **🎯 Type Relationship Formatting**: Clear display of damage multipliers and relationships

## 🔒 Security

- ✅ **No Authentication Required** - PokeAPI is public
- ✅ **Non-root Container** - Runs as unprivileged user
- ✅ **HTTPS Only** - All API requests use secure connections
- ✅ **No Data Storage** - No sensitive information stored or logged

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Quick Start for Contributors
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test thoroughly
5. Commit your changes: `git commit -m 'Add some feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

### Documentation
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Detailed contribution guidelines
- **[DEVELOPER.md](DEVELOPER.md)** - Technical implementation details
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes

## 🙏 Acknowledgments

- [PokeAPI](https://pokeapi.co/) for providing the comprehensive Pokémon database
- [Model Context Protocol](https://modelcontextprotocol.io/) for the MCP specification
- [Docker](https://www.docker.com/) for containerization support

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/yourusername/pokeapi-mcp-server/issues)
3. Create a new issue with detailed information about your problem

---

**Made with ❤️ for the Pokémon and AI communities**
