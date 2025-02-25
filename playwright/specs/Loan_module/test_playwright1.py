import time

from playwright.sync_api import Page

def test_playwright1(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")


def test_playwrightshortcut1(page:Page):

    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning")
    page.get_by_role("combobox").select_option("teach")
    page.locator("#terms").click()
    page.get_by_role("button",name="Sign in").click()
    time.sleep(5)