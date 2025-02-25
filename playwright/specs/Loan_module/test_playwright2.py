# import json
import time

from playwright.sync_api import Page


def test_playwright2(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")


def test_playwrightshortcut2(page:Page):
     # with open('Data/credentials.json') as f:
     #     test_Data = json.load(f)
     #      # print(test_Data)
    page.goto("https://rahulshettyacademy.com/loginpagePractise/")
    page.get_by_label("Username:").fill("rahulshettyacademy")
    page.get_by_label("Password:").fill("learning")
    page.get_by_role("combobox").select_option("teach")
    page.locator("#terms").click()
    page.get_by_role("button",name="Sign in").click()
    time.sleep(5)