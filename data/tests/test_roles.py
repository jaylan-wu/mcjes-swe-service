import pytest

from unittest.mock import patch

import data.roles as rls

@pytest.fixture
def roles():
    return rls.get_roles()

def test_get_roles(roles):
    if len(roles) == 0:
        pytest.skip('No roles available')
    assert isinstance(roles, dict)
    assert len(roles) > 0
    for role_code, role in roles.items():
        assert isinstance(role_code, str)
        assert isinstance(role, dict)

def test_get_role_codes():
    role_codes = rls.get_role_codes()
    assert isinstance(role_codes, list)
    assert len(role_codes) > 0
    for code in role_codes:
        assert isinstance(code, str)

@pytest.fixture
def test_code():
    return rls.TEST_CODE

def test_is_valid(test_code):
    assert rls.is_valid(test_code)


@pytest.fixture
def masthead_roles():
    return rls.get_masthead_roles()

def test_get_masthead_roles(masthead_roles):
    print(masthead_roles)
    assert isinstance(masthead_roles, dict)
    for code, role in masthead_roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)
