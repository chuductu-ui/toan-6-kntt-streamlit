"""Spaced Repetition Review Station view."""

import streamlit as st
from datetime import date
from pathlib import Path
from src.services import PracticeService, CurriculumService
from src.models import MasteryLevel
from src.srs_engine import SRSEngine
from config import UPLOADS_DIR


def render_review_view():
    """Render the SRS review station."""
    today = date.today()
    st.title("🔄 Phòng Ôn Tập Spaced Repetition")
    st.caption("Ôn tập đúng thời điểm ngắt quãng để kiến thức được khắc sâu vào trí nhớ dài hạn.")

    # Check if a specific problem was targeted from Dashboard
    target_pid = st.session_state.get("selected_problem_id")

    # Filter selector
    filter_mode = st.radio(
        "Chế độ hiển thị danh sách ôn tập:",
        options=["due", "upcoming", "all"],
        format_func=lambda x: "🔥 Các bài đến hạn hôm nay / Quá hạn" if x == "due" else ("📅 Các bài sắp đến hạn (trong 3 ngày tới)" if x == "upcoming" else "📚 Tất cả các dạng toán đã kích hoạt SRS"),
        horizontal=True
    )

    if filter_mode == "due":
        items = PracticeService.get_due_problem_types(current_date=today)
        title_section = f"Danh sách các dạng toán cần ôn lại hôm nay ({len(items)} bài)"
    elif filter_mode == "upcoming":
        items = PracticeService.get_upcoming_problem_types(days_ahead=3, current_date=today)
        title_section = f"Danh sách các dạng toán sắp đến hạn ({len(items)} bài)"
    else:
        # All items that have SRS
        conn = PracticeService.get_connection() if hasattr(PracticeService, "get_connection") else None
        # Use service query
        items = PracticeService.get_due_problem_types(current_date=date(2099, 1, 1))
        title_section = f"Toàn bộ các dạng toán đang theo dõi SRS ({len(items)} bài)"

    # If target_pid is specified, highlight or move to top
    if target_pid:
        target_item = CurriculumService.get_problem_type_by_id(target_pid)
        if target_item:
            st.info(f"🎯 Bạn đang tập trung vào dạng toán: **{target_item['title']}** ({target_item['lesson_title']})")
            if target_item["id"] not in [it["id"] for it in items]:
                items = [target_item] + items

    st.subheader(title_section)

    if not items:
        st.success("🎉 Hiện tại không có bài nào trong danh sách này! Con đã hoàn thành xuất sắc các bài ôn tập.", icon="🏆")
        return

    for idx, item in enumerate(items):
        item_id = item["id"]
        is_highlighted = (item_id == target_pid)

        with st.container(border=True):
            col_info, col_actions = st.columns([3.5, 1.5])

            with col_info:
                st.markdown(f"### {idx+1}. {item.get('problem_title', item.get('title'))}")
                st.caption(
                    f"📖 {item.get('lesson_title')} | {item.get('chapter_title', '')} | Độ khó: `{item.get('difficulty', 'Nâng cao')}`"
                )

                # Status and schedule
                next_rev = item.get("next_review")
                if next_rev:
                    badge, cat = SRSEngine.get_urgency_badge(date.fromisoformat(str(next_rev)))
                    st.markdown(f"**Tình trạng:** {badge} | Lần tự làm liên tiếp: **{item.get('repetitions', 0)} lần**")

                # Expandable Hints (Hidden by default so daughter tries on her own first!)
                with st.expander("💡 Bấm để xem Phương pháp / Công thức gợi ý", expanded=False):
                    st.markdown(item.get("method") or "Chưa có gợi ý.")

                # Reference image of problem type
                if item.get("image_path"):
                    ref_img = UPLOADS_DIR / item["image_path"]
                    if ref_img.exists():
                        with st.expander("📸 Xem ảnh đề bài / công thức gốc", expanded=False):
                            st.image(str(ref_img), caption="Đề bài gốc của dạng toán", use_container_width=True)

                # View past snapshot images
                history = PracticeService.get_practice_history(problem_type_id=item_id, limit=3)
                images = [h for h in history if h.get("image_path")]
                if images:
                    with st.expander(f"📸 Xem lại ảnh bài làm lần trước của con ({len(images)} ảnh)", expanded=False):
                        for img_rec in images:
                            img_file = UPLOADS_DIR / img_rec["image_path"]
                            if img_file.exists():
                                st.image(
                                    str(img_file),
                                    caption=f"Lần làm ngày {img_rec['practice_date']} ({'Tự làm' if img_rec['mastery_level'] == 'INDEPENDENT' else 'Cần gợi ý'}) - {img_rec.get('notes', '')}",
                                    use_container_width=True
                                )

            with col_actions:
                st.markdown("**Kết quả ôn tập hôm nay:**")

                # Quick Independent button
                if st.button("🟢 Con tự làm được!", key=f"rev_indep_{item_id}_{idx}", use_container_width=True, type="primary"):
                    res = PracticeService.record_practice(
                        problem_type_id=item_id,
                        practice_date=today,
                        mastery_level=MasteryLevel.INDEPENDENT,
                        notes="Ôn tập nhanh tại phòng SRS: Con tự giải được độc lập."
                    )
                    st.toast(f"Xuất sắc! Lần ôn tiếp theo vào ngày {res['next_review'].strftime('%d/%m/%Y')} (sau {res['interval_days']} ngày)")
                    if target_pid == item_id:
                        del st.session_state["selected_problem_id"]
                    st.rerun()

                # Quick Hinted button
                if st.button("🟡 Vẫn cần bố gợi ý", key=f"rev_hint_{item_id}_{idx}", use_container_width=True):
                    res = PracticeService.record_practice(
                        problem_type_id=item_id,
                        practice_date=today,
                        mastery_level=MasteryLevel.HINTED,
                        notes="Ôn tập nhanh tại phòng SRS: Con còn vướng mắc, cần gợi ý."
                    )
                    st.toast(f"Đã lưu! Hệ thống sẽ nhắc hai bố con rà soát lại vào ngày mai ({res['next_review'].strftime('%d/%m/%Y')})")
                    if target_pid == item_id:
                        del st.session_state["selected_problem_id"]
                    st.rerun()

                # Detailed practice entry with camera/upload
                if st.button("📷 Chụp ảnh bài mới", key=f"rev_cam_{item_id}_{idx}", use_container_width=True):
                    st.session_state["selected_problem_id"] = item_id
                    st.session_state["current_page"] = "✍️ Ghi Nhận Luyện Tập"
                    st.rerun()
