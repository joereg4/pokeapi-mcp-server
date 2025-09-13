# PokeAPI MCP Server - Developer Documentation

## Overview

This MCP server provides comprehensive access to Pokémon data through the PokeAPI. It's designed specifically for LLM consumption with clean, formatted responses and intelligent data processing.

## Implementation Details

### Core Features

1. **Smart Data Formatting**: All responses are formatted for easy LLM parsing with emojis and clear structure
2. **Error Handling**: User-friendly error messages instead of raw API responses
3. **Pagination Support**: Built-in pagination for list endpoints with sensible defaults
4. **Data Processing**: Handles PokeAPI gotchas like missing sprites, language filtering, and evolution chain flattening

### Tool Specifications

#### `get_pokemon(identifier: str)`
- Fetches complete Pokémon data including stats, types, abilities, sprites, and moves
- Formats sprites with direct URLs for easy access
- Shows first 10 moves with count of remaining moves
- Handles missing sprite data gracefully

#### `get_pokemon_species(identifier: str)`
- Retrieves species-specific data including flavor text and evolution info
- Filters to English flavor text automatically
- Extracts evolution chain ID for easy follow-up queries
- Includes capture rate and habitat information

#### `get_evolution_chain(chain_id: str)`
- Displays evolution chains in a readable tree format
- Shows all evolution paths and relationships
- Uses indentation to show evolution levels

#### `get_type(identifier: str)`
- Shows complete damage relations (weaknesses, resistances, immunities)
- Lists sample Pokémon of that type
- Formats damage multipliers clearly

#### `get_machine(machine_id: str)`
- Displays TM/HM/TR information
- Shows associated move and version group
- Includes item details

#### `get_pokedex(identifier: str)`
- Shows Pokédex entries with descriptions
- Lists Pokémon in entry order
- Includes region information

#### `list_pokemon(limit: str, offset: str)`
- Paginated Pokémon listing
- Caps limit at 100 for performance
- Shows pagination information

#### `list_types(limit: str, offset: str)`
- Lists all available Pokémon types
- Simple pagination support

#### `search_pokemon_by_type(type_name: str, limit: str)`
- Finds all Pokémon of a specific type
- Configurable result limit
- Shows total count information

### Data Processing Features

1. **Sprite Handling**: Extracts and formats sprite URLs, handles missing sprites
2. **Language Filtering**: Automatically filters flavor text to English
3. **Evolution Chain Flattening**: Converts complex evolution data to readable trees
4. **Move Data Processing**: Shows version group details and limits results
5. **Type Relationship Formatting**: Clear display of damage multipliers and relationships

### Error Handling Strategy

- **404 Errors**: Converted to "Resource not found" messages
- **Network Errors**: Graceful handling with retry information
- **Invalid Input**: Clear validation messages
- **Missing Data**: Graceful handling of optional fields

### Performance Considerations

- **Timeout Handling**: 10-second timeout for all API requests
- **Pagination Limits**: Maximum 100 items per request
- **Caching**: No caching implemented (PokeAPI is fast enough)
- **Rate Limiting**: No rate limiting (PokeAPI has no official limits)

### LLM Optimization

- **Structured Output**: All responses use consistent formatting with emojis
- **Clear Sections**: Data organized into logical sections
- **Actionable Information**: Includes IDs and URLs for follow-up queries
- **Readable Format**: Multi-line formatting for easy parsing

## Technical Architecture

- **Base URL**: https://pokeapi.co/api/v2
- **HTTP Client**: httpx with async support
- **Error Handling**: Comprehensive exception handling
- **Logging**: Structured logging to stderr
- **Container**: Docker with non-root user

## Future Enhancements

Potential additions for future versions:
- Move details with power/accuracy information
- Ability details with descriptions
- Location and encounter data
- Generation-specific information
- Search by multiple criteria
- Caching for frequently accessed data
