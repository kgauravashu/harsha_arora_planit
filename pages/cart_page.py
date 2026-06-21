import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):

    def load(self):
        self.open("/#/cart")
        self.wait_for_url("#/cart")
        self.wait_for_angular()
        time.sleep(2)  # let Angular fully render cart contents

        # Dump page source to stdout so CI logs show us the real DOM
        src = self.driver.page_source
        print("\n\n===== CART PAGE SOURCE =====")
        print(src[:8000])
        print("===== END CART SOURCE =====\n\n")
        return self

    def get_rows(self):
        rows_data = []
        # Try table rows first
        rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
        if not rows:
            # Fallback: any tr on the page
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr")

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
            (By.XPATH, "//*[contains(@class,'total') and contains(.,'$')]"),
            (By.XPATH, "//*[contains(text(),'Total')]/../*[contains(.,'$')]"),
        ]
        for locator in strategies:
            els = self.driver.find_elements(*locator)
            for el in els:
                text = el.text.strip()
                if text and ("$" in text or any(c.isdigit() for c in text)):
                    return text.replace("$", "").strip()
        raise Exception("Could not find cart total. URL: " + self.driver.current_url)
