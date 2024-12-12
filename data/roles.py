import data.db_connect as dbc

ROLES_COLLECTION = 'roles'

# data fields
ROLE_CODE = 'role_code'
ROLE = 'role'
IS_MASTHEAD = 'is_masthead'

TEST_CODE = 'AU'


def is_valid(code: str) -> bool:
    roles = get_roles()
    return code in roles


def get_roles() -> dict:
    roles = dbc.read_dict(ROLES_COLLECTION, ROLE_CODE)
    print(f'{roles=}')
    return roles


def get_role_codes() -> list:
    roles = dbc.read_dict(ROLES_COLLECTION, ROLE_CODE)
    return list(roles.keys())


def get_masthead_roles() -> dict:
    roles = get_roles()
    masthead_roles = {code: data["role"] for code, data in roles.items()
                      if data["is_masthead"]}
    return masthead_roles


def main():
    print(get_roles())
    print(get_masthead_roles())


if __name__ == '__main__':
    main()
