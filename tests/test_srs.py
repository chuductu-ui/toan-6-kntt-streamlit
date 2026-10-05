"""Unit tests for the Spaced Repetition System (SRS) Engine."""

import pytest
from datetime import date, timedelta
from src.srs_engine import SRSEngine, SRSReviewResult
from src.models import SRSStatus


def test_first_independent_practice():
    """First independent solve should schedule review for 1 day later."""
    base_date = date(2026, 10, 5)
    res = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=True,
        current_repetitions=0,
        current_ease_factor=2.5,
        current_interval=1,
    )
    assert res.interval_days == 1
    assert res.next_review == base_date + timedelta(days=1)
    assert res.repetitions == 1
    assert res.ease_factor == 2.6
    assert res.status == SRSStatus.REVIEW


def test_consecutive_independent_practices():
    """Consecutive independent solves should advance intervals: 1 -> 3 -> 7 -> multiplier."""
    base_date = date(2026, 10, 5)

    # 2nd independent practice
    res2 = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=True,
        current_repetitions=1,
        current_ease_factor=2.6,
        current_interval=1,
    )
    assert res2.interval_days == 3
    assert res2.next_review == base_date + timedelta(days=3)
    assert res2.repetitions == 2

    # 3rd independent practice
    res3 = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=True,
        current_repetitions=2,
        current_ease_factor=2.7,
        current_interval=3,
    )
    assert res3.interval_days == 7
    assert res3.next_review == base_date + timedelta(days=7)
    assert res3.repetitions == 3

    # 4th independent practice (repetition >= 3: multiplier)
    res4 = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=True,
        current_repetitions=3,
        current_ease_factor=2.8,
        current_interval=7,
    )
    expected_interval = int(round(7 * 2.8))  # 20 days
    assert res4.interval_days == expected_interval
    assert res4.repetitions == 4
    assert res4.status == SRSStatus.MASTERED


def test_hinted_practice_resets_repetition_and_schedules_tomorrow():
    """When hints are needed, reset repetitions to 0 and schedule next review tomorrow."""
    base_date = date(2026, 10, 5)
    res = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=False,
        current_repetitions=3,
        current_ease_factor=2.8,
        current_interval=20,
    )
    assert res.interval_days == 1
    assert res.next_review == base_date + timedelta(days=1)
    assert res.repetitions == 0
    assert res.ease_factor == 2.6
    assert res.status == SRSStatus.LEARNING


def test_ease_factor_bounds():
    """Ease factor should never exceed 3.0 or fall below 1.3."""
    base_date = date(2026, 10, 5)

    # Upper bound test
    res_high = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=True,
        current_repetitions=5,
        current_ease_factor=3.0,
        current_interval=30,
    )
    assert res_high.ease_factor <= 3.0

    # Lower bound test
    res_low = SRSEngine.calculate_next_schedule(
        practice_date=base_date,
        is_independent=False,
        current_repetitions=0,
        current_ease_factor=1.35,
        current_interval=1,
    )
    assert res_low.ease_factor >= 1.30


def test_is_due_and_days_until_due():
    """Verify due checking logic."""
    today = date(2026, 10, 5)
    
    # Overdue
    past_due = date(2026, 10, 3)
    assert SRSEngine.is_due(past_due, today) is True
    assert SRSEngine.days_until_due(past_due, today) == -2

    # Due today
    due_today = date(2026, 10, 5)
    assert SRSEngine.is_due(due_today, today) is True
    assert SRSEngine.days_until_due(due_today, today) == 0

    # Due in future
    future_due = date(2026, 10, 8)
    assert SRSEngine.is_due(future_due, today) is False
    assert SRSEngine.days_until_due(future_due, today) == 3


def test_urgency_badges():
    """Verify urgency badge labels."""
    today = date(2026, 10, 5)
    badge, cat = SRSEngine.get_urgency_badge(date(2026, 10, 4), today)
    assert "Quá hạn" in badge
    assert cat == "overdue"

    badge, cat = SRSEngine.get_urgency_badge(date(2026, 10, 5), today)
    assert "Đến hạn hôm nay" in badge
    assert cat == "due_today"

    badge, cat = SRSEngine.get_urgency_badge(date(2026, 10, 7), today)
    assert "Sắp tới" in badge
    assert cat == "upcoming"

    badge, cat = SRSEngine.get_urgency_badge(date(2026, 10, 15), today)
    assert "Còn" in badge
    assert cat == "future"
