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


# Fields kept in compact projection. Drops readings, day/month name variants,
# grade_abbr/display, event_idx, psalter_week, common_lcl, color, grade_lcl,
# liturgical_season_lcl — keep only what's needed to answer "what" and "when".
_COMPACT_FIELDS = (
    "event_key",
    "name",
    "date",
    "grade",
    "is_particular",
)

# Grade >= 6 = Solemnity or Feast of the Lord (the liturgically significant
# days most questions are actually about). Used as the default filter when
# no month is specified so year-overview queries stay within context.
HIGHLIGHT_GRADE_THRESHOLD = 6


def _compact_event(event: Dict[str, Any]) -> Dict[str, Any]:
    return {k: event[k] for k in _COMPACT_FIELDS if k in event}


def _load_general(year: str, locale: str) -> Any:
    return _read_json(_resolve_path(year, "universal", None, locale))


def _load_national(year: str, nation: str, locale: str) -> Any:
    nation = (nation or "").upper()
    if not nation:
        return {"error": "Missing `nation` parameter. Example: nation='IT' for Italy."}
    national = _read_json(_resolve_path(year, "nations", nation, locale))
    if isinstance(national, dict) and "error" in national:
        return national
    general = _load_general(year, locale)
    if isinstance(general, dict) and "error" not in general:
        national = _mark_particular_celebrations(national, general)
    return national


def _load_diocesan(year: str, diocese: str, locale: str) -> Any:
    if not diocese:
        return {"error": "Missing `diocese` parameter. Example: diocese='romamo_it'."}
    data = _read_json(_resolve_path(year, "dioceses", diocese, locale))
    if isinstance(data, dict) and "error" in data:
        return data
    general = _load_general(year, locale)
    if isinstance(general, dict) and "error" not in general:
        data = _mark_particular_celebrations(data, general)
    return data


def _shape_calendar(
    data: Dict[str, Any], month: Optional[int], detailed: bool
) -> Dict[str, Any]:
    """Trim a full calendar response for LLM consumption.

    Filter order:
      1. `month=N` → narrow to that month (all grades).
      2. else if not `detailed` → default to solemnities + feasts of the Lord
         (grade >= 6) so year-overview queries stay small. Weekdays and
         optional memorials are omitted unless the caller asks for a month
         or for detailed data.
      3. `detailed=True` returns full event records; otherwise events are
         projected to _COMPACT_FIELDS.
    """
    litcal = data.get("litcal", [])
    filter_applied = "none"

    if month is not None:
        if not 1 <= month <= 12:
            return {"error": f"month must be 1..12, got {month}"}
        tag = f"-{month:02d}-"
        litcal = [
            e for e in litcal if (_extract_iso_date(e.get("date")) or "")[4:8] == tag
        ]
        filter_applied = f"month={month:02d}"
    elif not detailed:
        litcal = [
            e for e in litcal if (e.get("grade", 0) or 0) >= HIGHLIGHT_GRADE_THRESHOLD
        ]
        filter_applied = "highlights (grade>=6: solemnities + feasts of the Lord)"

    if not detailed:
        litcal = [_compact_event(e) for e in litcal]

    return {
        "settings": data.get("settings", {}),
        "filter_applied": filter_applied,
        "count": len(litcal),
        "litcal": litcal,
    }


# Every tool accepts the _conversation_id / _trace_id / _fetched_urls metadata
# kwargs that some MCP clients inject, so pydantic validation doesn't reject them.


@mcp.tool()
def list_available_calendars(
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Dict[str, Any]:
    """
    WHEN TO USE: first call in any new conversation — enumerates valid nation
    codes, diocese ids, locales, and the covered year range so subsequent
    tool calls don't guess.

    TOOL MAP (read this once, pick the right tool per question):
      • Single date ("what's today's feast?")        → get_liturgy_of_the_day
      • Known event name ("when is St. Francis?")    → search_liturgical_event
      • Whole-month overview ("solemnities in Oct")  → get_*_calendar(month=N)
      • Year overview (solemnities only, default)    → get_*_calendar
      • Full detail (readings, etc.)                 → detailed=True or
                                                       get_liturgy_of_the_day

    By default get_*_calendar returns only solemnities + feasts of the Lord
    (grade >= 6, ~25 events/year). Pass `month=1..12` for full-month detail.

    Universal vs national: "IT" is the nation code for Italy; "it" is the
    Italian language. They are not interchangeable — use get_national_calendar
    with `nation="IT"` for Italy, not get_general_calendar with `locale="it"`.
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
    month: Optional[int] = None,
    detailed: bool = False,
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    WHEN TO USE: the UNIVERSAL (General Roman) calendar only. For a country
    use `get_national_calendar` — "IT" is Italy (nation), "it" is just the
    Italian locale. Not interchangeable.

    For a single date use `get_liturgy_of_the_day`; for a named event use
    `search_liturgical_event`.

    Default response shape (both apply unless overridden):
      • HIGHLIGHTS ONLY — solemnities + feasts of the Lord (grade >= 6),
        ~25 events/year. Weekdays and optional memorials are omitted.
        Pass `month=1..12` to get the full month instead.
      • COMPACT fields only: event_key, name, date, grade. Pass
        `detailed=True` for readings, day/month name variants, etc.

    `filter_applied` in the response tells you which default was used.

    Args:
        year: Four-digit year as a string, e.g. "2026".
        locale: Language code: "en", "it", "fr", "la", etc. Regional forms
            ("en_US") are truncated to the base language.
        month: Optional 1..12 filter. Strongly recommended — drops response
            to ~40 events.
        detailed: Full event records including `readings`. Large.
    """
    data = _load_general(year, locale)
    if isinstance(data, dict) and "error" in data:
        return data
    return _shape_calendar(data, month, detailed)


@mcp.tool()
def get_national_calendar(
    nation: str,
    year: str,
    locale: str = "en",
    month: Optional[int] = None,
    detailed: bool = False,
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    WHEN TO USE: a specific country's calendar. `nation` is a country code
    (e.g. "IT", "US"); it is NOT a language. For Italian-language universal
    calendar use get_general_calendar(locale="it") instead.

    Events particular to the nation (not in the General Roman Calendar, or
    tagged like "[USA]") are flagged `is_particular: true` so you can cite
    what's specific to this nation vs. universal.

    For a single date use `get_liturgy_of_the_day(category="nations", ...)`;
    for a named saint use `search_liturgical_event(nation=...)`.

    Default response shape:
      • HIGHLIGHTS ONLY — solemnities + feasts of the Lord (grade >= 6),
        ~25 events/year. Pass `month=1..12` for a full month view.
      • COMPACT fields: event_key, name, date, grade, is_particular.
        Pass `detailed=True` for readings, day-name variants, etc.

    `filter_applied` in the response tells you which default was used.

    Args:
        nation: ISO 3166-1 alpha-2 country code, uppercase. E.g. "IT", "US",
            "CA", "HR", "NL". Call `list_available_calendars` for the full list.
        year: Four-digit year as a string.
        locale: Language code. Each nation supports a specific set (see
            `list_available_calendars`).
        month: Optional 1..12 filter — strongly recommended for year queries.
        detailed: Full records (large).
    """
    national = _load_national(year, nation, locale)
    if isinstance(national, dict) and "error" in national:
        return national
    return _shape_calendar(national, month, detailed)


@mcp.tool()
def get_diocesan_calendar(
    diocese: str,
    year: str,
    locale: str = "en",
    month: Optional[int] = None,
    detailed: bool = False,
    _conversation_id: Optional[str] = None,
    _trace_id: Optional[str] = None,
    _fetched_urls: Optional[List[Any]] = None,
) -> Any:
    """
    WHEN TO USE: a specific diocese's calendar (rare — only use when the
    question explicitly names a diocese). For a country, use
    `get_national_calendar`. For a single date use `get_liturgy_of_the_day`.

    Events particular to the diocese are flagged `is_particular: true`.

    Default response: highlights only (grade >= 6) in compact fields. Pass
    `month=1..12` for a full month, or `detailed=True` for full records.
    `filter_applied` in the response confirms which default was used.

    Args:
        diocese: Diocese identifier, lowercase, suffixed with the ISO country
            code. E.g. "romamo_it" (Diocese of Rome). Call
            `list_available_calendars` for available ids.
        year: Four-digit year as a string.
        locale: Language code.
        month: Optional 1..12 filter.
        detailed: Full records (large).
    """
    data = _load_diocesan(year, diocese, locale)
    if isinstance(data, dict) and "error" in data:
        return data
    return _shape_calendar(data, month, detailed)


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
    WHEN TO USE: any question about a SINGLE DATE — "today's feast", "what's
    celebrated on 2026-04-05?", "liturgy for Christmas". This is the cheapest
    and most detailed tool: returns full event records (including readings
    when available) since at most a handful of events share a date.

    Prefer this over get_*_calendar whenever the user is asking about one day.

    Args:
        date: Target date in YYYY-MM-DD format. Defaults to today.
        category: "universal" | "nations" | "dioceses".
        identifier: Required for "nations" (e.g. "IT") and "dioceses"
            (e.g. "romamo_it"); ignored for "universal".
        locale: Language code. National/diocesan calendars expect a locale
            supported by that calendar (see `list_available_calendars`).
    """
    if not date:
        date = datetime.date.today().isoformat()
    try:
        target = datetime.date.fromisoformat(date)
    except ValueError:
        return {"error": f"Invalid date '{date}'. Expected YYYY-MM-DD."}

    year = str(target.year)
    if category == "universal":
        data = _load_general(year, locale)
    elif category == "nations":
        data = _load_national(year, identifier, locale)
    elif category == "dioceses":
        data = _load_diocesan(year, identifier, locale)
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
    WHEN TO USE: the user names a specific event — "when is St. Francis's
    feast?", "Advent date", "Easter 2026". Returns only matching events
    (full records) so the payload stays small even for common queries.

    Much cheaper than pulling a whole calendar and grepping locally.

    Case-insensitive substring match on the event's `name` and `event_key`
    in the requested locale. Pass `nation` or `diocese` to search within a
    particular calendar; otherwise searches the universal calendar.

    Args:
        year: Four-digit year as a string.
        query: Search string, e.g. "Easter", "Peter", "Advent", "Francis".
        nation: Optional nation code (e.g. "IT"). Ignored if `diocese` is set.
        diocese: Optional diocese id (e.g. "romamo_it").
        locale: Language code — searches that locale's translated names.
    """
    if diocese:
        data = _load_diocesan(year, diocese, locale)
    elif nation:
        data = _load_national(year, nation, locale)
    else:
        data = _load_general(year, locale)

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
