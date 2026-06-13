"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See bonus test at bottom

Test cases:
   TC-01  Đăng nhập thành công — email + mật khẩu đúng            ✅ Complete
   TC-02  Đăng nhập thất bại — sai mật khẩu                       ✅ Complete
   TC-03  Đăng nhập thất bại — bỏ trống cả hai trường             ✅ Complete
   BONUS  Data-driven login fail (parametrize TC-02 + TC-03)       ✅ B2 Bonus
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials (*Đăng nhập thành công với thông tin hợp lệ*)

    ✅ COMPLETED — Use as a reference example.
    📖 RIPR Model (Textbook Ch.2):
        [R] Reachability  — navigate to login page
        [I] Infection     — enter valid credentials, trigger login logic
        [P] Propagation   — wait for UI to reflect logged-in state
        [R✓] Revealability — assert display_name or Logout button appears
    """
    # [R] Reachability: navigate to login page
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection: enter valid credentials
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])
    flutter_click_button(page, "Đăng nhập")

    # [P] Propagation: Smart Wait — chờ nút "Đăng xuất" xuất hiện (thay vì time.sleep)
    wait_for_flutter(page, text="Đăng xuất")
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC01_login_success.png"))

    # [R✓] Revealability: assert logged-in state (B3 — detailed assertion)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_display_name = test_config["display_name"] in sem_text
    has_logout_btn = "Đăng xuất" in sem_text or "Logout" in sem_text

    assert has_display_name or has_logout_btn, (
        f"TC-01 FAIL: Expected display_name='{test_config['display_name']}' "
        f"or 'Đăng xuất' in page, but got: ...{sem_text[:200]}..."
    )


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail — wrong password (*Đăng nhập thất bại — sai mật khẩu*)

    📖 RIPR:
        [R] Navigate to login page
        [I] Enter correct email but WRONG password → trigger failed-login state
        [P] System stays on login page, no dashboard rendered
        [R✓] Assert: no logout button, email input still visible
    """
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection — correct email, wrong password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")
    flutter_click_button(page, "Đăng nhập")

    # [P] Smart Wait — chờ phản hồi UI (không dùng time.sleep)
    # Hệ thống không chuyển trang, nên chờ "Email" input vẫn còn hiển thị
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC02_login_fail_wrong_password.png"))

    # [R✓] Revealability — B3: detailed assertion
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    still_on_login = "Email" in sem_text or "Đăng nhập" in sem_text
    not_logged_in = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert not_logged_in, (
        "TC-02 FAIL: User was logged in despite wrong password — "
        "found 'Đăng xuất' in page"
    )
    assert still_on_login, (
        "TC-02 FAIL: Login page elements not found — "
        "'Email' or 'Đăng nhập' missing from page"
    )


def test_login_fail_empty_fields(page, test_config):
    """TC-03: Login fail — empty fields (*Đăng nhập thất bại — để trống cả hai trường*)

    📖 RIPR:
        [R] Navigate to login page
        [I] Do NOT enter email or password — click Đăng nhập immediately
        [P] System stays on login page (no navigation)
        [R✓] Assert: 'Đăng xuất' not present, login form still visible
    """
    # [R] Reachability
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    # [I] Infection — click login without entering anything
    flutter_click_button(page, "Đăng nhập")

    # [P] Smart Wait — chờ UI phản hồi mà không chuyển trang
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC03_login_fail_empty_fields.png"))

    # [R✓] Revealability — B3: detailed assertion
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    not_logged_in = "Đăng xuất" not in sem_text and "Logout" not in sem_text
    still_on_login = "Email" in sem_text or "Đăng nhập" in sem_text

    assert not_logged_in, (
        "TC-03 FAIL: User was logged in despite empty fields"
    )
    assert still_on_login, (
        "TC-03 FAIL: Expected to remain on login page with 'Email' or 'Đăng nhập' visible"
    )


# ---------------------------------------------------------------------------
# BONUS B2 — Data-Driven Testing: gộp TC-02 & TC-03 vào 1 test với parametrize
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("tc_id,email,password,scenario", [
    ("TC-02", "ba.nguyen@email.com", "wrongpassword", "wrong_password"),
    ("TC-03", "",                    "",              "empty_fields"),
    ("TC-02b", "nobody@test.com",   "anything",      "invalid_email"),   # extra scenario
])
def test_login_fail_parametrized(page, test_config, tc_id, email, password, scenario):
    """BONUS B2 — Data-Driven: multiple invalid login scenarios in one test.

    Covers TC-02 (wrong password), TC-03 (empty fields), and an extra case
    (non-existent email) — all sharing the same logic.
    """
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)

    if email:
        flutter_fill(page, "Email", email)
    if password:
        flutter_fill(page, "Mật khẩu", password)

    flutter_click_button(page, "Đăng nhập")

    # Smart Wait — chờ UI phản hồi
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)
    page.screenshot(path=os.path.join(
        SCREENSHOT_DIR, f"BONUS_login_fail_{tc_id}_{scenario}.png"
    ))

    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    not_logged_in = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert not_logged_in, (
        f"BONUS {tc_id} [{scenario}] FAIL: "
        f"Should NOT be logged in with email='{email}', password='{password}'"
    )
