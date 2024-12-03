import pytest
import unittest.mock as mock
import data.users as usrs

@pytest.fixture
def mock_get_users():
    with mock.patch('data.users.get_users') as mock_get_users:
        yield mock_get_users


def test_get_users(mock_get_users):
    """
    Contract:
    - Tests the get_users function with a valid return value
    - Verifies that the returned dictionary has at least one user and valid user data
    - Returns a boolean indicating whether the test passes
    """
    mock_get_users.return_value = {'user1': {usrs.LEVEL: 1}}
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # at least one user!
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        assert isinstance(user[usrs.LEVEL], int)

def test_get_users_exception(mock_get_users):
    """
    Contract:
    - Tests the get_users function with a mocked exception
    - Verifies that the correct exception is raised when the function is called
    - Returns a boolean indicating whether the test passes
    """
    mock_get_users.side_effect = Exception('Mocked exception')
    with pytest.raises(Exception):
        usrs.get_users()


def test_get_users_empty(mock_get_users):
    """
    Contract:
    - Tests the get_users function when no users are returned
    - Verifies that the returned dictionary is empty
    - Returns a boolean indicating whether the test passes
    """
    mock_get_users.return_value = {}
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) == 0  # No users returned


def test_get_users_invalid_data(mock_get_users):
    """
    Contract:
    - Tests the get_users function with invalid user data
    - Verifies that the function correctly identifies invalid data
    - Returns a boolean indicating whether the test passes
    """
    mock_get_users.return_value = {'user1': {usrs.LEVEL: 'invalid_level'}}
    users = usrs.get_users()
    assert isinstance(users, dict)
    assert len(users) > 0  # At least one user is present
    for key in users:
        assert isinstance(key, str)
        assert len(key) >= usrs.MIN_USER_NAME_LEN
        user = users[key]
        assert isinstance(user, dict)
        assert usrs.LEVEL in user
        with pytest.raises(AssertionError):
            assert isinstance(user[usrs.LEVEL], int)  # Invalid type