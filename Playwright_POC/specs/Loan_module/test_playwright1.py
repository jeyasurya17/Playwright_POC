import logging

from playwright.sync_api import expect

from Playwright_POC.conftest import regression,sanity

#@pytest.mark.regression
#@pytest.mark.xdist_group(name="group2")
@regression
def test_validateButtons(playwright_browser_context):
    page = playwright_browser_context
    buttons = page.locator(".btn-primary")
    assert buttons.count() == 5
    #print("Executed validating buttons count test")
    logging.info("Executed validating radio button test")



#@pytest.mark.sanity
#@pytest.mark.xdist_group(name="group1")
@sanity
def test_selectRadioButton(playwright_browser_context):
    page = playwright_browser_context
    radioButton = page.locator("//input[@name= 'radioButton']")
    radioButton_list = radioButton.all()
    radioButton_list[1].click()
    expect(radioButton_list[1]).to_be_checked()
    #print("Executed selecting radio button test")
    logging.info("Executed selecting radio button test")


#@pytest.mark.sanity
#@pytest.mark.xdist_group(name="group1")
@sanity
def test_playwright_saucelabs(playwright):
    browser = playwright.chromium.launch(channel="msedge",headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.saucedemo.com/")