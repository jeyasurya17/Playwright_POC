import pytest
import allure

@allure.title("validatePageHeaderValue")
@allure.description("Verify page header value is displayed in the webpage")
@allure.tag("regression(group2)")
@pytest.mark.regression
@pytest.mark.xdist_group(name="group2")
def test_validatePageHeaderValue(playwright_browser_context):
    page = playwright_browser_context
    headervalue = page.locator("//h1").text_content()
    assert headervalue == 'Practice Page',f"But found {headervalue}"
    print("Executed validating header value test")

@allure.title("selectCheckBox")
@allure.description("Verify user able to select the checkbox displayed in the webpage")
@allure.tag("regression(group2)")
@pytest.mark.regression
@pytest.mark.xdist_group(name="group2")
def test_selectCheckBox(playwright_browser_context):
    page = playwright_browser_context
    checkbox = page.locator("//input[@id='checkBoxOption1']")
    checkbox.click()
    assert checkbox.is_checked() is True,"checkbox should be checked"
    print("Executed selecting checkbox test")

@allure.title("Go to saucelabs2")
@allure.description("Verify page navigation to saucelabs site")
def test_playwright_saucelabs2(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")
