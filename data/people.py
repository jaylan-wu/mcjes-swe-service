"""
In this module, we interface with the People Datatype
"""
import re

import data.roles as rls

# data fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

# testing variables (TODO add more emails)
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

CHAR_OR_DIGIT = '[A-Za-z0-9]'

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
    pattern = f'^{CHAR_OR_DIGIT}+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,}}$'
    return re.match(pattern, email) is not None


def read():
    """
    Contract:
    - No arguments
    - Returns a dictionary of users keyed on user email
    - Each user email must be the key for dictionary entry
    """
    people = people_dict
    return people


def read_one(_id):
    """
    Contract:
    - Takes in id (unique email)
    - Searches dictionary for id
    - Returns person from dictionary if there
    - Returns None if no one is there
    """
    people = read()
    if _id in people:
        return people[_id]
    else:
        return None


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
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    if not is_valid_email(email):
        raise ValueError(f'Invalid email: {email}')
    if not rls.is_valid(role):
        raise ValueError(f'Invalid role: {role}')
    return True


def create(name: str, affiliation: str, email: str):
    """
    Contract:
    - Takes in a Name, Affiliation, and Email
    - Returns email if added, else it will raise an error
    - Creating/adding user email to dict
    """
    if email in people_dict:
        raise ValueError(f'Adding duplicate {email=}')
    people_dict[email] = {NAME: name, AFFILIATION: affiliation,
                          EMAIL: email}
    return email


# TODO if person has role add records to people_w_role
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
        people_w_role = {}
        for person in read():
            pass
        masthead[text] = people_w_role
    return masthead


def main():
    print(read())


if __name__ == '__main__':
    main()
