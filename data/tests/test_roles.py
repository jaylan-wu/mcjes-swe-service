import pytest

import data.roles as rls
import data.db_connect as dbc

test_roles = [
    ('AU', 'Author', False),
    ('CE', 'Consulting Editor', True),
    ('ED', 'Editor', True),
    ('ME', 'Managing Editor', True),
    ('RE', 'Referee', False),
]

@pytest.fixture(scope='function')
def temp_roles():
    for role_code, role, is_masthead in test_roles:
        rls.create(role_code, role, is_masthead)
    yield
    for role_code, role, is_masthead in test_roles:
        rls.delete(role_code)


def test_is_valid(temp_roles):
    assert rls.is_valid(rls.TEST_CODE)


def test_get_roles(temp_roles):
    roles = rls.get_roles()
    if len(roles) == 0:
        pytest.skip('No roles available')
    assert isinstance(roles, dict)
    assert len(roles) > 0
    for role_code, role, is_masthead in test_roles:
        assert role_code in roles
        assert roles[role_code][rls.ROLE] == role
        assert roles[role_code][rls.IS_MASTHEAD] == is_masthead


def test_get_role_codes(temp_roles):
    role_codes = rls.get_role_codes()
    assert isinstance(role_codes, list)
    assert len(role_codes) > 0
    for code in role_codes:
        assert isinstance(code, str)


def test_get_masthead_roles(temp_roles):
    masthead_roles = rls.get_masthead_roles()
    assert isinstance(masthead_roles, dict)
    for code, role in masthead_roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)
