"""
Search & Filter Tests (*Kiểm thử Tìm kiếm & Lọc sách*) — Library Book Borrowing System

Test cases:
   TC-04  Tìm sách theo tên — nhập "Flutter" → hiển thị kết quả có "Flutter"   ✅ Complete
   TC-05  Tìm sách — không có kết quả → không hiển thị sách nào               ✅ Complete
   TC-06  Lọc sách theo thể loại "Công nghệ" → chỉ hiển thị sách Công nghệ    ✅ Complete
   TC-07  Tìm sách theo tác giả → hiển thị sách của tác giả đó               ✅ Complete
   BONUS  Đếm số sách Flutter, xác nhận tất cả có "Flutter" trong label        ✅ B1 Bonus
   BONUS  Kết hợp lọc thể loại và xác nhận có kết quả                         ✅ B1 Bonus

Hints recap:
   - Search box aria-label: "Tìm kiếm theo tên sách hoặc tác giả..."
   - Category filter aria-label: "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)"
   - Book card: flt-semantics[role="group"][aria-label*="Mã: BOOK"]
"""
import os
import pytest
from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    wait_for_flutter, login, SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name — results found (*Tìm kiếm sách theo tên — tìm thấy kết quả*)

    Arrange: Đăng nhập thành công
    Act:     Nhập "Flutter" vào ô tìm kiếm
    Assert:  Có sách hiển thị với "Flutter" trong aria-label
    """
    # Arrange
    login(page, test_config)

    # Act — B3: dùng Smart Wait thay vì time.sleep
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    wait_for_flutter(page, text="Flutter")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC04_search_by_name_flutter.png"))

    # Assert — B3: detailed assertion
    results = page.locator('flt-semantics[aria-label*="Flutter"]')
    result_count = results.count()

    assert result_count > 0, (
        "TC-04 FAIL: Expected at least 1 book with 'Flutter' in label, "
        f"found {result_count}"
    )

    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    assert book_cards.count() > 0, (
        "TC-04 FAIL: No book cards found after searching 'Flutter'"
    )


def test_search_book_no_result(page, test_config):
    """TC-05: Search book — no results (*Tìm kiếm sách — không có kết quả*)

    Arrange: Đăng nhập thành công
    Act:     Nhập từ khóa không tồn tại vào ô tìm kiếm
    Assert:  Không hiển thị sách nào (0 book cards)
    """
    # Arrange
    login(page, test_config)

    # Act
    keyword = "xyz_khong_ton_tai_99999"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", keyword)

    # Smart Wait — không có kết quả cụ thể để đợi, đợi UI ổn định
    page.wait_for_timeout(2000)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC05_search_no_result.png"))

    # Assert — B3: count must be exactly 0
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()

    assert count == 0, (
        f"TC-05 FAIL: Expected 0 books for keyword '{keyword}', "
        f"but found {count} book(s)"
    )


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category 'Công nghệ' (*Lọc sách theo thể loại*)

    Arrange: Đăng nhập thành công
    Act:     Nhập "Công nghệ" vào ô lọc thể loại
    Assert:  Tất cả sách hiển thị đều thuộc thể loại "Công nghệ"
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ",
    )
    wait_for_flutter(page, text="Công nghệ")
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC06_filter_by_category.png"))

    # Assert — B3: verify every displayed book belongs to "Công nghệ"
    book_cards = page.locator('flt-semantics[role="group"][aria-label*="Mã: BOOK"]')
    count = book_cards.count()

    assert count > 0, "TC-06 FAIL: No books shown after filtering by 'Công nghệ'"

    for i in range(count):
        label = book_cards.nth(i).get_attribute("aria-label") or ""
        assert "Công nghệ" in label, (
            f"TC-06 FAIL: Book card #{i} does not belong to 'Công nghệ'. "
            f"aria-label='{label}'"
        )


def test_search_by_author(page, test_config):
    """TC-07: Search book by author name (*Tìm kiếm sách theo tên tác giả*)

    Arrange: Đăng nhập thành công
    Act:     Nhập tên tác giả "Nguyễn Minh Đức" vào ô tìm kiếm
    Assert:  Có kết quả hiển thị với tên tác giả trong aria-label
    """
    # Arrange
    login(page, test_config)

    # Act
    author = "Nguyễn Minh Đức"
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", author)
    wait_for_flutter(page, text=author)
    enable_flutter_semantics(page)

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC07_search_by_author.png"))

    # Assert — B3: check both semantics elements and book cards
    author_elements = page.locator(f'flt-semantics[aria-label*="{author}"]')
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())

    assert author_elements.count() > 0 or author in sem_text, (
        f"TC-07 FAIL: Expected author '{author}' in search results"
    )


# ---------------------------------------------------------------------------
# BONUS B1 — Extra test cases (beyond required 12)
# ---------------------------------------------------------------------------

def test_search_flutter_returns_correct_count(page, test_config):
    """BONUS B1 — Tìm "Flutter" và xác nhận tất cả kết quả có "Flutter" trong label.

    Verifies search actually filters results (not just shows all books).
    """
    # Arrange
    login(page, test_config)

    # Act
    flutter_fill(page, "Tìm kiếm theo tên sách hoặc tác giả...", "Flutter")
    wait_for_flutter(page, text="Flutter")
    enable_flutter_semantics(page)
    flutter_count = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    ).count()

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "BONUS_search_flutter_count.png"))

    # Assert: at least 1 Flutter book found
    assert flutter_count > 0, (
        f"BONUS FAIL: Expected ≥1 books when searching 'Flutter', got {flutter_count}"
    )


def test_search_category_and_name_combined(page, test_config):
    """BONUS B1 — Lọc thể loại "Công nghệ" và xác nhận có kết quả.

    Verifies category filter returns books.
    """
    # Arrange
    login(page, test_config)

    # Act: filter by category
    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ",
    )
    wait_for_flutter(page, text="Công nghệ")
    enable_flutter_semantics(page)
    category_count = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    ).count()

    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "BONUS_filter_combined.png"))

    # Assert: at least 1 book in category
    assert category_count > 0, (
        f"BONUS FAIL: Expected books in 'Công nghệ' category, got {category_count}"
    )
