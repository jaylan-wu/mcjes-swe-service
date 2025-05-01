import pytest  # type: ignore

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

def test_is_permitted_missing_user_list():
    # Simulate action info missing USER_LIST (should skip that check)
    sec.security_recs = {
        'some_feature': {
            'some_action': {
                sec.CHECKS: {
                    sec.LOGIN: True,
                }
            }
        }
    }
    assert sec.is_permitted('some_feature', 'some_action', sec.GOOD_USER_ID,
                             login_key='valid_key')

def test_is_permitted_missing_checks():
    # Simulate action with just USER_LIST, no CHECKS
    sec.security_recs = {
        'some_feature': {
            'some_action': {
                sec.USER_LIST: [sec.GOOD_USER_ID]
            }
        }
    }
    assert sec.is_permitted('some_feature', 'some_action', sec.GOOD_USER_ID)

def test_is_permitted_check_fails():
    # IP_ADDR check will fail because no ip_address is provided
    assert not sec.is_permitted(sec.TEXTS, sec.DELETE, sec.GOOD_USER_ID,
                                login_key='valid_key')

def test_is_permitted_check_passes_all():
    # Provide all required values for TEXTS.DELETE
    assert sec.is_permitted(sec.TEXTS, sec.DELETE, sec.GOOD_USER_ID,
                            login_key='valid_key', ip_address='127.0.0.1')

def test_is_permitted_unknown_check_raises():
    # Insert an invalid check name
    sec.security_recs = {
        'bad_feature': {
            'bad_action': {
                sec.USER_LIST: [sec.GOOD_USER_ID],
                sec.CHECKS: {
                    'nonexistent_check': True
                }
            }
        }
    }
    with pytest.raises(ValueError, match="Bad check passed to is_permitted"):
        sec.is_permitted('bad_feature', 'bad_action', sec.GOOD_USER_ID)

def test_is_permitted_check_not_required_skips():
    # Ensure it skips checks marked as False
    sec.security_recs = {
        'skippable_check_feature': {
            'some_action': {
                sec.USER_LIST: [sec.GOOD_USER_ID],
                sec.CHECKS: {
                    sec.LOGIN: False,
                    sec.IP_ADDR: False,
                }
            }
        }
    }
    assert sec.is_permitted('skippable_check_feature', 'some_action',
                            sec.GOOD_USER_ID)