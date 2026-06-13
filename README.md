[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ZpUiBug-)
# STQA Library Automation — NHÓM 13

Bài tập thực hành **Kiểm thử Web UI tự động** cho môn **Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)**.
(*A hands-on **Automated Web UI Testing** assignment for the **Software Testing & Quality Assurance (STQA)** course.*)

Sử dụng **Playwright + Python** để kiểm thử hệ thống Mượn sách Thư viện ABC tại [https://stqa.rbc.vn](https://stqa.rbc.vn).
(*Uses **Playwright + Python** to test the Library Book Borrowing System.*)

> **📚 Hệ thống hư cấu / Fictional System**: Thư viện ABC là hệ thống **hư cấu** được thiết kế cho mục đích học tập. Tên nhân vật, tổ chức và dữ liệu đều là giả lập. / *ABC Library is a **fictional** system designed for educational purposes. All names, organizations, and data are simulated.*

---

## 👥 Thông tin nhóm / Team Information

|              | Thông tin        |
| ------------ | ---------------- |
| **Tên nhóm** | `NHÓM 13`        |
| **Lớp**      | `ICT2.012`       |
| **Học kỳ**   | `HK2 2025-2026`  |

| #   | MSSV      | Họ và tên           | Vai trò     |
| --- | --------- | ------------------- | ----------- |
| 1   | 23BA14272 | Nguyễn Ngọc Thịnh   | Nhóm trưởng |
| 2   | 23BA14009 | Nguyễn Cao Việt Anh | Thành viên  |
| 3   |           |                     | Thành viên  |
| 4   |           |                     | Thành viên  |

---

## 📖 Trước khi bắt đầu — Bối cảnh / Before You Start — Context

### Bài tập này nằm ở đâu trong quy trình?

```
SRS (Yêu cầu phần mềm) → Dev xây hệ thống → A1: Kiểm thử thủ công → A2: Kiểm thử tự động (BẠN Ở ĐÂY)
```

Ở bài **A1** (nếu đã làm), bạn đã kiểm thử thủ công: mở trình duyệt, nhấn nút, ghi kết quả. Bây giờ ở **A2**, bạn sẽ **tự động hóa** các thao tác đó bằng code.

### Những ai liên quan? (*Stakeholders*)

| Vai trò         | Ai?            | Liên quan thế nào?                                                                                          |
| --------------- | -------------- | ----------------------------------------------------------------------------------------------------------- |
| **Khách hàng**  | Thư viện ABC   | Đưa ra yêu cầu nghiệp vụ ([BRD](docs/BRD-yeu-cau-nghiep-vu.md)) → BA viết [SRS](docs/SRS-library-system.md) |
| **Dev Team**    | Nhóm lập trình | Xây hệ thống                                                                                                |
| **Tester / QC** | **Bạn**        | Viết automated test, phát hiện lỗi                                                                          |
| **QA Lead**     | Giảng viên     | Review kết quả test                                                                                         |

### Tester dựa vào đâu để kiểm thử?

| Nguồn                      | Trong bài này                                                    |
| -------------------------- | ---------------------------------------------------------------- |
| **SRS** (đặc tả yêu cầu)   | [docs/SRS-library-system.md](docs/SRS-library-system.md) — 8 REQ |
| **Test accounts**          | [docs/test-accounts.md](docs/test-accounts.md) — 6 tài khoản     |
| **A1 test cases** (nếu có) | Tham khảo TC thủ công để viết code tự động                       |

### Software Testing vs Quality Assurance

|                  | **Testing** (Bài này)                             | **QA**                                       |
| ---------------- | ------------------------------------------------- | -------------------------------------------- |
| **Bạn đang làm** | ✅ Viết automated test, chạy test, chụp screenshot | Bonus B4: Viết REPORT.md đánh giá chất lượng |
| **Mục đích**     | Tìm lỗi tự động, nhanh, lặp lại được              | Đánh giá quy trình, đề xuất cải tiến         |

---

> ⚠️ Website sử dụng **Flutter Web (CanvasKit renderer)** — toàn bộ giao diện render trên `<canvas>`, không có HTML DOM thông thường. Dự án đã cung cấp sẵn các helper function để tương tác qua **Accessibility Semantics Tree**.
>
> (*The website uses **Flutter Web (CanvasKit renderer)** — the entire UI is rendered on `<canvas>`, with no standard HTML DOM. This project provides helper functions to interact via the Accessibility Semantics Tree.*)

---

## 📁 Cấu trúc dự án / Project Structure

```
stqa-automation-testing-stqa_group_13/
├── conftest.py          # Fixtures & helper functions (HOÀN CHỈNH)
├── web_detector.py      # Web technology detector module (HOÀN CHỈNH)
├── pytest.ini           # pytest configuration
├── requirements.txt     # Dependencies
├── .env.example         # Environment variable template
├── .gitignore
├── LICENSE
├── README.md
├── submission/
│   └── REPORT.md        # Báo cáo kết quả kiểm thử (Bonus B4)
└── tests/
    ├── test_login.py           # TC-01 ~ TC-03 + Bonus B2 (parametrize)
    ├── test_search.py          # TC-04 ~ TC-07 + Bonus B1
    ├── test_borrow_return.py   # TC-08 ~ TC-10
    └── test_general.py         # TC-11 ~ TC-12 + Bonus B1 (language)
```

---

## 🚀 Cài đặt / Installation

### 1. Clone repo & tạo môi trường ảo

```bash
git clone <repo-url>
cd stqa-automation-testing-stqa_group_13
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows
```

### 2. Cài đặt dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Cấu hình biến môi trường

Tạo file `.env` từ template:

```bash
cp .env.example .env
```

Sửa `.env` với thông tin đăng nhập của bạn:

```
BASE_URL=https://stqa.rbc.vn
TEST_EMAIL=your_email@example.com
TEST_PASSWORD=your_password
TEST_DISPLAY_NAME=Your Display Name
```

> ⚠️ **KHÔNG commit file `.env`** — file này đã được thêm vào `.gitignore`.

---

## ▶️ Chạy test / Running Tests

```bash
# Run all tests (Chạy tất cả test)
pytest

# Run a specific file (Chạy 1 file cụ thể)
pytest tests/test_login.py

# Run a specific test case (Chạy 1 test case cụ thể)
pytest tests/test_login.py::test_login_success

# Verbose output (Hiện output chi tiết)
pytest -v -s
```

Screenshot được lưu tự động vào thư mục `screenshots/`.

---

## 🤖 CI với GitHub Actions

Repo có workflow CI tại `.github/workflows/pytest-ci.yml` và tự chạy khi có `push` hoặc `pull_request`.

CI sẽ thực hiện:

1. Cài Python + dependencies
2. Cài Playwright Chromium
3. Chạy `pytest --junitxml=report.xml`
4. Upload artifacts: `report.xml` + `screenshots/**`

### Cách xem kết quả CI

1. Vào tab **Actions** trên GitHub
2. Mở run mới nhất của workflow **Pytest CI**
3. Kéo xuống phần **Artifacts** để tải `pytest-artifacts`
4. Mở `report.xml` để xem kết quả theo chuẩn JUnit XML

---

## 📋 Kết quả Test Case / Test Results

**🎉 CI kết quả: 18/18 passed ✅** — Xem [Actions](../../actions) để biết chi tiết.

| TC      | Mô tả                                                | File                    | Kết quả  |
| ------- | ---------------------------------------------------- | ----------------------- | -------- |
| TC-01   | Đăng nhập thành công (*Login success*)               | `test_login.py`         | ✅ PASS   |
| TC-02   | Đăng nhập thất bại — sai mật khẩu (*Wrong password*) | `test_login.py`         | ✅ PASS   |
| TC-03   | Đăng nhập thất bại — để trống (*Empty fields*)       | `test_login.py`         | ✅ PASS   |
| TC-04   | Tìm sách theo tên (*Search by name*)                 | `test_search.py`        | ✅ PASS   |
| TC-05   | Tìm sách — không có kết quả (*No result*)            | `test_search.py`        | ✅ PASS   |
| TC-06   | Lọc theo thể loại (*Filter by category*)             | `test_search.py`        | ✅ PASS   |
| TC-07   | Tìm theo tác giả (*Search by author*)                | `test_search.py`        | ✅ PASS   |
| TC-08   | Mượn sách (*Borrow a book*)                          | `test_borrow_return.py` | ✅ PASS   |
| TC-09   | Xem sách đang mượn (*View borrowed books*)           | `test_borrow_return.py` | ✅ PASS   |
| TC-10   | Trả sách (*Return a book*)                           | `test_borrow_return.py` | ✅ PASS   |
| TC-11   | Đăng xuất (*Logout*)                                 | `test_general.py`       | ✅ PASS   |
| TC-12   | Chuyển ngôn ngữ sang EN (*Switch language*)          | `test_general.py`       | ✅ PASS   |
| BONUS   | Parametrize login fail — 3 scenarios (B2)            | `test_login.py`         | ✅ PASS   |
| BONUS   | Search "Flutter" count (B1)                          | `test_search.py`        | ✅ PASS   |
| BONUS   | Filter "Công nghệ" category (B1)                     | `test_search.py`        | ✅ PASS   |
| BONUS   | Switch language back to Vietnamese (B1)              | `test_general.py`       | ✅ PASS   |

### Bonus đã thực hiện

| Bonus | Mô tả | Điểm |
| ----- | ----- | ---- |
| B1    | 4 test case mới ngoài 12 TC bắt buộc | +0.5 |
| B2    | `@pytest.mark.parametrize` cho login fail (3 scenarios) | +0.5 |
| B3    | Assertion chi tiết — kiểm tra text cụ thể, count, aria-label | +0.5 |
| B4    | [REPORT.md](submission/REPORT.md) mô tả từng TC + nhận xét | +0.5 |

---

## 🔧 Các hàm hỗ trợ có sẵn / Available Helper Functions

Các hàm đã được cung cấp trong `conftest.py` — **KHÔNG cần tự viết lại**.

### Flutter Web helpers

| Hàm                                 | Mô tả                                                                                     |
| ----------------------------------- | ----------------------------------------------------------------------------------------- |
| `enable_flutter_semantics(page)`    | Bật Semantics Tree — bắt buộc trước khi tương tác                                         |
| `flutter_fill(page, label, value)`  | Nhập text vào input field qua `aria-label`                                               |
| `flutter_click_button(page, text)`  | Click button theo text hiển thị                                                            |
| `wait_for_flutter(page, text, ...)` | Smart Wait — chờ Semantics Tree cập nhật (thay vì `time.sleep`)                          |

### Universal helpers

| Hàm                                    | Mô tả                                                                       |
| -------------------------------------- | --------------------------------------------------------------------------- |
| `smart_fill(page, label, value, tech)` | Tự chọn cách nhập phù hợp                                                    |
| `smart_click(page, text, tech)`        | Tự chọn cách click phù hợp                                                   |
| `login(page, test_config)`             | Đăng nhập với credentials từ `.env`                                        |

### Fixtures

| Fixture       | Mô tả                                                                                |
| ------------- | ------------------------------------------------------------------------------------ |
| `page`        | Context mới cho mỗi test (Playwright Page object — fresh browser context per test)   |
| `test_config` | Dict chứa `base_url`, `email`, `password`, `display_name`, `screenshot_dir`          |
| `web_tech`    | Thông tin công nghệ web (WebTech object)                                              |

---

## 💡 Cách tương tác với Flutter Web / How to Interact with Flutter Web

Flutter Web (CanvasKit) render mọi thứ lên `<canvas>` — **không có HTML DOM thông thường**. Để test, ta cần:

1. **Bật Semantics Tree**: Gọi `enable_flutter_semantics(page)` → Flutter tạo các elements ẩn `<flt-semantics>` phủ lên canvas
2. **Tương tác qua ARIA attributes**:
   - Input fields: `input[aria-label="Email"]`
   - Buttons: `flt-semantics[role="button"]:has-text("Đăng nhập")`
   - Tabs: `flt-semantics[role="tab"][aria-label="Mượn / Trả"]`
   - Groups (book cards): `flt-semantics[role="group"][aria-label*="Mã: BOOK"]`

### Pattern cơ bản

```python
from conftest import login, flutter_fill, wait_for_flutter

def test_example(page, test_config):
    # 1. Đăng nhập
    login(page, test_config)

    # 2. Tương tác
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")

    # 3. Smart Wait (thay vì time.sleep)
    wait_for_flutter(page, text="Flutter")

    # 4. Assert
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Flutter" in sem_text

    # 5. Screenshot
    page.screenshot(path=f"{test_config['screenshot_dir']}/TC_example.png")
```

---

## 📚 Tài liệu tham khảo / References

| Bạn muốn...                  | Đi đến                                                         |
| ---------------------------- | -------------------------------------------------------------- |
| Xem đề bài + rubric          | [docs/ASSIGNMENT.md](docs/ASSIGNMENT.md)                       |
| Đọc yêu cầu hệ thống (SRS)   | [docs/SRS-library-system.md](docs/SRS-library-system.md)       |
| Xem yêu cầu nghiệp vụ (BRD)  | [docs/BRD-yeu-cau-nghiep-vu.md](docs/BRD-yeu-cau-nghiep-vu.md) |
| Xem tài khoản test           | [docs/test-accounts.md](docs/test-accounts.md)                 |
| Báo cáo kết quả (B4)         | [submission/REPORT.md](submission/REPORT.md)                   |
| Playwright Python Docs       | https://playwright.dev/python/                                  |
| pytest Documentation         | https://docs.pytest.org/                                        |

---

## 🤖 Khai báo sử dụng AI

Nhóm sử dụng **Claude (Anthropic)** để hỗ trợ viết automation test code.

AI được dùng để: phân tích ASSIGNMENT.md và SRS, viết code 12 TC + 4 bonus TC, áp dụng Smart Wait pattern thay vì `time.sleep()`, và viết REPORT.md. Nhóm đã kiểm tra lại từng test case, điều chỉnh account strategy cho TC-08/09/10, và xác nhận kết quả CI.
