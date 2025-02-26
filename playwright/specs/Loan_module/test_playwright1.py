import pytest
from playwright.sync_api import expect

@pytest.mark.regression
@pytest.mark.xdist_group(name="group2")
def test_validateButtons(playwright_browser_context):
    page = playwright_browser_context
    buttons = page.locator(".btn-primary")
    assert buttons.count() == 5
    print("Executed validating buttons count test")


@pytest.mark.sanity
@pytest.mark.xdist_group(name="group1")
def test_selectRadioButton(playwright_browser_context):
    page = playwright_browser_context
    radioButton = page.locator("//input[@name= 'radioButton']")
    radioButton_list = radioButton.all()
    radioButton_list[1].click()
    expect(radioButton_list[1]).to_be_checked()
    print("Executed selecting radio button test")

@pytest.mark.sanity
@pytest.mark.xdist_group(name="group1")
def test_playwright_saucelabs(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")

