"""
General Feature Tests (*Kiểm thử Chức năng chung*) — Library Book Borrowing System

Test cases:
   TC-11  Đăng xuất — nhấn nút đăng xuất → trở về trang đăng nhập        ✅ Complete
   TC-12  Chuyển ngôn ngữ sang English → giao diện hiển thị tiếng Anh     ✅ Complete
   BONUS  Chuyển ngôn ngữ EN → quay lại VI → giao diện tiếng Việt         ✅ B1 Bonus

Notes:
   - Logout button: flt-semantics[role="button"]:has-text("Đăng xuất")
   - EN language button: flt-semantics[role="button"]:has-text("EN")
   - VI language button: flt-semantics[role="button"]:has-text("VI")
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success (*Đăng xuất thành công*)

    Arrange: Đăng nhập thành công
    Act:     Click nút "Đăng xuất"
    Assert:  Trang quay về màn hình đăng nhập (có "Email" input và "Đăng nhập" button)
    """
    # Arrange
    login(page, test_config)

    # Act — click Đăng xuất
    flutter_click_button(page, "Đăng xuất")

    # Smart Wait — chờ trang đăng nhập xuất hiện (thay vì time.sleep(3))
    wait_for_flutter(page, text="Đăng nhập")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC11_logout.png"))

    # Assert — B3: detailed assertion
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_login_btn = "Đăng nhập" in sem_text
    has_email_input = page.locator('input[aria-label="Email"]').count() > 0
    no_logout_btn = "Đăng xuất" not in sem_text and "Logout" not in sem_text

    assert has_login_btn or has_email_input, (
        "TC-11 FAIL: Expected to return to login page with 'Đăng nhập' button "
        "or 'Email' input after logout"
    )
    assert no_logout_btn, (
        "TC-11 FAIL: 'Đăng xuất' button still present after logout"
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English (*Chuyển ngôn ngữ sang tiếng Anh*)

    Arrange: Đăng nhập thành công (giao diện tiếng Việt)
    Act:     Click nút "EN"
    Assert:  Giao diện chuyển sang tiếng Anh
    """
    # Arrange
    login(page, test_config)

    # Act — click nút EN
    flutter_click_button(page, "EN")

    # KEY FIX: dùng timeout thay vì wait_for_flutter — app không có text "Logout" cụ thể
    page.wait_for_timeout(3000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC12_switch_language_en.png"))

    # Assert — kiểm tra ít nhất 1 từ tiếng Anh xuất hiện
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    english_keywords = ["Logout", "Borrow", "Library", "Search", "Return", "Available", "Log out", "Sign out"]
    matched = [kw for kw in english_keywords if kw in sem_text]

    assert len(matched) > 0, (
        "TC-12 FAIL: Expected at least one English keyword "
        f"({', '.join(english_keywords)}) after switching to EN. "
        f"sem_text snippet: '{sem_text[:300]}'"
    )


# ---------------------------------------------------------------------------
# BONUS B1 — Extra test: switch EN then back to VI
# ---------------------------------------------------------------------------

def test_switch_language_back_to_vietnamese(page, test_config):
    """BONUS B1 — Chuyển EN → VI → giao diện trở lại tiếng Việt."""
    # Arrange
    login(page, test_config)

    # Act 1: switch to EN
    flutter_click_button(page, "EN")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    # Act 2: switch back to VI
    flutter_click_button(page, "VI")
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(
        SCREENSHOT_DIR, "BONUS_switch_language_back_vi.png"
    ))

    # Assert: Vietnamese text reappears
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_viet = "Đăng xuất" in sem_text or "Tìm kiếm" in sem_text

    assert has_viet, (
        "BONUS FAIL: Expected Vietnamese text after switching back to VI"
    )
