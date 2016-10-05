import pytest

@pytest.fixture
def hello():
    return {
        'username': 'Hello Kitty',
        'host': 'Hello World'
    }