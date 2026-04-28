"""Unit tests for the NEPSE market-hours helper."""
from __future__ import annotations

from datetime import datetime

from app.services.data.market_hours import NPT, session_status


def _npt(y, m, d, hh, mm=0):
    return datetime(y, m, d, hh, mm, tzinfo=NPT)


class TestSessionStatus:
    def test_open_midsession(self):
        # 2026-04-26 is a Sunday — NEPSE trading day.
        s = session_status(_npt(2026, 4, 26, 12, 30))
        assert s.is_open is True
        assert s.is_poll_window is True
        assert s.reason == "market open"

    def test_preopen_buffer(self):
        # 10:57 on Sunday is inside the pre-open poll buffer.
        s = session_status(_npt(2026, 4, 26, 10, 57))
        assert s.is_open is False
        assert s.is_poll_window is True
        assert "pre" in s.reason

    def test_postclose_buffer(self):
        # 15:03 on Sunday is inside the post-close poll buffer.
        s = session_status(_npt(2026, 4, 26, 15, 3))
        assert s.is_open is False
        assert s.is_poll_window is True

    def test_after_postclose_buffer(self):
        # 16:00 on Sunday is outside both session and poll window.
        s = session_status(_npt(2026, 4, 26, 16, 0))
        assert s.is_open is False
        assert s.is_poll_window is False

    def test_friday_closed(self):
        # 2026-04-24 is a Friday — no trading.
        s = session_status(_npt(2026, 4, 24, 12, 0))
        assert s.is_open is False
        assert s.is_poll_window is False
        assert "friday" in s.reason.lower()

    def test_saturday_closed(self):
        s = session_status(_npt(2026, 4, 25, 12, 0))
        assert s.is_open is False
        assert s.is_poll_window is False
        assert "saturday" in s.reason.lower()

    def test_holiday_override(self):
        # Even on a Sunday, a holiday closes the market.
        s = session_status(_npt(2026, 4, 26, 12, 0), holidays=["2026-04-26"])
        assert s.is_open is False
        assert s.is_poll_window is False
        assert s.reason == "holiday"

    def test_next_session_open_computed(self):
        # Saturday 16:00 — next open should be Sunday 11:00 = ~19 hours.
        s = session_status(_npt(2026, 4, 25, 16, 0))
        assert s.seconds_to_open is not None
        assert 60 * 60 * 18 < s.seconds_to_open < 60 * 60 * 24
