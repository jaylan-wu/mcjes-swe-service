import pytest # type: ignore

import data.people as ppl
import data.db_connect as dbc

from data.roles import TEST_CODE as TEST_ROLE_CODE
from data.people import PEOPLE_COLLECTION, EMAIL

# test variables
ADD_EMAIL = "janedoe@nyu.edu"
NO_AT = "janedoenyu.edu"
NO_NAME = "@nyu.edu"
NO_DOMAIN = "janedoe@"
NO_EXT = "janedoe@nyu"

TEMP_EMAIL = 'temp_person@example.org'


@pytest.fixture
def temp_person():
    person = {'email': 'test@example.com', 'name': 'Test User', 'level': 1}
    dbc.insert_one(PEOPLE_COLLECTION, person)
    yield person
    dbc.delete_one(PEOPLE_COLLECTION, EMAIL, person['email'])

def test_read(temp_person):
    # Test that the read function correctly retrieves all users from the database
    # Verifies that the function returns a dictionary of users keyed on user email
    # and that the dictionary has the correct structure
    people = dbc.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    for email, person in people.items():
        assert isinstance(email, str)
        assert EMAIL in person
        assert isinstance(person[EMAIL], str)


#@pytest.mark.skip('Skipping because not done.')
def test_read_one():
    # Test that the read_one function correctly retrieves a user from the database
    # Verifies that the function returns a dictionary representing the user
    # and that the dictionary has the correct structure
    email = 'test@example.com'
    expected_person = {'email': email, 'name': 'Test User', 'level': 1}
    filter = {'email': email}
    dbc.create(PEOPLE_COLLECTION, expected_person)
    person = ppl.read_one(filter)
    assert isinstance(person, dict)
    assert person['email'] == email
    assert person['name'] == expected_person['name']
    assert person['level'] == expected_person['level']
    dbc.del_one(PEOPLE_COLLECTION, filter)

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

def test_update_not_there(temp_person):
    with pytest.raises(ValueError):
        ppl.update('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)


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

def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)