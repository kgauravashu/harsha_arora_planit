from pages.base_page import BasePage


class HomePage(BasePage):
    def load(self):
        self.open("/#/")
        self.wait_for_app_idle()
        return self
