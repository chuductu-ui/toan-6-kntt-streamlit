"""Configuration module for Toan 6 KNTT Streamlit platform."""

from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = DATA_DIR / "uploads"
DB_PATH = DATA_DIR / "math6.db"

# Ensure directories exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# App branding and metadata
APP_TITLE = "Vườn Toán Lớp 6 - Học Cùng Con"
APP_SUBTITLE = "Hệ thống theo dõi kiến thức Toán 6 & Lặp lại ngắt quãng (Spaced Repetition)"
APP_URL = "https://toan-6-kntt-app.streamlit.app"

# SRS Default Parameters
DEFAULT_EASE_FACTOR = 2.5
MIN_EASE_FACTOR = 1.3
MAX_EASE_FACTOR = 3.0

# Intervals for initial repetitions (days)
SRS_INTERVALS = {
    0: 1,   # 1st independent success: 1 day
    1: 3,   # 2nd independent success: 3 days
    2: 7,   # 3rd independent success: 7 days
}

# Image upload settings
MAX_IMAGE_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]
MAX_IMAGE_DIMENSION = 1600  # Resize large images to save space
