"""Main Streamlit Application: Vườn Toán Lớp 6 - Học Cùng Con."""

import streamlit as st
from datetime import date

# 1. Page Configuration (Wide layout, responsive for desktop & tablet)
st.set_page_config(
    page_title="Vườn Toán Lớp 6 - Học Cùng Con",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Database Auto-Initialization & Seeding Check
from src.database import init_db
from src.seed_data import seed_database
from src.services import PracticeService, CurriculumService

# Check and sync from Google Drive if on Streamlit Cloud
try:
    from src.gdrive_sync import GDriveSync, is_gdrive_configured
    if is_gdrive_configured():
        GDriveSync.download_db_from_gdrive()
except Exception as e:
    print(f"GDrive initial sync check: {e}")

init_db()
# Auto-seed if database is empty
stats_check = PracticeService.get_dashboard_stats()
if stats_check["total_problems"] == 0:
    seed_database()

# 3. View Imports
from src.views import (
    render_dashboard,
    render_curriculum_view,
    render_practice_view,
    render_review_view,
    render_history_view
)

# 4. Session State Management
NAV_DASHBOARD = "🏠 Trang Chủ / Dashboard"
NAV_REVIEW = "🔄 Phòng Ôn Tập SRS"
NAV_PRACTICE = "✍️ Ghi Nhận Luyện Tập"
NAV_CURRICULUM = "🗺️ Bản Đồ Tri Thức"
NAV_HISTORY = "📜 Lịch Sử & Tiến Bộ"

PAGES = [NAV_DASHBOARD, NAV_REVIEW, NAV_PRACTICE, NAV_CURRICULUM, NAV_HISTORY]

if "current_page" not in st.session_state:
    st.session_state["current_page"] = NAV_DASHBOARD

# 5. Sidebar Navigation & Badges
with st.sidebar:
    st.markdown("## 📐 Vườn Toán Lớp 6")
    st.markdown("*Đồng hành cùng con chinh phục Toán 6 KNTT*")
    st.markdown("---")

    # Dynamic badge for due items
    today = date.today()
    due_count = PracticeService.get_dashboard_stats(current_date=today)["due_today_count"]
    review_label = f"🔄 Phòng Ôn Tập SRS ({due_count} bài)" if due_count > 0 else "🔄 Phòng Ôn Tập SRS"

    nav_map = {
        NAV_DASHBOARD: NAV_DASHBOARD,
        NAV_REVIEW: review_label,
        NAV_PRACTICE: NAV_PRACTICE,
        NAV_CURRICULUM: NAV_CURRICULUM,
        NAV_HISTORY: NAV_HISTORY
    }

    # Reverse lookup to keep current_page synchronized
    current_selection = st.session_state["current_page"]
    selected_page_key = st.radio(
        "Menu chức năng chính:",
        options=PAGES,
        format_func=lambda p: nav_map[p],
        index=PAGES.index(current_selection) if current_selection in PAGES else 0
    )

    # Sync selection back to state
    if selected_page_key != st.session_state["current_page"]:
        st.session_state["current_page"] = selected_page_key
        st.rerun()

    st.markdown("---")

    # Spaced Repetition Reference Card in Sidebar
    with st.expander("ℹ️ Về Phương Pháp Spaced Repetition", expanded=False):
        st.markdown("""
        **Lặp lại ngắt quãng (SRS):**
        - **🟢 Tự làm được**: Tăng khoảng cách ôn tập (1 ngày $\\rightarrow$ 3 ngày $\\rightarrow$ 7 ngày $\\rightarrow$ 14 ngày $\\rightarrow$ 30 ngày...).
        - **🟡 Cần gợi ý**: Reset về 1 ngày (nhắc làm lại ngay hôm sau).
        
        *Mục tiêu: Đưa kiến thức vào vùng trí nhớ dài hạn bền vững.*
        """)

    # Mobile Access QR Code & Link
    with st.expander("📱 Mở Trên Điện Thoại / iPad (Online 24/7)", expanded=True):
        from config import APP_URL
        st.markdown("**Quét mã QR để mở ngay ứng dụng:**")
        try:
            import io
            import qrcode
            qr = qrcode.QRCode(box_size=4, border=2)
            qr.add_data(APP_URL)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Quét bằng Camera iPhone/iPad", width=200)
        except Exception as e:
            pass
        st.markdown(f"👉 **Link trực tiếp:** [{APP_URL}]({APP_URL})")
        st.caption("*(Truy cập mượt mà trên mọi thiết bị và mạng 4G/5G/Wi-Fi mọi lúc mọi nơi)*")

    st.caption("👨‍👧 Dành cho bố Chu Đức Tú & Con gái")
    st.caption("Bộ sách: Kết nối tri thức với cuộc sống")

# 6. Render Active View
page = st.session_state["current_page"]
if page == NAV_DASHBOARD:
    render_dashboard()
elif page == NAV_REVIEW:
    render_review_view()
elif page == NAV_PRACTICE:
    render_practice_view()
elif page == NAV_CURRICULUM:
    render_curriculum_view()
elif page == NAV_HISTORY:
    render_history_view()
