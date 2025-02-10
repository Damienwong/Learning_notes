import pytest


def add(x, y):
    return x + y


def test_add():
    assert add(2, 3) == 5
    assert add(-2, 2) == 0


def test_example():
    assert 1 + 1 == 2
    assert 'hello'.upper() == 'HELLO'
    assert len([1, 2, 3]) == 3


@pytest.mark.parametrize('x, y, expected', [
    (1, 2, 3),
    (-2, 2, 0),
    (10, 5, 15)
])
def test_add1(x, y, expected):
    assert x + y == expected


@pytest.fixture
def sample_data():
    return {'name': 'Alice', 'age': 25}


def test_sample_data(sample_data):
    assert sample_data['name'] == 'Alice'
    assert sample_data['age'] == 25