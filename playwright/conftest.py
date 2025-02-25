import pytest
import os

def pytest_runtest_protocol(item, nextitem):
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    print(f" Running {item.name} on Worker {worker_id}")
    return None
