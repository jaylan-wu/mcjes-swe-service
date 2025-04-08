import pytest

import security.security as sec

def setup_function():
    """Reset security_recs before each test."""
    sec.security_recs = None

def test_check_login_good():
    assert sec.check_login(sec.GOOD_USER_ID, login_key='valid_key')

def test_check_login_bad():
    assert not sec.check_login(sec.GOOD_USER_ID)  # No login_key provided

def test_read():
    recs = sec.read()
    assert isinstance(recs, dict)
    for feature, actions in recs.items():
        assert isinstance(feature, str)
        assert isinstance(actions, dict)

def test_read_feature():
    recs = sec.read()
    feature = sec.read_feature(sec.PEOPLE)
    assert isinstance(feature, dict)

def test_is_permitted_no_such_feature():
    # If the feature does not exist, is_permitted returns True
    assert sec.is_permitted('non_existent_feature', sec.CREATE, 'any_user')

def test_is_permitted_action_missing():
    # If the action doesn't exist inside the feature, should still return True
    assert sec.is_permitted(sec.PEOPLE, sec.PEOPLE_MISSING_ACTION, 'any_user')

def test_is_permitted_bad_user():
    # User is not in the permitted user list
    assert not sec.is_permitted(sec.PEOPLE, sec.CREATE, 'wrong_user')

def test_is_permitted_all_good():
    # Correct user, correct feature, correct login_key
    assert sec.is_permitted(sec.PEOPLE, sec.CREATE, sec.GOOD_USER_ID,
                            login_key='valid_key')
