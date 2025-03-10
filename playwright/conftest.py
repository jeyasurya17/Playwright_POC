from email.policy import default

from playwright.sync_api import Playwright
import pytest
import os
import yaml

def pytest_runtest_protocol(item, nextitem):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    print(f" Running {item.name} on Worker {worker_id}")
    return None

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa", help="Specify the environment (qa, dev, stage)")
    parser.addoption("--url", action="store", default="https://google.com", help="Site url for test")
    parser.addoption("--browser-name", action="store", default="msedge", help="Browser name for test")
    parser.addoption("--headed-browser", action="store_false", help="Browser in headed mode for test")

# Load the environment settings from the YAML file
def load_environment_config(env):
    with open("environments.yaml", "r") as f:
        config = yaml.safe_load(f)
    return config.get(env)

# Fixture to handle the environment configuration
@pytest.fixture(scope="session")
def environment(request):
    # Get the environment passed via the command line, default to 'qa'
    env = request.config.getoption("--env")
    config = load_environment_config(env)
    if config is None:
        pytest.exit(f"Environment '{env}' is not defined in environments.yaml")
    return config

# qa dev stage (load those file values like qa url)
@pytest.fixture(scope="function")
def playwright_browser_context(playwright : Playwright,request,environment):
    browserName = request.config.getoption("--browser-name")
    headlessMode = request.config.getoption("--headed-browser")
    browser = playwright.chromium.launch( channel=browserName,headless=headlessMode)
    context = browser.new_context()
    page =  context.new_page()
    #url = request.config.getoption("--url")
    url = environment['url']
    page.goto(url)
    # https://rahulshettyacademy.com/AutomationPractice/
    yield page
    page.close()
    browser.close()