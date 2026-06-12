# Test Cases — STQA Group 13

| Field | Value |
|-------|-------|
| **Group** | Group 13 |
| **Date** | 27/05/2026 |
| **System Under Test** | https://stqa.rbc.vn (Library Management System) |
| **Reference** | SRS v1.0 |
| **Total Test Cases** | 34 |

---

## Part 1 — Input Domain Modeling (IDM)

*Before designing test cases, the input domain for each requirement is partitioned into equivalence classes.*

### REQ-01: User Login

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Email field state | Filled with registered email | `librarian@library.com` | Login proceeds |
| | Filled with unregistered email | `ghost@nowhere.com` | Error: user not found |
| | Empty | `""` | Error: fields required |
| Password field state | Correct password | `admin123` | Login proceeds |
| | Wrong password | `pass9999` | Error: wrong password |
| | Empty | `""` | Error: fields required |
| Only one field empty | Only email empty | email=`""`, pw=`admin123` | Error: fields required |
| | Only password empty | email=`librarian@library.com`, pw=`""` | Error: fields required |

### REQ-02: View Book List

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Logged-in role | Librarian | `librarian@library.com` | All books + Members tab visible |
| | Member | `biet.hoang@email.com` | Books & Borrow tabs only; no Members tab |
| Book status in list | Available | BOOK002 | Status badge = "Có sẵn" |
| | Borrowed | BOOK003 | Status badge = "Đang mượn" |
| | Lost | BOOK007 | Status badge = "Thất lạc" |

### REQ-03: Search & Filter Books

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Search keyword | Matches book title | `"Python"` | Books with "Python" in title shown |
| | Matches author name | `"Lê Thị Hoa"` | Books by that author shown |
| | No match | `"AAAAA999"` | Empty list, no error |
| Keyword case | All lowercase | `"python"` | Same results as "Python" |
| | All uppercase | `"PYTHON"` | Same results as "Python" |
| Genre filter | Valid genre (Vietnamese) | `"Kinh tế"` | Only Economics books shown |
| | Non-existent genre | `"Science Fiction"` | Empty list |
| | English genre name in EN mode | `"Technology"` | Empty list (localization bug — stored as "Công nghệ") |

### REQ-04: Borrow Book — BVA on Borrow Count + Decision Table

**Boundary Values for borrow count (limit = 3):**

| BV Point | Books Currently Borrowed | Action | Expected |
|----------|--------------------------|--------|----------|
| Min | 0 | Borrow | ✅ Allowed |
| Min+1 | 1 | Borrow | ✅ Allowed |
| Nominal | 2 | Borrow | ✅ Allowed |
| Max (at limit) | 3 | Borrow | ❌ Rejected — limit reached |
| Max+1 (over limit) | 4+ | Borrow | ❌ Rejected (system should already have blocked at 3) |
| Overdue escape | 3 active + 1 overdue | Borrow | ❌ Rejected — overdue books must also count toward limit |

**Decision Table — Borrow Book Conditions:**

| Rule | Book Available? | Member Active? | Count < 3? | Result |
|------|:--------------:|:-------------:|:----------:|--------|
| R1 | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Borrow succeeds |
| R2 | ✅ Yes | ✅ Yes | ❌ No | ❌ Rejected: limit exceeded |
| R3 | ✅ Yes | ❌ No (Suspended/Expired) | ✅ Yes | ❌ Rejected: account inactive |
| R4 | ❌ No (Borrowed/Lost) | ✅ Yes | ✅ Yes | ❌ Rejected: book unavailable |
| R5 | ❌ No | ❌ No | ❌ No | ❌ Rejected (all conditions fail) |

### REQ-05: Return Book

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Book return status | On time | BR004 (not overdue) | Success toast, no warning |
| | Overdue | BR001 (due 15/09/2024) | Success toast + overdue alert |

### REQ-06: Overdue Detection

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Record due date vs today | Past due date | BR001 (due 15/09/2024) | Status → "Quá hạn" after check |
| | Still within due date | BR (due in future) | Status unchanged |
| User role viewing overdue | Librarian | All overdue records visible | Can see all |
| | Member | Only own overdue records | Others hidden |

### REQ-07: Member Management

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Email format | Valid (`user@domain.com`) | `newmember@test.com` | Member created |
| | Invalid — missing TLD (`user@domain`) | `user@nodot` | Rejected |
| | Duplicate (already registered) | `ba.nguyen@email.com` | Rejected with clear message |
| | Missing `@` symbol | `usernodomain.com` | Rejected |
| Name field | Filled | `"Nguyen Van A"` | Proceeds |
| | Empty | `""` | Rejected |
| Phone field | Valid digits | `0934567890` | Member created |
| | Empty | `""` | Rejected with phone-specific error message |
| | Non-numeric | `"abcde"` | Rejected with phone-specific error message |
| Access control | Librarian | Can see Members tab | ✅ |
| | Member | No Members tab | ✅ Restricted |

### REQ-08: Borrow Record Lookup

| Characteristic | Partition | Representative Value | Expected Outcome |
|---|---|---|---|
| Viewer role | Librarian | All 5 records visible | All shown |
| | Member | Only own records | Filtered |
| Member ID search | Valid ID with records | `MEM006` | Returns MEM006's records |
| | Valid ID no records | `MEM999` | Empty list, no crash |
| Search field visibility | For Librarian | Search box present | ✅ |
| | For Member | No search box | ✅ Restricted |

---

## Part 2 — Test Cases

*Naming convention: TC-[REQ#]-[Sequence] — e.g., TC-01-03 = REQ-01, 3rd test case.*

### REQ-01: User Login (5 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-01-01 | Login succeeds with valid librarian credentials | System at login page | 1. Enter email. 2. Enter password. 3. Click Login. | Email: `librarian@library.com`, PW: `admin123` | Redirected to home. AppBar shows "Nguyễn Thủ Thư (Thủ thư)". Three nav tabs visible. | EP |
| TC-01-02 | Login succeeds with valid member credentials | System at login page | 1. Enter member email. 2. Enter password. 3. Click Login. | Email: `biet.hoang@email.com`, PW: `password123` | Redirected to home. AppBar shows role "(Thành viên)". Only "Sách" and "Mượn / Trả" tabs. | EP |
| TC-01-03 | Login fails — unregistered email | System at login page | 1. Enter unknown email. 2. Enter any password. 3. Click Login. | Email: `ghost@nowhere.com`, PW: `pass9999` | Error toast: "Không tìm thấy thành viên." or equivalent. No navigation. | EP |
| TC-01-04 | Login fails — wrong password | System at login page | 1. Enter valid email. 2. Enter wrong password. 3. Click Login. | Email: `librarian@library.com`, PW: `wrongpass` | Error toast: "Mật khẩu không đúng." No navigation. | EP |
| TC-01-05 | Login fails — both fields empty | System at login page | 1. Leave both fields empty. 2. Click Login. | Email: `""`, PW: `""` | Error message: "Vui lòng nhập email và mật khẩu." No navigation. | EP |

### REQ-02: View Book List (3 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-02-01 | Librarian sees complete book list with all details | Logged in as Librarian | 1. Navigate to "Sách" tab. 2. Observe list. | — | Full list displayed (≥18 books). Each row shows: title, author, genre, year, status. All status types visible. | EP |
| TC-02-02 | Member cannot see Members tab | Logged in as `biet.hoang@email.com` | 1. Observe navigation tabs. | — | Only "Sách" and "Mượn / Trả" tabs are shown. No "Thành viên" tab. | EP |
| TC-02-03 | Lost book is correctly shown in book list | Logged in as Librarian | 1. Scroll through book list to find BOOK007. | — | BOOK007 "Kinh tế vi mô" is visible with status "Thất lạc" (Lost). Status displayed correctly. | EP |

### REQ-03: Search & Filter Books (4 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-03-01 | Search by title keyword — case-insensitive | Logged in, "Sách" tab | 1. Type keyword in search box. | `"python"` (lowercase) | Books with "Python" in title displayed. Result same as searching "PYTHON". | EP |
| TC-03-02 | Search returns empty for non-existent keyword | Logged in, "Sách" tab | 1. Type non-existent keyword. | `"AAAAA999"` | Message "Không tìm thấy sách nào." List is empty. No crash. | EP |
| TC-03-03 | Filter by genre shows correct subset | Logged in, "Sách" tab | 1. Type genre name in filter field. | `"Kinh tế"` | Only Economics books shown (e.g., BOOK007, BOOK014, BOOK015). | EP |
| TC-03-04 | Search by author name returns correct results | Logged in, "Sách" tab | 1. Type author name in search box. | `"Lê Thị Hoa"` | BOOK003 "Kiểm thử phần mềm nhập môn" by Lê Thị Hoa displayed. No unrelated books. | EP |
| TC-03-05 | Filter by English category name returns no results (i18n mismatch) | Logged in, EN mode, "Books" tab | 1. Set UI to English. 2. Click category filter field. 3. Type `Technology`. | `"Technology"` (EN mode) | **FAIL — DEFECT-07:** "No books found." even though books with category "Công nghệ" exist. The hint "e.g. Technology" is misleading. | EP |

### REQ-04: Borrow Book (6 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-04-01 | Borrow first book (BVA: 0 books → 1) | Logged in as MEM006 (`biet.hoang@email.com`), 0 active borrows | 1. On "Sách" tab, click "+" next to BOOK002. 2. Confirm. | Book: BOOK002, Member: MEM006 | Toast "Mượn sách thành công!". BOOK002 → "Đang mượn". | EP, BVA |
| TC-04-02 | Borrow second book (BVA: 1 → 2) | MEM006 has 1 active borrow | 1. Click "+" next to BOOK005. 2. Confirm. | Book: BOOK005, Member: MEM006 | Toast "Mượn sách thành công!". BOOK005 → "Đang mượn". | BVA |
| TC-04-03 | Borrow third book — at limit (BVA: 2 → 3) | MEM006 has 2 active borrows | 1. Click "+" next to BOOK008. 2. Confirm. | Book: BOOK008, Member: MEM006 | Toast "Mượn sách thành công!". BOOK008 → "Đang mượn". Member now at 3-book limit. | BVA |
| TC-04-04 | Borrow 4th book — exceeds limit (BVA: over limit) | MEM006 has 3 active borrows | 1. Click "+" next to BOOK010. 2. Confirm in dialog. | Book: BOOK010, Member: MEM006 | **System rejects borrow.** Error: "Bạn đã đạt giới hạn 3 sách." BOOK010 remains "Có sẵn". | BVA, R2 |
| TC-04-05 | Suspended member cannot borrow | Logged in as MEM004 (`cu.le@email.com`) | 1. Navigate to "Sách" tab. 2. Observe "+" button on available books. | Member: MEM004 (Tạm ngưng) | No "+" borrow button visible / clickable for any book. Cannot initiate borrow. | EP, R3 |
| TC-04-06 | Cannot borrow a book that is already borrowed | Logged in as any active member | 1. Locate BOOK003 (status: "Đang mượn"). 2. Observe borrow button. | Book: BOOK003 | No "+" button shown for BOOK003. Cannot initiate borrow dialog. | EP, R4 |
| TC-04-07 | Member with overdue book — borrow limit bypass check | MEM006 logged in. MEM006 has 3 "Đang mượn" (BR006/07/08) + 1 "Quá hạn" (BR003). | 1. As Librarian, run "Kiểm tra sách quá hạn" to set BR003 → "Quá hạn". 2. Log in as MEM006. 3. Attempt to borrow BOOK009 (Available). 4. Confirm dialog. | Member: MEM006, Book: BOOK009 | **FAIL — DEFECT-08:** System shows borrow dialog and confirms "Book borrowed successfully!" MEM006 now holds 4 active + 1 overdue. Overdue books should count toward the 3-book limit. | BVA, EP |

### REQ-05: Return Book (2 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-05-01 | Return a borrowed book successfully | Logged in as Librarian. BR003 is "Đang mượn". | 1. Go to "Mượn / Trả" tab. 2. Find BR003. 3. Click "Trả sách". | Record: BR003 | Toast: "Trả sách thành công." BR003 status → "Đã trả". BOOK013 → "Có sẵn". | EP |
| TC-05-02 | Return an overdue book — overdue warning check | Logged in as Librarian. BR001 has past-due date (15/09/2024). | 1. Click "Kiểm tra sách quá hạn". 2. Locate BR001 (Overdue). 3. Click "Trả sách". | Record: BR001 | Return success + **overdue warning displayed** (e.g., "Sách này đã quá hạn X ngày"). BR001 → "Đã trả". | EP |

### REQ-06: Overdue Handling (2 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-06-01 | Overdue check button updates record statuses | Logged in as Librarian. BR001 (due 15/09/2024) and BR003 (due 15/10/2024) are "Đang mượn". | 1. Go to "Mượn / Trả" tab. 2. Click "Kiểm tra sách quá hạn". | — | BR001 and BR003 statuses updated to "Quá hạn". Toast shows count of overdue records. | EP |
| TC-06-02 | Member views only their own overdue record | Logged in as MEM002 (`ba.nguyen@email.com`). BR001 is overdue (MEM002's record). | 1. Go to "Mượn / Trả" tab. | — | Only BR001 (MEM002) shown with status "Quá hạn". No other members' records visible. | EP |

### REQ-07: Member Management (5 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-07-01 | Add new member with valid data | Logged in as Librarian | 1. Click Add Member icon. 2. Fill all fields with valid data. 3. Submit. | Name: `Tran Van New`, Email: `tranvannew@test.com`, Phone: `0923100001` | Success toast with new member ID (e.g., MEM00X). Member appears in list. | EP |
| TC-07-02 | Add member — invalid email (no dot in domain) | Logged in as Librarian, Add Member form open | 1. Enter email without dot in domain. 2. Fill other fields validly. 3. Submit. | Email: `user@nodot`, Name: `Test Invalid`, Phone: `0900000099` | System rejects. Error message. No member created. | EP, BVA |
| TC-07-03 | Add member — duplicate email | Logged in as Librarian | 1. Enter email already used by existing member. 2. Fill other fields. 3. Submit. | Email: `ba.nguyen@email.com` (existing: MEM002) | System rejects. Error should clearly state the email is already registered — NOT an "invalid email" message. | EP |
| TC-07-04 | Add member — email without "@" symbol | Logged in as Librarian | 1. Enter email missing "@". 2. Other fields valid. 3. Submit. | Email: `usernodomain.com`, Name: `No At Sign`, Phone: `0912111222` | System rejects with validation error. No member created. | EP, BVA |
| TC-07-05 | Member account cannot access member management | Logged in as `biet.hoang@email.com` (MEM006) | 1. Observe AppBar and navigation after login. | — | No Add Member button in AppBar. No "Thành viên" (Members) nav tab. Role-based restriction enforced. | EP |
| TC-07-06 | Add member — empty phone number field | Logged in as Librarian, Add Member form open | 1. Fill Name and Email with valid values. 2. Leave Phone Number blank. 3. Submit. | Name: `Test Empty Phone`, Email: `emptyphone@test.com`, Phone: `""` | **FAIL — DEFECT-05:** Error "Email không hợp lệ." displayed for empty phone field. Expected: phone-specific error message. | EP |
| TC-07-07 | Add member — non-numeric phone number | Logged in as Librarian, Add Member form open | 1. Fill Name and Email validly. 2. Enter `abcdefghij` in Phone Number. 3. Submit. | Name: `Test Bad Phone`, Email: `badphone@test.com`, Phone: `abcdefghij` | **FAIL — DEFECT-06:** Error "Email không hợp lệ." displayed for non-numeric phone. Expected: "Phone number must contain only digits." | EP |

### REQ-08: Borrow Record Lookup (3 TCs)

| TC ID | Objective | Precondition | Steps | Input | Expected Result | Technique |
|-------|-----------|-------------|-------|-------|-----------------|-----------|
| TC-08-01 | Librarian views all borrow records from all members | Logged in as Librarian | 1. Go to "Mượn / Trả" tab → "Tất cả phiếu mượn". | — | All records (BR001–BR005) are visible with full details: ID, book, member, dates, status. | EP |
| TC-08-02 | Librarian searches borrow records by member ID | Logged in as Librarian | 1. Go to "Tra cứu phiếu mượn". 2. Enter member ID. 3. Search. | Member ID: `MEM006` | Only MEM006's borrow records shown. Records from MEM002, MEM003 etc. are not displayed. | EP |
| TC-08-03 | Member can only view their own records | Logged in as MEM006 (`biet.hoang@email.com`) | 1. Go to "Mượn / Trả" tab. | — | Only MEM006's own records visible. No records belonging to other members shown. No member ID search input available. | EP |

---

## Summary

| Feature Group | TCs | TC IDs | REQ Covered | Techniques |
|--------------|-----|--------|-------------|------------|
| User Login | 5 | TC-01-01 to TC-01-05 | REQ-01 | EP |
| View Book List | 3 | TC-02-01 to TC-02-03 | REQ-02 | EP |
| Search & Filter | 5 | TC-03-01 to TC-03-05 | REQ-03 | EP |
| Borrow Book | 7 | TC-04-01 to TC-04-07 | REQ-04 | EP, BVA, Decision Table |
| Return Book | 2 | TC-05-01 to TC-05-02 | REQ-05 | EP |
| Overdue Handling | 2 | TC-06-01 to TC-06-02 | REQ-06 | EP |
| Member Management | 7 | TC-07-01 to TC-07-07 | REQ-07 | EP, BVA |
| Borrow Record Lookup | 3 | TC-08-01 to TC-08-03 | REQ-08 | EP |
| **Total** | **34** | **TC-01-01 – TC-08-03** | **8 / 8 REQ** | **EP + BVA + Decision Table** |

### Technique Justification

**Equivalence Partitioning (EP)** was applied to all 8 requirements because every input field has clearly separable valid/invalid partitions — one representative value per partition is sufficient to verify system behaviour.

**Boundary Value Analysis (BVA)** was applied to REQ-04 for the numeric borrow limit (0, 1, 2, 3 = at limit, 4 = over limit). Defects most often occur at the exact boundary of a constraint. BVA was also applied to REQ-07 email format, testing the precise boundary between a valid format and one missing the TLD dot.

**Decision Table** was applied to REQ-04 because the borrow approval logic depends on three independent boolean conditions simultaneously (book availability × member status × borrow count). A decision table guarantees all significant rule combinations are considered.
