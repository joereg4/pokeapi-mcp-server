#!/usr/bin/env python3
"""
Simple PokeAPI MCP Server - Access Pokémon data from PokeAPI
"""
import os
import sys
import logging
from datetime import datetime, timezone
import httpx
from mcp.server.fastmcp import FastMCP

# Configure logging to stderr
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("pokeapi-server")

# Initialize MCP server - NO PROMPT PARAMETER!
mcp = FastMCP("pokeapi")

# Configuration
BASE_URL = "https://pokeapi.co/api/v2"

# === UTILITY FUNCTIONS ===

async def fetch_pokeapi_data(endpoint: str) -> dict:
    """Fetch data from PokeAPI with error handling."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}{endpoint}", timeout=10)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Resource not found: {endpoint}")
        else:
            raise Exception(f"API Error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise Exception(f"Network error: {str(e)}")

def format_pokemon_data(data: dict) -> str:
    """Format Pokémon data for LLM consumption."""
    result = f"🔍 **{data['name'].title()}** (ID: {data['id']})\n\n"
    
    # Basic info
    result += f"📏 **Height:** {data['height'] / 10:.1f}m\n"
    result += f"⚖️ **Weight:** {data['weight'] / 10:.1f}kg\n\n"
    
    # Types
    types = [t['type']['name'] for t in data['types']]
    result += f"🎯 **Types:** {', '.join(types)}\n\n"
    
    # Abilities
    abilities = []
    for ability in data['abilities']:
        ability_name = ability['ability']['name']
        if ability['is_hidden']:
            abilities.append(f"{ability_name} (Hidden)")
        else:
            abilities.append(ability_name)
    result += f"✨ **Abilities:** {', '.join(abilities)}\n\n"
    
    # Stats
    result += "📊 **Base Stats:**\n"
    for stat in data['stats']:
        stat_name = stat['stat']['name'].replace('-', ' ').title()
        result += f"  - {stat_name}: {stat['base_stat']}\n"
    result += "\n"
    
    # Sprites
    sprites = data.get('sprites', {})
    if sprites.get('front_default'):
        result += f"🖼️ **Sprites:**\n"
        result += f"  - Front: {sprites['front_default']}\n"
        if sprites.get('back_default'):
            result += f"  - Back: {sprites['back_default']}\n"
        if sprites.get('other', {}).get('official-artwork', {}).get('front_default'):
            result += f"  - Official Art: {sprites['other']['official-artwork']['front_default']}\n"
        result += "\n"
    
    # Moves (first 10)
    moves = data.get('moves', [])[:10]
    if moves:
        result += f"⚔️ **Sample Moves:** {', '.join([m['move']['name'] for m in moves])}\n"
        if len(data.get('moves', [])) > 10:
            result += f"  (and {len(data['moves']) - 10} more...)\n"
        result += "\n"
    
    return result

def format_species_data(data: dict) -> str:
    """Format species data for LLM consumption."""
    result = f"🔬 **{data['name'].title()} Species Data**\n\n"
    
    # Basic info
    result += f"📝 **Genus:** {data.get('genera', [{}])[0].get('genus', 'Unknown')}\n"
    result += f"🎨 **Color:** {data.get('color', {}).get('name', 'Unknown')}\n"
    result += f"🏠 **Habitat:** {data.get('habitat', {}).get('name', 'Unknown')}\n\n"
    
    # Flavor text (English)
    flavor_texts = data.get('flavor_text_entries', [])
    english_flavor = None
    for entry in flavor_texts:
        if entry.get('language', {}).get('name') == 'en':
            english_flavor = entry.get('flavor_text', '').replace('\n', ' ').replace('\f', ' ')
            break
    
    if english_flavor:
        result += f"📖 **Description:** {english_flavor}\n\n"
    
    # Capture rate
    capture_rate = data.get('capture_rate', 0)
    result += f"🎣 **Capture Rate:** {capture_rate}/255\n\n"
    
    # Evolution chain
    evolution_chain = data.get('evolution_chain', {})
    if evolution_chain.get('url'):
        chain_id = evolution_chain['url'].split('/')[-2]
        result += f"🔄 **Evolution Chain ID:** {chain_id}\n\n"
    
    return result

def format_evolution_chain(data: dict) -> str:
    """Format evolution chain data for LLM consumption."""
    def format_evolution(chain, level=0):
        indent = "  " * level
        result = f"{indent}🔸 {chain['species']['name'].title()}\n"
        
        for evolution in chain.get('evolves_to', []):
            result += format_evolution(evolution, level + 1)
        
        return result
    
    result = f"🔄 **Evolution Chain** (ID: {data['id']})\n\n"
    result += format_evolution(data['chain'])
    return result

def format_type_data(data: dict) -> str:
    """Format type data for LLM consumption."""
    result = f"🎯 **{data['name'].title()} Type**\n\n"
    
    # Damage relations
    damage_relations = data.get('damage_relations', {})
    
    if damage_relations.get('double_damage_from'):
        types = [t['name'] for t in damage_relations['double_damage_from']]
        result += f"❌ **Weak to (2x):** {', '.join(types)}\n"
    
    if damage_relations.get('double_damage_to'):
        types = [t['name'] for t in damage_relations['double_damage_to']]
        result += f"✅ **Strong against (2x):** {', '.join(types)}\n"
    
    if damage_relations.get('half_damage_from'):
        types = [t['name'] for t in damage_relations['half_damage_from']]
        result += f"🛡️ **Resistant to (0.5x):** {', '.join(types)}\n"
    
    if damage_relations.get('half_damage_to'):
        types = [t['name'] for t in damage_relations['half_damage_to']]
        result += f"⚡ **Weak against (0.5x):** {', '.join(types)}\n"
    
    if damage_relations.get('no_damage_from'):
        types = [t['name'] for t in damage_relations['no_damage_from']]
        result += f"🚫 **Immune to:** {', '.join(types)}\n"
    
    if damage_relations.get('no_damage_to'):
        types = [t['name'] for t in damage_relations['no_damage_to']]
        result += f"🔒 **No effect on:** {', '.join(types)}\n"
    
    result += "\n"
    
    # Pokémon of this type
    pokemon = data.get('pokemon', [])[:10]
    if pokemon:
        result += f"🔍 **Sample Pokémon:** {', '.join([p['pokemon']['name'] for p in pokemon])}\n"
        if len(data.get('pokemon', [])) > 10:
            result += f"  (and {len(data['pokemon']) - 10} more...)\n"
    
    return result

def format_pokedex_data(data: dict) -> str:
    """Format Pokédex data for LLM consumption."""
    result = f"📚 **{data['name'].title()} Pokédex**\n\n"
    
    result += f"📝 **Description:** {data.get('descriptions', [{}])[0].get('description', 'No description available')}\n\n"
    
    # Region
    region = data.get('region', {})
    if region:
        result += f"🌍 **Region:** {region.get('name', 'Unknown')}\n\n"
    
    # Pokémon entries
    entries = data.get('pokemon_entries', [])[:20]
    if entries:
        result += f"🔍 **Pokémon Entries** (showing first 20):\n"
        for entry in entries:
            pokemon = entry.get('pokemon_species', {})
            entry_number = entry.get('entry_number', '?')
            result += f"  {entry_number:3d}. {pokemon.get('name', 'Unknown').title()}\n"
        
        total_entries = len(data.get('pokemon_entries', []))
        if total_entries > 20:
            result += f"\n  ... and {total_entries - 20} more entries\n"
    
    return result

# === MCP TOOLS ===

@mcp.tool()
async def get_pokemon(identifier: str = "") -> str:
    """Get detailed information about a Pokémon by name or ID."""
    if not identifier.strip():
        return "❌ Error: Pokémon name or ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/pokemon/{identifier.lower()}")
        return format_pokemon_data(data)
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_pokemon_species(identifier: str = "") -> str:
    """Get species information about a Pokémon by name or ID."""
    if not identifier.strip():
        return "❌ Error: Pokémon name or ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/pokemon-species/{identifier.lower()}")
        return format_species_data(data)
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_evolution_chain(chain_id: str = "") -> str:
    """Get evolution chain information by chain ID."""
    if not chain_id.strip():
        return "❌ Error: Evolution chain ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/evolution-chain/{chain_id}")
        return format_evolution_chain(data)
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_type(identifier: str = "") -> str:
    """Get type information including damage relations by name or ID."""
    if not identifier.strip():
        return "❌ Error: Type name or ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/type/{identifier.lower()}")
        return format_type_data(data)
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_machine(machine_id: str = "") -> str:
    """Get machine (TM/HM/TR) information by ID."""
    if not machine_id.strip():
        return "❌ Error: Machine ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/machine/{machine_id}")
        result = f"🔧 **Machine {data['id']}**\n\n"
        
        # Item
        item = data.get('item', {})
        result += f"📦 **Item:** {item.get('name', 'Unknown').title()}\n"
        
        # Move
        move = data.get('move', {})
        result += f"⚔️ **Move:** {move.get('name', 'Unknown').title()}\n"
        
        # Version group
        version_group = data.get('version_group', {})
        result += f"🎮 **Version Group:** {version_group.get('name', 'Unknown').title()}\n"
        
        return result
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_pokedex(identifier: str = "") -> str:
    """Get Pokédex information by name or ID."""
    if not identifier.strip():
        return "❌ Error: Pokédex name or ID is required"
    
    try:
        data = await fetch_pokeapi_data(f"/pokedex/{identifier.lower()}")
        return format_pokedex_data(data)
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def list_pokemon(limit: str = "20", offset: str = "0") -> str:
    """List Pokémon with pagination support."""
    try:
        limit_int = int(limit) if limit.strip() else 20
        offset_int = int(offset) if offset.strip() else 0
        
        if limit_int > 100:
            limit_int = 100
            result = "⚠️ Limit capped at 100 for performance\n\n"
        else:
            result = ""
        
        data = await fetch_pokeapi_data(f"/pokemon?limit={limit_int}&offset={offset_int}")
        
        result += f"🔍 **Pokémon List** (showing {limit_int} starting from {offset_int})\n\n"
        
        for pokemon in data.get('results', []):
            result += f"• {pokemon['name'].title()}\n"
        
        # Pagination info
        count = data.get('count', 0)
        result += f"\n📊 **Total Pokémon:** {count}\n"
        result += f"📄 **Current page:** {offset_int // limit_int + 1} of {(count + limit_int - 1) // limit_int}\n"
        
        return result
    except ValueError as e:
        return f"❌ Error: Invalid limit or offset: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def list_types(limit: str = "20", offset: str = "0") -> str:
    """List all Pokémon types with pagination support."""
    try:
        limit_int = int(limit) if limit.strip() else 20
        offset_int = int(offset) if offset.strip() else 0
        
        data = await fetch_pokeapi_data(f"/type?limit={limit_int}&offset={offset_int}")
        
        result = f"🎯 **Type List**\n\n"
        
        for type_data in data.get('results', []):
            result += f"• {type_data['name'].title()}\n"
        
        return result
    except ValueError as e:
        return f"❌ Error: Invalid limit or offset: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def search_pokemon_by_type(type_name: str = "", limit: str = "20") -> str:
    """Find Pokémon of a specific type."""
    if not type_name.strip():
        return "❌ Error: Type name is required"
    
    try:
        limit_int = int(limit) if limit.strip() else 20
        
        # Get type data
        type_data = await fetch_pokeapi_data(f"/type/{type_name.lower()}")
        
        result = f"🔍 **{type_name.title()} Type Pokémon**\n\n"
        
        pokemon_list = type_data.get('pokemon', [])[:limit_int]
        for pokemon_data in pokemon_list:
            pokemon_name = pokemon_data['pokemon']['name']
            result += f"• {pokemon_name.title()}\n"
        
        total_count = len(type_data.get('pokemon', []))
        if total_count > limit_int:
            result += f"\n📊 Showing {limit_int} of {total_count} Pokémon\n"
        
        return result
    except ValueError as e:
        return f"❌ Error: {str(e)}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# === SERVER STARTUP ===
if __name__ == "__main__":
    logger.info("Starting PokeAPI MCP server...")
    
    try:
        mcp.run(transport='stdio')
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)
