# Đặc Tả Kỹ Thuật (Specification)
# Nền Tảng Quản Lý, Theo Dõi & Lặp Lại Ngắt Quãng Kiến Thức Toán 6 (KNTT) Trên Streamlit

## 1. Objective (Mục Tiêu)
Xây dựng một nền tảng web ứng dụng chạy trên Streamlit giúp phụ huynh (anh Tú) theo dõi, ghi chép nhật ký học tập, quản lý cây tri thức môn Toán 6 (bộ sách Kết nối tri thức với cuộc sống), và áp dụng phương pháp Lặp lại ngắt quãng (Spaced Repetition System - SRS) để thông báo ôn tập đúng thời điểm cho con gái lớp 6.

### Chân dung người dùng & Hành vi chính:
- **Phụ huynh & Con gái lớp 6**: Cùng nhau học tập, giao bài và rà soát kiến thức hằng ngày/tuần trên máy tính.
- **Nhu cầu cốt lõi**:
  1. **Bản đồ tri thức Toán 6 (Toán 6 KNTT)**: Tra cứu nhanh toàn bộ cây kiến thức từ Tập 1 đến Tập 2 (Chương I đến Chương IX), biết con đã học đến đâu, phần nào còn hổng.
  2. **Khởi tạo sẵn các dạng toán nâng cao**: Nạp sẵn một số dạng toán nâng cao cốt lõi cho từng bài học để hai bố con rèn luyện ngay, đồng thời cho phép bố linh hoạt thêm mới các dạng toán khác trong quá trình học.
  3. **Quản lý Dạng toán & Lưu snapshot bài làm**: Với mỗi bài học/chủ đề, lưu các dạng bài toán đã làm qua, chụp ảnh bài giải của con hoặc tải ảnh từ máy tính/điện thoại.
  4. **Đánh giá mức độ tự chủ**: Ghi nhận con "Tự làm được" hay "Cần gợi ý/hướng dẫn", kèm ngày làm bài và ghi chú điểm con cần lưu ý.
  5. **Bảng Dashboard thông minh & Chuyển hướng 1 chạm**: Bảng điều khiển trung tâm hiển thị rõ ràng hôm nay có bao nhiêu dạng bài đến hạn cần ôn tập (Due for Review Today), cho phép click trực tiếp để nhảy ngay tới dạng bài cần ôn để làm lại hoặc ghi nhận kết quả.
  6. **Thuật toán Spaced Repetition (SRS)**: Tự động tính toán lịch nhắc nhở ôn lại theo chu kỳ 1 -> 3 -> 7 -> 14 -> 30 ngày (tự làm được) hoặc 1 ngày (cần gợi ý).

---

## 2. Tech Stack (Công Nghệ)
- **Ngôn ngữ**: Python 3.12+
- **Frontend / UI Framework**: Streamlit (v1.57+) với bố cục tối ưu cho cả máy tính và tablet (iPad).
- **Cơ sở dữ liệu**: SQLite (`data/math6.db`) - gọn nhẹ, bền vững, lưu trữ toàn bộ cây kiến thức, dạng toán, lịch sử làm bài và tham số SRS.
- **Xử lý hình ảnh**: Pillow (PIL) - tối ưu dung lượng ảnh chụp snapshot, nén và hiển thị sắc nét.
- **Trực quan hóa**: Altair / Plotly / Streamlit native metrics - hiển thị tỉ lệ thành thạo, tiến độ chương trình và lịch trình ôn tập.
- **Testing**: `pytest` - kiểm thử toàn diện thuật toán SRS, cơ chế CRUD dữ liệu và integrity của database.

---

## 3. Commands (Lệnh Thực Thi)
- **Cài đặt thư viện**:
  ```bash
  pip install streamlit pillow pytest pandas
  ```
- **Chạy ứng dụng (Dev/Production)**:
  ```bash
  streamlit run app.py
  ```
- **Chạy kiểm thử (Unit test SRS & Database)**:
  ```bash
  pytest tests/test_srs.py tests/test_db.py -v
  ```
- **Khởi tạo / Nạp dữ liệu cây kiến thức Toán 6 gốc**:
  ```bash
  python -m src.seed_curriculum
  ```

---

## 4. Project Structure (Cấu Trúc Thư Mục)
```text
Toan 6 KNTT/
├── app.py                      # File khởi chạy ứng dụng Streamlit
├── config.py                   # Cấu hình đường dẫn, hằng số SRS, thông số giao diện
├── data/
│   ├── math6.db                # SQLite database chính
│   ├── curriculum_seed.json    # Cây kiến thức chuẩn SGK Toán 6 Tập 1 & Tập 2
│   └── uploads/                # Thư mục lưu snapshot đề bài & bài giải của con
├── src/
│   ├── __init__.py
│   ├── database.py             # Kết nối SQLite, tạo bảng, schema migrations
│   ├── models.py               # Data models / dataclasses
│   ├── srs_engine.py           # Thuật toán Spaced Repetition (SM-2 cải tiến cho học sinh)
│   ├── curriculum_service.py   # Truy vấn, tìm kiếm cây kiến thức
│   ├── practice_service.py     # Quản lý dạng toán, snapshot ảnh, nhật ký luyện tập
│   └── views/                  # Các module giao diện Streamlit
│       ├── __init__.py
│       ├── home_dashboard.py   # Trang tổng quan, báo cáo SRS hôm nay & thống kê
│       ├── curriculum_map.py   # Bản đồ kiến thức Toán 6 (Tập 1 + Tập 2)
│       ├── practice_entry.py   # Màn hình nhập bài tập mới (upload/camera snapshot)
│       └── srs_review.py       # Màn hình phòng ôn tập Spaced Repetition
├── tests/
│   ├── __init__.py
│   ├── test_srs.py             # Unit tests cho thuật toán Spaced Repetition
│   └── test_db.py              # Unit tests cho thao tác CSDL & lưu ảnh
└── docs/
    └── SPEC_TOAN6_STREAMLIT.md # Bản đặc tả này
```

---

## 5. Data Model & SRS Algorithm Design (Mô Hình Dữ Liệu & Thuật Toán)

### 5.1. Database Schema (SQLite)
1. **`chapters`**:
   - `id` (TEXT, PK): ví dụ `ch-01`, `ch-06`
   - `volume` (INT): 1 hoặc 2 (Tập 1 hoặc Tập 2)
   - `code` (TEXT): I, II, ..., IX
   - `title` (TEXT): Tên chương (VD: Số học và phân số, Số nguyên, ...)
   - `order_num` (INT)

2. **`lessons`**:
   - `id` (TEXT, PK): ví dụ `bai-01`, `bai-23`
   - `chapter_id` (TEXT, FK)
   - `title` (TEXT): Tên bài học
   - `pages` (TEXT): Số trang SGK
   - `order_num` (INT)

3. **`concepts`** (Đơn vị kiến thức cần nắm):
   - `id` (TEXT, PK)
   - `lesson_id` (TEXT, FK)
   - `title` (TEXT): Tên định lý, khái niệm, quy tắc
   - `summary` (TEXT): Tóm tắt lý thuyết, công thức ngắn gọn
   - `example` (TEXT): Ví dụ mẫu chuẩn SGK

4. **`problem_types`** (Các dạng toán cụ thể):
   - `id` (TEXT, PK)
   - `concept_id` (TEXT, FK)
   - `title` (TEXT): Tên dạng bài (VD: "Tìm x trong phép chia phân số", "Bài toán có lời văn về tỉ số %")
   - `method` (TEXT): Phương pháp giải / mẹo nhớ
   - `difficulty` (TEXT): Cơ bản / Nâng cao

5. **`practice_records`** (Nhật ký làm bài):
   - `id` (TEXT, PK)
   - `problem_type_id` (TEXT, FK)
   - `practice_date` (DATE): Ngày làm
   - `mastery_level` (TEXT): `INDEPENDENT` (Tự làm được) hoặc `HINTED` (Cần gợi ý)
   - `image_path` (TEXT, Nullable): Đường dẫn snapshot đề / bài làm
   - `notes` (TEXT): Nhận xét của phụ huynh / lỗi con hay mắc
   - `created_at` (TIMESTAMP)

6. **`srs_items`** (Trạng thái Lặp lại ngắt quãng cho từng Dạng toán):
   - `problem_type_id` (TEXT, PK, FK)
   - `interval_days` (FLOAT): Số ngày cách nhau đến lần nhắc tiếp theo
   - `repetitions` (INT): Số lần liên tiếp tự làm được thành công
   - `ease_factor` (FLOAT): Hệ số dễ nhớ (mặc định 2.5)
   - `last_studied` (DATE): Ngày làm gần nhất
   - `next_review` (DATE): Ngày đến hạn ôn tập tiếp theo
   - `status` (TEXT): `NEW`, `LEARNING`, `REVIEW`, `MASTERED`

### 5.2. Thuật toán Spaced Repetition (SRS Engine)
Dựa trên nguyên lý đường cong lãng quên Ebbinghaus và thuật toán SM-2 tối ưu cho học sinh phổ thông:
- Khi con làm một bài thuộc Dạng toán:
  - **Trường hợp 1: "Tự làm được" (INDEPENDENT - Thành công)**:
    - Nếu `repetitions == 0`: `interval = 1 ngày`
    - Nếu `repetitions == 1`: `interval = 3 ngày`
    - Nếu `repetitions == 2`: `interval = 7 ngày`
    - Nếu `repetitions >= 3`: `interval = round(previous_interval * ease_factor)` (VD: 14 ngày, 30 ngày, 60 ngày)
    - Tăng `repetitions += 1`
    - Tăng nhẹ `ease_factor = min(3.0, ease_factor + 0.1)`
    - `next_review = practice_date + interval`
  - **Trường hợp 2: "Cần gợi ý" (HINTED - Cần ôn lại gấp)**:
    - Reset `repetitions = 0` (chưa tự chủ được, cần củng cố)
    - Đặt `interval = 1 ngày` (nhắc ôn lại ngay ngày hôm sau hoặc tối đa 2 ngày)
    - Giảm nhẹ `ease_factor = max(1.3, ease_factor - 0.2)`
    - `next_review = practice_date + 1 ngày`
- **Phân loại hiển thị**:
  - 🔴 **Quá hạn / Đến hạn hôm nay**: `next_review <= today`
  - 🟡 **Sắp đến hạn (Trong 3 ngày tới)**: `today < next_review <= today + 3 ngày`
  - 🟢 **Đã ôn tập / Chưa đến hạn**: `next_review > today + 3 ngày`

---

## 6. Code Style (Phong Cách Lập Trình)
- Tuân thủ PEP 8, kiểu gõ chú thích (`type hints`), docstrings rõ ràng.
- Tách biệt rành mạch giữa UI (Streamlit), Service (Business Logic), Database, và Engine SRS.
- Ví dụ phong cách code:

```python
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional

@dataclass
class SRSReviewResult:
    next_review: date
    interval_days: int
    repetitions: int
    ease_factor: float
    status: str

class SRSEngine:
    @staticmethod
    def calculate_next_schedule(
        practice_date: date,
        is_independent: bool,
        current_repetitions: int = 0,
        current_ease_factor: float = 2.5,
        current_interval: int = 1,
    ) -> SRSReviewResult:
        """Tính toán lịch lặp lại ngắt quãng tiếp theo cho học sinh."""
        if is_independent:
            if current_repetitions == 0:
                new_interval = 1
            elif current_repetitions == 1:
                new_interval = 3
            elif current_repetitions == 2:
                new_interval = 7
            else:
                new_interval = int(round(current_interval * current_ease_factor))
            
            new_repetitions = current_repetitions + 1
            new_ease = min(3.0, current_ease_factor + 0.1)
            status = "MASTERED" if new_repetitions >= 4 else "REVIEW"
        else:
            new_interval = 1
            new_repetitions = 0
            new_ease = max(1.3, current_ease_factor - 0.2)
            status = "LEARNING"

        next_date = practice_date + timedelta(days=new_interval)
        return SRSReviewResult(
            next_review=next_date,
            interval_days=new_interval,
            repetitions=new_repetitions,
            ease_factor=new_ease,
            status=status
        )
```

---

## 7. Testing Strategy (Chiến Lược Kiểm Thử)
- **Unit Tests (`tests/test_srs.py`)**:
  - Test chuỗi ôn tập thành công liên tiếp (1 -> 3 -> 7 -> 14 ngày...).
  - Test khi con cần gợi ý -> interval lập tức reset về 1 ngày, repetitions về 0.
  - Test biên: ease_factor không vượt quá 3.0 và không nhỏ hơn 1.3.
- **Database & Upload Tests (`tests/test_db.py`)**:
  - Test thêm, sửa, xóa dạng toán và nhật ký luyện tập.
  - Test lưu file ảnh snapshot hợp lệ, xử lý file ảnh dung lượng lớn/sai định dạng.
- **UI Smoke Test**:
  - Khởi chạy Streamlit kiểm tra không có lỗi crash, màn hình tải mượt mà.

---

## 8. Boundaries (Quy Tắc Biên)
- **Luôn luôn làm (Always)**:
  - Sử dụng SQLite và lưu ảnh cục bộ trong thư mục dự án (`data/uploads/`) để phụ huynh toàn quyền sở hữu dữ liệu offline, an toàn và dễ đồng bộ Drive.
  - Kiểm tra tính hợp lệ của ngày tháng và file ảnh snapshot trước khi ghi vào CSDL.
  - Viết unit test tự động và chạy `pytest` trước khi bàn giao hoàn thành.
  - Tách giao diện tiếng Việt trong sáng, dễ hiểu, giao diện trực quan hỗ trợ cả màn hình điện thoại/máy tính bảng.
- **Hỏi trước khi làm (Ask first)**:
  - Nếu muốn thay đổi cấu trúc bảng CSDL sau khi đã khởi tạo.
  - Nếu muốn mở rộng thêm môn học khác (Toán 7, Toán 8, Khoa học tự nhiên...).
- **Không bao giờ làm (Never)**:
  - Không xóa vĩnh viễn ảnh hoặc dữ liệu lịch sử làm bài nếu không có xác nhận từ phụ huynh.
  - Không hardcode các đường dẫn tuyệt đối phụ thuộc vào máy của tác giả; sử dụng đường dẫn tương đối theo thư mục gốc dự án.

---

## 9. Success Criteria (Tiêu Chí Nghiệm Thu Cụ Thể)
1. **Bản đồ tri thức đầy đủ & Dạng toán nâng cao nạp sẵn**:
   - Nạp đầy đủ toàn bộ chương trình Toán 6 KNTT (Tập 1: 5 chương, Tập 2: 4 chương + Ôn tập) với cấu trúc phân cấp trực quan: Chương -> Bài học -> Đơn vị kiến thức.
   - Nạp sẵn các dạng toán nâng cao điển hình cho từng bài học (ví dụ: lũy thừa nâng cao, chia hết và đồng dư/chữ số tận cùng, nguyên lý Dirichlet cơ bản, phân số nâng cao dãy số quy luật, bất đẳng thức phân số, hình học tính diện tích nâng cao...).
   - Cho phép thêm mới dạng toán tự do không giới hạn.
2. **Dashboard thống kê & Chuyển hướng 1 chạm**:
   - Hiển thị badge số lượng dạng bài đến hạn cần ôn hôm nay.
   - Bảng danh sách các dạng bài đến hạn có nút click để nhảy trực tiếp sang giao diện ôn tập / làm bài của dạng toán đó.
3. **Lưu trữ dạng toán & Snapshot linh hoạt**:
   - Phụ huynh có thể nhập tên dạng toán, phương pháp giải.
   - Hỗ trợ tải ảnh lên (PNG/JPG) HOẶC chụp ảnh trực tiếp qua camera/webcam từ Streamlit (`st.camera_input`).
   - Ảnh được lưu trữ an toàn trong thư mục `data/uploads/` và hiển thị xem lại ngay trong nhật ký.
4. **Đánh giá trạng thái & Ngày làm**:
   - Ghi nhận rõ ràng: "Tự làm được" (được đánh dấu xanh) và "Cần gợi ý" (được đánh dấu vàng/cam).
   - Chọn ngày làm bài (mặc định là ngày hôm nay, cho phép chọn ngày quá khứ nếu ghi chép bù).
5. **Thuật toán Spaced Repetition hoạt động chính xác**:
   - Chu kỳ: 1 -> 3 -> 7 -> 14 -> 30 -> 60 ngày nếu Tự làm được; 1 ngày nếu Cần gợi ý.
   - Tính tự động `next_review_date` ngay khi lưu bài.
   - Phân loại rõ ràng: Đã quá hạn / Đến hạn hôm nay, Sắp đến hạn (trong 3 ngày), Đã nắm vững.
6. **Độ ổn định & Kiểm thử**:
   - Khởi động bằng lệnh `streamlit run app.py` giao diện mượt mà, trực quan trên máy tính.
   - Toàn bộ unit test với `pytest` đạt 100% pass.
