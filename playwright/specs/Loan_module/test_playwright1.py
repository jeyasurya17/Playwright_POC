from playwright.sync_api import expect

def test_validateButtons(playwright_browser_context):
    page = playwright_browser_context
    buttons = page.locator(".btn-primary")
    assert buttons.count() == 5
    print("Executed validating buttons count test")


def test_selectRadioButton(playwright_browser_context):
    page = playwright_browser_context
    radioButton = page.locator("//input[@name= 'radioButton']")
    radioButton_list = radioButton.all()
    radioButton_list[1].click()
    expect(radioButton_list[1]).to_be_checked()
    print("Executed selecting radio button test")