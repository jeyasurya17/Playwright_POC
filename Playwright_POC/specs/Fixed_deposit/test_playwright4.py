import pytest

from Playwright_POC.playwright.conftest import smoke, smokeandregression

@smoke
#@pytest.mark.smokeandregression
def test_alertBox(playwright_browser_context):
    page = playwright_browser_context
    alertBtn = page.locator("//input[@id='alertbtn']")
    alertBtn.click()
    def handle_alert(dialog):
        assert "Hello" in dialog.message
        dialog.accept()

    page.on('dialog', handle_alert)
    print("Executed Alert box test")

#@pytest.mark.smoke
#@pytest.mark.xdist_group(name="group3")
@smoke
def test_confirmBox(playwright_browser_context):
    page = playwright_browser_context
    confirmBtn = page.locator("//input[@id='confirmbtn']")
    confirmBtn.click()
    def handle_confirm(dialog):
        dialog.accept()

    page.on('dialog', handle_confirm)
    print("Executed confirm box test")