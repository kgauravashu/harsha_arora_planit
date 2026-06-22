import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):

    def load(self):
        cart_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li#nav-cart a"))
        )
        cart_link.click()
        self.wait_for_url("#/cart")
        self.wait_for_angular()
        time.sleep(1.5)

        empty = self.driver.find_elements(By.XPATH, "//*[contains(text(),'cart is empty')]")
        if empty and empty[0].is_displayed():
            raise Exception("Cart is empty — items were not persisted.")

        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr")))
        return self

    def get_rows(self):
        rows_data = []
        for row in self.find_all((By.CSS_SELECTOR, "table tbody tr")):
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
            for el in self.driver.find_elements(*locator):
                text = el.text.strip()
                # Strip label prefix e.g. "Total: 116.9" or "$116.90"
                text = text.replace("$", "")
                if ":" in text:
                    text = text.split(":")[-1]
                text = text.strip()
                if text and any(c.isdigit() for c in text):
                    return text
        raise Exception("Could not locate cart grand total.")
