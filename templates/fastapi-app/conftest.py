import os

import pytest


@pytest.hookimpl
def pytest_configure(config):
    os.environ["POSTGRES_DB"] = "test-<REPO_NAME>"
