import pytest # type: ignore

import data.people as ppl

# test variables
ADD_EMAIL = "janedoe@nyu.edu"
NO_AT = "janedoenyu.edu"
NO_NAME = "@nyu.edu"
NO_DOMAIN = "janedoe@"
NO_EXT = "janedoe@nyu"

def test_is_valid_email_no_at():
    assert not ppl.is_valid_email(NO_AT)

def test_is_valid_email_no_name():
    assert not ppl.is_valid_email(NO_NAME)

def test_is_valid_email_no_domain():
    assert not ppl.is_valid_email(NO_DOMAIN)

def test_is_valid_email_no_ext():
    assert not ppl.is_valid_email(NO_EXT)



def test_read():
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # check for string IDs:
    for _id, person in people.items():
        assert isinstance(_id, str)
        assert ppl.NAME in person     


def test_read_one():
    # sample data for testing
    people = ppl.read()
    assert isinstance(people, dict)
    assert len(people) > 0
    # test with a valid _id that exists in the people dictionary
    valid_id = ppl.SR_EMAIL  # get the first key from the dictionary
    person = ppl.read_one(valid_id)
    assert person is not None
    assert ppl.NAME in person 


def test_delete():
    people = ppl.read()
    old_len = len(people)
    ppl.delete(ppl.DEL_EMAIL)
    people = ppl.read()
    assert len(people) < old_len
    assert ppl.DEL_EMAIL not in people


def test_create():
    people = ppl.read()
    assert ADD_EMAIL not in people
    ppl.create('Joe Smith', 'NYU', ADD_EMAIL)
    people = ppl.read()
    assert ADD_EMAIL in people


def test_create_dupe():
    with pytest.raises(ValueError):
        ppl.create('Do not care about name',
                   'Or affiliation', ppl.JW_EMAIL)
