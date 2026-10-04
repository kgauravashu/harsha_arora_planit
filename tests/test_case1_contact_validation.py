from pages.contact_page import ContactPage
from pages.home_page import HomePage
from tests.expected_data import CONTACT_ERRORS


def test_contact_form_validation_errors(driver):
    HomePage(driver).load().go_to_contact()
    contact = ContactPage(driver).wait_for_form()

    contact.click_submit()
    contact.wait_for_error_count(len(CONTACT_ERRORS))

    # Exact-match each message: a substring check such as "required" would
    # still pass if the wrong field showed the wrong (or a different) error.
    assert contact.get_forename_error() == CONTACT_ERRORS["forename"]
    assert contact.get_email_error() == CONTACT_ERRORS["email"]
    assert contact.get_message_error() == CONTACT_ERRORS["message"]

    contact.fill_mandatory_fields()

    contact.wait_for_error_count(0)
