# from functools import wraps

# Constants
COLLECT_NAME = 'security'
CREATE = 'create'
READ = 'read'
UPDATE = 'update'
DELETE = 'delete'
USER_LIST = 'user_list'
CHECKS = 'checks'
LOGIN = 'login'
LOGIN_KEY = 'login_key'

# Features (Examples)
PEOPLE = 'people'
BAD_FEATURE = 'bad_feature'

# Good test user
GOOD_USER_ID = 'jw6639@nyu.edu'

# Simulated DB records
# TODO: transition these to to DB records
TEST_RECS = {
    PEOPLE: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                LOGIN: True,
            },
        },
    },
    BAD_FEATURE: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                LOGIN: True,
            },
        },
    },
}

# Globals
security_recs = None


def is_valid_key(user_id: str, login_key: str):
    """
    TODO: implement a proper is_valid_key later on
    """
    return True


def check_login(user_id: str, **kwargs):
    if LOGIN_KEY not in kwargs:
        return False
    return is_valid_key(user_id, kwargs[LOGIN_KEY])


CHECK_FUNCS = {
    LOGIN: check_login,
    # Future: add more checks here
}


# Utility to load security records
def read() -> dict:
    global security_recs
    security_recs = TEST_RECS
    return security_recs
