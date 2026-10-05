"""Curriculum and Advanced Problem Types Seeder for Math 6 KNTT.

Seeds:
- Volume 1 & 2
- Chapters I through IX
- Lessons 1 through 43
- Key theoretical concepts
- Pre-seeded Advanced Math Problem Types for each lesson
"""

from typing import List, Dict, Any
from src.database import get_connection, init_db

CHAPTERS_DATA = [
    # Tap 1
    {"id": "ch-01", "volume": 1, "code": "I", "title": "Tập hợp các số tự nhiên", "order_num": 1},
    {"id": "ch-02", "volume": 1, "code": "II", "title": "Tính chia hết trong tập hợp các số tự nhiên", "order_num": 2},
    {"id": "ch-03", "volume": 1, "code": "III", "title": "Số nguyên", "order_num": 3},
    {"id": "ch-04", "volume": 1, "code": "IV", "title": "Một số hình phẳng trong thực tiễn", "order_num": 4},
    {"id": "ch-05", "volume": 1, "code": "V", "title": "Tính đối xứng của hình phẳng trong tự nhiên", "order_num": 5},
    # Tap 2
    {"id": "ch-06", "volume": 2, "code": "VI", "title": "Phân số", "order_num": 6},
    {"id": "ch-07", "volume": 2, "code": "VII", "title": "Số thập phân", "order_num": 7},
    {"id": "ch-08", "volume": 2, "code": "VIII", "title": "Những hình hình học cơ bản", "order_num": 8},
    {"id": "ch-09", "volume": 2, "code": "IX", "title": "Dữ liệu và xác suất thực nghiệm", "order_num": 9},
]

LESSONS_DATA = [
    # Tap 1 - Chuong I
    {"id": "bai-01", "chapter_id": "ch-01", "title": "Bài 1. Tập hợp", "pages": "6-9", "order_num": 1,
     "concept": "Khái niệm tập hợp, phần tử thuộc/không thuộc, hai cách viết tập hợp.",
     "example": "A = {x ∈ N | x < 5} = {0, 1, 2, 3, 4}.",
     "adv_problems": [
         {"title": "Tính số phần tử của tập hợp cách đều và tập hợp con",
          "method": "Số phần tử = (Số cuối - Số đầu) : khoảng cách + 1. Tập có n phần tử thì có 2^n tập con.",
          "difficulty": "Nâng cao"},
         {"title": "Tìm số chữ số cần dùng để đánh số trang sách",
          "method": "Chia trang thành các nhóm 1 chữ số (1-9), 2 chữ số (10-99), 3 chữ số (100-999)... rồi tính tổng chữ số.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-02", "chapter_id": "ch-01", "title": "Bài 2. Cách ghi số tự nhiên", "pages": "10-12", "order_num": 2,
     "concept": "Hệ thập phân, giá trị theo vị trí của chữ số, số La Mã.",
     "example": "Số 235 = 200 + 30 + 5. Số XIV = 14.",
     "adv_problems": [
         {"title": "Cấu tạo số tự nhiên: Tìm số khi viết thêm chữ số vào bên trái/phải",
          "method": "Đặt số cần tìm là ab (10a+b). Khi viết thêm chữ số k vào bên phải thì số mới là 10*ab + k.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-03", "chapter_id": "ch-01", "title": "Bài 3. Thứ tự trong tập hợp các số tự nhiên", "pages": "13-15", "order_num": 3,
     "concept": "So sánh hai số tự nhiên, tia số, các quan hệ thứ tự.",
     "example": "Nếu a < b và b < c thì a < c.",
     "adv_problems": [
         {"title": "Tìm số tự nhiên thỏa mãn bất đẳng thức kép",
          "method": "Biến đổi hai đầu chặn bất đẳng thức để tìm các giá trị nguyên thỏa mãn.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-04", "chapter_id": "ch-01", "title": "Bài 4. Phép cộng và phép trừ số tự nhiên", "pages": "16-19", "order_num": 4,
     "concept": "Tính chất giao hoán, kết hợp của phép cộng. Điều kiện thực hiện phép trừ.",
     "example": "a + b = b + a; (a + b) + c = a + (b + c).",
     "adv_problems": [
         {"title": "Tính nhanh tổng dãy số tự nhiên có quy luật (cấp số cộng)",
          "method": "Tổng = (Số đầu + Số cuối) * Số số hạng / 2.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-05", "chapter_id": "ch-01", "title": "Bài 5. Phép nhân và phép chia số tự nhiên", "pages": "20-23", "order_num": 5,
     "concept": "Tính chất phân phối của phép nhân đối với phép cộng. Phép chia có dư: a = b.q + r (0 <= r < b).",
     "example": "a(b + c) = ab + ac.",
     "adv_problems": [
         {"title": "Bài toán phép chia có dư nâng cao: Tìm số bị chia và số chia",
          "method": "Sử dụng bất đẳng thức số dư r < b kết hợp phân tích thừa số.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-06", "chapter_id": "ch-01", "title": "Bài 6. Lũy thừa với số mũ tự nhiên", "pages": "24-26", "order_num": 6,
     "concept": "Lũy thừa bậc n của a là tích của n thừa số a. Nhân, chia hai lũy thừa cùng cơ số.",
     "example": "a^m . a^n = a^(m+n); a^m : a^n = a^(m-n).",
     "adv_problems": [
         {"title": "So sánh hai lũy thừa không cùng cơ số và số mũ",
          "method": "Đưa về cùng cơ số trung gian hoặc đưa về cùng số mũ bằng cách tách tích: a^(m.k) = (a^m)^k.",
          "difficulty": "Vận dụng cao"},
         {"title": "Tìm chữ số tận cùng của lũy thừa lớn",
          "method": "Tìm chu kỳ tuần hoàn chữ số tận cùng (chu kỳ 4 của các số tận cùng 2,3,7,8).",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-07", "chapter_id": "ch-01", "title": "Bài 7. Thứ tự thực hiện các phép tính", "pages": "27-29", "order_num": 7,
     "concept": "Thứ tự: Lũy thừa -> Nhân, chia -> Cộng, trừ. Dấu ngoặc: () -> [] -> {}.",
     "example": "Tính từ trong ngoặc tròn trước, đến ngoặc vuông, rồi ngoặc nhọn.",
     "adv_problems": [
         {"title": "Tìm x trong biểu thức chứa nhiều tầng dấu ngoặc và lũy thừa",
          "method": "Tìm x ngược từ ngoài vào trong: Coi biểu thức trong ngoặc là một ẩn phụ.",
          "difficulty": "Nâng cao"},
         {"title": "Tính tổng dãy lũy thừa liên tiếp A = 1 + a + a^2 + ... + a^n",
          "method": "Nhân a.A rồi lấy a.A - A = a^(n+1) - 1 => A = (a^(n+1) - 1) / (a - 1).",
          "difficulty": "Vận dụng cao"}
     ]},

    # Tap 1 - Chuong II
    {"id": "bai-08", "chapter_id": "ch-02", "title": "Bài 8. Quan hệ chia hết và tính chất", "pages": "31-34", "order_num": 8,
     "concept": "Khái niệm a chia hết cho b (a ⋮ b). Tính chất chia hết của một tổng: nếu a ⋮ m và b ⋮ m thì (a+b) ⋮ m.",
     "example": "Nếu 12 ⋮ 3 và 15 ⋮ 3 thì (12 + 15) ⋮ 3.",
     "adv_problems": [
         {"title": "Chứng minh biểu thức chia hết cho một số với mọi n tự nhiên",
          "method": "Sử dụng tính chất tích của k số tự nhiên liên tiếp luôn chia hết cho k.",
          "difficulty": "Vận dụng cao"},
         {"title": "Tìm số tự nhiên n để biểu thức hữu tỉ nhận giá trị nguyên",
          "method": "Tách tử thức theo mẫu: (an + b)/(cn + d) = k + r/(cn + d), rồi cho cn+d là ước của r.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-09", "chapter_id": "ch-02", "title": "Bài 9. Dấu hiệu chia hết cho 2, cho 5", "pages": "35-37", "order_num": 9,
     "concept": "Tận cùng chẵn chia hết cho 2; tận cùng 0 hoặc 5 chia hết cho 5.",
     "example": "Số có chữ số tận cùng là 0 thì chia hết cho cả 2 và 5.",
     "adv_problems": [
         {"title": "Điền chữ số để số chia hết cho cả 2 và 5 kết hợp điều kiện khác",
          "method": "Xác định chữ số tận cùng trước (phải là 0), sau đó giải điều kiện còn lại.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-10", "chapter_id": "ch-02", "title": "Bài 10. Dấu hiệu chia hết cho 3, cho 9", "pages": "38-40", "order_num": 10,
     "concept": "Tổng các chữ số chia hết cho 3 (hoặc 9) thì số đó chia hết cho 3 (hoặc 9). Số dư khi chia cho 9 bằng số dư của tổng chữ số.",
     "example": "Số 234 có 2+3+4 = 9 chia hết cho 9.",
     "adv_problems": [
         {"title": "Tìm số thỏa mãn đồng thời chia hết cho 2, 3, 5, 9 và có dư",
          "method": "Lập luận tìm chữ số hàng đơn vị trước, sau đó dùng tổng chữ số chặn khoảng tìm các chữ số còn lại.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-11", "chapter_id": "ch-02", "title": "Bài 11. Số nguyên tố. Hợp số. Phân tích ra thừa số nguyên tố", "pages": "41-45", "order_num": 11,
     "concept": "Số nguyên tố chỉ có 2 ước là 1 và chính nó. Phân tích một số ra thừa số nguyên tố.",
     "example": "60 = 2^2 . 3 . 5.",
     "adv_problems": [
         {"title": "Tìm số nguyên tố p sao cho p+2, p+4 cũng là số nguyên tố",
          "method": "Xét số dư của p khi chia cho 3: p = 3k, 3k+1, 3k+2.",
          "difficulty": "Vận dụng cao"},
         {"title": "Tính số lượng ước và tổng tất cả các ước của một số tự nhiên",
          "method": "Nếu N = p1^a . p2^b thì số ước là (a+1)(b+1).",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-12", "chapter_id": "ch-02", "title": "Bài 12. Ước chung. Ước chung lớn nhất - Bội chung. Bội chung nhỏ nhất", "pages": "46-53", "order_num": 12,
     "concept": "ƯCLN là số lớn nhất trong tập các ước chung. BCNN là số nhỏ nhất khác 0 trong tập bội chung.",
     "example": "ƯCLN(12, 18) = 6. BCNN(12, 18) = 36.",
     "adv_problems": [
         {"title": "Tìm hai số tự nhiên a và b biết ƯCLN và BCNN hoặc tổng/tích của chúng",
          "method": "Đặt a = d.x, b = d.y với d = ƯCLN(a,b) và ƯCLN(x,y) = 1.",
          "difficulty": "Vận dụng cao"},
         {"title": "Bài toán thực tế quy về tìm BCNN và bội chung",
          "method": "Mô hình hóa bài toán xếp hàng, chia nhóm thành điều kiện chia hết có cùng số dư.",
          "difficulty": "Nâng cao"}
     ]},

    # Tap 1 - Chuong III
    {"id": "bai-13", "chapter_id": "ch-03", "title": "Bài 13. Tập hợp các số nguyên", "pages": "58-61", "order_num": 13,
     "concept": "Tập hợp Z gồm số nguyên âm, số 0 và số nguyên dương. Trục số nguyên.",
     "example": "Z = {..., -2, -1, 0, 1, 2, ...}.",
     "adv_problems": [
         {"title": "Tìm các giá trị nguyên của x thỏa mãn điều kiện khoảng cách trên trục số",
          "method": "Sử dụng ý nghĩa hình học của giá trị tuyệt đối / khoảng cách trên trục số.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-14", "chapter_id": "ch-03", "title": "Bài 14. Phép cộng và phép trừ số nguyên", "pages": "62-67", "order_num": 14,
     "concept": "Cộng hai số nguyên cùng dấu, khác dấu. Phép trừ: a - b = a + (-b).",
     "example": "(-3) + (-5) = -8; 5 + (-8) = -3.",
     "adv_problems": [
         {"title": "Tính nhanh tổng đại số xen kẽ dấu A = 1 - 2 + 3 - 4 + ... + (2n-1) - 2n",
          "method": "Gộp từng cặp hai số liên tiếp có tổng bằng -1.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-15", "chapter_id": "ch-03", "title": "Bài 15. Quy tắc dấu ngoặc", "pages": "68-70", "order_num": 15,
     "concept": "Bỏ ngoặc đằng trước có dấu '+': giữ nguyên; đằng trước có dấu '-': đổi dấu toàn bộ số hạng trong ngoặc.",
     "example": "a - (b - c + d) = a - b + c - d.",
     "adv_problems": [
         {"title": "Rút gọn biểu thức chứa nhiều lớp dấu ngoặc và biến đổi đại số",
          "method": "Bỏ ngoặc tuần tự kết hợp nhóm các số hạng triệt tiêu nhau.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-16", "chapter_id": "ch-03", "title": "Bài 16. Phép nhân số nguyên", "pages": "71-74", "order_num": 16,
     "concept": "Quy tắc dấu khi nhân hai số nguyên: cùng dấu dương, khác dấu âm.",
     "example": "(-2) . (-3) = 6; (-2) . 3 = -6.",
     "adv_problems": [
         {"title": "Tìm các số nguyên x, y thỏa mãn phương trình tích (ax+b)(cy+d) = k",
          "method": "Phân tích k thành tích các ước số nguyên của k để xét từng trường hợp.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-17", "chapter_id": "ch-03", "title": "Bài 17. Phép chia hết. Ước và bội của một số nguyên", "pages": "75-77", "order_num": 17,
     "concept": "Cho a, b ∈ Z (b ≠ 0), nếu có q ∈ Z sao cho a = b.q thì a ⋮ b. Ước và bội trong Z bao gồm cả số âm.",
     "example": "Ước của 6 là {±1, ±2, ±3, ±6}.",
     "adv_problems": [
         {"title": "Tìm số nguyên n để biểu thức (2n+1) là ước của (3n+5)",
          "method": "Nhân tử số để triệt tiêu n: 2(3n+5) - 3(2n+1) = 7 ⋮ (2n+1).",
          "difficulty": "Vận dụng cao"}
     ]},

    # Tap 1 - Chuong IV
    {"id": "bai-18", "chapter_id": "ch-04", "title": "Bài 18. Tam giác đều. Hình vuông. Lục giác đều", "pages": "80-84", "order_num": 18,
     "concept": "Đặc điểm cạnh, góc, đường chéo của tam giác đều, hình vuông, lục giác đều.",
     "example": "Hình vuông có 4 cạnh bằng nhau, 4 góc vuông, 2 đường chéo bằng nhau và vuông góc.",
     "adv_problems": [
         {"title": "Bài toán cắt ghép và tính số hình lát nền lục giác đều, hình vuông",
          "method": "Tính diện tích một viên gạch và chia diện tích sàn cần lát.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-19", "chapter_id": "ch-04", "title": "Bài 19. Hình chữ nhật. Hình thoi. Hình bình hành. Hình thang cân", "pages": "85-90", "order_num": 19,
     "concept": "Nhận biết các cạnh đối, góc đối, đường chéo của từng tứ giác đặc biệt.",
     "example": "Hình thoi có 2 đường chéo vuông góc tại trung điểm mỗi đường.",
     "adv_problems": [
         {"title": "Xác định loại tứ giác và tính độ dài cạnh/đường chéo nâng cao",
          "method": "Vận dụng tính chất đường chéo và hệ thức phân chia đối xứng.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-20", "chapter_id": "ch-04", "title": "Bài 20. Chu vi và diện tích của một số tứ giác", "pages": "91-95", "order_num": 20,
     "concept": "Công thức chu vi và diện tích: HCN, hình vuông, hình bình hành, hình thoi (1/2 d1.d2), hình thang (1/2(a+b)h).",
     "example": "S_thoi = 1/2 . d1 . d2.",
     "adv_problems": [
         {"title": "Tính diện tích hình phức tạp bằng phương pháp cắt ghép hoặc phần bù",
          "method": "Bao quanh hình bằng một hình chữ nhật lớn rồi trừ đi các diện tích tam giác vuông/góc thừa.",
          "difficulty": "Vận dụng cao"},
         {"title": "Bài toán trồng cây xung quanh khu vườn và chừa lối đi",
          "method": "Tính diện tích lối đi bằng hiệu hai diện tích; tính chu vi viền ngoài trừ khoảng cách cổng.",
          "difficulty": "Nâng cao"}
     ]},

    # Tap 1 - Chuong V
    {"id": "bai-21", "chapter_id": "ch-05", "title": "Bài 21. Hình có trục đối xứng", "pages": "98-102", "order_num": 21,
     "concept": "Trục đối xứng chia hình thành hai phần gấp chồng khít lên nhau.",
     "example": "Đường tròn có vô số trục đối xứng đi qua tâm.",
     "adv_problems": [
         {"title": "Xác định số trục đối xứng của các chữ cái và hình đa giác phức tạp",
          "method": "Phân tích trục đối xứng qua các cặp đỉnh và trung điểm cạnh đối diện.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-22", "chapter_id": "ch-05", "title": "Bài 22. Hình có tâm đối xứng", "pages": "103-107", "order_num": 22,
     "concept": "Tâm đối xứng: quay nửa vòng (180 độ) quanh tâm thì hình trùng khít với chính nó.",
     "example": "Hình bình hành có tâm đối xứng là giao điểm hai đường chéo.",
     "adv_problems": [
         {"title": "Phân biệt hình có trục đối xứng, tâm đối xứng hoặc cả hai",
          "method": "Lập bảng kiểm tra tính đối xứng qua phép quay 180 độ và phép lật gương.",
          "difficulty": "Nâng cao"}
     ]},

    # Tap 2 - Chuong VI
    {"id": "bai-23", "chapter_id": "ch-06", "title": "Bài 23. Mở rộng phân số. Phân số bằng nhau", "pages": "4-8", "order_num": 23,
     "concept": "Phân số a/b (a, b ∈ Z, b ≠ 0). Hai phân số bằng nhau khi a.d = b.c.",
     "example": "-2/3 = 4/(-6) vì (-2).(-6) = 3.4.",
     "adv_problems": [
         {"title": "Tìm số nguyên n để phân số A = (n+1)/(n-2) là số nguyên hoặc tối giản",
          "method": "Tách A = 1 + 3/(n-2) => n-2 là ước của 3 để A nguyên; ƯCLN(n+1, n-2) = 1 để tối giản.",
          "difficulty": "Vận dụng cao"},
         {"title": "Chứng minh phân số tối giản với mọi n tự nhiên",
          "method": "Gọi d = ƯCLN(tử, mẫu). Nhân hệ số để triệt tiêu n, suy ra d = 1.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-24", "chapter_id": "ch-06", "title": "Bài 24. So sánh phân số. Hỗn số dương", "pages": "9-12", "order_num": 24,
     "concept": "Quy đồng mẫu số dương rồi so sánh tử. Hỗn số a b/c = a + b/c.",
     "example": "-3/4 < -2/4.",
     "adv_problems": [
         {"title": "So sánh hai phân số bằng phương pháp bắc cầu qua phân số trung gian hoặc phần bù",
          "method": "Nếu hai phân số gần 1 thì so sánh 1 - a/b; hoặc so sánh với phân số trung gian có tử của số này, mẫu của số kia.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-25", "chapter_id": "ch-06", "title": "Bài 25. Phép cộng và phép trừ phân số", "pages": "15-18", "order_num": 25,
     "concept": "Cùng mẫu: cộng/trừ tử, giữ nguyên mẫu. Khác mẫu: quy đồng mẫu số trước.",
     "example": "1/3 + 1/4 = 4/12 + 3/12 = 7/12.",
     "adv_problems": [
         {"title": "Tính nhanh tổng dãy phân số có quy luật: S = 1/(1.2) + 1/(2.3) + ... + 1/(n.(n+1))",
          "method": "Tách từng số hạng: 1/(k(k+1)) = 1/k - 1/(k+1). Các số hạng ở giữa sẽ triệt tiêu.",
          "difficulty": "Vận dụng cao"},
         {"title": "Tính tổng dãy phân số cách nhau d đơn vị ở mẫu: S = d/(1.(1+d)) + ...",
          "method": "Nhận xét tử số bằng hiệu hai thừa số ở mẫu số để tách hiệu.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-26", "chapter_id": "ch-06", "title": "Bài 26. Phép nhân và phép chia phân số", "pages": "19-21", "order_num": 26,
     "concept": "Nhân tử với tử, mẫu với mẫu. Chia cho phân số là nhân với phân số nghịch đảo.",
     "example": "(a/b) : (c/d) = (a/b) . (d/c).",
     "adv_problems": [
         {"title": "Tính tích chuỗi phân số rút gọn: P = (1 - 1/2)(1 - 1/3)...(1 - 1/n)",
          "method": "Tính giá trị từng ngoặc: 1/2 . 2/3 . 3/4 ... (n-1)/n rồi triệt tiêu chéo.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-27", "chapter_id": "ch-06", "title": "Bài 27. Hai bài toán về phân số", "pages": "22-24", "order_num": 27,
     "concept": "Bài toán 1: Tìm m/n của số b => tính b . (m/n). Bài toán 2: Tìm một số biết m/n của nó bằng a => tính a : (m/n).",
     "example": "Tìm 2/3 của 18 là 18 . 2/3 = 12.",
     "adv_problems": [
         {"title": "Bài toán có lời văn nâng cao về tỉ lệ phân số và phần còn lại qua nhiều ngày",
          "method": "Vẽ sơ đồ đoạn thẳng hoặc tính phân số chỉ phần còn lại sau từng bước từ cuối lên.",
          "difficulty": "Vận dụng cao"}
     ]},

    # Tap 2 - Chuong VII
    {"id": "bai-28", "chapter_id": "ch-07", "title": "Bài 28. Số thập phân", "pages": "28-30", "order_num": 28,
     "concept": "Phân số thập phân và cách biểu diễn số thập phân âm, dương.",
     "example": "-15/100 = -0,15.",
     "adv_problems": [
         {"title": "Biến đổi phân số tuần hoàn vô hạn thành phân số tối giản",
          "method": "Đặt x = 0,(a) rồi nhân 10^k trừ đi x để đưa về phân số thường.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-29", "chapter_id": "ch-07", "title": "Bài 29. Tính toán với số thập phân", "pages": "31-34", "order_num": 29,
     "concept": "Quy tắc cộng, trừ, nhân, chia số thập phân và thứ tự tính.",
     "example": "Đặt dấu phẩy thẳng hàng khi cộng trừ số thập phân.",
     "adv_problems": [
         {"title": "Tính nhanh giá trị biểu thức số thập phân bằng cách nhóm nhân tử chung",
          "method": "Áp dụng tính chất phân phối kết hợp làm tròn khéo léo để tạo số tròn chục.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-30", "chapter_id": "ch-07", "title": "Bài 30. Làm tròn và ước lượng", "pages": "35-37", "order_num": 30,
     "concept": "Quy tắc làm tròn: chữ số ngay sau hàng làm tròn < 5 thì bỏ đi, >= 5 thì tăng thêm 1.",
     "example": "3,14159 làm tròn đến hàng phần trăm là 3,14.",
     "adv_problems": [
         {"title": "Ứng dụng làm tròn và ước lượng sai số trong đo đạc thực tế",
          "method": "Đánh giá sai số tuyệt đối lớn nhất khi làm tròn một phép đo thực tế.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-31", "chapter_id": "ch-07", "title": "Bài 31. Một số bài toán về tỉ số và tỉ số phần trăm", "pages": "38-40", "order_num": 31,
     "concept": "Tỉ số a/b. Tỉ số phần trăm: (a/b).100%. Hai bài toán tỉ số % cơ bản.",
     "example": "Tỉ số phần trăm của 3 và 4 là (3/4).100% = 75%.",
     "adv_problems": [
         {"title": "Bài toán thực tế về bài toán lãi kép và mua sắm giảm giá nhiều đợt",
          "method": "Giá sau 2 lần giảm x% và y%: P_moi = P * (1 - x%) * (1 - y%). Chú ý không được cộng gộp phần trăm.",
          "difficulty": "Vận dụng cao"},
         {"title": "Bài toán nồng độ dung dịch và pha trộn tỉ lệ",
          "method": "Lập phương trình bảo toàn khối lượng chất tan khi thêm nước hoặc muối.",
          "difficulty": "Vận dụng cao"}
     ]},

    # Tap 2 - Chuong VIII
    {"id": "bai-32", "chapter_id": "ch-08", "title": "Bài 32. Điểm và đường thẳng", "pages": "43-47", "order_num": 32,
     "concept": "Điểm thuộc/không thuộc đường thẳng. Ba điểm thẳng hàng. Hai đường thẳng cắt nhau, song song.",
     "example": "Qua 2 điểm phân biệt vẽ được duy nhất 1 đường thẳng.",
     "adv_problems": [
         {"title": "Tính số đường thẳng tạo bởi n điểm phân biệt (trong đó có k điểm thẳng hàng)",
          "method": "Nếu không có 3 điểm nào thẳng hàng: n(n-1)/2. Nếu có k điểm thẳng hàng: trừ k(k-1)/2 rồi cộng thêm 1.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-33", "chapter_id": "ch-08", "title": "Bài 33. Điểm nằm giữa hai điểm. Tia", "pages": "48-50", "order_num": 33,
     "concept": "Điểm nằm giữa hai điểm. Định nghĩa tia, hai tia đối nhau, hai tia trùng nhau.",
     "example": "Hai tia Ox và Oy đối nhau tạo thành đường thẳng xy.",
     "adv_problems": [
         {"title": "Xác định số tia và mối quan hệ vị trí giữa các điểm trên một đường thẳng",
          "method": "Với n điểm phân biệt trên đường thẳng, tạo ra 2n tia và 2n tia đối.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-34", "chapter_id": "ch-08", "title": "Bài 34. Đoạn thẳng. Độ dài đoạn thẳng", "pages": "51-54", "order_num": 34,
     "concept": "Đoạn thẳng AB. Khi điểm M nằm giữa A và B thì AM + MB = AB.",
     "example": "Nếu AM = 3cm, MB = 4cm và M nằm giữa A, B thì AB = 7cm.",
     "adv_problems": [
         {"title": "Tính số đoạn thẳng tạo thành từ n điểm trên đường thẳng",
          "method": "Số đoạn thẳng = n(n-1)/2.",
          "difficulty": "Nâng cao"},
         {"title": "Tìm vị trí điểm để tổng khoảng cách MA + MB đạt giá trị nhỏ nhất",
          "method": "MA + MB >= AB, dấu bằng xảy ra khi M nằm trên đoạn thẳng AB.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-35", "chapter_id": "ch-08", "title": "Bài 35. Trung điểm của đoạn thẳng", "pages": "55-56", "order_num": 35,
     "concept": "M là trung điểm của AB khi M nằm giữa A, B và MA = MB = AB/2.",
     "example": "Nếu AB = 8cm thì trung điểm M cách A và B 4cm.",
     "adv_problems": [
         {"title": "Bài toán xác định trung điểm liên tiếp của các đoạn thẳng nối tiếp",
          "method": "Sử dụng tính chất cộng đoạn thẳng và biến đổi biểu thức độ dài.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-36", "chapter_id": "ch-08", "title": "Bài 36. Góc", "pages": "58-60", "order_num": 36,
     "concept": "Góc là hình gồm hai tia chung gốc. Đỉnh và hai cạnh của góc. Điểm trong của góc.",
     "example": "Góc xOy có đỉnh O và hai cạnh Ox, Oy.",
     "adv_problems": [
         {"title": "Tính số góc tạo bởi n tia chung gốc",
          "method": "Số góc tạo thành = n(n-1)/2.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-37", "chapter_id": "ch-08", "title": "Bài 37. Số đo góc", "pages": "61-64", "order_num": 37,
     "concept": "Thước đo góc. Góc vuông (90°), góc nhọn (<90°), góc tù (90°-180°), góc bẹt (180°).",
     "example": "Góc nhọn < Góc vuông < Góc tù < Góc bẹt.",
     "adv_problems": [
         {"title": "Tính góc tạo bởi kim giờ và kim phút tại thời điểm h giờ m phút",
          "method": "Vận tốc kim phút: 6°/phút; vận tốc kim giờ: 0,5°/phút. Tính góc chênh lệch |30h - 5,5m|.",
          "difficulty": "Vận dụng cao"}
     ]},

    # Tap 2 - Chuong IX
    {"id": "bai-38", "chapter_id": "ch-09", "title": "Bài 38. Dữ liệu và thu thập dữ liệu", "pages": "68-72", "order_num": 38,
     "concept": "Dữ liệu là các số liệu, chữ cái, hình ảnh... được thu thập. Dữ liệu định tính và định lượng.",
     "example": "Số học sinh là số liệu; xếp loại hạnh kiểm là dữ liệu không phải là số.",
     "adv_problems": [
         {"title": "Thiết kế bảng câu hỏi và thu thập dữ liệu thống kê không thiên vị",
          "method": "Chọn mẫu ngẫu nhiên và kiểm tra tính hợp lý của dữ liệu.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-39", "chapter_id": "ch-09", "title": "Bài 39. Bảng thống kê và biểu đồ tranh", "pages": "73-76", "order_num": 39,
     "concept": "Bảng thống kê gồm hàng và cột. Biểu đồ tranh dùng biểu tượng để biểu diễn số lượng.",
     "example": "Mỗi biểu tượng ngôi sao đại diện cho 10 học sinh giỏi.",
     "adv_problems": [
         {"title": "Phân tích, suy luận và tìm dữ liệu ẩn từ biểu đồ tranh phức hợp",
          "method": "Đọc chú giải biểu tượng và tính toán tỉ lệ nghịch để tìm số lượng gốc.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-40", "chapter_id": "ch-09", "title": "Bài 40. Biểu đồ cột", "pages": "77-81", "order_num": 40,
     "concept": "Biểu đồ cột dùng các cột chữ nhật rời nhau để biểu diễn số liệu. Chiều cao cột biểu thị giá trị.",
     "example": "So sánh doanh số hoặc số lượng học sinh giữa các tổ.",
     "adv_problems": [
         {"title": "Vẽ và phân tích xu hướng biến động từ biểu đồ cột thực tế",
          "method": "Tính tỉ lệ phần trăm tăng/giảm giữa các cột liên tiếp.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-41", "chapter_id": "ch-09", "title": "Bài 41. Biểu đồ cột kép", "pages": "82-86", "order_num": 41,
     "concept": "Biểu đồ cột kép ghép đôi hai cột để so sánh hai nhóm dữ liệu cùng tiêu chí.",
     "example": "So sánh điểm số nam và nữ theo từng môn học.",
     "adv_problems": [
         {"title": "So sánh đa chỉ số từ biểu đồ cột kép và rút ra nhận xét logic",
          "method": "Tính độ chênh lệch tuyệt đối và chênh lệch tương đối giữa hai nhóm số liệu.",
          "difficulty": "Nâng cao"}
     ]},
    {"id": "bai-42", "chapter_id": "ch-09", "title": "Bài 42. Kết quả có thể và sự kiện trong trò chơi, thí nghiệm", "pages": "89-93", "order_num": 42,
     "concept": "Kết quả có thể xảy ra. Sự kiện chắc chắn, sự kiện không thể, sự kiện có thể.",
     "example": "Tung đồng xu có 2 kết quả có thể: sấp hoặc ngửa.",
     "adv_problems": [
         {"title": "Liệt kê không gian kết quả và đếm số sự kiện thuận lợi bằng sơ đồ cây",
          "method": "Dùng sơ đồ hình cây (tree diagram) để liệt kê tất cả các khả năng khi thực hiện 2-3 hành động liên tiếp.",
          "difficulty": "Vận dụng cao"}
     ]},
    {"id": "bai-43", "chapter_id": "ch-09", "title": "Bài 43. Xác suất thực nghiệm", "pages": "94-96", "order_num": 43,
     "concept": "Xác suất thực nghiệm = (Số lần sự kiện xảy ra) : (Tổng số lần thử).",
     "example": "Tung xúc xắc 100 lần, mặt 6 chấm ra 18 lần => xác suất thực nghiệm là 18/100 = 0,18.",
     "adv_problems": [
         {"title": "Dự đoán số lần xuất hiện của sự kiện trong tương lai dựa trên xác suất thực nghiệm",
          "method": "Số lần dự kiến = Tổng số phép thử mới * Xác suất thực nghiệm đã ghi nhận.",
          "difficulty": "Nâng cao"}
     ]},
]


def seed_database() -> Dict[str, int]:
    """Seed all curriculum data and advanced math problem types into SQLite database."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    counts = {"chapters": 0, "lessons": 0, "concepts": 0, "problem_types": 0}

    # 1. Insert Chapters
    for ch in CHAPTERS_DATA:
        cursor.execute("""
            INSERT OR REPLACE INTO chapters (id, volume, code, title, order_num)
            VALUES (?, ?, ?, ?, ?)
        """, (ch["id"], ch["volume"], ch["code"], ch["title"], ch["order_num"]))
        counts["chapters"] += 1

    # 2. Insert Lessons, Concepts, and Advanced Problem Types
    for l_idx, lesson in enumerate(LESSONS_DATA):
        cursor.execute("""
            INSERT OR REPLACE INTO lessons (id, chapter_id, title, pages, order_num, kind)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (lesson["id"], lesson["chapter_id"], lesson["title"], lesson["pages"], lesson["order_num"], "lesson"))
        counts["lessons"] += 1

        # Insert Concept
        concept_id = f"c_{lesson['id']}"
        cursor.execute("""
            INSERT OR REPLACE INTO concepts (id, lesson_id, title, summary, example, order_num)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            concept_id,
            lesson["id"],
            f"Trọng tâm: {lesson['title']}",
            lesson["concept"],
            lesson.get("example", ""),
            1
        ))
        counts["concepts"] += 1

        # Insert Pre-seeded Advanced Problem Types
        adv_list = lesson.get("adv_problems", [])
        for p_idx, prob in enumerate(adv_list):
            prob_id = f"pt_{lesson['id']}_{p_idx+1}"
            cursor.execute("""
                INSERT OR REPLACE INTO problem_types (id, concept_id, title, method, difficulty, is_custom)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (
                prob_id,
                concept_id,
                prob["title"],
                prob.get("method", ""),
                prob.get("difficulty", "Nâng cao")
            ))
            counts["problem_types"] += 1

    conn.commit()
    conn.close()
    return counts


if __name__ == "__main__":
    res = seed_database()
    print("Seed complete! Summary:", res)
