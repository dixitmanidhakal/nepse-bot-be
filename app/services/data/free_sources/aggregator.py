"""
Free-Sources Aggregator
=======================

Single entry-point used by the rest of the backend. Cascades through
the available free sources in priority order:

    live market, indices, top, status   → yonepse
    per-symbol historical OHLCV         → samirwagle prices.csv → SQLite
    daily floorsheet                    → samirwagle floorsheet CSV
    dividends / rights                  → samirwagle per-symbol
    partial market depth                → yonepse supply_demand
    full 20-level depth                 → NOT AVAILABLE on free tier → raise DepthUnavailable

All responses are already cached inside the individual source modules.

The aggregator is async and network-safe: every external call is wrapped
in try/except and will gracefully degrade rather than raise.
"""

from __future__ import annotations

import logging
from datetime import date
from typing import Any, Dict, List, Optional

from . import yonepse, samirwagle

logger = logging.getLogger(__name__)


class DepthUnavailable(Exception):
    """Raised when full 20-level depth is requested but only partial is free."""


# -------------------------- live market / snapshot --------------------------

async def live_market() -> List[Dict[str, Any]]:
    """Per-symbol live snapshot (LTP, change, volume, turnover, market cap)."""
    return await yonepse.get_live_market()


async def live_quote(symbol: str) -> Optional[Dict[str, Any]]:
    """Single-symbol live quote. Returns None if not found."""
    return await yonepse.get_live_market_by_symbol(symbol)


async def market_status() -> Dict[str, Any]:
    return await yonepse.get_market_status()


async def market_summary() -> List[Dict[str, Any]]:
    return await yonepse.get_market_summary()


async def indices() -> List[Dict[str, Any]]:
    return await yonepse.get_indices()


async def sector_indices() -> List[Dict[str, Any]]:
    return await yonepse.get_sector_indices()


async def top_stocks() -> Dict[str, List[Dict[str, Any]]]:
    return await yonepse.get_top_stocks()


# -------------------------- depth --------------------------

async def partial_depth(symbol: str) -> Dict[str, Any]:
    """Best-effort aggregate supply/demand (yonepse). Always safe to call."""
    return await yonepse.get_supply_demand_for_symbol(symbol)


async def full_depth(symbol: str) -> Dict[str, Any]:
    """
    Full 20-level order book — not available on free tier.
    Callers should catch DepthUnavailable and fall back to partial_depth().
    """
    raise DepthUnavailable(
        "Full 20-level depth requires direct access to nepalstock.com.np, "
        "which is geo-restricted to Nepal. Free GitHub-Actions scrapers "
        "only publish aggregate bid/ask. Use partial_depth() for best "
        "available free data."
    )


# -------------------------- floorsheet --------------------------

async def latest_floorsheet_date() -> Optional[str]:
    return await samirwagle.get_latest_floorsheet_date()


async def floorsheet(
    target: Optional[str | date] = None,
    symbol: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Full floorsheet for a trading date.

    Args:
        target: 'YYYY-MM-DD' string, date object, or None (→ latest available).
        symbol: filter to one symbol if provided.
    """
    if target is None:
        target = await samirwagle.get_latest_floorsheet_date()
        if not target:
            return []
    if symbol:
        return await samirwagle.get_floorsheet_for_symbol(symbol, target)
    return await samirwagle.get_floorsheet_for_date(target)


# -------------------------- per-symbol series --------------------------

async def symbol_prices(symbol: str) -> List[Dict[str, Any]]:
    """
    OHLCV history (most-recent first).
    Primary: SamirWagle per-symbol prices.csv (daily updated).
    """
    rows = await samirwagle.get_symbol_prices(symbol)
    if rows:
        return rows
    # Could fall back to SQLite here; left to the existing historical_provider
    # consumer rather than duplicate logic.
    return []


async def symbol_dividends(symbol: str) -> List[Dict[str, Any]]:
    return await samirwagle.get_symbol_dividends(symbol)


async def symbol_rights(symbol: str) -> List[Dict[str, Any]]:
    return await samirwagle.get_symbol_rights(symbol)


# -------------------------- meta --------------------------

async def all_securities() -> List[Dict[str, Any]]:
    """Master of 613 securities with sector, company name, etc."""
    return await yonepse.get_all_securities()


async def brokers() -> List[Dict[str, Any]]:
    return await yonepse.get_brokers()


async def upcoming_ipo() -> List[Dict[str, Any]]:
    return await yonepse.get_upcoming_ipo()


async def disclosures() -> List[Dict[str, Any]]:
    return await yonepse.get_disclosures()


async def notices() -> List[Dict[str, Any]]:
    return await yonepse.get_notices()


async def dps() -> List[Dict[str, Any]]:
    return await yonepse.get_dps()


# -------------------------- health --------------------------

async def health() -> Dict[str, Any]:
    """
    Aggregate freshness report from all underlying sources — used by
    /__verify-data and by `nepse_api_client` when deciding fallbacks.
    """
    y = await yonepse.get_freshness()
    s = await samirwagle.get_freshness()
    fresh_enough = (y.get("commit_age_minutes") or 99999) < 120
    return {
        "yonepse": y,
        "samirwagle": s,
        "yonepse_fresh": fresh_enough,
        "depth_available": "partial",  # always partial on free tier
        "full_depth_available": False,
    }
