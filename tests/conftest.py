import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

FAILURE_DIR = "failure_screenshots"


def _build_options():
    options = Options()
    if os.environ.get("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    # Chrome's sandbox cannot start inside most CI containers; locally we
    # keep it on, so the flag is only added when the CI env var is set.
    if os.environ.get("CI"):
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # small /dev/shm in containers
    return options


@pytest.fixture
def driver(request):
    # Selenium Manager (bundled with selenium >= 4.6) resolves a matching
    # chromedriver, so no third-party driver downloader is needed.
    drv = webdriver.Chrome(options=_build_options())
    yield drv

    report = getattr(request.node, "rep_call", None)
    if report is not None and report.failed:
        os.makedirs(FAILURE_DIR, exist_ok=True)
        name = request.node.name.replace("/", "_").replace(":", "_")
        drv.save_screenshot(f"{FAILURE_DIR}/{name}.png")
        with open(f"{FAILURE_DIR}/{name}_source.html", "w", encoding="utf-8") as fh:
            fh.write(drv.page_source)

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Exposes each phase's result to fixtures so teardown can tell if the test failed.
    outcome = yield
    setattr(item, f"rep_{outcome.get_result().when}", outcome.get_result())
