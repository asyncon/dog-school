import pytest

from dog_school import __version__


@pytest.fixture
def version():
    return __version__
