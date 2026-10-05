# Vườn Toán Lớp 6 - Học Cùng Con (Toán 6 KNTT & Spaced Repetition)

Nền tảng Streamlit quản lý toàn diện cây tri thức môn **Toán 6 (Bộ Kết nối tri thức với cuộc sống)**, ghi chép nhật ký bài tập có đính kèm ảnh chụp snapshot (upload hoặc webcam), và áp dụng thuật toán **Lặp lại ngắt quãng (Spaced Repetition System - SRS)** để tự động thông báo và nhắc ôn tập đúng thời điểm cho con gái lớp 6.

---

## 🌟 Tính Năng Nổi Bật

1. **Bảng Dashboard Thông Minh & Điều Hướng 1 Chạm**:
   - Hiển thị ngay số lượng dạng toán cần ôn tập hôm nay với thông báo nổi bật.
   - Thống kê tỉ lệ tự làm được độc lập vs cần gợi ý, số dạng bài đã thành thạo (`Mastered`).
   - Bảng danh sách các dạng bài đến hạn có nút **"🎯 Ôn tập ngay"** để nhảy trực tiếp vào phòng ôn tập.
2. **Cây Tri Thức Chuẩn SGK & 54+ Dạng Toán Nâng Cao Sẵn Có**:
   - Nạp đầy đủ 9 chương Toán 6 (Tập 1: Chương I-V; Tập 2: Chương VI-IX), 43 bài học.
   - Mỗi bài học đều được nạp sẵn các **dạng toán nâng cao cốt lõi** (Lũy thừa nâng cao, Dãy số quy luật, Bất đẳng thức phân số, Dãy phân số rút gọn, Bài toán thực tế, Đo lường và góc...).
   - Cho phép phụ huynh tự thêm dạng toán mới bất kỳ lúc nào.
3. **Ghi Nhận Luyện Tập Đa Phương Thức & Snapshot Ảnh**:
   - Chụp bài giải của con trực tiếp qua **Camera / Webcam** hoặc **Tải file ảnh** (PNG, JPG).
   - Đánh giá mức độ tự chủ: 🟢 **Con tự làm được độc lập** hoặc 🟡 **Cần bố gợi ý / hướng dẫn**.
   - Ghi chú các bẫy con hay mắc, lỗi sai cần lưu ý.
4. **Thuật Toán Lặp Lại Ngắt Quãng (Spaced Repetition System - SRS)**:
   - Khi con tự làm được: Chu kỳ kéo dài dần: **1 ngày $\rightarrow$ 3 ngày $\rightarrow$ 7 ngày $\rightarrow$ 14 ngày $\rightarrow$ 30 ngày $\rightarrow$ 60 ngày**.
   - Khi con cần gợi ý: Chu kỳ tự động reset về **1 ngày** để củng cố ngay vào ngày hôm sau.
5. **Phòng Ôn Tập Chuyên Biệt (SRS Review Station)**:
   - Rà soát các bài đến hạn hôm nay.
   - Mở xem lại ảnh bài làm cũ của con để đối chiếu.
   - Bấm nút 1 chạm để cập nhật kết quả ôn tập hôm nay.
6. **Lịch Sử & Tiến Bộ Của Con**:
   - Dòng thời gian chi tiết và thư viện ảnh snapshot từng bước trưởng thành của con.

---

## 🚀 Hướng Dẫn Cài Đặt & Khởi Chạy

### 1. Yêu cầu môi trường
- Python 3.10+ (Đã thử nghiệm thành công trên Python 3.12).
- Môi trường Windows / macOS / Linux.

### 2. Cài đặt các thư viện cần thiết
```bash
pip install streamlit pillow pytest pandas
```

### 3. Khởi chạy ứng dụng
Mở terminal trong thư mục dự án và chạy:
```bash
streamlit run app.py
```
Ứng dụng sẽ tự động mở trong trình duyệt tại địa chỉ: `http://localhost:8501`.

*(Lưu ý: Hệ thống sẽ tự động khởi tạo cơ sở dữ liệu SQLite tại `data/math6.db` và nạp toàn bộ 9 chương cùng 54 dạng toán nâng cao trong lần chạy đầu tiên mà không cần thao tác thủ công nào).*

---

## 🧪 Chạy Kiểm Thử (Unit Tests)

Dự án áp dụng phương pháp Spec-Driven & Test-Driven Development với 11 unit test bao phủ toàn bộ SRS Engine và Database Services:
```bash
python -m pytest tests/ -v
```

---

## 📁 Cấu Trúc Dự Án
```text
Toan 6 KNTT/
├── app.py                      # File khởi chạy ứng dụng Streamlit chính
├── config.py                   # Cấu hình đường dẫn, tham số SRS và ảnh
├── conftest.py                 # Cấu hình pytest
├── data/
│   ├── math6.db                # SQLite database lưu trữ dữ liệu
│   └── uploads/                # Thư mục lưu ảnh snapshot bài làm của con
├── docs/
│   ├── SPEC_TOAN6_STREAMLIT.md # Đặc tả kỹ thuật chi tiết
│   └── PLAN_AND_TASKS.md       # Kế hoạch và danh sách nhiệm vụ kỹ thuật
├── src/
│   ├── __init__.py
│   ├── database.py             # Schema SQLite và khởi tạo kết nối
│   ├── models.py               # Dataclasses và Enums
│   ├── seed_data.py            # Dữ liệu 9 chương Toán 6 và dạng toán nâng cao
│   ├── srs_engine.py           # Thuật toán Spaced Repetition (SM-2 tối ưu)
│   ├── services.py             # Data service, CRUD, xử lý ảnh snapshot
│   └── views/                  # 5 module giao diện Streamlit
│       ├── __init__.py
│       ├── dashboard.py        # Dashboard & Điều hướng 1 chạm
│       ├── curriculum_view.py  # Bản đồ tri thức & Thêm dạng toán
│       ├── practice_view.py    # Ghi nhận bài tập, Camera & Snapshot
│       ├── review_view.py      # Phòng ôn tập Spaced Repetition
│       └── history_view.py     # Nhật ký & Thư viện ảnh tiến bộ
└── tests/
    ├── test_srs.py             # Unit tests cho SRS Engine
    └── test_db.py              # Unit tests cho Service Layer & SQLite
```
