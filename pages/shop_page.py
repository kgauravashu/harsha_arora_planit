import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ShopPage(BasePage):

    PRODUCT_ITEMS = (By.CSS_SELECTOR, "li.product")

    def load(self):
        self.open("/#/shop")
        self.wait_for_url("#/shop")
        self.wait_for_angular()
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        return self

    def _get_cart_count(self):
        """Read current cart count from the nav badge."""
        els = self.driver.find_elements(By.CSS_SELECTOR, "span.cart-count")
        if els:
            try:
                return int(els[0].text.strip())
            except ValueError:
                return 0
        return 0

    def _click_buy_for_product(self, product_name):
        """
        Find the Buy <a> inside the product card and trigger ng-click via JS
        WITHOUT following href="" which would navigate away and reset the cart.
        """
        # Find all product li elements
        items = self.driver.find_elements(By.CSS_SELECTOR, "li.product")
        for item in items:
            h4s = item.find_elements(By.CSS_SELECTOR, "h4.product-title")
            if h4s and h4s[0].text.strip() == product_name:
                btn = item.find_element(By.CSS_SELECTOR, "a.btn")
                # Use JS click to fire ng-click without following href=""
                self.driver.execute_script("arguments[0].click();", btn)
                return True
        return False

    def buy_product(self, product_name, quantity):
        """
        Stay on the shop page the entire time — reload only once at the start.
        Click Buy via JS each time to prevent href="" navigation.
        """
        self.load()  # Navigate to shop once

        for i in range(quantity):
            before = self._get_cart_count()
            success = self._click_buy_for_product(product_name)

            if not success:
                raise Exception(
                    f"Product '{product_name}' not found on shop page (iteration {i+1}). "
                    f"Available products: "
                    f"{[el.text for el in self.driver.find_elements(By.CSS_SELECTOR, 'h4.product-title')]}"
                )

            # Wait for cart count to increment — confirms the item was added
            try:
                self.wait.until(lambda d: self._get_cart_count() > before)
            except Exception:
                raise Exception(
                    f"Cart count did not increase after clicking Buy for '{product_name}' "
                    f"(iteration {i+1}). Count before: {before}, after: {self._get_cart_count()}"
                )

        return self
