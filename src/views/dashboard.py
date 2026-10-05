"""Dashboard view: central command hub displaying SRS metrics, due problem types, and 1-click navigation."""

import streamlit as st
from datetime import date
from src.services import PracticeService, CurriculumService
from src.srs_engine import SRSEngine


def render_dashboard():
    """Render the main dashboard."""
    today = date.today()
    stats = PracticeService.get_dashboard_stats(current_date=today)
    due_items = PracticeService.get_due_problem_types(current_date=today)
    upcoming_items = PracticeService.get_upcoming_problem_types(days_ahead=3, current_date=today)

    st.title("🏠 Bảng Điều Khiển - Học Toán Cùng Con")
    st.caption(f"Hôm nay là: **{today.strftime('Ngày %d tháng %m năm %Y')}** | Lớp 6 - Kết nối tri thức với cuộc sống")

    # 1. Prominent Notification Banner
    due_count = stats["due_today_count"]
    if due_count > 0:
        st.error(
            f"🔔 **Hôm nay có {due_count} dạng toán cần con ôn tập lại theo phương pháp Spaced Repetition!** "
            "Nhấp vào nút **'Ôn tập ngay'** bên dưới để mở thẳng dạng bài cần luyện tập.",
            icon="🔥"
        )
    else:
        st.success(
            "🎉 **Tuyệt vời! Hiện không có dạng toán nào bị quá hạn hôm nay.** "
            "Hai bố con có thể khám phá dạng toán mới hoặc ôn tập trước các bài sắp đến hạn!",
            icon="✨"
        )

    # 2. Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(
            label="🎯 Cần ôn hôm nay",
            value=f"{due_count} bài",
            delta=f"-{due_count} bài cần giải quyết" if due_count > 0 else "Đã xong",
            delta_color="inverse" if due_count > 0 else "normal"
        )
    with col2:
        st.metric(
            label="📚 Tổng số dạng toán",
            value=f"{stats['total_problems']} dạng",
            help="Bao gồm các dạng toán nâng cao sẵn có và dạng tự thêm"
        )
    with col3:
        total_p = stats["total_practices"]
        indep_pct = round((stats["independent_count"] / total_p * 100), 1) if total_p > 0 else 0
        st.metric(
            label="🌟 Tỉ lệ tự làm được",
            value=f"{indep_pct}%",
            delta=f"{stats['independent_count']}/{total_p} lượt làm"
        )
    with col4:
        st.metric(
            label="🏆 Đã nắm rất vững (Mastered)",
            value=f"{stats['mastered_count']} dạng",
            help="Các dạng bài con đã tự làm đúng từ 4 lần liên tiếp trở lên"
        )

    st.markdown("---")

    # 3. INTERACTIVE TABLE: DUE FOR REVIEW TODAY (With 1-Click Jump)
    st.subheader("🔥 Danh Sách Các Dạng Bài Cần Ôn Tập Hôm Nay")
    if not due_items:
        st.info("Chưa có dạng bài nào đến hạn ôn tập hôm nay. Hai bố con hãy vào mục '✍️ Ghi Nhận Luyện Tập' để ghi chép bài học mới nhé!")
    else:
        for idx, item in enumerate(due_items):
            with st.container(border=True):
                c_info, c_action = st.columns([4, 1])
                with c_info:
                    days_overdue = int(item.get("days_overdue", 0))
                    if days_overdue > 0:
                        urgency_badge = f":red[🔴 Quá hạn {days_overdue} ngày]"
                    else:
                        urgency_badge = ":orange[🟠 Đến hạn hôm nay]"

                    st.markdown(
                        f"**{item['problem_title']}** {urgency_badge} `Độ khó: {item['difficulty']}`"
                    )
                    st.caption(
                        f"📖 {item['lesson_title']} ({item['chapter_title']}) | "
                        f"Lần làm gần nhất: {item['last_practiced']} | Lần tự làm liên tiếp: {item['repetitions']}"
                    )
                    if item.get("method"):
                        st.markdown(f"💡 *Gợi ý phương pháp*: {item['method']}")

                with c_action:
                    st.write("")
                    # ONE-CLICK DIRECT NAVIGATION BUTTON
                    if st.button("🎯 Ôn tập ngay", key=f"btn_due_{item['id']}_{idx}", use_container_width=True, type="primary"):
                        st.session_state["selected_problem_id"] = item["id"]
                        st.session_state["current_page"] = "🔄 Phòng Ôn Tập SRS"
                        st.rerun()

    st.markdown("---")

    # 4. UPCOMING REVIEWS (Next 3 days)
    with st.expander(f"📅 Các dạng bài sắp đến hạn ôn tập trong 3 ngày tới ({len(upcoming_items)} dạng)", expanded=False):
        if not upcoming_items:
            st.write("Không có bài nào sắp đến hạn trong 3 ngày tới.")
        else:
            for up in upcoming_items:
                c1, c2 = st.columns([4, 1])
                with c1:
                    days = int(up.get("days_ahead", 1))
                    st.markdown(f"• **{up['problem_title']}** (Sau {days} ngày nữa - {up['next_review']})")
                    st.caption(f"{up['lesson_title']} | Lần tự làm liên tiếp: {up['repetitions']}")
                with c2:
                    if st.button("Làm sớm", key=f"btn_up_{up['id']}", use_container_width=True):
                        st.session_state["selected_problem_id"] = up["id"]
                        st.session_state["current_page"] = "🔄 Phòng Ôn Tập SRS"
                        st.rerun()

    # 5. PROGRESS OVERVIEW BY CHAPTER
    with st.expander("📊 Thống Kê Tiến Độ Theo Toàn Bộ 9 Chương Toán 6", expanded=False):
        chapters = CurriculumService.get_chapters()
        for ch in chapters:
            lessons = CurriculumService.get_lessons_by_chapter(ch["id"])
            st.markdown(f"**Tập {ch['volume']} - Chương {ch['code']}: {ch['title']}** ({len(lessons)} bài học)")
