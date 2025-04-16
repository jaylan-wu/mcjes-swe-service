from functools import wraps

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
IP_ADDR = 'ip_address'
DUAL_FACTOR = 'dual_factor'

# Features (Examples)
PEOPLE = 'people'
TEXTS = 'texts'
BAD_FEATURE = 'bad_feature'
PEOPLE_MISSING_ACTION = READ

# Good test user
GOOD_USER_ID = 'jw6639@nyu.edu'

PEOPLE_CHANGE_PERMISSIONS = {
    USER_LIST: [GOOD_USER_ID],
    CHECKS: {
        LOGIN: True,
    },
}

# Simulated DB records
# TODO: transition these to to DB records
TEST_RECS = {
    PEOPLE: {
        CREATE: PEOPLE_CHANGE_PERMISSIONS,
        DELETE: PEOPLE_CHANGE_PERMISSIONS,
        UPDATE: PEOPLE_CHANGE_PERMISSIONS,
    },
    TEXTS: {
        CREATE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                LOGIN: True,
            },
        },
        DELETE: {
            USER_LIST: [GOOD_USER_ID],
            CHECKS: {
                LOGIN: True,
                IP_ADDR: True,
                DUAL_FACTOR: True,
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


def check_ip(user_id: str, **kwargs):
    if IP_ADDR not in kwargs:
        return False
    # we would check user's IP address here
    return True


def dual_factor(user_id: str, **kwargs):
    return True


CHECK_FUNCS = {
    LOGIN: check_login,
    # Future: add more checks here
    IP_ADDR: check_ip,
    DUAL_FACTOR: dual_factor,
}


# Utility to load security records
def read() -> dict:
    global security_recs
    security_recs = TEST_RECS
    return security_recs


def needs_recs(fn):
    """Decorator: load security records if not already loaded"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global security_recs
        if security_recs is None:
            security_recs = read()
        return fn(*args, **kwargs)
    return wrapper


@needs_recs
def read_feature(feature_name: str) -> dict:
    return security_recs.get(feature_name)


@needs_recs
def is_permitted(feature_name: str, action: str,
                 user_id: str, **kwargs) -> bool:
    prot = read_feature(feature_name)
    if prot is None:
        return True
    if action not in prot:
        return True
    action_info = prot[action]
    if USER_LIST in action_info:
        if user_id not in action_info[USER_LIST]:
            return False
    if CHECKS not in action_info:
        return True
    for check_name, check_required in action_info[CHECKS].items():
        if not check_required:
            continue  # If check isn't required, skip it
        if check_name not in CHECK_FUNCS:
            raise ValueError(f'Bad check passed to is_permitted: {check_name}')
        if not CHECK_FUNCS[check_name](user_id, **kwargs):
            return False
    return True
