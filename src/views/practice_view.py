"""Practice entry view: record exercise attempts, upload/camera snapshots, and evaluate mastery."""

import streamlit as st
from datetime import date
from pathlib import Path
from src.services import CurriculumService, PracticeService
from src.models import MasteryLevel
from src.srs_engine import SRSEngine
from config import UPLOADS_DIR


def render_practice_view():
    """Render the practice recording and snapshot interface."""
    st.title("✍️ Ghi Nhận Bài Tập Của Con")
    st.caption("Lưu lại hình ảnh bài làm thực tế, đánh giá mức độ tự chủ và kích hoạt thuật toán nhắc lịch.")

    # 1. Determine Selected Problem Type
    selected_pt_id = st.session_state.get("selected_problem_id")

    # Cascaded Selectors
    chapters = CurriculumService.get_chapters()
    ch_options = {f"Tập {c['volume']} - Chương {c['code']}: {c['title']}": c["id"] for c in chapters}

    # If already selected, find chapter and lesson
    preselected_pt = None
    default_ch_idx = 0
    if selected_pt_id:
        preselected_pt = CurriculumService.get_problem_type_by_id(selected_pt_id)
        if preselected_pt:
            ch_target = f"Tập {preselected_pt['volume']} - Chương {preselected_pt['chapter_code']}: {preselected_pt['chapter_title']}"
            if ch_target in ch_options:
                default_ch_idx = list(ch_options.keys()).index(ch_target)

    c_ch, c_les, c_prob = st.columns([1.2, 1.2, 1.6])
    with c_ch:
        ch_name = st.selectbox("Chương:", options=list(ch_options.keys()), index=default_ch_idx)
        ch_id = ch_options[ch_name]

    lessons = CurriculumService.get_lessons_by_chapter(ch_id)
    les_options = {l["title"]: l["id"] for l in lessons}

    default_les_idx = 0
    if preselected_pt and preselected_pt["lesson_title"] in les_options:
        default_les_idx = list(les_options.keys()).index(preselected_pt["lesson_title"])

    with c_les:
        les_name = st.selectbox("Bài học:", options=list(les_options.keys()), index=default_les_idx)
        les_id = les_options[les_name]

    concepts = CurriculumService.get_concepts_by_lesson(les_id)
    concept_id = concepts[0]["id"] if concepts else None
    prob_types = CurriculumService.get_problem_types_by_concept(concept_id) if concept_id else []

    if not prob_types:
        st.warning("Bài học này chưa có dạng toán nào. Vui lòng vào mục '🗺️ Bản Đồ Tri Thức' để thêm dạng bài.")
        return

    pt_options = {f"{pt['title']} ({pt.get('difficulty', 'Nâng cao')})": pt["id"] for pt in prob_types}

    default_pt_idx = 0
    if preselected_pt and preselected_pt["id"] in [pt["id"] for pt in prob_types]:
        for idx, (label, pid) in enumerate(pt_options.items()):
            if pid == preselected_pt["id"]:
                default_pt_idx = idx
                break

    with c_prob:
        pt_name = st.selectbox("Dạng toán:", options=list(pt_options.keys()), index=default_pt_idx)
        active_pt_id = pt_options[pt_name]

    # Load full details of active problem type
    active_pt = CurriculumService.get_problem_type_by_id(active_pt_id)

    # 2. Display problem details & current SRS status card
    with st.container(border=True):
        col_t, col_s = st.columns([3, 1.5])
        with col_t:
            st.markdown(f"### 🎯 {active_pt['title']}")
            if active_pt.get("method"):
                st.markdown(f"💡 **Phương pháp / Gợi ý giải:** {active_pt['method']}")
            st.caption(f"Trực thuộc bài: {active_pt['lesson_title']} | Độ khó: {active_pt['difficulty']}")
        with col_s:
            next_rev = active_pt.get("next_review")
            if next_rev:
                badge, cat = SRSEngine.get_urgency_badge(date.fromisoformat(next_rev))
                st.markdown(f"**Tình trạng hiện tại:**\n{badge}")
                st.caption(f"Lần độc lập liên tiếp: **{active_pt.get('repetitions', 0)}**")
            else:
                st.markdown("**Tình trạng:** ⚪ *Chưa từng làm qua*")

    st.markdown("---")

    # 3. Practice Recording Form
    st.subheader("📝 Ghi Nhận Lượt Làm Bài Của Con")

    col_form1, col_form2 = st.columns([1, 1])

    with col_form1:
        # Date picker
        practice_date = st.date_input("Ngày làm bài:", value=date.today())

        # Mastery selection
        st.markdown("**Mức độ tự chủ của con khi làm dạng bài này:**")
        mastery_choice = st.radio(
            "Chọn kết quả:",
            options=["INDEPENDENT", "HINTED"],
            format_func=lambda x: "🟢 Con tự làm được độc lập (Hiểu bản chất, không cần nhắc)" if x == "INDEPENDENT" else "🟡 Cần bố gợi ý / hướng dẫn (Chưa tự làm được hoặc quên cách làm)",
            index=0
        )
        mastery_level = MasteryLevel.INDEPENDENT if mastery_choice == "INDEPENDENT" else MasteryLevel.HINTED

        # Notes
        notes = st.text_area(
            "Ghi chú của bố (điểm con làm tốt, lỗi sai cần lưu ý):",
            placeholder="Ví dụ: Con tính nhẩm tốt nhưng hay nhầm dấu ngoặc âm; cần chú ý bước quy đồng mẫu...",
            height=120
        )

    with col_form2:
        st.markdown("**📸 Hình ảnh / Snapshot bài làm của con:**")
        snapshot_method = st.radio(
            "Phương thức chụp/tải ảnh:",
            options=["upload", "camera"],
            format_func=lambda x: "📁 Tải file ảnh lên từ máy tính/điện thoại" if x == "upload" else "📷 Chụp trực tiếp bằng Webcam/Camera",
            horizontal=True
        )

        image_data = None
        if snapshot_method == "upload":
            image_data = st.file_uploader("Chọn ảnh bài tập/bài giải (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg", "webp"])
        else:
            image_data = st.camera_input("Chụp ảnh bài tập:")

        if image_data:
            st.image(image_data, caption="Xem trước hình ảnh snapshot", use_container_width=True)

    # 4. Save Button
    st.markdown("")
    if st.button("💾 Lưu Bài Làm & Tự Động Lên Lịch Ôn Tập (SRS)", type="primary", use_container_width=True):
        # Save snapshot image if provided
        saved_img_filename = None
        if image_data:
            saved_img_filename = PracticeService.save_snapshot_image(image_data, active_pt_id)

        # Record practice and calculate SRS
        result = PracticeService.record_practice(
            problem_type_id=active_pt_id,
            practice_date=practice_date,
            mastery_level=mastery_level,
            image_path=saved_img_filename,
            notes=notes
        )

        st.balloons()
        st.success("🎉 **Đã lưu thành công lượt làm bài của con!**")

        # Display SRS result card
        with st.container(border=True):
            r_c1, r_c2, r_c3 = st.columns(3)
            with r_c1:
                st.metric("📅 Lần nhắc ôn lại tiếp theo", f"{result['next_review'].strftime('%d/%m/%Y')}")
            with r_c2:
                st.metric("⏳ Khoảng cách nhắc lại", f"{result['interval_days']} ngày sau")
            with r_c3:
                st.metric("🔁 Số lần tự làm liên tiếp", f"{result['repetitions']} lần")

            if mastery_level == MasteryLevel.INDEPENDENT:
                st.info("🌟 Con đã tự làm được độc lập! Khoảng cách ôn tập đã được kéo dài để chuyển hóa thành trí nhớ dài hạn.")
            else:
                st.warning("💡 Vì con cần gợi ý, hệ thống đã xếp lịch nhắc hai bố con rà soát lại vào ngày mai!")

        # Reset selection state
        if "selected_problem_id" in st.session_state:
            del st.session_state["selected_problem_id"]
