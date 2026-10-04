import re
from decimal import Decimal

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from pages.base_page import BasePage

_MONEY = re.compile(r"-?\d+(?:\.\d+)?")


def parse_money(text):
    """Extract a Decimal from strings like '$9.99' or 'Total: 116.9'.

    Decimal (not float) so price x quantity can be compared exactly.
    """
    match = _MONEY.search(text.replace(",", ""))
    if not match:
        raise ValueError(f"No monetary value found in '{text}'")
    return Decimal(match.group())


class CartPage(BasePage):
    ROWS = (By.CSS_SELECTOR, "table tbody tr")
    TOTAL = (By.CSS_SELECTOR, "strong.total")

    # Column positions in the cart table.
    COL_PRODUCT, COL_PRICE, COL_QUANTITY, COL_SUBTOTAL = range(4)

    def load(self):
        self.go_to_cart()
        try:
            self.find_all(self.ROWS)
        except TimeoutException:
            raise AssertionError(
                "Cart table has no rows; items were not carried over from the shop page."
            ) from None
        return self

    def get_rows(self):
        rows = []
        for row in self.find_all(self.ROWS):
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) <= self.COL_SUBTOTAL:
                continue
            # Quantity is an editable <input> in the cart, so read its value
            # rather than the cell text (which is empty).
            qty_inputs = cells[self.COL_QUANTITY].find_elements(By.TAG_NAME, "input")
            qty_text = (qty_inputs[0].get_attribute("value")
                        if qty_inputs else cells[self.COL_QUANTITY].text)
            rows.append({
                "product": cells[self.COL_PRODUCT].text.strip(),
                "price": parse_money(cells[self.COL_PRICE].text),
                "quantity": int(qty_text.strip()),
                "subtotal": parse_money(cells[self.COL_SUBTOTAL].text),
            })
        return rows

    def get_total(self):
        return parse_money(self.get_text(self.TOTAL))
