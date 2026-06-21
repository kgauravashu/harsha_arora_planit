import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def get_driver():
    options = Options()
    if os.environ.get("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")

    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    except Exception:
        return webdriver.Chrome(options=options)


@pytest.fixture
def driver(request):
    drv = get_driver()
    drv.implicitly_wait(0)
    yield drv

    # On failure: save screenshot + page source for debugging
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        screenshot_dir = "failure_screenshots"
        os.makedirs(screenshot_dir, exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace(":", "_")
        drv.save_screenshot(f"{screenshot_dir}/{safe_name}.png")
        with open(f"{screenshot_dir}/{safe_name}_source.html", "w") as f:
            f.write(drv.page_source)

    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
