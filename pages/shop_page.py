import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ShopPage(BasePage):

    PRODUCT_ITEMS = (By.CSS_SELECTOR, "li.product")

    def load(self):
        """Initial load only — use driver.get once to bootstrap the Angular app."""
        self.open("/#/shop")
        self.wait_for_url("#/shop")
        self.wait_for_angular()
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        return self

    def go_to_shop_via_nav(self):
        """
        Navigate back to shop WITHOUT a full page reload — click the Shop nav link.
        This keeps Angular's in-memory cart state intact.
        """
        shop_link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li#nav-shop a"))
        )
        shop_link.click()
        self.wait_for_url("#/shop")
        self.wait_for_angular()
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))

    def _get_cart_count(self):
        els = self.driver.find_elements(By.CSS_SELECTOR, "span.cart-count")
        if els:
            try:
                return int(els[0].text.strip())
            except ValueError:
                return 0
        return 0

    def _click_buy_for_product(self, product_name):
        items = self.driver.find_elements(By.CSS_SELECTOR, "li.product")
        for item in items:
            h4s = item.find_elements(By.CSS_SELECTOR, "h4.product-title")
            if h4s and h4s[0].text.strip() == product_name:
                btn = item.find_element(By.CSS_SELECTOR, "a.btn")
                # JS click fires ng-click without following href=""
                self.driver.execute_script("arguments[0].click();", btn)
                return True
        return False

    def buy_product(self, product_name, quantity):
        """
        Add product N times. Stay on the shop page the whole time using
        nav-link clicks (not driver.get) so Angular cart state is preserved.
        """
        for i in range(quantity):
            # If not already on shop, navigate back via nav link (preserves cart)
            if "#/shop" not in self.driver.current_url:
                self.go_to_shop_via_nav()

            before = self._get_cart_count()
            success = self._click_buy_for_product(product_name)

            if not success:
                available = [el.text for el in self.driver.find_elements(
                    By.CSS_SELECTOR, "h4.product-title")]
                raise Exception(
                    f"Product '{product_name}' not found (iteration {i+1}). "
                    f"Available: {available}"
                )

            # Wait for cart count to increase — confirms add was successful
            try:
                self.wait.until(lambda d, b=before: self._get_cart_count() > b)
            except Exception:
                raise Exception(
                    f"Cart count did not increase after clicking Buy for '{product_name}' "
                    f"(iteration {i+1}). Before={before}, after={self._get_cart_count()}"
                )

        return self
