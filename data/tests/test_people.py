import pytest # type: ignore

from data.people import People
from data.roles import Roles
from data.utilities import Utilities

# Instantiate Roles Object
ppl = People()
rls = Roles()
util = Utilities()

# Test Variables
TEST_EMAIL = 'janedoe@nyu.edu'
TEST_INEXISTENT_EMAIL = 'john@nyu.edu'
TEST_ROLE_CODE = 'AU'

test_roles = [
    ('AU', 'Author', False),
    ('CE', 'Consulting Editor', True),
    ('ED', 'Editor', True),
    ('ME', 'Managing Editor', True),
    ('RE', 'Referee', False),
]

@pytest.fixture(scope='function')
def temp_person():
    for role_code, role, is_masthead in test_roles:
        rls.create(role_code, role, is_masthead)
    person = ppl.create('Jane', 'Doe', 'NYU', TEST_EMAIL, [TEST_ROLE_CODE])
    yield person
    try:
        ppl.delete(person)
        for role_code, role, is_masthead in test_roles:
            rls.delete(role_code)
    except:
        print('Person already deleted.')


def test_exists():
    for role_code, role, is_masthead in test_roles:
        rls.create(role_code, role, is_masthead)
    if not ppl.exists(TEST_EMAIL):
        ppl.delete(TEST_EMAIL)
    ppl.create('Jane', 'Doe', 'NYU', TEST_EMAIL, [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Adding duplicate: email='janedoe@nyu.edu'"):
        ppl.create('Jane', 'Doe', 'NYU', TEST_EMAIL, [TEST_ROLE_CODE])
    assert ppl.exists(TEST_EMAIL)
    ppl.delete(TEST_EMAIL)
    for role_code, role, is_masthead in test_roles:
        rls.delete(role_code)


def test_is_valid_person(temp_person):
    assert ppl.is_valid_person('test@example.com', [TEST_ROLE_CODE]) == True
    with pytest.raises(ValueError, match="Invalid email: test@exa"):
        ppl.is_valid_person('test@exa', [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Invalid role: NO"):
        ppl.is_valid_person('test@example.com', ["NO"]) 


def test_create():
    for role_code, role, is_masthead in test_roles:
        rls.create(role_code, role, is_masthead)
    if ppl.exists(TEST_EMAIL):
        ppl.delete(TEST_EMAIL)
    ppl.create('Jane', 'Doe', 'NYU', TEST_EMAIL, [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Adding duplicate: email='janedoe@nyu.edu'"):
        ppl.create('Jane', 'Doe', 'NYU', TEST_EMAIL, [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Invalid email: test@exa"):
        ppl.create('Jane', 'Doe', 'NYU', 'test@exa', [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Invalid role: NO"):
        ppl.create('Jane', 'Doe', 'NYU', 'test@nyu.edu', ["NO"])
    assert ppl.exists(TEST_EMAIL)
    ppl.delete(TEST_EMAIL)
    for role_code, role, is_masthead in test_roles:
        rls.delete(role_code)


def test_read(temp_person):
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for email, person in people.items():
        assert isinstance(email, str)
        assert ppl.FIRST_NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(TEST_EMAIL) is not None


def test_read_one_not_found():
    assert ppl.read_one(TEST_EMAIL) is None


def test_update(temp_person):
    with pytest.raises(ValueError, match="Updating non-existent person: email='john@nyu.edu'"):
        ppl.update('Jane', 'Doe', 'NYU', TEST_INEXISTENT_EMAIL, [TEST_ROLE_CODE])
    with pytest.raises(ValueError, match="Invalid role: NO"):
        ppl.update('Jane', 'Doe', 'NYU', TEST_EMAIL, ["NO"])
    ppl.update('Buffalo', 'Bill', 'UBuffalo', TEST_EMAIL, [TEST_ROLE_CODE])


def test_has_role(temp_person):
    assert ppl.has_role(ppl.read_one(temp_person), TEST_ROLE_CODE) == True
    assert ppl.has_role(ppl.read_one(temp_person), 'NO') == False


def test_get_masthead(temp_person):
    ppl.create('Jane', 'Doe', 'NYU', "jane@nyu.edu", ['CE'])
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)
    ppl.delete('jane@nyu.edu')