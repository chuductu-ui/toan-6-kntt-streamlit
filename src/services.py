"""Service layer managing curriculum, practice logs, image snapshots, and SRS state."""

import uuid
import io
from pathlib import Path
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Tuple
from PIL import Image

from config import UPLOADS_DIR, MAX_IMAGE_DIMENSION
from src.database import get_connection
from src.models import (
    Chapter, Lesson, Concept, ProblemType, PracticeRecord, SRSItem,
    MasteryLevel, SRSStatus
)
from src.srs_engine import SRSEngine


class CurriculumService:
    """Service for querying and managing curriculum hierarchy."""

    @staticmethod
    def get_chapters(volume: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        if volume:
            cursor.execute("SELECT * FROM chapters WHERE volume = ? ORDER BY order_num ASC", (volume,))
        else:
            cursor.execute("SELECT * FROM chapters ORDER BY order_num ASC")
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_lessons_by_chapter(chapter_id: str) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM lessons WHERE chapter_id = ? ORDER BY order_num ASC", (chapter_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_lesson_detail(lesson_id: str) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.*, c.title AS chapter_title, c.volume, c.code AS chapter_code
            FROM lessons l
            JOIN chapters c ON l.chapter_id = c.id
            WHERE l.id = ?
        """, (lesson_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def get_concepts_by_lesson(lesson_id: str) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM concepts WHERE lesson_id = ? ORDER BY order_num ASC", (lesson_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_problem_types_by_concept(concept_id: str) -> List[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.*, s.interval_days, s.repetitions, s.ease_factor, s.last_practiced, s.next_review, s.status AS srs_status
            FROM problem_types pt
            LEFT JOIN srs_items s ON pt.id = s.problem_type_id
            WHERE pt.concept_id = ?
            ORDER BY pt.created_at ASC
        """, (concept_id,))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_problem_type_by_id(pt_id: str) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.*, c.title AS concept_title, c.summary AS concept_summary, c.example AS concept_example,
                   l.id AS lesson_id, l.title AS lesson_title, ch.title AS chapter_title, ch.volume, ch.code AS chapter_code,
                   s.interval_days, s.repetitions, s.ease_factor, s.last_practiced, s.next_review, s.status AS srs_status
            FROM problem_types pt
            JOIN concepts c ON pt.concept_id = c.id
            JOIN lessons l ON c.lesson_id = l.id
            JOIN chapters ch ON l.chapter_id = ch.id
            LEFT JOIN srs_items s ON pt.id = s.problem_type_id
            WHERE pt.id = ?
        """, (pt_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add_custom_problem_type(
        concept_id: str,
        title: str,
        method: str = "",
        difficulty: str = "Nâng cao"
    ) -> str:
        """Add a custom user-defined problem type."""
        conn = get_connection()
        cursor = conn.cursor()
        pt_id = f"custom_pt_{uuid.uuid4().hex[:8]}"
        cursor.execute("""
            INSERT INTO problem_types (id, concept_id, title, method, difficulty, is_custom)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (pt_id, concept_id, title.strip(), method.strip(), difficulty))
        conn.commit()
        conn.close()

        # Cloud Google Drive sync if configured
        try:
            from src.gdrive_sync import GDriveSync, is_gdrive_configured
            if is_gdrive_configured():
                GDriveSync.upload_db_to_gdrive()
        except Exception as e:
            print(f"Cloud GDrive sync skipped: {e}")

        return pt_id


class PracticeService:
    """Service for handling exercise snapshots, logs, and SRS calculations."""

    @staticmethod
    def save_snapshot_image(uploaded_file, problem_type_id: str) -> Optional[str]:
        """Save and compress an uploaded image or camera snapshot to data/uploads/.
        
        Returns:
            Relative file name or None if saving failed.
        """
        if uploaded_file is None:
            return None

        try:
            # Handle both Streamlit UploadedFile and raw bytes
            if hasattr(uploaded_file, "read"):
                image_bytes = uploaded_file.read()
            else:
                image_bytes = uploaded_file

            img = Image.open(io.BytesIO(image_bytes))

            # Convert RGBA to RGB for JPEG saving if necessary
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Resize if too large while preserving aspect ratio
            width, height = img.size
            if max(width, height) > MAX_IMAGE_DIMENSION:
                scale = MAX_IMAGE_DIMENSION / max(width, height)
                new_size = (int(width * scale), int(height * scale))
                img = img.resize(new_size, Image.Resampling.LANCZOS)

            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snap_{problem_type_id}_{timestamp}_{uuid.uuid4().hex[:4]}.jpg"
            save_path = UPLOADS_DIR / filename
            img.save(save_path, "JPEG", quality=85, optimize=True)
            return filename
        except Exception as e:
            print(f"Error saving snapshot image: {e}")
            return None

    @staticmethod
    def record_practice(
        problem_type_id: str,
        practice_date: date,
        mastery_level: MasteryLevel,
        image_path: Optional[str] = None,
        notes: str = ""
    ) -> Dict[str, Any]:
        """Record a practice attempt and automatically update its SRS card."""
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Insert practice record
        record_id = f"rec_{uuid.uuid4().hex[:10]}"
        cursor.execute("""
            INSERT INTO practice_records (id, problem_type_id, practice_date, mastery_level, image_path, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (record_id, problem_type_id, str(practice_date), mastery_level.value, image_path, notes.strip()))

        # 2. Get current SRS item if exists
        cursor.execute("SELECT * FROM srs_items WHERE problem_type_id = ?", (problem_type_id,))
        srs_row = cursor.fetchone()

        if srs_row:
            cur_reps = srs_row["repetitions"]
            cur_ease = srs_row["ease_factor"]
            cur_int = srs_row["interval_days"]
        else:
            cur_reps = 0
            cur_ease = 2.5
            cur_int = 1

        is_independent = (mastery_level == MasteryLevel.INDEPENDENT)
        srs_calc = SRSEngine.calculate_next_schedule(
            practice_date=practice_date,
            is_independent=is_independent,
            current_repetitions=cur_reps,
            current_ease_factor=cur_ease,
            current_interval=cur_int,
        )

        # 3. Update or Insert SRS item
        cursor.execute("""
            INSERT INTO srs_items (problem_type_id, interval_days, repetitions, ease_factor, last_practiced, next_review, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(problem_type_id) DO UPDATE SET
                interval_days = excluded.interval_days,
                repetitions = excluded.repetitions,
                ease_factor = excluded.ease_factor,
                last_practiced = excluded.last_practiced,
                next_review = excluded.next_review,
                status = excluded.status
        """, (
            problem_type_id,
            srs_calc.interval_days,
            srs_calc.repetitions,
            srs_calc.ease_factor,
            str(practice_date),
            str(srs_calc.next_review),
            srs_calc.status.value
        ))

        conn.commit()
        conn.close()

        # Cloud Google Drive sync if configured
        try:
            from src.gdrive_sync import GDriveSync, is_gdrive_configured
            if is_gdrive_configured():
                if image_path:
                    GDriveSync.upload_image_to_gdrive(image_path)
                GDriveSync.upload_db_to_gdrive()
        except Exception as e:
            print(f"Cloud GDrive sync skipped: {e}")

        return {
            "record_id": record_id,
            "problem_type_id": problem_type_id,
            "next_review": srs_calc.next_review,
            "interval_days": srs_calc.interval_days,
            "repetitions": srs_calc.repetitions,
            "status": srs_calc.status.value,
        }

    @staticmethod
    def get_due_problem_types(current_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Fetch all problem types that are due for review today or overdue."""
        today = current_date or date.today()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.id, pt.title AS problem_title, pt.method, pt.difficulty,
                   c.title AS concept_title, l.id AS lesson_id, l.title AS lesson_title,
                   ch.code AS chapter_code, ch.title AS chapter_title, ch.volume,
                   s.interval_days, s.repetitions, s.ease_factor, s.last_practiced, s.next_review, s.status,
                   (julianday(?) - julianday(s.next_review)) AS days_overdue
            FROM srs_items s
            JOIN problem_types pt ON s.problem_type_id = pt.id
            JOIN concepts c ON pt.concept_id = c.id
            JOIN lessons l ON c.lesson_id = l.id
            JOIN chapters ch ON l.chapter_id = ch.id
            WHERE date(s.next_review) <= date(?)
            ORDER BY s.next_review ASC
        """, (str(today), str(today)))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_upcoming_problem_types(days_ahead: int = 3, current_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Fetch problem types due in the next few days."""
        today = current_date or date.today()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pt.id, pt.title AS problem_title, pt.method, pt.difficulty,
                   c.title AS concept_title, l.title AS lesson_title, ch.code AS chapter_code,
                   s.interval_days, s.repetitions, s.last_practiced, s.next_review, s.status,
                   (julianday(s.next_review) - julianday(?)) AS days_ahead
            FROM srs_items s
            JOIN problem_types pt ON s.problem_type_id = pt.id
            JOIN concepts c ON pt.concept_id = c.id
            JOIN lessons l ON c.lesson_id = l.id
            JOIN chapters ch ON l.chapter_id = ch.id
            WHERE date(s.next_review) > date(?) AND date(s.next_review) <= date(?, '+' || ? || ' days')
            ORDER BY s.next_review ASC
        """, (str(today), str(today), str(today), days_ahead))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows

    @staticmethod
    def get_dashboard_stats(current_date: Optional[date] = None) -> Dict[str, Any]:
        """Aggregate high-level metrics for dashboard."""
        today = current_date or date.today()
        conn = get_connection()
        cursor = conn.cursor()

        # Total counts
        cursor.execute("SELECT COUNT(*) FROM problem_types")
        total_problems = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM practice_records")
        total_practices = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM practice_records WHERE mastery_level = 'INDEPENDENT'")
        independent_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM practice_records WHERE mastery_level = 'HINTED'")
        hinted_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM srs_items WHERE date(next_review) <= date(?)", (str(today),))
        due_today_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM srs_items WHERE status = 'MASTERED'")
        mastered_count = cursor.fetchone()[0]

        # Problems practiced at least once
        cursor.execute("SELECT COUNT(DISTINCT problem_type_id) FROM practice_records")
        problems_practiced = cursor.fetchone()[0]

        conn.close()

        return {
            "total_problems": total_problems,
            "total_practices": total_practices,
            "independent_count": independent_count,
            "hinted_count": hinted_count,
            "due_today_count": due_today_count,
            "mastered_count": mastered_count,
            "problems_practiced": problems_practiced,
            "unpracticed_count": max(0, total_problems - problems_practiced),
        }

    @staticmethod
    def get_practice_history(problem_type_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history of practice attempts."""
        conn = get_connection()
        cursor = conn.cursor()
        query = """
            SELECT pr.*, pt.title AS problem_title, l.title AS lesson_title, ch.title AS chapter_title
            FROM practice_records pr
            JOIN problem_types pt ON pr.problem_type_id = pt.id
            JOIN concepts c ON pt.concept_id = c.id
            JOIN lessons l ON c.lesson_id = l.id
            JOIN chapters ch ON l.chapter_id = ch.id
        """
        params = []
        if problem_type_id:
            query += " WHERE pr.problem_type_id = ? "
            params.append(problem_type_id)

        query += " ORDER BY pr.practice_date DESC, pr.created_at DESC LIMIT ? "
        params.append(limit)

        cursor.execute(query, tuple(params))
        rows = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return rows
