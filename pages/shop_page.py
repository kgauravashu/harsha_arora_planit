from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ShopPage(BasePage):
    PRODUCT_ITEMS = (By.CSS_SELECTOR, "li.product")
    PRODUCT_TITLES = (By.CSS_SELECTOR, "li.product h4.product-title")
    CART_COUNT = (By.CSS_SELECTOR, "span.cart-count")

    # Parameterised locator: the Buy button is only unique within its product card.
    _BUY_BUTTON_TEMPLATE = (
        "//li[contains(@class,'product')][.//h4[normalize-space()='{name}']]"
        "//a[contains(@class,'btn')]"
    )

    def load(self):
        # Direct URL load is fine here: it is the first navigation, so there
        # is no cart state to lose yet.
        self.open("/#/shop")
        self.wait_for_url("#/shop")
        self.wait_for_app_idle()
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        return self

    def _buy_button(self, product_name):
        return (By.XPATH, self._BUY_BUTTON_TEMPLATE.format(name=product_name))

    def cart_count(self):
        # The badge is not rendered until the first item is added.
        elements = self.driver.find_elements(*self.CART_COUNT)
        if not elements:
            return 0
        text = elements[0].text.strip()
        return int(text) if text.isdigit() else 0

    def available_products(self):
        return [el.text.strip() for el in self.driver.find_elements(*self.PRODUCT_TITLES)]

    def buy_product(self, product_name, quantity):
        buy_button = self._buy_button(product_name)
        if not self.driver.find_elements(*buy_button):
            raise AssertionError(
                f"Product '{product_name}' not found. Available: {self.available_products()}"
            )

        for _ in range(quantity):
            before = self.cart_count()
            self.click(buy_button)
            # Each click must raise the badge by one; waiting on that makes the
            # next click safe and surfaces a dropped click immediately.
            self.wait.until(
                lambda _, b=before: self.cart_count() > b,
                message=f"Cart count did not increase after buying '{product_name}' "
                        f"(was {before}, now {self.cart_count()})",
            )
        return self
