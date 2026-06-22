import time
from pages.home_page import HomePage
from pages.contact_page import ContactPage


def test_contact_form_validation_errors(driver):
    home    = HomePage(driver)
    contact = ContactPage(driver)

    # 1. From home page go to contact page
    home.load()
    home.go_to_contact()
    contact.wait_for_form()

    # 2. Click Submit without filling any fields
    contact.click_submit()

    # 3. Verify error messages are displayed
    time.sleep(1)  # allow Angular to render validation
    errors_before = contact.errors_present()
    assert len(errors_before) > 0, "Expected validation errors after empty submit"

    forename_err = contact.get_forename_error()
    email_err    = contact.get_email_error()
    message_err  = contact.get_message_error()

    assert "required" in forename_err.lower(), f"Unexpected forename error: {forename_err}"
    assert "required" in email_err.lower(),    f"Unexpected email error: {email_err}"
    assert "required" in message_err.lower(),  f"Unexpected message error: {message_err}"

    # 4. Populate mandatory fields
    contact.fill_mandatory_fields()

    # 5. Validate errors are gone (Angular clears them on valid input)
    time.sleep(1)
    errors_after = contact.errors_present()
    assert len(errors_after) == 0, \
        f"Expected no errors after filling fields, still found: {[e.text for e in errors_after]}"
