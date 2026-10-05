"""Curriculum map and problem type management view."""

import streamlit as st
from datetime import date
from src.services import CurriculumService, PracticeService
from src.srs_engine import SRSEngine


def render_curriculum_view():
    """Render the curriculum tree and problem type browser."""
    st.title("🗺️ Bản Đồ Kiến Thức Toán 6 (KNTT)")
    st.caption("Tra cứu toàn bộ cây tri thức 9 chương, lý thuyết trọng tâm và các dạng toán nâng cao.")

    # 1. Volume selection
    vol_option = st.radio(
        "Chọn Tập sách:",
        options=[0, 1, 2],
        format_func=lambda v: "Toàn bộ chương trình (Tập 1 & Tập 2)" if v == 0 else f"Toán 6 - Tập {v}",
        horizontal=True
    )
    volume_filter = None if vol_option == 0 else vol_option

    chapters = CurriculumService.get_chapters(volume=volume_filter)

    # 2. Select Chapter and Lesson
    col_ch, col_less = st.columns([1, 1])
    with col_ch:
        ch_names = {f"Tập {c['volume']} - Chương {c['code']}: {c['title']}": c["id"] for c in chapters}
        selected_ch_name = st.selectbox("1. Chọn Chương:", options=list(ch_names.keys()))
        selected_ch_id = ch_names[selected_ch_name]

    lessons = CurriculumService.get_lessons_by_chapter(selected_ch_id)
    with col_less:
        lesson_names = {f"{l['title']} (Trang {l.get('pages', '')})": l["id"] for l in lessons}
        selected_lesson_name = st.selectbox("2. Chọn Bài học:", options=list(lesson_names.keys()))
        selected_lesson_id = lesson_names[selected_lesson_name]

    st.markdown("---")

    # 3. Lesson details and Concepts
    concepts = CurriculumService.get_concepts_by_lesson(selected_lesson_id)
    if not concepts:
        st.warning("Chưa có thông tin khái niệm cho bài học này.")
        return

    main_concept = concepts[0]

    with st.container(border=True):
        st.subheader(f"📖 {selected_lesson_name}")
        st.markdown(f"**Lý thuyết & Trọng tâm kiến thức:**")
        st.info(main_concept["summary"])
        if main_concept.get("example"):
            st.markdown(f"📌 **Ví dụ minh họa SGK:** `{main_concept['example']}`")

    # 4. Problem Types list
    st.subheader("📝 Các Dạng Toán Đã Thiết Lập Cho Bài Này")
    prob_types = CurriculumService.get_problem_types_by_concept(main_concept["id"])

    if not prob_types:
        st.info("Chưa có dạng toán nào được tạo cho bài học này. Hãy thêm dạng toán bên dưới!")
    else:
        for idx, pt in enumerate(prob_types):
            with st.container(border=True):
                c_detail, c_status, c_act = st.columns([3, 1.5, 1.2])

                with c_detail:
                    custom_tag = " `[Tự thêm]`" if pt.get("is_custom") else ""
                    st.markdown(f"#### {idx+1}. {pt['title']}{custom_tag}")
                    st.markdown(f"**Độ khó:** `{pt.get('difficulty', 'Nâng cao')}`")
                    if pt.get("method"):
                        st.markdown(f"💡 **Phương pháp / Mẹo giải:** {pt['method']}")

                    # Display problem type reference snapshot image if available
                    if pt.get("image_path"):
                        from config import UPLOADS_DIR
                        img_ref = UPLOADS_DIR / pt["image_path"]
                        if img_ref.exists():
                            with st.expander("📸 Xem ảnh đề bài / công thức mẫu", expanded=False):
                                st.image(str(img_ref), caption=f"Đề bài/Công thức: {pt['title']}", use_container_width=True)

                with c_status:
                    next_rev = pt.get("next_review")
                    if next_rev:
                        badge, cat = SRSEngine.get_urgency_badge(date.fromisoformat(next_rev))
                        st.markdown(f"**Hạn ôn tập:** {badge}")
                        st.caption(f"Lần làm gần nhất: {pt.get('last_practiced')}")
                        st.caption(f"Số lần độc lập: {pt.get('repetitions', 0)}")
                    else:
                        st.markdown("**Hạn ôn tập:** ⚪ *Chưa làm bài nào*")

                with c_act:
                    st.write("")
                    if st.button("✍️ Ghi nhận bài", key=f"curric_btn_{pt['id']}", use_container_width=True, type="primary"):
                        st.session_state["selected_problem_id"] = pt["id"]
                        st.session_state["current_page"] = "✍️ Ghi Nhận Luyện Tập"
                        st.rerun()

    # 5. Add Custom Problem Type (Supports Camera, File Upload, and Text)
    with st.expander("➕ Thêm Dạng Toán Mới Cho Bài Học Này (Hỗ Trợ Chụp Ảnh / Camera / Upload)", expanded=False):
        st.markdown(f"### Thêm dạng bài mới vào **{selected_lesson_name}**")
        st.caption("Anh có thể chụp ảnh trực tiếp từ sách, tải ảnh đề bài từ máy, hoặc gõ văn bản.")

        pt_input_mode = st.radio(
            "Hình thức nhập dạng toán:",
            options=["camera", "upload", "text_only"],
            format_func=lambda x: "📷 Chụp trực tiếp bằng Camera / Webcam" if x == "camera" else ("📁 Tải file ảnh chụp đề bài từ máy tính/điện thoại" if x == "upload" else "✍️ Chỉ nhập bằng chữ (Không kèm ảnh)"),
            horizontal=True,
            key=f"mode_pt_{main_concept['id']}"
        )

        pt_image_data = None
        if pt_input_mode == "camera":
            pt_image_data = st.camera_input("Chụp ảnh đề bài / công thức mẫu từ sách hoặc tài liệu:", key=f"cam_add_{main_concept['id']}")
        elif pt_input_mode == "upload":
            pt_image_data = st.file_uploader("Chọn file ảnh đề bài (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg", "webp"], key=f"upload_add_{main_concept['id']}")

        if pt_image_data:
            st.image(pt_image_data, caption="Xem trước ảnh đề bài mẫu", use_container_width=True)

        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            new_title = st.text_input(
                "Tên dạng toán:",
                placeholder="Ví dụ: Bài toán chia hết chứa ẩn ở số mũ (hoặc để trống nếu đã có ảnh)",
                key=f"title_add_{main_concept['id']}"
            )
            new_method = st.text_area(
                "Phương pháp giải / Gợi ý cách làm (tùy chọn):",
                placeholder="Ví dụ: Đặt thừa số chung, áp dụng hằng đẳng thức hoặc xét số dư...",
                key=f"method_add_{main_concept['id']}"
            )
        with col_f2:
            new_difficulty = st.selectbox(
                "Mức độ khó:",
                ["Nâng cao", "Vận dụng cao", "Cơ bản"],
                key=f"diff_add_{main_concept['id']}"
            )

        if st.button("💾 Lưu Dạng Toán Mới Này", type="primary", use_container_width=True, key=f"save_btn_pt_{main_concept['id']}"):
            if not new_title.strip() and not pt_image_data:
                st.error("Vui lòng nhập tên dạng toán hoặc chụp/tải ảnh đề bài lên!")
            else:
                final_title = new_title.strip()
                if not final_title:
                    import datetime
                    final_title = f"Dạng toán ảnh chụp - {selected_lesson_name} ({datetime.date.today().strftime('%d/%m')})"

                saved_pt_img = None
                if pt_image_data:
                    saved_pt_img = PracticeService.save_snapshot_image(pt_image_data, f"pt_ref_{main_concept['id']}")

                new_id = CurriculumService.add_custom_problem_type(
                    concept_id=main_concept["id"],
                    title=final_title,
                    method=new_method,
                    difficulty=new_difficulty,
                    image_path=saved_pt_img
                )
                st.balloons()
                st.success(f"🎉 Đã thêm thành công dạng toán: **{final_title}**!")
                st.rerun()
