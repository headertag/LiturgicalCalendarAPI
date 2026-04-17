#!/usr/bin/env python3
"""
Liturgical Calendar MCP Server — Static Edition.

Serves pre-baked calendars from dist/v1/{year}/{category}/{identifier}/{locale}.json
over the MCP Streamable HTTP transport (spec 2025-03-26).

Tools are split by calendar category — get_general_calendar / get_national_calendar /
get_diocesan_calendar — so the model cannot conflate a nation (e.g. 'IT' for Italy)
with a language (e.g. 'it' for Italian). The previous single-tool signature
(`get_calendar(category, identifier, locale)`) allowed exactly that confusion.

The mark_particular_celebrations helper and tool-split approach are adapted from
https://github.com/CatholicOS/liturgical-calendar-mcp.
"""

import copy
import datetime
import json
import os
import re
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

mcp = FastMCP("Liturgical Calendar Static Tool")

DIST_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "dist"))
DIST_DIR = os.path.join(DIST_ROOT, "v1")
METADATA_PATH = os.path.join(DIST_ROOT, "metadata.json")

BRACKET_PATTERN = re.compile(r"\[.*\]")


def _base_locale(locale: str) -> str:
    return locale.split("_")[0].split("-")[0].lower()


def _read_json(path: str) -> Any:
    if not os.path.exists(path):
        rel = os.path.relpath(path, DIST_ROOT)
        return {"error": f"Calendar not found at dist/{rel}"}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"Error reading {path}: {e}"}


def _load_metadata() -> Dict[str, Any]:
    if os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _resolve_path(year: str, category: str, identifier: Optional[str], locale: str) -> str:
    loc = _base_locale(locale)
    if category == "universal":
        return os.path.join(DIST_DIR, year, "universal", f"{loc}.json")
    return os.path.join(DIST_DIR, year, category, identifier or "", f"{loc}.json")


def _mark_particular_celebrations(
    calendar_data: Dict[str, Any], general_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Flag events particular to this calendar by diffing against the General Roman Calendar.

    An event is particular if its event_key isn't in the general calendar OR its name
    contains bracketed region markers like '[USA]'. Weekday events (grade=0) are skipped.
    Adapted from CatholicOS/liturgical-calendar-mcp.
    """
    result = copy.deepcopy(calendar_data)
    general_keys = {
        e.get("event_key")
        for e in general_data.get("litcal", [])
        if e.get("event_key")
    }
    for event in result.get("litcal", []):
        if event.get("grade", 0) == 0:
            event["is_particular"] = False
            continue
        key = event.get("event_key", "")
        name = event.get("name", "")
        event["is_particular"] = (key not in general_keys) or bool(
            BRACKET_PATTERN.search(name)
        )
    return result


def _extract_iso_date(raw: Any) -> Optional[str]:
    """Return 'YYYY-MM-DD' from a baked event 'date' field (ISO string or unix ts)."""
    if isinstance(raw, (int, float)):
        try:
            return datetime.datetime.fromtimestamp(
                int(raw), tz=datetime.timezone.utc
            ).strftime("%Y-%m-%d")
        except Exception:
            return None
    if isinstance(raw, str) and len(raw) >= 10:
        return raw[:10]
    return None


# Every tool accepts the _conversation_id / _trace_id / _fetched_urls metadata
# kwargs that some MCP clients inject, so pydantic validation doesn't reject them.


@mcp.tool()
def list_available_calendars(
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """
    List every universal, national, and diocesan calendar available in the baked
    cache, with their supported locales and the covered year range.

    Use this first to discover which `nation` codes, `diocese` ids, and `locale`
    values are valid before calling the other tools.
    """
    metadata = _load_metadata().get("litcal_metadata", {})
    years: List[int] = []
    if os.path.exists(DIST_DIR):
        years = sorted(int(y) for y in os.listdir(DIST_DIR) if y.isdigit())

    return {
        "year_range": {"start": years[0], "end": years[-1]} if years else None,
        "universal_locales": metadata.get("locales", []),
        "national_calendars": [
            {
                "calendar_id": c.get("calendar_id"),
                "locales": c.get("locales", []),
                "regions": c.get("regions", []),
            }
            for c in metadata.get("national_calendars", [])
        ],
        "diocesan_calendars": [
            {
                "calendar_id": c.get("calendar_id"),
                "diocese": c.get("diocese"),
                "nation": c.get("nation"),
                "locales": c.get("locales", []),
            }
            for c in metadata.get("diocesan_calendars", [])
        ],
    }


@mcp.tool()
def get_general_calendar(
    year: str,
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    Return the General Roman Calendar (the universal calendar) for a given year
    in the requested language.

    This is the UNIVERSAL calendar only. For a specific country's calendar, use
    `get_national_calendar` instead. 'IT' is the nation code for Italy; 'it' is
    merely the Italian language — they are not interchangeable.

    Args:
        year: Four-digit year as a string, e.g. "2026".
        locale: Language code: "en", "it", "fr", "la", etc. Regional forms like
            "en_US" are accepted and truncated to the base language.
    """
    return _read_json(_resolve_path(year, "universal", None, locale))


@mcp.tool()
def get_national_calendar(
    nation: str,
    year: str,
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    Return the liturgical calendar for a specific NATION.

    Events particular to the nation (not present in the General Roman Calendar,
    or marked with bracketed region tags like '[USA]') are flagged with
    `"is_particular": true` so the caller can highlight them.

    Args:
        nation: ISO 3166-1 alpha-2 country code, uppercase. Examples: "IT" (Italy),
            "US" (United States), "CA" (Canada), "HR" (Croatia), "NL" (Netherlands).
        year: Four-digit year as a string.
        locale: Language code. Use `list_available_calendars` to see which locales
            each nation supports.
    """
    nation = (nation or "").upper()
    if not nation:
        return {"error": "Missing `nation` parameter. Example: nation='IT' for Italy."}
    national = _read_json(_resolve_path(year, "nations", nation, locale))
    if isinstance(national, dict) and "error" in national:
        return national
    general = _read_json(_resolve_path(year, "universal", None, locale))
    if isinstance(general, dict) and "error" not in general:
        national = _mark_particular_celebrations(national, general)
    return national


@mcp.tool()
def get_diocesan_calendar(
    diocese: str,
    year: str,
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    Return the liturgical calendar for a specific DIOCESE. Events particular to
    the diocese (vs. the General Roman Calendar) are flagged with
    `"is_particular": true`.

    Args:
        diocese: Diocese identifier, lowercase, typically suffixed with the ISO
            country code. Example: "romamo_it" for the Diocese of Rome.
        year: Four-digit year as a string.
        locale: Language code.
    """
    if not diocese:
        return {"error": "Missing `diocese` parameter. Example: diocese='romamo_it'."}
    data = _read_json(_resolve_path(year, "dioceses", diocese, locale))
    if isinstance(data, dict) and "error" in data:
        return data
    general = _read_json(_resolve_path(year, "universal", None, locale))
    if isinstance(general, dict) and "error" not in general:
        data = _mark_particular_celebrations(data, general)
    return data


@mcp.tool()
def get_liturgy_of_the_day(
    date: str = "",
    category: str = "universal",
    identifier: str = "",
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    Return celebrations for a specific date, from the universal calendar or a
    nation/diocese.

    Args:
        date: Target date in YYYY-MM-DD format. Defaults to today.
        category: "universal" | "nations" | "dioceses".
        identifier: Required for "nations" (e.g. "IT") and "dioceses"
            (e.g. "romamo_it"). Ignored for "universal".
        locale: Language code.
    """
    if not date:
        date = datetime.date.today().isoformat()
    try:
        target = datetime.date.fromisoformat(date)
    except ValueError:
        return {"error": f"Invalid date '{date}'. Expected YYYY-MM-DD."}

    year = str(target.year)
    if category == "universal":
        data = get_general_calendar(year, locale)
    elif category == "nations":
        data = get_national_calendar(identifier, year, locale)
    elif category == "dioceses":
        data = get_diocesan_calendar(identifier, year, locale)
    else:
        return {
            "error": f"Unknown category '{category}'. "
            "Use 'universal', 'nations', or 'dioceses'."
        }

    if isinstance(data, dict) and "error" in data:
        return data

    iso = target.isoformat()
    celebrations = [
        e for e in data.get("litcal", []) if _extract_iso_date(e.get("date")) == iso
    ]
    return {
        "date": iso,
        "category": category,
        "identifier": identifier if category != "universal" else None,
        "locale": locale,
        "celebrations": celebrations,
    }


@mcp.tool()
def search_liturgical_event(
    year: str,
    query: str,
    nation: Optional[str] = None,
    diocese: Optional[str] = None,
    locale: str = "en",
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Substring search over event names and event_keys within a single calendar
    resolved from (diocese | nation | universal) for a given year.

    Args:
        year: Four-digit year as a string.
        query: Search string, e.g. "Easter", "Peter", "Advent".
        nation: Optional nation code (e.g. "IT"). Ignored if `diocese` is set.
        diocese: Optional diocese id (e.g. "romamo_it").
        locale: Language code.
    """
    if diocese:
        data = get_diocesan_calendar(diocese, year, locale)
    elif nation:
        data = get_national_calendar(nation, year, locale)
    else:
        data = get_general_calendar(year, locale)

    if isinstance(data, dict) and "error" in data:
        return [data]

    q = query.lower()
    return [
        e
        for e in data.get("litcal", [])
        if q in e.get("name", "").lower() or q in e.get("event_key", "").lower()
    ]


if __name__ == "__main__":
    from starlette.middleware import Middleware
    from starlette.middleware.cors import CORSMiddleware

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
