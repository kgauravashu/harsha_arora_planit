import os

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Overridable so a slow CI runner can be given more headroom without code changes.
DEFAULT_TIMEOUT = int(os.environ.get("UI_TIMEOUT", "20"))


class BasePage:
    BASE_URL = os.environ.get("BASE_URL", "http://jupiter.cloud.planittesting.com")

    # Top navigation is rendered on every page, so it lives here once rather
    # than being re-declared (and drifting) in each page object.
    NAV_SHOP = (By.CSS_SELECTOR, "li#nav-shop a")
    NAV_CONTACT = (By.CSS_SELECTOR, "li#nav-contact a")
    NAV_CART = (By.CSS_SELECTOR, "li#nav-cart a")

    # AngularJS keeps in-flight XHRs on $http; zero pending means data-bound
    # content has stopped changing for network reasons.
    _ANGULAR_IDLE_JS = """
        if (document.readyState !== 'complete') return false;
        if (!window.angular) return true;
        var injector = angular.element(document.body).injector();
        return !injector || injector.get('$http').pendingRequests.length === 0;
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # --- navigation -------------------------------------------------------

    def open(self, path=""):
        self.driver.get(f"{self.BASE_URL}{path}")

    def wait_for_url(self, fragment):
        self.wait.until(EC.url_contains(fragment))

    def wait_for_app_idle(self):
        """Wait for the document and Angular's pending requests to settle.

        Replaces fixed sleeps: it returns as soon as the app is ready, and
        fails loudly (TimeoutException) instead of silently racing the UI.
        """
        self.wait.until(lambda d: d.execute_script(self._ANGULAR_IDLE_JS))

    def _navigate_via_nav(self, nav_locator, url_fragment):
        # The cart lives in Angular's in-memory state, so a full page load
        # (driver.get) would empty it. Clicking the nav link keeps the SPA alive.
        self.click(nav_locator)
        self.wait_for_url(url_fragment)
        self.wait_for_app_idle()

    def go_to_shop(self):
        self._navigate_via_nav(self.NAV_SHOP, "#/shop")
        return self

    def go_to_contact(self):
        self._navigate_via_nav(self.NAV_CONTACT, "#/contact")
        return self

    def go_to_cart(self):
        self._navigate_via_nav(self.NAV_CART, "#/cart")
        return self

    # --- element helpers --------------------------------------------------

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        # Short pages can leave the target under the sticky navbar.
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", element
        )
        try:
            element.click()
        except ElementClickInterceptedException:
            # Fall back to a DOM click only for overlay interception (e.g. the
            # "Sending Feedback" modal fading out). Any other error is a real
            # failure and must not be masked.
            self.driver.execute_script("arguments[0].click();", element)

    def type_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find(locator).text.strip()
