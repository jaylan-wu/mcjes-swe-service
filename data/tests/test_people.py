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
NO_SUB_DOMAIN = 'janedoe@com'
DOMAIN_TOO_SHORT = 'janedoe@nyu.e'
DOMAIN_TOO_LONG = 'janedoe@nyu.eedduu'

TEMP_EMAIL = 'temp_person@example.org'


@pytest.fixture(scope='function')
def temp_person():
    email = ppl.create('Joe Smith', 'NYU', TEMP_EMAIL, TEST_ROLE_CODE)
    yield email
    try:
        ppl.delete(email)
    except:
        print('Person already deleted.')


def test_get_mh_fields():
    flds = ppl.get_mh_fields()
    assert isinstance(flds, list)
    assert len(flds) > 0


def test_create_mh_rec(temp_person):
    person_rec = ppl.read_one(temp_person)
    mh_rec = ppl.create_mh_rec(person_rec)
    assert isinstance(mh_rec, dict)
    for field in ppl.MH_FIELDS:
        assert field in mh_rec


def test_has_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert ppl.has_role(person_rec, TEST_ROLE_CODE)


def test_doesnt_have_role(temp_person):
    person_rec = ppl.read_one(temp_person)
    assert not ppl.has_role(person_rec, 'Not a good role!')


def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)


def test_is_valid_no_name():
    assert not ppl.is_valid_email(NO_NAME)


def test_is_valid_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)


def test_is_valid_no_sub_domain():
    assert not ppl.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not ppl.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not ppl.is_valid_email(DOMAIN_TOO_LONG)


def test_read(temp_person):
    # Test that the read function correctly retrieves all users from the database
    # Verifies that the function returns a dictionary of users keyed on user email
    # and that the dictionary has the correct structure
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for email, person in people.items():
        assert isinstance(email, str)
        assert ppl.NAME in person


def test_read_one(temp_person):
    assert ppl.read_one(temp_person) is not None


def test_read_one_not_there():
    assert ppl.read_one('Not an existing email!') is None


def test_exists(temp_person):
    assert ppl.exists(temp_person)


def test_doesnt_exist():
    assert not ppl.exists('Not an existing email!')


def test_delete(temp_person):
    ppl.delete(temp_person)
    assert not ppl.exists(temp_person)


def test_create():
    ppl.create('Joe Smith', 'NYU', ADD_EMAIL, TEST_ROLE_CODE)
    assert ppl.exists(ADD_EMAIL)
    ppl.delete(ADD_EMAIL)


def test_create_duplicate(temp_person):
    with pytest.raises(ValueError):
        ppl.create('Random name',
                   'Random affiliation', temp_person, 
                   TEST_ROLE_CODE)


VALID_ROLES = ['ED', 'AU']


@pytest.mark.skip('Skipping because not done.')
def test_update(temp_person):
    ppl.update('Buffalo Bill', 'UBuffalo', temp_person, VALID_ROLES)


@pytest.mark.skip('Skipping because not done.')
def test_update_not_there(temp_person):
    with pytest.raises(ValueError):
        ppl.update('Will Fail', 'University of the Void',
                   'Non-existent email', VALID_ROLES)


def test_create_bad_email():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                    'Or affiliation', 'bademail', TEST_ROLE_CODE)


def test_get_masthead():
    mh = ppl.get_masthead()
    assert isinstance(mh, dict)