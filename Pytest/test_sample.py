import pytest
from unittest.mock import MagicMock


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


@pytest.fixture(scope="session")
def db_connection():
    print('\nConnect with db')
    conn = 'database object'
    yield conn
    print('\nClose the connection')


def test_query_1(db_connection):
    print('\nConduct query1')
    assert db_connection == 'database object'


def test_query_2(db_connection):
    print('\nConduct query2')
    assert db_connection == 'database object'


@pytest.fixture
def user_data():
    return {'name': 'Alice', 'age': 25}


@pytest.fixture
def user_db(user_data):
    print('\n模拟写入数据库')
    return f"User {user_data['name']} added to DB"


def test_user_creation(user_db):
    assert 'Alice' in user_db


def fetch_data_from_api():
    # 假设这个函数会调用外部API
    raise RuntimeError('真实API不能被调用')


def test_mock_api():
    mock_api = MagicMock(return_value={'status': 'success', 'data': [1, 2, 3]})
    assert mock_api() == {'status': 'success', 'data': [1, 2, 3]}


def pytest_runtest_setup(item):
    print(f"\n[HOOK] 运行测试：{item.name}")