"""Unit tests for database services and practice recording."""

import io
from pathlib import Path
from datetime import date, timedelta
from PIL import Image

from src.database import init_db, get_connection
from src.seed_data import seed_database
from src.services import CurriculumService, PracticeService
from src.models import MasteryLevel


def test_database_curriculum_queries(tmp_path):
    """Verify chapters, lessons, and concepts can be queried."""
    chapters = CurriculumService.get_chapters()
    assert len(chapters) == 9

    # Volume 1 should have 5 chapters
    vol1 = CurriculumService.get_chapters(volume=1)
    assert len(vol1) == 5

    # Volume 2 should have 4 chapters
    vol2 = CurriculumService.get_chapters(volume=2)
    assert len(vol2) == 4

    # Chapter 1 should have 7 lessons
    ch1_lessons = CurriculumService.get_lessons_by_chapter("ch-01")
    assert len(ch1_lessons) == 7

    # Lesson 1 concepts
    concepts = CurriculumService.get_concepts_by_lesson("bai-01")
    assert len(concepts) >= 1

    # Problem types for lesson 1 (initially empty before user/daughter adds them)
    pt_list = CurriculumService.get_problem_types_by_concept(concepts[0]["id"])
    assert isinstance(pt_list, list)


def test_add_custom_problem_type():
    """Verify parents can add custom math problem types."""
    concepts = CurriculumService.get_concepts_by_lesson("bai-01")
    c_id = concepts[0]["id"]

    new_id = CurriculumService.add_custom_problem_type(
        concept_id=c_id,
        title="Dạng toán tự chế về số chia hết đặc biệt",
        method="Sử dụng sơ đồ Ven để phân chia tập hợp",
        difficulty="Nâng cao",
        image_path="test_sample_image.jpg"
    )
    assert new_id.startswith("custom_pt_")

    pt = CurriculumService.get_problem_type_by_id(new_id)
    assert pt is not None
    assert pt["title"] == "Dạng toán tự chế về số chia hết đặc biệt"
    assert pt["is_custom"] == 1
    assert pt["image_path"] == "test_sample_image.jpg"

    # Cleanup
    CurriculumService.delete_problem_type(new_id)


def test_practice_recording_and_srs_update():
    """Verify recording practice updates SRS table correctly."""
    concepts = CurriculumService.get_concepts_by_lesson("bai-01")
    c_id = concepts[0]["id"]
    pt_id = CurriculumService.add_custom_problem_type(
        concept_id=c_id,
        title="Dạng toán kiểm thử SRS",
        difficulty="Nâng cao"
    )

    today = date(2026, 10, 5)

    # Attempt 1: Independent solve
    res1 = PracticeService.record_practice(
        problem_type_id=pt_id,
        practice_date=today,
        mastery_level=MasteryLevel.INDEPENDENT,
        notes="Con làm bài rất tập trung và tính toán chính xác."
    )
    assert res1["repetitions"] == 1
    assert res1["interval_days"] == 1
    assert res1["next_review"] == today + timedelta(days=1)

    # Attempt 2: Next day, independent solve
    res2 = PracticeService.record_practice(
        problem_type_id=pt_id,
        practice_date=today + timedelta(days=1),
        mastery_level=MasteryLevel.INDEPENDENT,
        notes="Con nhớ bài tốt."
    )
    assert res2["repetitions"] == 2
    assert res2["interval_days"] == 3
    assert res2["next_review"] == today + timedelta(days=4)

    # Attempt 3: Hinted solve (should reset)
    res3 = PracticeService.record_practice(
        problem_type_id=pt_id,
        practice_date=today + timedelta(days=4),
        mastery_level=MasteryLevel.HINTED,
        notes="Bị quên công thức tính số phần tử, cần bố nhắc nhẹ."
    )
    assert res3["repetitions"] == 0
    assert res3["interval_days"] == 1
    assert res3["next_review"] == today + timedelta(days=5)

    # Cleanup
    CurriculumService.delete_problem_type(pt_id)


def test_get_due_problem_types():
    """Verify querying due problem types for a specific date."""
    concepts = CurriculumService.get_concepts_by_lesson("bai-02")
    c_id = concepts[0]["id"]
    pt_id = CurriculumService.add_custom_problem_type(
        concept_id=c_id,
        title="Dạng toán kiểm thử hạn SRS",
        difficulty="Cơ bản"
    )

    test_date = date(2026, 10, 5)

    # Record practice with hinted (due next day: 2026-10-06)
    PracticeService.record_practice(
        problem_type_id=pt_id,
        practice_date=test_date,
        mastery_level=MasteryLevel.HINTED
    )

    # On test_date (2026-10-05), it is not due yet
    due_today = PracticeService.get_due_problem_types(current_date=test_date)
    due_ids = [d["id"] for d in due_today]
    assert pt_id not in due_ids

    # On next day (2026-10-06), it is DUE!
    due_tomorrow = PracticeService.get_due_problem_types(current_date=test_date + timedelta(days=1))
    due_ids_tomorrow = [d["id"] for d in due_tomorrow]
    assert pt_id in due_ids_tomorrow

    # Cleanup
    CurriculumService.delete_problem_type(pt_id)


def test_save_snapshot_image():
    """Verify snapshot image compression and saving."""
    img = Image.new("RGB", (2000, 2000), color="blue")
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    filename = PracticeService.save_snapshot_image(buf, "test_prob")
    assert filename is not None
    assert filename.endswith(".jpg")

    saved_file = Path("data/uploads") / filename
    assert saved_file.exists()
    assert saved_file.stat().st_size > 0

    # Ensure it was resized within MAX_IMAGE_DIMENSION
    with Image.open(saved_file) as saved_img:
        assert max(saved_img.size) <= 1600

    # Cleanup test image
    saved_file.unlink(missing_ok=True)


def test_delete_problem_type():
    """Verify deleting a problem type removes it and cascades properly."""
    concepts = CurriculumService.get_concepts_by_lesson("bai-01")
    c_id = concepts[0]["id"]

    # 1. Create a custom problem type
    pt_id = CurriculumService.add_custom_problem_type(
        concept_id=c_id,
        title="Dạng toán cần xóa thử nghiệm",
        method="Phương pháp thử nghiệm",
        difficulty="Cơ bản"
    )
    assert pt_id is not None
    assert CurriculumService.get_problem_type_by_id(pt_id) is not None

    # 2. Record a practice for it (which creates record and srs_item)
    PracticeService.record_practice(
        problem_type_id=pt_id,
        practice_date=date.today(),
        mastery_level=MasteryLevel.INDEPENDENT,
        notes="Thử nghiệm xóa"
    )

    # Verify srs item exists
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM srs_items WHERE problem_type_id = ?", (pt_id,))
    assert c.fetchone() is not None
    c.execute("SELECT * FROM practice_records WHERE problem_type_id = ?", (pt_id,))
    assert len(c.fetchall()) > 0
    conn.close()

    # 3. Delete the problem type
    deleted = CurriculumService.delete_problem_type(pt_id)
    assert deleted is True

    # 4. Verify problem type is gone
    assert CurriculumService.get_problem_type_by_id(pt_id) is None

    # 5. Verify cascade deleted srs_items and practice_records
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM srs_items WHERE problem_type_id = ?", (pt_id,))
    assert c.fetchone() is None
    c.execute("SELECT * FROM practice_records WHERE problem_type_id = ?", (pt_id,))
    assert len(c.fetchall()) == 0
    conn.close()

