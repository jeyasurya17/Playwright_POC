## _Playwright Pytest Framework_
Using Playwright Pytest created this framework for UI e2e automation POC, exploring framework capabilities like parallel test execution, define test tags, run tests using tag/suite or both, using pytest fixtures, Allure report integration.

### _Prerequisites:_
- Python3 
- (Will list others like Allure(Java))

### _Setup:_
- To install project dependencies run cmd:
``pip install -r requirements.txt``

### _Test Fixtures (Hook Class):_


### _Parallel Execution:_
With [pytest-xdist](https://pypi.org/project/pytest-xdist/) plugin define `--numprocesses` or `-n` with values like `auto`/`logical`/`numberOfProcesses>2`.


### _Tags:_


### _Test Execution:_


### Reporting (Allure):
With [allure-pytest](https://allurereport.org/docs/pytest/) adaptor