"""
Free Data Sources Package
=========================

Cascading data-provider stack used when nepse-bot runs from environments
that cannot reach nepalstock.com.np directly (e.g. Vercel US, non-Nepal hosts).

Source priorities:
    1. `yonepse`    – GitHub-Actions JSON scraper (updates every ~15 min).
                      Covers: live market, indices, sector indices, top stocks,
                      supply/demand, market status, brokers, disclosures, notices,
                      dividends, upcoming IPO, all securities.
    2. `samirwagle` – GitHub-Actions scraper with daily floorsheet CSVs and
                      per-symbol price / dividend / right-share CSVs.
    3. `sharesansar_html` / `merolagani_html` – On-demand HTML scraping when
                      the above are stale or missing a specific field.
    4. Bundled SQLite (historical) – last-resort offline fallback.

All upstream responses go through `cache.TTLCache` to keep Vercel cold starts
cheap and stay within free-tier request budgets.
"""

from .cache import TTLCache, get_cache
from . import yonepse, samirwagle, aggregator

__all__ = ["TTLCache", "get_cache", "yonepse", "samirwagle", "aggregator"]
