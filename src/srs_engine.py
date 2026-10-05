"""Spaced Repetition System (SRS) Engine for Math 6."""

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional, Tuple
from config import DEFAULT_EASE_FACTOR, MIN_EASE_FACTOR, MAX_EASE_FACTOR, SRS_INTERVALS
from src.models import SRSStatus


@dataclass
class SRSReviewResult:
    next_review: date
    interval_days: int
    repetitions: int
    ease_factor: float
    status: SRSStatus


class SRSEngine:
    """Spaced Repetition algorithm adapted from SM-2 for Grade 6 student learning."""

    @staticmethod
    def calculate_next_schedule(
        practice_date: date,
        is_independent: bool,
        current_repetitions: int = 0,
        current_ease_factor: float = DEFAULT_EASE_FACTOR,
        current_interval: int = 1,
    ) -> SRSReviewResult:
        """Calculate the next review date and updated repetition parameters.
        
        Args:
            practice_date: Date the exercise was performed.
            is_independent: True if the student solved it independently, False if hints were needed.
            current_repetitions: Count of consecutive successful independent solves.
            current_ease_factor: Difficulty multiplier (default 2.5).
            current_interval: The previous interval in days.
            
        Returns:
            SRSReviewResult containing next_review date, new interval, repetitions, ease factor, and status.
        """
        if is_independent:
            if current_repetitions == 0:
                new_interval = SRS_INTERVALS.get(0, 1)
            elif current_repetitions == 1:
                new_interval = SRS_INTERVALS.get(1, 3)
            elif current_repetitions == 2:
                new_interval = SRS_INTERVALS.get(2, 7)
            else:
                new_interval = int(round(current_interval * current_ease_factor))
                if new_interval <= current_interval:
                    new_interval = current_interval + 1

            new_repetitions = current_repetitions + 1
            new_ease = min(MAX_EASE_FACTOR, current_ease_factor + 0.1)
            status = SRSStatus.MASTERED if new_repetitions >= 4 else SRSStatus.REVIEW
        else:
            # When student needed guidance/hints, reset the repetition chain and review tomorrow
            new_interval = 1
            new_repetitions = 0
            new_ease = max(MIN_EASE_FACTOR, current_ease_factor - 0.2)
            status = SRSStatus.LEARNING

        next_date = practice_date + timedelta(days=new_interval)

        return SRSReviewResult(
            next_review=next_date,
            interval_days=new_interval,
            repetitions=new_repetitions,
            ease_factor=round(new_ease, 2),
            status=status,
        )

    @staticmethod
    def is_due(next_review: date, current_date: Optional[date] = None) -> bool:
        """Check if an item is due for review today or overdue."""
        today = current_date or date.today()
        return next_review <= today

    @staticmethod
    def days_until_due(next_review: date, current_date: Optional[date] = None) -> int:
        """Return the number of days until the review is due (negative if overdue)."""
        today = current_date or date.today()
        return (next_review - today).days

    @staticmethod
    def get_urgency_badge(next_review: date, current_date: Optional[date] = None) -> Tuple[str, str]:
        """Return label and color tag for UI display.
        
        Returns:
            (badge_text, category_code): e.g. ('🔴 Quá hạn', 'overdue'), ('🟠 Đến hạn hôm nay', 'due_today'), ...
        """
        days = SRSEngine.days_until_due(next_review, current_date)
        if days < 0:
            return f"🔴 Quá hạn ({abs(days)} ngày)", "overdue"
        elif days == 0:
            return "🟠 Đến hạn hôm nay", "due_today"
        elif days <= 3:
            return f"🟡 Sắp tới ({days} ngày)", "upcoming"
        else:
            return f"🟢 Còn {days} ngày", "future"
