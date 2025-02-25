def test_selectDropdownOption(playwright_browser_context):
    page = playwright_browser_context
    page.select_option("select#dropdown-class-example",value="Option1")
    selected_value =  page.locator("select#dropdown-class-example").input_value()
    assert selected_value=="option1",f"But found {selected_value}"
    print("Executed dropdpwn case")

def test_openwindow(playwright_browser_context):
    page = playwright_browser_context
    openwindow_button = page.locator("//button[@id='openwindow']")
    with page.expect_popup() as new_page: openwindow_button.click()
    popupValue  = new_page.value
    assert "QA" in popupValue.title()
    print("Executed open new window")