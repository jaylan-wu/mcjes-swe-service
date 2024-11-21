"""
In this module, we interface with the People Datatype
"""
import re

import data.db_connect as dbc
import data.roles as rls

PEOPLE_COLLECTION = 'people'

# data fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

CW_EMAIL = 'caw9180@nyu.edu'
ED_EMAIL = 'ed233@nyu.edu'
JW_EMAIL = 'jw6639@nyu.edu'
SR_EMAIL = 'sr5826@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'

people_dict = {
    CW_EMAIL: {
        NAME: 'Cheyenne Williams',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: CW_EMAIL,
    },
    ED_EMAIL: {
        NAME: 'Eduardo De Los Santos',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: ED_EMAIL,
    },
    JW_EMAIL: {
        NAME: 'Jaylan Wu',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: JW_EMAIL,
    },
    SR_EMAIL: {
        NAME: 'Saadat Rafin',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: SR_EMAIL,
    },
    DEL_EMAIL: {
        NAME: 'DELETE',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: DEL_EMAIL,
    },
}

client = dbc.connect_db()
print(f'{client=}')

CHAR_OR_DIGIT = '[A-Za-z0-9]'
VALID_CHARS = '[A-Za-z0-9_.]'

'''
def is_valid_email(email: str) -> bool:
    return re.match(f"{CHAR_OR_DIGIT}.*@{CHAR_OR_DIGIT}.*", email)
'''


def is_valid_email(email: str) -> bool:
    """
    Contract:
    - Takes in email address (str)
    - Checks for all email componants
    - Returns a boolean if email is valid
    """
    pattern = f'^{VALID_CHARS}+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$'
    return re.match(pattern, email) is not None


def read() -> dict:
    """
    Contract:
    - No arguments
    - Returns a dictionary of users keyed on user email
    - Each user email must be the key for dictionary entry
    """
    print('read() has been called')
    # people = people_dict
    people = dbc.read_dict(PEOPLE_COLLECTION, EMAIL)
    print(f'{people=}')
    return people


def read_one(email: str) -> dict:
    """
    Contract:
    - Takes in id (unique email)
    - Searches dictionary for id
    - Returns person from dictionary if there
    - Returns None if no one is there
    """
    person = dbc.fetch_one(PEOPLE_COLLECTION, email)
    print(f'{person=}')
    return person


def delete(_id):
    """
    Contract:
    - Takes in id (unique email)
    - Searches dictionary for id
    - Returns and deletes email if found
    - Returns None if email not in dict
    """
    people = read()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str) -> bool:
    """
    Contract:
    - Takes in a Name, Affiliation, Email, and Role
    - Checks if:
        - The email already exists in the dictionary (raises error)
        - The email is valid (raises an error if invalid)
        - The role is valid using rls.is_valid (raises an error if invalid)
    - Returns True if all checks pass
    """
    if dbc.read_one(PEOPLE_COLLECTION, EMAIL, email):
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if not rls.is_valid(role):
        raise ValueError(f'Invalid role: {role}')
    return True


def create(name: str, affiliation: str, email: str, role: str):
    """
    Contract:
    - Takes in a Name, Affiliation, and Email
    - Returns email if added, else it will raise an error
    - Creating/adding user email to dict
    """
    if dbc.read_one(PEOPLE_COLLECTION, EMAIL, email):
        raise ValueError(f'Adding duplicate {email=}')
    if is_valid_person(name, affiliation, email, role):
        roles = []
        if role:
            roles.append(role)
        person = {
            NAME: name,
            AFFILIATION: affiliation,
            EMAIL: email,
            ROLES: roles
        }
        print(person)
        dbc.create(PEOPLE_COLLECTION, person)
        return email


def update(name: str, affiliation: str, email: str, roles: list):
    if email not in people_dict:
        raise ValueError(f'Updating non-existent person: {email=}')
    if is_valid_person(name, affiliation, email, roles=roles):
        people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                              EMAIL: email, ROLES: roles}
        return email


def has_role(person: dict, role: str) -> bool:
    if role in person.get(ROLES, []):
        return True
    return False


def get_masthead() -> dict:
    """
    Contract:
    - No arguments
    - Returns dictionary where keys are masthead role names and values are
      dictionaries of people with those roles.
    - Checks which people hold that role and organizes them into the masthead.
    """
    masthead = {}
    mh_roles = rls.get_masthead_roles()
    for mh_role, text in mh_roles.items():
        people_w_role = []
        people = read()
        for _id, person in people.items():
            if has_role(person, mh_role):
                rec = create_mh_rec(person)
                people_w_role.append(rec)
        masthead[text] = people_w_role
    return masthead


MH_FIELDS = [NAME, AFFILIATION]


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def main():
    print(read())
    print(get_masthead())
    print(f'{client=}')


if __name__ == '__main__':
    main()
