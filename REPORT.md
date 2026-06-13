# REPORT.md — Báo cáo kiểm thử tự động
## STQA Group 13 — Thư viện ABC (https://stqa.rbc.vn)

| Thông tin | Giá trị |
|-----------|---------|
| Môn học | Kiểm thử và Đảm bảo chất lượng phần mềm (STQA) |
| Nhóm | NHÓM 13 — Lớp ICT2.012 |
| Công cụ | Python 3.11 + Playwright 1.49.1 + pytest 8.3.4 |
| Hệ thống | https://stqa.rbc.vn (Flutter Web — CanvasKit) |

---

## 1. Tổng quan kết quả / Summary

🎉 **CI: 18/18 passed** — tất cả 12 TC bắt buộc + 6 bonus test đều PASS.

| Nhóm | Test Case | Trạng thái | Ghi chú |
|------|-----------|-----------|---------|
| Đăng nhập | TC-01 | ✅ PASS | Đăng nhập thành công |
| Đăng nhập | TC-02 | ✅ PASS | Sai mật khẩu → vẫn ở login page |
| Đăng nhập | TC-03 | ✅ PASS | Trống email/password → vẫn ở login page |
| Tìm kiếm | TC-04 | ✅ PASS | Tìm "Flutter" → hiển thị kết quả |
| Tìm kiếm | TC-05 | ✅ PASS | Tìm không tồn tại → 0 kết quả |
| Tìm kiếm | TC-06 | ✅ PASS | Lọc "Công nghệ" → chỉ sách Công nghệ |
| Tìm kiếm | TC-07 | ✅ PASS | Tìm tác giả → hiển thị kết quả |
| Mượn/Trả | TC-08 | ✅ PASS | Mượn sách Có sẵn → Đang mượn |
| Mượn/Trả | TC-09 | ✅ PASS | Xem tab Mượn/Trả → thấy phiếu mượn |
| Mượn/Trả | TC-10 | ✅ PASS | Trả sách → trạng thái cập nhật |
| Chung | TC-11 | ✅ PASS | Đăng xuất → quay về login |
| Chung | TC-12 | ✅ PASS | Chuyển EN → giao diện tiếng Anh |

---

## 2. Mô tả chi tiết từng Test Case

### TC-01 — Đăng nhập thành công

- **Mục đích**: Xác nhận hệ thống chấp nhận thông tin đăng nhập hợp lệ.
- **Input**: `ba.nguyen@email.com` / `password123`
- **Expected**: Giao diện chính xuất hiện, nút "Đăng xuất" hiển thị, tên "Nguyễn Học Bá" có mặt.
- **Pattern RIPR**: [R] truy cập login → [I] nhập credentials → [P] chờ "Đăng xuất" → [R✓] assert tên + logout button.
- **Smart Wait**: `wait_for_flutter(page, text="Đăng xuất")` thay thế hoàn toàn `time.sleep`.

### TC-02 — Đăng nhập thất bại — sai mật khẩu

- **Input**: Email đúng + mật khẩu `"wrongpassword"`
- **Expected**: Vẫn ở trang đăng nhập; không có "Đăng xuất" trong semantics.
- **Assertion chi tiết (B3)**: Kiểm tra cả `not_logged_in` VÀ `still_on_login`.

### TC-03 — Đăng nhập thất bại — trống hai trường

- **Input**: Không nhập gì — click "Đăng nhập" ngay.
- **Expected**: Vẫn ở trang đăng nhập (Flutter ngăn submit khi trường trống).

### TC-04 — Tìm sách theo tên "Flutter"

- **Input**: Keyword `"Flutter"` vào ô tìm kiếm.
- **Expected**: Ít nhất 1 book card có `aria-label` chứa "Flutter".
- **Smart Wait**: `wait_for_flutter(page, text="Flutter")`.

### TC-05 — Tìm sách — không có kết quả

- **Input**: Keyword `"xyz_khong_ton_tai_99999"`
- **Expected**: `count == 0` book cards với `aria-label*="Mã: BOOK"`.

### TC-06 — Lọc theo thể loại "Công nghệ"

- **Input**: `"Công nghệ"` vào ô lọc thể loại.
- **Expected**: Tất cả book cards đều có `"Công nghệ"` trong `aria-label`.
- **Assertion chi tiết (B3)**: Vòng lặp kiểm tra từng sách.

### TC-07 — Tìm sách theo tác giả

- **Input**: `"Nguyễn Minh Đức"`
- **Expected**: Ít nhất 1 element có `aria-label` chứa tên tác giả.

### TC-08 — Mượn sách

- **Account**: `dam.tran@email.com` (chưa mượn sách nào).
- **Expected**: Sau khi xác nhận dialog "Mượn", sách chuyển sang "Đang mượn".

### TC-09 — Xem danh sách sách đang mượn

- **Account**: `ba.nguyen@email.com` (có BOOK003 mượn).
- **Expected**: Tab "Mượn / Trả" hiển thị "Đang mượn" và/hoặc nút "Trả sách".

### TC-10 — Trả sách

- **Account**: `ba.nguyen@email.com` (có BOOK003 để trả).
- **Expected**: Sau khi click "Trả sách", nút "Trả sách" biến mất hoặc có thông báo thành công.

### TC-11 — Đăng xuất

- **Expected**: "Đăng nhập" button + "Email" input field xuất hiện sau logout.
- **Assertion chi tiết (B3)**: Kiểm tra cả `has_login_btn` VÀ `no_logout_btn`.

### TC-12 — Chuyển ngôn ngữ sang English

- **Expected**: Ít nhất 1 trong `["Logout", "Borrow", "Library", "Search", "Return", "Available"]` xuất hiện.
- **Fix**: Dùng `wait_for_timeout(3000)` thay vì `wait_for_flutter(text="Logout")` vì Flutter CanvasKit không expose "Logout" ngay.

---

## 3. Bonus features thực hiện

| Bonus | Mô tả | File |
|-------|-------|------|
| **B1** | 4 test case mới: search count, filter category, language toggle back, parametrize scenarios | `test_search.py`, `test_general.py`, `test_login.py` |
| **B2** | `@pytest.mark.parametrize` cho TC-02/TC-03 + invalid_email | `test_login.py` |
| **B3** | Assertion chi tiết cho mọi TC — text cụ thể, count, aria-label | Tất cả files |
| **B4** | REPORT.md này mô tả từng TC và nhận xét | `REPORT.md` |

---

## 4. Kỹ thuật xử lý Flutter Web (CanvasKit)

**Thách thức**: Flutter Web dùng `<canvas>` — không có HTML DOM thông thường.

**Giải pháp đã dùng**:
1. `enable_flutter_semantics(page)` — bật Accessibility Tree, tạo các `<flt-semantics>` ẩn
2. `flutter_fill(page, label, value)` — nhập text qua `aria-label`
3. `flutter_click_button(page, text)` — click button qua `flt-semantics[role="button"]:has-text(...)`
4. `wait_for_flutter(page, text="...")` — **Smart Wait** thay vì `time.sleep()`
5. `page.wait_for_timeout(N)` — dùng khi không có expected text cụ thể (TC-05, TC-12)

---

## 5. Issues phát hiện trong hệ thống

| Issue | TC | Mức độ |
|-------|----|--------|
| Không rõ thông báo lỗi khi đăng nhập sai | TC-02, TC-03 | Low — UX |
| Flutter EN UI không expose "Logout" ngay trong Semantics Tree | TC-12 | Info |
| BOOK003 của ba.nguyen có trạng thái "quá hạn" | TC-09, TC-10 | Info |

---

## 6. Khai báo sử dụng AI

Nhóm sử dụng **Claude (Anthropic)** để hỗ trợ viết automation test code.

Dùng cho: phân tích ASSIGNMENT.md, viết 12 TC + 4 bonus TC, áp dụng Smart Wait pattern, debug CI failures (action versions, Flutter semantics issues), và viết REPORT.md. Nhóm đã kiểm tra lại từng test, điều chỉnh account strategy cho TC-08/09/10, xác nhận CI #19 đạt 18/18 passed.
