"""Data models and constants for Toan 6 KNTT."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional, List
from enum import Enum


class MasteryLevel(str, Enum):
    INDEPENDENT = "INDEPENDENT"  # Con tự làm được độc lập
    HINTED = "HINTED"            # Cần gợi ý / hướng dẫn


class SRSStatus(str, Enum):
    NEW = "NEW"                  # Chưa làm bao giờ
    LEARNING = "LEARNING"        # Đang củng cố (sau khi cần gợi ý)
    REVIEW = "REVIEW"            # Đang trong chu kỳ lặp lại ngắt quãng
    MASTERED = "MASTERED"        # Đã nắm rất vững (>= 4 lần độc lập liên tiếp)


@dataclass
class Chapter:
    id: str
    volume: int                  # 1: Tập 1, 2: Tập 2
    code: str                    # "I", "II", ..., "IX"
    title: str
    order_num: int


@dataclass
class Lesson:
    id: str
    chapter_id: str
    title: str
    pages: str
    order_num: int
    kind: str = "lesson"         # "lesson", "review", "activity"


@dataclass
class Concept:
    id: str
    lesson_id: str
    title: str
    summary: str
    example: str = ""
    order_num: int = 1


@dataclass
class ProblemType:
    id: str
    concept_id: str
    title: str
    method: str = ""             # Phương pháp giải / công thức / mẹo
    difficulty: str = "Nâng cao" # "Cơ bản", "Nâng cao", "Thực tế"
    image_path: Optional[str] = None # Ảnh chụp đề bài / công thức dạng toán
    is_custom: bool = False      # True nếu do phụ huynh tự thêm
    created_at: Optional[datetime] = None


@dataclass
class PracticeRecord:
    id: str
    problem_type_id: str
    practice_date: date
    mastery_level: MasteryLevel
    image_path: Optional[str] = None
    notes: str = ""
    created_at: Optional[datetime] = None


@dataclass
class SRSItem:
    problem_type_id: str
    interval_days: int
    repetitions: int
    ease_factor: float
    last_practiced: date
    next_review: date
    status: SRSStatus = SRSStatus.LEARNING
