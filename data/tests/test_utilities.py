import pytest

# Import Utilities object
from data.utilities import Utilities

# Instantiate Utilities Object
util = Utilities()

# Test Variables
ADD_EMAIL = "janedoe@nyu.edu"
NO_AT = "janedoenyu.edu"
NO_NAME = "@nyu.edu"
NO_DOMAIN = "janedoe@"
NO_EXT = "janedoe@nyu"
NO_SUB_DOMAIN = 'janedoe@com'
DOMAIN_TOO_SHORT = 'janedoe@nyu.e'
DOMAIN_TOO_LONG = 'janedoe@nyu.eedduu'


def test_is_valid_email():
    assert util.is_valid_email(ADD_EMAIL)


def test_is_valid_email_no_at():
    assert not util.is_valid_email(NO_AT)


def test_is_valid_email_no_name():
    assert not util.is_valid_email(NO_NAME)


def test_is_valid_email_no_domain():
    assert not util.is_valid_email(NO_DOMAIN)


def test_is_valid_email_no_ext():
    assert not util.is_valid_email(NO_EXT)


def test_is_valid_email_no_sub_domain():
    assert not util.is_valid_email(NO_SUB_DOMAIN)


def test_is_valid_email_domain_too_short():
    assert not util.is_valid_email(DOMAIN_TOO_SHORT)


def test_is_valid_email_domain_too_long():
    assert not util.is_valid_email(DOMAIN_TOO_LONG)
