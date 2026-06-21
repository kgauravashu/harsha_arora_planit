import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException


class BasePage:
    BASE_URL = "http://jupiter.cloud.planittesting.com"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)  # increased timeout

    def open(self, path=""):
        self.driver.get(f"{self.BASE_URL}{path}")

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        # Scroll into view + JS click to avoid intercept issues on SPA
        el = self.wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        try:
            el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)

    def js_click(self, locator):
        el = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", el)

    def type_text(self, locator, text):
        el = self.find(locator)
        el.clear()
        el.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text

    def wait_for_url(self, partial):
        self.wait.until(lambda d: partial in d.current_url)

    def wait_for_angular(self):
        """Small sleep to let Angular digest after navigation."""
        time.sleep(1)
