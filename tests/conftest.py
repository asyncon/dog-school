import pytest
from fastapi.testclient import TestClient

from dog_school import __version__, main


@pytest.fixture
def version():
    return __version__


@pytest.fixture
def app():
    yield TestClient(main.app)
