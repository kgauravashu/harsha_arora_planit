import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class ContactPage(BasePage):
    FORENAME = (By.ID, "forename")
    EMAIL    = (By.ID, "email")
    MESSAGE  = (By.ID, "message")

    # Jupiter app uses <a class="btn">Submit</a>
    SUBMIT_BTN = (By.XPATH, "//a[contains(@class,'btn') and normalize-space()='Submit']")

    # Validation error elements — ONLY the *-err ids, not hint text
    FORENAME_ERROR = (By.ID, "forename-err")
    EMAIL_ERROR    = (By.ID, "email-err")
    MESSAGE_ERROR  = (By.ID, "message-err")

    # All three validation error ids in one shot
    VALIDATION_ERRORS = (By.CSS_SELECTOR, "#forename-err, #email-err, #message-err")

    # Success banner
    SUCCESS_BANNER = (By.XPATH, "//div[contains(@class,'alert-success')]")

    def wait_for_form(self):
        self.find(self.FORENAME)
        return self

    def click_submit(self):
        self.js_click(self.SUBMIT_BTN)
        time.sleep(0.8)  # let Angular render validation state
        return self

    def get_forename_error(self):
        return self.get_text(self.FORENAME_ERROR)

    def get_email_error(self):
        return self.get_text(self.EMAIL_ERROR)

    def get_message_error(self):
        return self.get_text(self.MESSAGE_ERROR)

    def errors_present(self):
        """Return only true validation error elements (the *-err ids), visible and non-empty."""
        els = self.driver.find_elements(By.CSS_SELECTOR, "#forename-err, #email-err, #message-err")
        return [e for e in els if e.is_displayed() and e.text.strip()]

    def fill_mandatory_fields(self, forename="John", email="john@example.com",
                              message="This is an automated test message."):
        self.type_text(self.FORENAME, forename)
        self.type_text(self.EMAIL, email)
        self.type_text(self.MESSAGE, message)
        return self

    def get_success_message(self):
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_BANNER))
        return self.get_text(self.SUCCESS_BANNER)
