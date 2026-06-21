import time
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ShopPage(BasePage):

    def load(self):
        self.open("/#/shop")
        self.wait_for_url("#/shop")
        self.wait_for_angular()
        # Wait for any h4 (product names) to appear
        self.wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "h4")) > 0)

        # Dump shop DOM once so we know actual structure
        src = self.driver.page_source
        print("\n\n===== SHOP PAGE SOURCE =====")
        print(src[:6000])
        print("===== END SHOP SOURCE =====\n\n")
        return self

    def _find_buy_button(self, product_name):
        strategies = [
            f"//li[.//h4[normalize-space()='{product_name}']]//a[contains(@class,'btn')]",
            f"//div[.//h4[normalize-space()='{product_name}']]//a[contains(@class,'btn')]",
            f"//h4[normalize-space()='{product_name}']/following::a[contains(@class,'btn')][1]",
            f"//h4[contains(normalize-space(),'{product_name}')]/following::a[contains(@class,'btn')][1]",
            f"//*[contains(text(),'{product_name}')]/ancestor::*[position()<=5]//a[contains(@class,'btn')]",
            # Broader: any button that follows the product name
            f"//*[normalize-space(text())='{product_name}']/following::a[1]",
        ]
        for xpath in strategies:
            els = self.driver.find_elements(By.XPATH, xpath)
            if els:
                return els[0]
        return None

    def buy_product(self, product_name, quantity):
        for i in range(quantity):
            self.open("/#/shop")
            self.wait_for_url("#/shop")
            self.wait_for_angular()
            self.wait.until(lambda d: len(d.find_elements(By.TAG_NAME, "h4")) > 0)
            time.sleep(0.5)

            btn = self._find_buy_button(product_name)
            if btn is None:
                src = self.driver.page_source
                raise Exception(
                    f"Buy button not found for '{product_name}' on iteration {i+1}.\n"
                    f"Page source:\n{src[1500:5000]}"
                )
            self.driver.execute_script("arguments[0].scrollIntoView(true);", btn)
            try:
                btn.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.4)
        return self
