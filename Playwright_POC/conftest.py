import logging
from multiprocessing import get_logger

import yaml
from playwright.sync_api import Playwright, sync_playwright
import pytest
import os

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Specify the environment (qa, dev, stage)")
    parser.addoption("--url", action="store", default="https://google.com", help="Site url for test")
    parser.addoption("--browser-name", action="store", default="msedge", help="Browser name for test")
    parser.addoption("--headed-browser", action="store_false", help="Browser in headed mode for test")

# Load the environment settings from the YAML file
def load_environment_config(env):
    file_path = os.path.join(os.path.dirname(__file__), "environments.yaml")
    with open(file_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get(env)

@pytest.fixture(scope= "session",autouse=True)
def cleanup_traces():
    trace_dir = "Traces"
    if os.path.exists(trace_dir):
        try:
            shutil.rmtree(trace_dir)
        except FileNotFoundError:
            pass
    yield

# Fixture to handle the environment configuration
@pytest.fixture(scope="session")
def environment(request):
    # Get the environment passed via the command line, default to 'qa'
    env = request.config.getoption("--env")
    config = load_environment_config(env)
    if config is None:
        pytest.exit(f"Environment '{env}' is not defined in environments.yaml")
    return config

def pytest_runtest_protocol(item, nextitem):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    print(f" Running {item.name} on Worker {worker_id}")
    return None


# qa dev stage (load those file values like qa url)
@pytest.fixture(scope="function")
def playwright_browser_context(playwright : Playwright,request,environment):
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
    browserName = request.config.getoption("--browser-name")
    headlessMode = request.config.getoption("--headed-browser")
    browser = playwright.chromium.launch( channel=browserName,headless=headlessMode)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page =  context.new_page()
    #url = request.config.getoption("--url")
    url = environment['url']
    page.goto(url)
    # https://rahulshettyacademy.com/AutomationPractice/
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

#Not a working solution currently
def smokeandregression(func):
    """Custom decorator to apply multiple pytest markers."""
    func = pytest.mark.regression(func)
    func = pytest.mark.xdist_group(name="group2")(func)
    func = pytest.mark.smoke(func)
    func = pytest.mark.xdist_group(name="group3")(func)
    return func


# Configure logging for parallel execution
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(process)d] [%(levelname)s] - %(message)s",
    )

    # Ensure logs from worker processes are captured
    logger = get_logger()
    logger.setLevel(logging.INFO)

configure_logging()  # Apply logging before tests start
