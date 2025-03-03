import pytest

from Playwright_POC.playwright.conftest import regression


#@pytest.mark.regression
#@pytest.mark.xdist_group(name="group2")
@regression
def test_validatePageHeaderValue(playwright_browser_context):
    page = playwright_browser_context
    headervalue = page.locator("//h1").text_content()
    assert headervalue == 'Practice Page',f"But found {headervalue}"
    print("Executed validating header value test")


#@pytest.mark.regression
#@pytest.mark.xdist_group(name="group2")
@regression
def test_selectCheckBox(playwright_browser_context):
    page = playwright_browser_context
    checkbox = page.locator("//input[@id='checkBoxOption1']")
    checkbox.click()
    assert checkbox.is_checked() is True,"checkbox should be checked"
    print("Executed selecting checkbox test")


def test_playwright_saucelabs2(playwright):
    browser = playwright.chromium.launch(channel="msedge",headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
