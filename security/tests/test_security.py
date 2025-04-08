import pytest  # type: ignore

import security.security as sec

def test_check_login_good():
    assert sec.check_login(sec.GOOD_USER_ID,
                           login_key='any key will do for now')

def test_check_login_bad():
    assert not sec.check_login(sec.GOOD_USER_ID)