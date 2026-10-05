"""History view: chronological learning journey, snapshot gallery, and detailed notes."""

import streamlit as st
from pathlib import Path
from src.services import PracticeService
from config import UPLOADS_DIR


def render_history_view():
    """Render the learning history and snapshot gallery."""
    st.title("📜 Nhật Ký & Tiến Bộ Học Tập Của Con")
    st.caption("Xem lại dòng thời gian các buổi học, những bài con đã tự làm được và ảnh chụp bài giải.")

    records = PracticeService.get_practice_history(limit=100)

    if not records:
        st.info("Chưa có lượt làm bài nào được ghi nhận. Hãy bắt đầu ghi bài tập đầu tiên ở mục '✍️ Ghi Nhận Luyện Tập'!")
        return

    # Filter options
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        filter_status = st.selectbox(
            "Lọc theo kết quả làm bài:",
            options=["ALL", "INDEPENDENT", "HINTED"],
            format_func=lambda x: "Tất cả các lượt làm" if x == "ALL" else ("🟢 Con tự làm được" if x == "INDEPENDENT" else "🟡 Cần bố gợi ý")
        )
    with col_f2:
        has_image_only = st.checkbox("Chỉ hiển thị các bài có kèm ảnh chụp snapshot", value=False)

    filtered_records = records
    if filter_status != "ALL":
        filtered_records = [r for r in filtered_records if r["mastery_level"] == filter_status]
    if has_image_only:
        filtered_records = [r for r in filtered_records if r.get("image_path")]

    st.markdown(f"**Tổng số lượt hiển thị: {len(filtered_records)} lượt**")

    for rec in filtered_records:
        with st.container(border=True):
            col_main, col_media = st.columns([3, 2])

            with col_main:
                is_indep = (rec["mastery_level"] == "INDEPENDENT")
                status_badge = "🟢 **Tự làm được**" if is_indep else "🟡 **Cần gợi ý**"

                st.markdown(f"#### {rec['problem_title']}")
                st.markdown(f"📅 **Ngày làm:** {rec['practice_date']} | Đánh giá: {status_badge}")
                st.caption(f"Bài: {rec['lesson_title']} ({rec['chapter_title']})")

                if rec.get("notes"):
                    st.markdown(f"📝 **Ghi chú của bố:** {rec['notes']}")

            with col_media:
                img_name = rec.get("image_path")
                if img_name:
                    img_file = UPLOADS_DIR / img_name
                    if img_file.exists():
                        st.image(str(img_file), caption=f"Ảnh bài làm - {rec['practice_date']}", use_container_width=True)
                    else:
                        st.caption("Ảnh đã lưu nhưng không tìm thấy file.")
                else:
                    st.caption("*(Không có ảnh snapshot đính kèm)*")
