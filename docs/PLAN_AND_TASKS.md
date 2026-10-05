# Kế Hoạch Triển Khai Kỹ Thuật (Technical Plan & Tasks)
# Nền Tảng Quản Lý Toán 6 KNTT & Spaced Repetition Trên Streamlit

## PHẦN 1: TECHNICAL IMPLEMENTATION PLAN (KẾ HOẠCH KỸ THUẬT)

### 1. Phân Tích Thành Phần & Phụ Thuộc (Components & Dependencies)
```mermaid
graph TD
    A[Curriculum Seed Data (Toán 6 KNTT Tập 1 + 2 + Dạng toán nâng cao)] --> B[Database Layer (SQLite & Schemas)]
    B --> C[SRS Engine (Thuật toán Spaced Repetition)]
    B --> D[Data Services & Storage (CRUD, Image Handler)]
    C --> D
    D --> E1[View: Dashboard & 1-Click Jump]
    D --> E2[View: Bản Đồ Tri Thức & Thêm Dạng Bài]
    D --> E3[View: Ghi Nhận Luyện Tập & Snapshot]
    D --> E4[View: Phòng Ôn Tập SRS & Lịch Sử]
    E1 & E2 & E3 & E4 --> F[App Main Entry: app.py]
```

### 2. Thứ Tự Triển Khai (Implementation Order)
1. **Module 1: Cấu hình & Cơ sở dữ liệu (`config.py`, `src/models.py`, `src/database.py`)**:
   - Định nghĩa schema SQLite, tự động khởi tạo thư mục `data/uploads/` và file database `data/math6.db`.
2. **Module 2: Thuật toán Spaced Repetition (`src/srs_engine.py`) & Unit Tests (`tests/test_srs.py`)**:
   - Viết logic SM-2 cải tiến theo TDD (Test-Driven Development).
   - Kiểm thử 100% các kịch bản: Tự làm liên tiếp, Cần gợi ý, Reset chu kỳ, Tính `next_review_date`.
3. **Module 3: Cây kiến thức Toán 6 & Dạng toán nâng cao nạp sẵn (`src/seed_data.py`)**:
   - Nạp toàn bộ 9 chương của Toán 6 KNTT (Tập 1: 5 chương, Tập 2: 4 chương).
   - Tích hợp sẵn các **dạng toán nâng cao điển hình** cho từng bài (Lũy thừa, Chia hết & đồng dư, Số nguyên, Dãy phân số quy luật, Bất đẳng thức phân số, Bài toán hình học thực tế, Xác suất...).
4. **Module 4: Data Service Layer (`src/services.py`) & Tests (`tests/test_db.py`)**:
   - Các hàm CRUD: nạp bài, ghi nhận kết quả làm bài, lưu và nén ảnh snapshot, truy vấn các dạng bài đến hạn hôm nay.
5. **Module 5: Giao diện Streamlit (`app.py`, `src/views/*`)**:
   - **Dashboard**: Card thống kê số bài đến hạn hôm nay, bảng danh sách kèm nút 1-click nhảy trực tiếp tới dạng bài ôn tập.
   - **Bản đồ tri thức**: Cây kiến thức trực quan, tra cứu lý thuyết & công thức, nút thêm dạng toán mới.
   - **Ghi nhận làm bài**: Chụp ảnh bằng camera hoặc upload file ảnh, chọn "Tự làm được" / "Cần gợi ý", lưu bài và tính SRS ngay lập tức.
   - **Phòng ôn tập & Lịch sử**: Rà soát các bài đến hạn, xem lại ảnh bài làm cũ, bấm cập nhật tiến độ ôn tập.
6. **Module 6: Tích hợp, Kiểm thử tổng thể & Tài liệu hướng dẫn sử dụng**.

---

## PHẦN 2: DANH SÁCH NHIỆM VỤ CHI TIẾT (TASK BREAKDOWN)

- [x] **Task 1: Thiết lập cấu hình và Schema Cơ sở dữ liệu SQLite**
  - **Mô tả**: Viết `config.py`, `src/models.py` và `src/database.py`. Tạo các bảng `chapters`, `lessons`, `concepts`, `problem_types`, `practice_records`, `srs_items`.
  - **Acceptance Criteria**: Database SQLite được khởi tạo đúng cấu trúc, tạo thư mục `data/uploads/` nếu chưa có.
  - **Verify**: Đã chạy test khởi tạo DB độc lập, kiểm tra schema bảng SQLite thành công.
  - **Files**: `config.py`, `src/models.py`, `src/database.py`.

- [x] **Task 2: Xây dựng SRS Engine và Bộ Unit Test**
  - **Mô tả**: Viết `src/srs_engine.py` và `tests/test_srs.py` kiểm thử thuật toán lặp lại ngắt quãng (chu kỳ 1, 3, 7, 14, 30, 60 ngày khi Tự làm được, reset về 1 ngày khi Cần gợi ý).
  - **Acceptance Criteria**: 100% tests trong `tests/test_srs.py` pass.
  - **Verify**: `pytest tests/test_srs.py -v` (6/6 tests passed).
  - **Files**: `src/srs_engine.py`, `tests/test_srs.py`.

- [x] **Task 3: Xây dựng bộ dữ liệu Cây tri thức Toán 6 KNTT & Dạng toán nâng cao**
  - **Mô tả**: Viết `src/seed_data.py` nạp đầy đủ chương trình Toán 6 KNTT (Tập 1: Chương I-V, Tập 2: Chương VI-IX) cùng các dạng toán nâng cao cốt lõi được định nghĩa sẵn cho từng bài.
  - **Acceptance Criteria**: Dữ liệu nạp đầy đủ vào SQLite: 9 chương, 43 bài học, 43 khái niệm trọng tâm và 54 dạng toán nâng cao sẵn có.
  - **Verify**: Lệnh `python -m src.seed_data` chạy thành công, nạp 9 chương, 43 bài, 54 dạng toán.
  - **Files**: `src/seed_data.py`.

- [x] **Task 4: Xây dựng Service Layer (Nghiệp vụ, Lưu ảnh Snapshot & DB Tests)**
  - **Mô tả**: Viết `src/services.py` cung cấp các hàm lấy dữ liệu, lưu snapshot ảnh (nén an toàn bằng Pillow), ghi log luyện tập, cập nhật SRS, truy vấn bài cần ôn hôm nay. Viết `tests/test_db.py`.
  - **Acceptance Criteria**: Đầy đủ các hàm CRUD và xử lý ảnh, test pass 100%.
  - **Verify**: `pytest tests/ -v` (11/11 tests passed).
  - **Files**: `src/services.py`, `tests/test_db.py`.

- [x] **Task 5: Xây dựng Bảng Dashboard & Điều Hướng 1 Chạm**
  - **Mô tả**: Viết `src/views/dashboard.py` hiển thị tổng quan tiến độ, số dạng toán đến hạn hôm nay, và bảng tương tác với nút chuyển trực tiếp tới dạng bài ôn tập.
  - **Acceptance Criteria**: Dashboard hiển thị rõ số lượng bài đến hạn; bấm nút ôn tập dạng bài sẽ chuyển ngay sang màn hình làm bài / ôn tập tương ứng.
  - **Verify**: Tích hợp session state điều hướng 1 chạm thành công.
  - **Files**: `src/views/dashboard.py`.

- [x] **Task 6: Xây dựng Màn hình Bản Đồ Tri Thức & Quản Lý Dạng Toán**
  - **Mô tả**: Viết `src/views/curriculum_view.py` xem cây tri thức phân cấp (Tập 1, 2 -> Chương -> Bài -> Lý thuyết & Dạng toán), có form thêm mới dạng bài tùy biến.
  - **Acceptance Criteria**: Người dùng xem được lý thuyết, công thức, các dạng bài nâng cao và thêm được dạng toán mới.
  - **Verify**: Cây tri thức duyệt theo Tập, Chương, Bài và form thêm dạng bài hoạt động chính xác.
  - **Files**: `src/views/curriculum_view.py`.

- [x] **Task 7: Xây dựng Màn hình Ghi Nhận Luyện Tập (Snapshot & Camera)**
  - **Mô tả**: Viết `src/views/practice_view.py` cho phép chọn dạng bài, tải ảnh bài làm lên hoặc chụp ảnh trực tiếp bằng camera, đánh giá "Tự làm được" / "Cần gợi ý", ghi chú và lưu vào CSDL.
  - **Acceptance Criteria**: Hỗ trợ cả 2 hình thức: file upload và camera input; lưu ảnh vào `data/uploads/`, cập nhật ngay trạng thái SRS.
  - **Verify**: Test lưu ảnh, nén ảnh Pillow và ghi log thành công.
  - **Files**: `src/views/practice_view.py`.

- [x] **Task 8: Xây dựng Phòng Ôn Tập SRS & Lịch Sử Làm Bài**
  - **Mô tả**: Viết `src/views/review_view.py` (ôn tập chuyên biệt cho các bài đến hạn) và `src/views/history_view.py` (xem lại dòng thời gian và ảnh bài giải cũ).
  - **Acceptance Criteria**: Hiển thị ảnh bài làm trước đó, nút cập nhật nhanh kết quả ôn tập hôm nay để đẩy lịch lần sau.
  - **Verify**: Các chức năng ôn tập, xem ảnh lịch sử hoàn thành.
  - **Files**: `src/views/review_view.py`, `src/views/history_view.py`.

- [x] **Task 9: Tích hợp ứng dụng chính `app.py`, Smoke Test và Hướng dẫn sử dụng**
  - **Mô tả**: Viết `app.py` kết nối toàn bộ các views, cấu hình sidebar, title, theme, state navigation. Chạy smoke test toàn bộ app. Viết `README.md` hướng dẫn chạy.
  - **Acceptance Criteria**: Ứng dụng chạy mượt mà bằng lệnh `streamlit run app.py`, không lỗi crash, giao diện tiếng Việt đẹp mắt, dễ dùng cho phụ huynh.
  - **Verify**: Import check thành công, 11/11 unit tests pass 100%.
  - **Files**: `app.py`, `README.md`.
