import shutil

from playwright.sync_api import Playwright, sync_playwright
import pytest
import os

def pytest_runtest_protocol(item, nextitem):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    print(f" Running {item.name} on Worker {worker_id}")
    return None

@pytest.fixture(scope= "session",autouse=True)
def cleanup_traces():
    trace_dir = "Traces"
    if os.path.exists(trace_dir):
        try:
            shutil.rmtree(trace_dir)
        except FileNotFoundError:
            pass
    yield

# @pytest.fixture(scope="function")
# def playwright_browser_context(playwright : Playwright,request):
#     #browser = playwright.chromium.launch( channel="msedge",headless=False)
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page =  context.new_page()
#     page.goto("https://rahulshettyacademy.com/AutomationPractice/")
#     yield page
#     page.close()
#     browser.close()


@pytest.fixture(scope="function")
def playwright_browser_context(base_url,request):
    with sync_playwright() as p:
        group_marker = None
        for marker in request.node.iter_markers():
                group_marker = marker.name
                break
        else:
            group_marker = 'untagged'

        if group_marker:
            trace_dir = os.path.join("Traces", group_marker)

        if not os.path.exists(trace_dir):
            os.makedirs(trace_dir)

        test_id = request.node.nodeid.replace("::", "_")
        trace_file_path = os.path.join(trace_dir, f"{test_id}.zip")

        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = context.new_page()

        #print(f"base_url : {base_url}")
        #page.goto(base_url)
        page.goto("https://rahulshettyacademy.com/AutomationPractice/")
        yield page
        # if request.node.rep_call.failed:
        #     context.tracing.stop(path=trace_file_path)
        #     allure.attach.file(trace_file_path,name="Playwright Trace", attachment_type=allure.attachment_type.ZIP)
        # else:
        #     context.tracing.stop()  # Stop tracing without saving
        context.tracing.stop(path=trace_file_path)
        # allure.attach.file(trace_file_path, name="Playwright Trace", extension="ZIP")
        page.close()
        browser.close()

def sanity(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.sanity(func)
    func = pytest.mark.xdist_group(name="group1")(func)
    return func

def regression(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.regression(func)
    func = pytest.mark.xdist_group(name="group2")(func)
    return func

def smoke(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.smoke(func)
    func = pytest.mark.xdist_group(name="group3")(func)
    return func

# Not a working solution currently
def smokeandregression(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.regression(func)
    func = pytest.mark.xdist_group(name="group2")(func)
    func = pytest.mark.smoke(func)
    func = pytest.mark.xdist_group(name="group3")(func)
    return func


