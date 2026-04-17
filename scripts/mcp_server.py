#!/usr/bin/env python3

import os
import json
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("Liturgical Calendar Static Tool")

# Constants
DIST_DIR = os.path.join(os.path.dirname(__file__), "..", "dist", "v1")

# Common metadata arguments injected by some MCP clients
EXTRA_ARGS = {
    "_conversation_id": None,
    "_trace_id": None,
    "_fetched_urls": None
}

@mcp.tool()
def list_available_calendars(
    year: str, 
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None
) -> Dict[str, List[str]]:
    """
    Lists all available nations, dioceses, and universal calendars for a given year.
    
    Args:
        year: The year to check (e.g., "2026").
    """
    year_dir = os.path.join(DIST_DIR, year)
    if not os.path.exists(year_dir):
        return {"error": f"Year {year} not found."}
    
    result = {
        "universal": [],
        "nations": [],
        "dioceses": []
    }
    
    for category in result.keys():
        cat_dir = os.path.join(year_dir, category)
        if os.path.exists(cat_dir):
            result[category] = sorted(os.listdir(cat_dir))
            
    return result

@mcp.tool()
def get_calendar(
    year: str, 
    category: str, 
    identifier: str, 
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None
) -> Any:
    """
    Retrieves the full liturgical calendar for a specific configuration.
    
    Args:
        year: Year (e.g., "2026")
        category: "universal", "nations", or "dioceses"
        identifier: The specific ID (e.g., "IT" for nation, "romamo_it" for diocese, "en" for universal)
        locale: Language code (e.g., "en", "it", "la")
    """
    if category == "universal":
        file_path = os.path.join(DIST_DIR, year, "universal", f"{locale}.json")
    else:
        file_path = os.path.join(DIST_DIR, year, category, identifier, f"{locale}.json")
        
    if not os.path.exists(file_path):
        return {"error": f"Calendar not found at {file_path}"}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Error reading file: {str(e)}"}

@mcp.tool()
def search_liturgical_event(
    year: str, 
    query: str, 
    nation: Optional[str] = None, 
    diocese: Optional[str] = None, 
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None
) -> List[Dict[str, Any]]:
    """
    Searches for events in a specific calendar by name or event_key.
    
    Args:
        year: Year to search (e.g. "2026")
        query: Search string (e.g. "Easter", "Peter", "Advent")
        nation: Optional nation ID
        diocese: Optional diocese ID
        locale: Locale for search
    """
    if diocese:
        category, identifier = "dioceses", diocese
    elif nation:
        category, identifier = "nations", nation
    else:
        category, identifier = "universal", locale
        
    calendar = get_calendar(year, category, identifier, locale)
    if isinstance(calendar, dict) and "error" in calendar:
        return [calendar]
    
    events = calendar.get("litcal", [])
    query = query.lower()
    
    matches = []
    for event in events:
        name = event.get("name", "").lower()
        key = event.get("event_key", "").lower()
        if query in name or query in key:
            matches.append(event)
            
    return matches

if __name__ == "__main__":
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

    # MCP Streamable HTTP transport (2025-03-26 spec). Single endpoint at /mcp.
    # Permissive CORS so browser-based MCP clients (llama-server UI, Claude Desktop
    # web flows, etc.) can reach it; Mcp-Session-Id must be in expose_headers.
    cors = Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Mcp-Session-Id"],
    )
    port = int(os.environ.get("PORT", "8080"))
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=port,
        middleware=[cors],
        stateless_http=True,
    )
