import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    """
    Cart page DOM (confirmed from page source):
    - Cart items rendered inside ng-view when cart.getCount() > 0
    - Empty cart shows: <div class="alert"><strong>Your cart is empty</strong></div>
    - Populated cart: table with rows per product
    """

    def load(self):
        self.open("/#/cart")
        self.wait_for_url("#/cart")
        self.wait_for_angular()
        time.sleep(1.5)  # allow ng-view to render cart contents

        # Confirm cart is NOT empty before proceeding
        empty = self.driver.find_elements(By.XPATH, "//*[contains(text(),'cart is empty')]")
        if empty and empty[0].is_displayed():
            raise Exception(
                "Cart is empty on load — products were not added successfully. "
                "Check shop_page.buy_product()."
            )

        # Wait for table rows to appear
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        return self

    def get_rows(self):
        rows_data = []
        rows = self.find_all((By.CSS_SELECTOR, "table tbody tr"))
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:
                continue
            qty_cell = cells[2]
            inputs = qty_cell.find_elements(By.TAG_NAME, "input")
            quantity = inputs[0].get_attribute("value").strip() if inputs else qty_cell.text.strip()
            rows_data.append({
                "product":  cells[0].text.strip(),
                "price":    cells[1].text.strip().replace("$", "").strip(),
                "quantity": quantity,
                "subtotal": cells[3].text.strip().replace("$", "").strip(),
            })
        return rows_data

    def get_total(self):
        strategies = [
            (By.XPATH, "//tr[td[normalize-space()='Total:']]/td[last()]"),
            (By.ID, "total"),
            (By.XPATH, "//tfoot//td[contains(.,'$')]"),
            (By.XPATH, "//strong[contains(.,'$')]"),
            (By.XPATH, "//*[contains(@class,'total')]"),
        ]
        for locator in strategies:
            els = self.driver.find_elements(*locator)
            for el in els:
                text = el.text.strip().replace("$", "").strip()
                if text and any(c.isdigit() for c in text):
                    return text
        raise Exception("Could not locate cart grand total.")
