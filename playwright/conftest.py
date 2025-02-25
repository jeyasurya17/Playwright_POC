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