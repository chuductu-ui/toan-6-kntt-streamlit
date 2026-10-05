"""Database management module using SQLite."""

import sqlite3
from pathlib import Path
from typing import Optional
from config import DB_PATH, DATA_DIR, UPLOADS_DIR


def get_connection(db_path: Optional[Path] = None) -> sqlite3.Connection:
    """Get SQLite database connection with row factory enabled."""
    target_path = db_path or DB_PATH
    target_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: Optional[Path] = None) -> None:
    """Initialize database tables and indexes."""
    conn = get_connection(db_path)
    cursor = conn.cursor()

    # Table 1: Chapters (Các chương trong SGK Toán 6 Tập 1 & 2)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chapters (
        id TEXT PRIMARY KEY,
        volume INTEGER NOT NULL,
        code TEXT NOT NULL,
        title TEXT NOT NULL,
        order_num INTEGER NOT NULL
    );
    """)

    # Table 2: Lessons (Các bài học trong chương)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lessons (
        id TEXT PRIMARY KEY,
        chapter_id TEXT NOT NULL,
        title TEXT NOT NULL,
        pages TEXT,
        order_num INTEGER NOT NULL,
        kind TEXT DEFAULT 'lesson',
        FOREIGN KEY (chapter_id) REFERENCES chapters(id) ON DELETE CASCADE
    );
    """)

    # Table 3: Concepts (Các trọng tâm kiến thức / lý thuyết)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS concepts (
        id TEXT PRIMARY KEY,
        lesson_id TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        example TEXT,
        order_num INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE
    );
    """)

    # Table 4: Problem Types (Các dạng toán cụ thể của từng kiến thức)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problem_types (
        id TEXT PRIMARY KEY,
        concept_id TEXT NOT NULL,
        title TEXT NOT NULL,
        method TEXT,
        difficulty TEXT DEFAULT 'Nâng cao',
        is_custom INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (concept_id) REFERENCES concepts(id) ON DELETE CASCADE
    );
    """)

    # Table 5: Practice Records (Lịch sử từng lần con làm bài)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS practice_records (
        id TEXT PRIMARY KEY,
        problem_type_id TEXT NOT NULL,
        practice_date DATE NOT NULL,
        mastery_level TEXT NOT NULL, -- 'INDEPENDENT' or 'HINTED'
        image_path TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (problem_type_id) REFERENCES problem_types(id) ON DELETE CASCADE
    );
    """)

    # Table 6: SRS Items (Trạng thái lặp lại ngắt quãng hiện tại của từng Dạng toán)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS srs_items (
        problem_type_id TEXT PRIMARY KEY,
        interval_days INTEGER NOT NULL DEFAULT 1,
        repetitions INTEGER NOT NULL DEFAULT 0,
        ease_factor REAL NOT NULL DEFAULT 2.5,
        last_practiced DATE NOT NULL,
        next_review DATE NOT NULL,
        status TEXT NOT NULL DEFAULT 'LEARNING',
        FOREIGN KEY (problem_type_id) REFERENCES problem_types(id) ON DELETE CASCADE
    );
    """)

    # Create Indexes for fast querying
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_lessons_chapter ON lessons(chapter_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_concepts_lesson ON concepts(lesson_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_problem_types_concept ON problem_types(concept_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_practice_problem ON practice_records(problem_type_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_srs_next_review ON srs_items(next_review);")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
