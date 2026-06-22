from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class HomePage(BasePage):
    # Nav links are inside the top navbar
    NAV_CONTACT = (By.XPATH, "//a[normalize-space()='Contact']")
    NAV_SHOP    = (By.XPATH, "//a[normalize-space()='Shop']")

    def load(self):
        self.open("/#/")
        self.wait_for_angular()
        return self

    def go_to_contact(self):
        self.click(self.NAV_CONTACT)
        self.wait_for_url("#/contact")
        self.wait_for_angular()
        return self

    def go_to_shop(self):
        self.click(self.NAV_SHOP)
        self.wait_for_url("#/shop")
        self.wait_for_angular()
        return self
