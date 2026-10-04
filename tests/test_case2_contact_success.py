import pytest

from pages.contact_page import ContactPage
from pages.home_page import HomePage
from tests.expected_data import CONTACT_SUCCESS_TEMPLATE


# Five runs of the same journey are a deliberate stability check (the brief
# asks for 100% pass rate), so each run uses distinct data to avoid any
# false pass from state left over by a previous submission.
@pytest.mark.parametrize("run", range(1, 6))
def test_contact_form_successful_submission(driver, run):
    forename = f"Tester{run}"

    HomePage(driver).load().go_to_contact()
    contact = ContactPage(driver).wait_for_form()

    contact.fill_mandatory_fields(
        forename=forename,
        email=f"tester{run}@example.com",
        message=f"Automated test submission run {run}.",
    )
    contact.click_submit()

    assert contact.get_success_message() == CONTACT_SUCCESS_TEMPLATE.format(forename=forename)
