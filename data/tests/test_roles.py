import pytest

from data.roles import Roles

# Instantiate roles object for testing
rls = Roles()

# Test Variables
TEST_CODE = 'AU'
TEST_ROLE = 'Author'
TEST_IS_MASTHEAD = False

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


def test_exists():
    # Assert that the instance doesn't exist
    assert not rls.exists(TEST_CODE)
    # Create an instance and assert its existence
    rls.create(TEST_CODE, TEST_ROLE, TEST_IS_MASTHEAD)
    assert rls.exists(TEST_CODE)
    # Delete the instnace and assert that its deleted
    rls.delete(TEST_CODE)
    assert not rls.exists(TEST_CODE)


def test_create():
    if not rls.exists(TEST_CODE):
        rls.delete(TEST_CODE)
    rls.create(TEST_CODE, TEST_ROLE, TEST_IS_MASTHEAD)
    with pytest.raises(ValueError, match="Adding duplicate: role_code='AU'"):
        rls.create(TEST_CODE, TEST_ROLE, TEST_IS_MASTHEAD)
    assert rls.exists(TEST_CODE)
    rls.delete(TEST_CODE)


def test_read(temp_roles):
    roles = rls.read()
    if len(roles) == 0:
        pytest.skip('No roles available')
    assert isinstance(roles, dict)
    assert len(roles) > 0
    for role_code, role, is_masthead in test_roles:
        assert role_code in roles
        assert roles[role_code][rls.ROLE] == role
        assert roles[role_code][rls.IS_MASTHEAD] == is_masthead


def test_read_one(temp_roles):
    assert rls.read_one(TEST_CODE) is not None


def test_read_one_not_found():
    assert rls.read_one(TEST_CODE) is None


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
