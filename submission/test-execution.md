# Test Execution Report — STQA Group 13

| Field | Value |
|-------|-------|
| **Group** | Group 13 |
| **Execution Date** | 27/05/2026 |
| **Tester** | Group 13 |
| **System Under Test** | https://stqa.rbc.vn |
| **Browser** | Chrome (Flutter Web — CanvasKit rendering) |
| **Reference** | test-cases.md (34 TCs) |

---

## Execution Summary

| Metric | Value |
|--------|-------|
| Total Test Cases Executed | 34 |
| **PASS** | **26** |
| **FAIL** | **8** |
| Blocked | 0 |
| Not Run | 0 |
| **Pass Rate** | **76.5%** |

---

## Detailed Results

### REQ-01: User Login

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-01-01 | Valid librarian login | `librarian@library.com` / `admin123` | Redirect to home, role shown | Redirected to home. AppBar shows "Nguyễn Thủ Thư (Thủ thư)". Three tabs (Sách, Mượn/Trả, Thành viên) visible. | **PASS** | — |
| TC-01-02 | Valid member login | `biet.hoang@email.com` / `password123` | Redirect, member role shown | Redirected to home. AppBar shows "Hoàng Cá Biệt (Thành viên)". Only Sách and Mượn/Trả tabs shown. | **PASS** | — |
| TC-01-03 | Unregistered email | `ghost@nowhere.com` / `pass9999` | "User not found" error | Toast displayed: "Không tìm thấy thành viên." Page did not navigate. | **PASS** | — |
| TC-01-04 | Wrong password | `librarian@library.com` / `wrongpass` | "Wrong password" error | Toast: "Mật khẩu không đúng." No navigation. | **PASS** | — |
| TC-01-05 | Both fields empty | `""` / `""` | "Please fill in fields" error | Toast: "Vui lòng nhập email và mật khẩu." No navigation. | **PASS** | — |

### REQ-02: View Book List

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-02-01 | Librarian sees full book list | — | ≥18 books with full details | All 20 books displayed. Each shows title, author, genre, year, and status. BOOK003 shows "Đang mượn", BOOK007 shows "Thất lạc". | **PASS** | — |
| TC-02-02 | Member sees no Members tab | Logged in as MEM006 | Only Sách and Mượn/Trả tabs | After member login: no "Thành viên" tab in navigation. Only 2 tabs visible. | **PASS** | — |
| TC-02-03 | Lost book shown in list | — | BOOK007 displayed with "Thất lạc" status | BOOK007 "Kinh tế vi mô" visible in list with status "Thất lạc" (Lost). Correctly displayed. | **PASS** | — |

### REQ-03: Search & Filter Books

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-03-01 | Case-insensitive title search | `"python"` | Same results as "Python" | BOOK002 and BOOK010 (Python books) displayed. Result identical to uppercase search. | **PASS** | — |
| TC-03-02 | Search — no results | `"AAAAA999"` | Empty list, "no results" message | "Không tìm thấy sách nào." displayed. Empty list. No crash. | **PASS** | — |
| TC-03-03 | Filter by genre | `"Kinh tế"` | Only Economics books | BOOK007, BOOK014, BOOK015 shown. All have genre "Kinh tế". No other genre books visible. | **PASS** | — |
| TC-03-04 | Search by author name | `"Lê Thị Hoa"` | Books by Lê Thị Hoa displayed | BOOK003 "Kiểm thử phần mềm nhập môn" displayed. No irrelevant books shown. | **PASS** | — |
| TC-03-05 | Filter by English category in EN mode | `"Technology"` (EN mode) | "Technology" books displayed | **UI set to EN mode. Typed "Technology" in category filter. Result: "No books found."** Books with category "Công nghệ" exist but are not matched. The placeholder hint "e.g. Technology" implies English filtering is supported, but it is not. | **FAIL** | DEFECT-07 |

### REQ-04: Borrow Book

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-04-01 | Borrow first book (0→1) | BOOK002 / MEM006 | Success; BOOK002 → Borrowed | Toast "Mượn sách thành công!" shown. BOOK002 changed to "Đang mượn". | **PASS** | — |
| TC-04-02 | Borrow second book (1→2) | BOOK005 / MEM006 | Success; BOOK005 → Borrowed | Toast "Mượn sách thành công!" shown. BOOK005 changed to "Đang mượn". | **PASS** | — |
| TC-04-03 | Borrow third book — at limit (2→3) | BOOK008 / MEM006 | Success; BOOK008 → Borrowed | Toast "Mượn sách thành công!" shown. BOOK008 changed to "Đang mượn". MEM006 now at 3-book limit. | **PASS** | — |
| TC-04-04 | Borrow 4th book — over limit | BOOK010 / MEM006 | **Rejected.** Error shown. BOOK010 stays "Có sẵn". | **System accepted the borrow request.** Toast "Mượn sách thành công!" shown. BOOK010 changed to "Đang mượn". MEM006 now has 4 active borrows — exceeds limit. | **FAIL** | DEFECT-01 |
| TC-04-05 | Suspended member cannot borrow | MEM004 (`cu.le@email.com`) | No "+" button shown | After login as MEM004: "+" borrow button not rendered for any book. Cannot initiate borrow. Suspension is enforced at UI level. | **PASS** | — |
| TC-04-06 | Cannot borrow already-borrowed book | BOOK003 (status: Borrowed) | No "+" button for BOOK003 | BOOK003 displayed with "Đang mượn" badge. No "+" button visible. Cannot open borrow dialog. | **PASS** | — |
| TC-04-07 | Member with overdue book exceeds borrow limit | MEM006: 3 "Đang mượn" + 1 "Quá hạn" (BR003); attempt BOOK009 | **Rejected.** Overdue books count toward limit. | **Librarian ran "Kiểm tra sách quá hạn" → BR003 flagged as "Quá hạn". Member list shows MEM006 "Đang mượn: 3 sách". As MEM006, tapped "+" on BOOK009. Borrow dialog appeared. Clicked Borrow. Toast: "Book borrowed successfully!" — system allowed a 4th active borrow despite 4 total unreturned books.** | **FAIL** | DEFECT-08 |

### REQ-05: Return Book

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-05-01 | Return book successfully | Record: BR003 | Success toast; BR003 → Returned; BOOK013 → Available | Toast "Trả sách thành công." shown. BR003 status changed to "Đã trả". BOOK013 status changed to "Có sẵn". | **PASS** | — |
| TC-05-02 | Return overdue book — check for warning | Record: BR001 (due 15/09/2024, overdue) | Return success + overdue warning shown | Toast showed only "Trả sách thành công." **No overdue warning or alert was displayed.** BR001 status changed to "Đã trả" without any overdue annotation. | **FAIL** | DEFECT-03 |

### REQ-06: Overdue Handling

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-06-01 | Overdue check updates record statuses | — | BR001, BR003 → "Quá hạn" | Clicked "Kiểm tra sách quá hạn". BR001 and BR002 changed to "Quá hạn". Toast showed overdue count. | **PASS** | — |
| TC-06-02 | Member sees only own overdue record | MEM002 login | Only MEM002's BR001 shown | Logged in as MEM002. "Mượn / Trả" tab shows only BR001 (status: Quá hạn). No other member records visible. | **PASS** | — |

### REQ-07: Member Management

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-07-01 | Add valid new member | Name: `Tran Van New`, Email: `tranvannew@test.com`, Phone: `0923100001` | Success. New member ID assigned. | Toast "Thêm thành viên thành công! Mã: MEM00X". New member visible in list with correct data. | **PASS** | — |
| TC-07-02 | Add member — invalid email (no TLD dot) | Email: `user@nodot` | Rejected. Error message shown. | **System accepted the invalid email.** Toast "Thêm thành viên thành công!" displayed. Member was created with email `user@nodot` stored in the database. | **FAIL** | DEFECT-02 |
| TC-07-03 | Add member — duplicate email | Email: `ba.nguyen@email.com` (existing) | Rejected. Clear "already exists" error. | System rejected submission but displayed: **"Email không hợp lệ."** This message implies a format error, not a duplicate — misleading to the user. | **FAIL** | DEFECT-04 |
| TC-07-04 | Add member — email missing "@" | Email: `usernodomain.com` | Rejected. Validation error. | System rejected and displayed "Email không hợp lệ." No member created. The missing "@" is detected by client-side validation correctly. | **PASS** | — |
| TC-07-05 | Member cannot access member management | MEM006 logged in | No Add Member button. No Members tab. | After member login: no "Thành viên" tab in navigation. No add-member icon in AppBar. Role restriction enforced correctly. | **PASS** | — |
| TC-07-06 | Add member — empty phone field | Name: `Test Empty Phone`, Email: `emptyphone@test.com`, Phone: `""` | Phone-specific error message | **Left Phone Number blank. Clicked Submit. Error displayed: "Email không hợp lệ." — an email error for a phone field.** No phone-specific message shown. | **FAIL** | DEFECT-05 |
| TC-07-07 | Add member — non-numeric phone | Name: `Test Bad Phone`, Email: `badphone@test.com`, Phone: `abcdefghij` | "Phone must contain digits only" or equivalent | **Entered "abcdefghij" in phone field. Clicked Submit. Error displayed: "Email không hợp lệ." — the same incorrect error as TC-07-06. System rejects input but uses wrong error message.** | **FAIL** | DEFECT-06 |

### REQ-08: Borrow Record Lookup

| TC ID | Objective | Input | Expected | Actual Result | Status | Defect |
|-------|-----------|-------|----------|---------------|--------|--------|
| TC-08-01 | Librarian views all records | — | All BR001–BR005 visible | All 5 borrow records visible in "Mượn / Trả" tab with full details: record ID, book title, member name, dates, and status. | **PASS** | — |
| TC-08-02 | Librarian searches by member ID | Member ID: `MEM006` | MEM006's records returned | Entered MEM006 in search. MEM006's borrow records returned correctly. Records from other members not displayed. | **PASS** | — |
| TC-08-03 | Member sees only own records | MEM006 logged in | Only MEM006's records visible | After login as MEM006: only MEM006's records visible in "Mượn / Trả". No member ID search field shown. Other members' records hidden. | **PASS** | — |

---

## Defect Summary

| Defect ID | Severity | TC Found | Description |
|-----------|----------|----------|-------------|
| DEFECT-01 | Critical | TC-04-04 | System allows borrowing beyond the 3-book limit — borrow count not enforced |
| DEFECT-02 | High | TC-07-02 | Email without dot-in-domain (e.g., `user@nodot`) accepted and stored |
| DEFECT-03 | Medium | TC-05-02 | No overdue warning displayed when a librarian returns an overdue book |
| DEFECT-04 | Low | TC-07-03 | Duplicate email rejection shows "Email không hợp lệ." instead of "Email already registered" |
| DEFECT-05 | Medium | TC-07-06 | Empty phone field shows "Email không hợp lệ." — wrong field error message |
| DEFECT-06 | Medium | TC-07-07 | Non-numeric phone shows "Email không hợp lệ." — wrong field error message |
| DEFECT-07 | Low | TC-03-05 | English category names in filter produce no results — placeholder hint is misleading |
| DEFECT-08 | High | TC-04-07 | Overdue books excluded from borrow count — member can exceed 3-book limit |

---

## Coverage by Requirement

| REQ | TCs Run | PASS | FAIL | Status |
|-----|---------|------|------|--------|
| REQ-01 | 5 | 5 | 0 | ✅ All Pass |
| REQ-02 | 3 | 3 | 0 | ✅ All Pass |
| REQ-03 | 5 | 4 | 1 (TC-03-05) | ⚠️ DEFECT-07 |
| REQ-04 | 7 | 5 | 2 (TC-04-04, TC-04-07) | ⚠️ DEFECT-01, DEFECT-08 |
| REQ-05 | 2 | 1 | 1 (TC-05-02) | ⚠️ DEFECT-03 |
| REQ-06 | 2 | 2 | 0 | ✅ All Pass |
| REQ-07 | 7 | 3 | 4 (TC-07-02, 03, 06, 07) | ⚠️ DEFECT-02, 04, 05, 06 |
| REQ-08 | 3 | 3 | 0 | ✅ All Pass |
| **Total** | **34** | **26** | **8** | **8/8 REQ covered** |
