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

**Tổng: 12/12 test case hoàn thành.**

---

## 2. Mô tả chi tiết từng Test Case

### TC-01 — Đăng nhập thành công

- **Mục đích**: Xác nhận hệ thống chấp nhận thông tin đăng nhập hợp lệ.
- **Input**: `ba.nguyen@email.com` / `password123`
- **Expected**: Giao diện chính xuất hiện, nút "Đăng xuất" hiển thị, tên người dùng "Nguyễn Học Bá" có mặt.
- **Pattern**: RIPR Model — [R] truy cập login → [I] nhập credentials → [P] chờ "Đăng xuất" → [R✓] assert tên + logout button.
- **Smart Wait**: `wait_for_flutter(page, text="Đăng xuất")` — thay thế hoàn toàn `time.sleep`.

### TC-02 — Đăng nhập thất bại — sai mật khẩu

- **Mục đích**: Hệ thống từ chối khi mật khẩu sai.
- **Input**: Email đúng + mật khẩu `"wrongpassword"`
- **Expected**: Vẫn ở trang đăng nhập; không có "Đăng xuất" trong semantics.
- **Assertion chi tiết (B3)**: Kiểm tra cả `not_logged_in` VÀ `still_on_login`.

### TC-03 — Đăng nhập thất bại — trống hai trường

- **Mục đích**: Hệ thống không cho phép đăng nhập khi bỏ trống cả email lẫn mật khẩu.
- **Input**: Không nhập gì — click "Đăng nhập" ngay.
- **Expected**: Vẫn ở trang đăng nhập.
- **Observation**: Hệ thống Flutter Web ngăn chặn submit khi trường trống — không có navigation xảy ra.

### TC-04 — Tìm sách theo tên "Flutter"

- **Mục đích**: Tính năng tìm kiếm theo tên sách hoạt động đúng.
- **Input**: Keyword `"Flutter"` vào ô tìm kiếm.
- **Expected**: Ít nhất 1 book card có `aria-label` chứa "Flutter".
- **Smart Wait**: `wait_for_flutter(page, text="Flutter")` — chờ Semantics Tree cập nhật sau khi Flutter rerender.

### TC-05 — Tìm sách — không có kết quả

- **Mục đích**: Hệ thống xử lý đúng khi không tìm thấy sách.
- **Input**: Keyword `"xyz_khong_ton_tai_99999"`
- **Expected**: `count == 0` book cards với `aria-label*="Mã: BOOK"`.
- **Note**: Dùng `page.wait_for_timeout(2000)` thay vì wait_for_flutter vì không có text cụ thể để đợi trong trường hợp "không có kết quả".

### TC-06 — Lọc theo thể loại "Công nghệ"

- **Mục đích**: Bộ lọc thể loại chỉ hiển thị đúng loại sách.
- **Input**: `"Công nghệ"` vào ô lọc thể loại.
- **Expected**: Tất cả book cards đều có `"Công nghệ"` trong `aria-label`.
- **Assertion chi tiết (B3)**: Vòng lặp kiểm tra từng sách, log tên sách nếu sai thể loại.

### TC-07 — Tìm sách theo tác giả

- **Mục đích**: Ô tìm kiếm hoạt động cho cả tên tác giả (không chỉ tên sách).
- **Input**: `"Nguyễn Minh Đức"`
- **Expected**: Ít nhất 1 element có `aria-label` chứa tên tác giả.

### TC-08 — Mượn sách

- **Mục đích**: Quy trình mượn sách hoàn chỉnh (click → dialog → xác nhận → trạng thái thay đổi).
- **Account**: `dam.tran@email.com` (chưa mượn sách nào — đảm bảo có sách Có sẵn để mượn).
- **Expected**: Sau khi xác nhận dialog "Mượn", sách chuyển sang "Đang mượn".
- **Note**: Test hardcode tài khoản `dam.tran` thay vì dùng `test_config` vì `ba.nguyen` (account CI mặc định) đã có sách mượn quá hạn.

### TC-09 — Xem danh sách sách đang mượn

- **Mục đích**: Tab "Mượn / Trả" hiển thị đúng danh sách đang mượn.
- **Account**: `ba.nguyen@email.com` (có BOOK003 mượn trong initial state).
- **Expected**: Tab "Mượn / Trả" hiển thị "Đang mượn" và/hoặc nút "Trả sách".
- **Smart Wait**: `wait_for_flutter(page, text="Đang mượn")` sau khi click tab.

### TC-10 — Trả sách

- **Mục đích**: Quy trình trả sách hoạt động đúng, trạng thái cập nhật sau khi trả.
- **Account**: `ba.nguyen@email.com` (có BOOK003 để trả).
- **Expected**: Sau khi click "Trả sách", nút "Trả sách" biến mất hoặc có thông báo thành công.
- **Fallback**: Nếu có dialog xác nhận "Trả", test tự động click xác nhận.

### TC-11 — Đăng xuất

- **Mục đích**: Nút đăng xuất hoạt động và trả user về màn hình login.
- **Expected**: "Đăng nhập" button + "Email" input field xuất hiện sau logout.
- **Assertion chi tiết (B3)**: Kiểm tra cả `has_login_btn` VÀ `no_logout_btn`.

### TC-12 — Chuyển ngôn ngữ sang English

- **Mục đích**: Nút "EN" chuyển toàn bộ giao diện sang tiếng Anh.
- **Expected**: Ít nhất 1 trong các từ `["Logout", "Borrow", "Library", "Search", "Return", "Available"]` xuất hiện.
- **Smart Wait**: `wait_for_flutter(page, text="Logout")` thay vì `time.sleep(2)`.

---

## 3. Bonus features thực hiện

| Bonus | Mô tả | File |
|-------|-------|------|
| **B1** | Thêm 4 test case mới (search recovery, language toggle back, search clear) | `test_search.py`, `test_general.py` |
| **B2** | `@pytest.mark.parametrize` gộp TC-02, TC-03, và thêm case `invalid_email` | `test_login.py` |
| **B3** | Assertion chi tiết cho mọi TC — kiểm tra cả text cụ thể, count, aria-label | Tất cả files |
| **B4** | REPORT.md với mô tả từng TC và nhận xét | `submission/REPORT.md` |

---

## 4. Kỹ thuật xử lý Flutter Web (CanvasKit)

**Thách thức**: Flutter Web dùng `<canvas>` để render — không có HTML DOM thông thường. Playwright không thể `page.get_by_text()` trực tiếp.

**Giải pháp đã dùng**:
1. `enable_flutter_semantics(page)` — bật Accessibility Tree, tạo các `<flt-semantics>` ẩn
2. `flutter_fill(page, label, value)` — nhập text qua `aria-label`, xử lý hidden input của Flutter
3. `flutter_click_button(page, text)` — click button qua `flt-semantics[role="button"]:has-text(...)`
4. `wait_for_flutter(page, text="...")` — **Smart Wait** thay vì `time.sleep()`, chờ Semantics Tree cập nhật
5. Re-enable semantics sau các thao tác lớn (click tab, dialog) vì Flutter có thể rebuild widget tree

**Tránh được**:
- `time.sleep()` (chỉ dùng `page.wait_for_timeout(2000)` duy nhất ở TC-05 vì không có expected text)
- `page.get_by_text()` (không có DOM thông thường)
- XPath (không ổn định với Flutter Canvas)

---

## 5. Issues phát hiện trong hệ thống

| Issue | TC | Mức độ |
|-------|----|--------|
| Không rõ thông báo lỗi khi đăng nhập sai | TC-02, TC-03 | Low — UX |
| BOOK003 của ba.nguyen có trạng thái "quá hạn" trong initial state | TC-09, TC-10 | Info |
| Việc trả sách có thể cần dialog xác nhận (không chắc) | TC-10 | Info |

---

## 6. Khai báo sử dụng AI

Nhóm sử dụng **Claude (Anthropic)** để hỗ trợ viết automation test code.

AI được dùng để:
- Phân tích yêu cầu từ ASSIGNMENT.md và test-accounts.md
- Viết code cho 12 test cases và 4 bonus test cases
- Áp dụng Smart Wait pattern thay thế `time.sleep()`
- Viết REPORT.md này

Nhóm đã kiểm tra lại từng test case, điều chỉnh account strategy cho TC-08/09/10, và xác nhận logic assertion là đúng với yêu cầu đề bài.
