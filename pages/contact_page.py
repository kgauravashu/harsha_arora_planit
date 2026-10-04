from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ContactPage(BasePage):
    FORENAME = (By.ID, "forename")
    EMAIL = (By.ID, "email")
    MESSAGE = (By.ID, "message")

    # The submit control is an <a>, not a <button>, so match on text as well
    # as class to avoid hitting any other .btn on the page.
    SUBMIT_BTN = (By.XPATH, "//a[contains(@class,'btn') and normalize-space()='Submit']")

    # Only the *-err elements carry validation text; the sibling hint
    # elements would give false positives.
    FORENAME_ERROR = (By.ID, "forename-err")
    EMAIL_ERROR = (By.ID, "email-err")
    MESSAGE_ERROR = (By.ID, "message-err")
    VALIDATION_ERRORS = (By.CSS_SELECTOR, "#forename-err, #email-err, #message-err")

    SUCCESS_BANNER = (By.CSS_SELECTOR, "div.alert-success")

    def wait_for_form(self):
        self.find(self.FORENAME)
        return self

    def click_submit(self):
        self.click(self.SUBMIT_BTN)
        return self

    def fill_mandatory_fields(self, forename="John", email="john@example.com",
                              message="This is an automated test message."):
        self.type_text(self.FORENAME, forename)
        self.type_text(self.EMAIL, email)
        self.type_text(self.MESSAGE, message)
        return self

    # --- validation state -------------------------------------------------

    def visible_errors(self):
        """Validation errors that are displayed and have text."""
        return [
            el for el in self.driver.find_elements(*self.VALIDATION_ERRORS)
            if el.is_displayed() and el.text.strip()
        ]

    def wait_for_error_count(self, expected):
        """Poll until exactly `expected` errors are visible.

        Used for both "errors appeared" (3) and "errors cleared" (0), so the
        test synchronises on the outcome it asserts rather than on elapsed time.
        """
        self.wait.until(
            lambda _: len(self.visible_errors()) == expected,
            message=f"Expected {expected} visible validation errors, "
                    f"found {[e.text for e in self.visible_errors()]}",
        )

    def get_forename_error(self):
        return self.get_text(self.FORENAME_ERROR)

    def get_email_error(self):
        return self.get_text(self.EMAIL_ERROR)

    def get_message_error(self):
        return self.get_text(self.MESSAGE_ERROR)

    # --- submission result ------------------------------------------------

    def get_success_message(self):
        # The banner only appears after the app's "Sending Feedback" progress
        # phase completes, so waiting on visibility covers that delay.
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_BANNER))
        return self.get_text(self.SUCCESS_BANNER)
