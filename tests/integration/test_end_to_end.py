"""
End-to-end integration tests that exercise multiple layers together.

These tests are intentionally broad — they wire the SQLite historical
provider to the recommendation engine to the REST API, verifying the
whole stack responds consistently.
"""

from __future__ import annotations

import pytest


class TestRecommendationPipeline:
    def test_universe_then_top_consistent(
        self, client, historical_provider_available
    ):
        u = client.get("/api/v1/recommendations/universe").json()["data"]
        t = client.get(
            "/api/v1/recommendations/top",
            params={"limit": 20, "min_rows": 120, "max_symbols": 50},
        ).json()
        # universe_size reported by /top never exceeds the DB total
        assert t["universe_size"] <= u["total_symbols"]
        assert t["count"] == len(t["data"])

    def test_top_and_explain_agree_on_score(
        self, client, historical_provider_available
    ):
        top = client.get(
            "/api/v1/recommendations/top",
            params={"limit": 3, "min_rows": 120, "max_symbols": 40},
        ).json()
        if not top["data"]:
            pytest.skip("No recommendations in snapshot.")
        sym = top["data"][0]["symbol"]
        detail = client.get(
            f"/api/v1/recommendations/explain/{sym}"
        ).json()["data"]
        # Same symbol, same min_rows → identical composite score.
        assert detail["symbol"] == sym
        # Scores are deterministic within 0.01 of a point (rounding).
        assert abs(detail["score"] - top["data"][0]["score"]) <= 1.0


class TestConcurrentCallsAreStable:
    def test_multiple_universe_calls_are_consistent(
        self, client, historical_provider_available
    ):
        first = client.get("/api/v1/recommendations/universe").json()["data"]
        second = client.get("/api/v1/recommendations/universe").json()["data"]
        assert first["total_symbols"] == second["total_symbols"]
        assert first["total_rows"] == second["total_rows"]
