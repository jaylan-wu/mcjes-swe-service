import pytest

import data.roles as rls

def test_is_valid():
    test_code = rls.TEST_CODE
    assert rls.is_valid(test_code)


def test_get_roles():
    roles = rls.get_roles()
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


def test_get_masthead_roles():
    masthead_roles = rls.get_masthead_roles()
    assert isinstance(masthead_roles, dict)
    for code, role in masthead_roles.items():
        assert isinstance(code, str)
        assert isinstance(role, str)
