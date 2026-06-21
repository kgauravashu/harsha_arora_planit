import pytest
from pages.home_page import HomePage
from pages.contact_page import ContactPage


@pytest.mark.parametrize("run", range(1, 6))
def test_contact_form_successful_submission(driver, run):
    home    = HomePage(driver)
    contact = ContactPage(driver)

    # 1. From home page go to contact page
    home.load()
    home.go_to_contact()
    contact.wait_for_form()

    # 2. Populate mandatory fields
    contact.fill_mandatory_fields(
        forename=f"Tester{run}",
        email=f"tester{run}@example.com",
        message=f"Automated test submission run {run}."
    )

    # 3. Click Submit
    contact.click_submit()

    # 4. Validate successful submission message
    success_text = contact.get_success_message()
    assert success_text, f"Run {run}: No success message found"
    assert any(kw in success_text for kw in ["Thanks", "thank", "success", "submitted"]), \
        f"Run {run}: Unexpected success message: '{success_text}'"
