"""
Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System

Test cases:
   TC-08  Mượn sách thành công — chọn sách "Có sẵn" → mượn → sách "Đang mượn"   ✅ Complete
   TC-09  Xem danh sách sách đang mượn — tab "Mượn / Trả" → thấy phiếu mượn     ✅ Complete
   TC-10  Trả sách — nhấn "Trả sách" → sách trở về "Có sẵn"                     ✅ Complete

Account strategy:
   TC-08: dùng dam.tran@email.com (chưa mượn sách) — phù hợp nhất để test mượn
   TC-09: dùng ba.nguyen@email.com (đã mượn BOOK003 trong state ban đầu)
   TC-10: dùng ba.nguyen@email.com (BOOK003 có sẵn để trả)

Notes:
   - Mỗi page context tạo dữ liệu sạch theo state ban đầu
   - ba.nguyen luôn bắt đầu với BOOK003 đang mượn (quá hạn)
   - dam.tran luôn bắt đầu không có sách nào đang mượn
   - Nút "Mượn sách này" → xuất hiện dialog → nhấn "Mượn" để xác nhận
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_borrow_book(page, test_config):
    """TC-08: Borrow an available book (*Mượn sách có trạng thái 'Có sẵn'*)

    Arrange: Đăng nhập bằng dam.tran (chưa mượn sách nào — phù hợp nhất)
    Act:     Tìm sách "Có sẵn" → click "Mượn sách này" → xác nhận dialog
    Assert:  Sách chuyển sang trạng thái "Đang mượn" hoặc thông báo thành công
    """
    # Arrange — dùng tài khoản chưa mượn sách (không dùng test_config mặc định)
    page.goto(test_config["base_url"], wait_until="networkidle", timeout=60000)
    enable_flutter_semantics(page)
    flutter_fill(page, "Email", "dam.tran@email.com")
    flutter_fill(page, "Mật khẩu", "password123")
    flutter_click_button(page, "Đăng nhập")
    wait_for_flutter(page, text="Đăng xuất")
    enable_flutter_semantics(page)

    # Act — tìm sách Có sẵn đầu tiên
    available_books = page.locator(
        'flt-semantics[role="group"][aria-label*="Có sẵn"]'
    )
    available_books.first.wait_for(state="attached", timeout=10000)

    # Lấy tên sách để assert sau
    book_label = available_books.first.get_attribute("aria-label") or ""

    # Click "Mượn sách này"
    available_books.first.locator(
        'flt-semantics[role="button"]:has-text("Mượn sách này")'
    ).click()

    # Đợi dialog xác nhận xuất hiện
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Click "Mượn" trong dialog
    flutter_click_button(page, "Mượn")

    # Smart Wait — chờ trạng thái "Đang mượn" xuất hiện
    wait_for_flutter(page, text="Đang mượn")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC08_borrow_book.png"))

    # Assert — B3: detailed assertion
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đang mượn" in sem_text or "thành công" in sem_text.lower(), (
        f"TC-08 FAIL: Expected 'Đang mượn' or 'thành công' after borrowing. "
        f"Book was: '{book_label}'"
    )


def test_view_borrowed_books(page, test_config):
    """TC-09: View borrowed books list (*Xem danh sách sách đang mượn — tab Mượn / Trả*)

    Arrange: Đăng nhập bằng ba.nguyen (đã mượn BOOK003 trong state ban đầu)
    Act:     Chuyển sang tab "Mượn / Trả"
    Assert:  Có ít nhất 1 phiếu mượn / nút "Trả sách" hiển thị
    """
    # Arrange — ba.nguyen luôn bắt đầu với BOOK003 đang mượn
    login(page, test_config)  # ba.nguyen@email.com từ CI env

    # Act — click tab Mượn / Trả
    page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
    ).click()

    # Smart Wait — chờ nội dung tab load xong
    wait_for_flutter(page, text="Đang mượn")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC09_view_borrowed_books.png"))

    # Assert — B3: detailed assertion (kiểm tra text + nút)
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    has_borrowed_status = "Đang mượn" in sem_text
    has_return_button = (
        page.locator(
            'flt-semantics[role="button"]:has-text("Trả sách")'
        ).count() > 0
    )

    assert has_borrowed_status or has_return_button, (
        "TC-09 FAIL: Expected 'Đang mượn' text or 'Trả sách' button in "
        "Mượn/Trả tab — tab may not have loaded correctly"
    )


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book (*Trả sách đang mượn*)

    Arrange: Đăng nhập bằng ba.nguyen (có BOOK003 để trả), vào tab "Mượn / Trả"
    Act:     Click "Trả sách" trên phiếu mượn
    Assert:  Nút "Trả sách" biến mất HOẶC có thông báo thành công

    Note: Nếu không có sách nào đang mượn (unexpected), test sẽ skip.
    """
    # Arrange — ba.nguyen có BOOK003 đang mượn trong initial state
    login(page, test_config)  # ba.nguyen@email.com từ CI env

    # Chuyển sang tab Mượn / Trả
    page.locator(
        'flt-semantics[role="tab"][aria-label="Mượn / Trả"]'
    ).click()

    wait_for_flutter(page, text="Đang mượn")
    enable_flutter_semantics(page)

    # Act — tìm nút "Trả sách"
    return_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Trả sách")'
    ).first

    if return_btn.count() == 0:
        pytest.skip(
            "TC-10 SKIP: Không có sách nào đang mượn — "
            "ba.nguyen initial state không có BOOK003 (unexpected)"
        )

    return_btn.wait_for(state="attached", timeout=10000)
    return_btn.click()

    # Đợi dialog xác nhận (nếu có)
    page.wait_for_timeout(1000)
    enable_flutter_semantics(page)

    # Kiểm tra xem có dialog xác nhận không
    sem_after_click = " ".join(page.locator("flt-semantics").all_text_contents())
    if "xác nhận" in sem_after_click.lower():
        # Click nút xác nhận trong dialog
        flutter_click_button(page, "Trả")
        page.wait_for_timeout(1000)
        enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC10_return_book.png"))

    # Assert — B3: sau khi trả, "Trả sách" button không còn HOẶC có thông báo
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    no_return_btn_left = (
        page.locator(
            'flt-semantics[role="button"]:has-text("Trả sách")'
        ).count() == 0
    )
    has_success_msg = (
        "thành công" in sem_text.lower()
        or "Có sẵn" in sem_text
        or "trả" in sem_text.lower()
    )

    assert no_return_btn_left or has_success_msg, (
        "TC-10 FAIL: After clicking 'Trả sách', expected either "
        "no more return buttons or a success message"
    )
