import pytest # type: ignore

import data.people as ppl

from data.roles import TEST_CODE as TEST_ROLE_CODE

# test variables
ADD_EMAIL = "janedoe@nyu.edu"
NO_AT = "janedoenyu.edu"
NO_NAME = "@nyu.edu"
NO_DOMAIN = "janedoe@"
NO_EXT = "janedoe@nyu"

TEMP_EMAIL = 'temp_person@example.org'


@pytest.fixture(scope='function')
def temp_person():
    _id = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield _id
    ppl.delete(_id)
    

def test_read(temp_person):
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    person = ppl.read_one(temp_person)
    assert isinstance(person, dict)
    assert ppl.NAME in person
    assert 'email' in person
    assert isinstance(person['email'], str)


def test_delete():
    # Test case 1: Deleting an existing entry
    result = ppl.delete(ppl.DEL_EMAIL)
    assert result == ppl.DEL_EMAIL, f"Expected {ppl.DEL_EMAIL} to be returned, but got {result}"

    # Ensure the entry has been deleted
    people = ppl.read()
    assert ppl.DEL_EMAIL not in people, "The entry should have been deleted but was found in the dictionary."

    # Test case 2: Attempting to delete a non-existent entry
    result = ppl.delete(TEMP_EMAIL)
    assert result is None, f"Expected None to be returned for non-existent ID, but got {result}"


def test_create():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create('Joe Smith', 'NYU', ADD_EMAIL, TEST_ROLE_CODE)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_create_dupe():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                   'Or affiliation', ppl.JW_EMAIL,  TEST_ROLE_CODE)
        

VALID_ROLES = ['ED', 'AU']


@pytest.mark.skip('Skipping because not done.')
def test_update(temp_person):
    ppl.update('Buffalo Bill', 'UBuffalo', temp_person, VALID_ROLES)


@pytest.fixture
def invalid_emails():
    return ['bademail', 'no_at', 'no_name', 'no_domain', 'no_ext']

def test_create_bad_email(invalid_emails):
    for email in invalid_emails:
        with pytest.raises(ValueError):
            ppl.create('Do not care about name',
                       'Or affiliation', email, TEST_ROLE_CODE)
            

@pytest.fixture
def valid_emails():
    return [ADD_EMAIL]

def test_create(valid_emails):
    for email in valid_emails:
        ppl.create('Joe Smith', 'NYU', email, TEST_ROLE_CODE)
        people = ppl.read()
        assert email in people