from playwright.sync_api import Playwright
import pytest
import os

def pytest_runtest_protocol(item, nextitem):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    print(f" Running {item.name} on Worker {worker_id}")
    return None

@pytest.fixture(scope="function")
def playwright_browser_context(playwright : Playwright,request):
    browser = playwright.chromium.launch( channel="msedge",headless=False)
    context = browser.new_context()
    page =  context.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    yield page
    page.close()
    browser.close()

def sanity(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.sanity(func)
    func = pytest.mark.xdist_group(name="group1")(func)
    return func

def regression(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.regression(func)
    func = pytest.mark.xdist_group(name="group2")(func)
    return func

def smoke(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.smoke(func)
    func = pytest.mark.xdist_group(name="group3")(func)
    return func

#Not a working solution currently
def smokeandregression(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.regression(func)
    func = pytest.mark.xdist_group(name="group2")(func)
    func = pytest.mark.smoke(func)
    func = pytest.mark.xdist_group(name="group3")(func)
    return func



