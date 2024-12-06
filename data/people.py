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


def is_valid_email(email: str) -> bool:
    """
    Contract:
    - Takes in email address (str)
    - Checks for all email componants
    - Returns a boolean if email is valid
    """
    pattern = f'^{VALID_CHARS}+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,3}}$'
    return re.match(pattern, email) is not None


def read() -> dict:
    """
    Contract:
    - No arguments
    - Returns a dictionary of users keyed on user email
    - Each user email must be the key for dictionary entry
    """
    people = dbc.read_dict(PEOPLE_COLLECTION, EMAIL)
    print(f'{people=}')
    return people


def read_one(email: str) -> dict:
    """
    Contract:
    - Takes in an email
    - Returns person from dictionary if there
    - Returns None if no one is there
    """
    return dbc.read_one(PEOPLE_COLLECTION, {EMAIL: email})


def exists(email: str) -> bool:
    """
    Contract:
    - Takes in an email
    - Returns True if the person exists in database, False otherwise
    """
    return dbc.read_one(PEOPLE_COLLECTION, {EMAIL: email}) is not None


def delete(email: str):
    """
    Contract:
    - Takes in an email
    - Returns and deletes email if found
    - Returns None if email not in dict
    """
    print(f'{EMAIL=}, {email=}')
    return dbc.delete(PEOPLE_COLLECTION, {EMAIL: email})


def is_valid_person(name: str, affiliation: str, email: str,
                    role: str = None, roles: list = None) -> bool:
    """
    Contract:
    - Takes in a Name, Affiliation, Email, and Role
    - Checks if:
        - Email already exists in the dictionary (raises error)
        - Email is valid (raises an error if invalid)
        - The role is valid using rls.is_valid
    - Returns True if all checks pass
    """
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if role:
        if not rls.is_valid(role):
            raise ValueError(f'Invalid role: {role}')
    elif roles:
        for role in roles:
            if not rls.is_valid(role):
                raise ValueError(f'Invalid role: {role}')
    return True


def create(name: str, affiliation: str, email: str, role: str):
    """
    Contract:
    - Takes in a Name, Affiliation, and Email
    - Returns email if added, else raise an error
    - Creating/adding user email to dict
    """
    if exists(email):
        raise ValueError(f'Adding duplicate {email=}')
    if is_valid_person(name, affiliation, email, role=role):
        roles = []
        if role:
            roles.append(role)
        person = {NAME: name, AFFILIATION: affiliation,
                  EMAIL: email, ROLES: roles}
        print(person)
        dbc.create(PEOPLE_COLLECTION, person)
        return email


def update(name: str, affiliation: str, email: str, roles: list):
    """
     Contract:
    - Takes in a Name, Affiliation, Email, and Roles
    - Updates person's details in database if exists, else error
    - Returns modified count if updated
    """
    if not exists(email):
        raise ValueError(f'Updating non-existent person: {email=}')
    if is_valid_person(name, affiliation, email, roles=roles):
        ret = dbc.update(PEOPLE_COLLECTION,
                         {EMAIL: email},
                         {NAME: name, AFFILIATION: affiliation,
                          EMAIL: email, ROLES: roles})
        print(f'{ret=}')
        return email


def has_role(person: dict, role: str) -> bool:
    """
    Contract:
    - Takes in person dictionary and a Role
    - Returns True if the person has the role, False otherwise
    """
    if role in person.get(ROLES):
        return True
    return False


MH_FIELDS = [NAME, AFFILIATION]


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


def get_mh_fields(journal_code=None) -> list:
    return MH_FIELDS


def create_mh_rec(person: dict) -> dict:
    mh_rec = {}
    for field in get_mh_fields():
        mh_rec[field] = person.get(field, '')
    return mh_rec


def main():
    print(get_masthead())


if __name__ == '__main__':
    main()
