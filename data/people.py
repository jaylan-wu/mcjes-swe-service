"""
In this module, we interface with the People Datatype
"""

# data fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

# testing variables (TODO add more emails)
CW_EMAIL = 'caw9180@nyu.edu'
JW_EMAIL = 'jw6639@nyu.edu'
SR_EMAIL = 'sr5826@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'

people_dict = {
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


def get_people():
    """
    Contract:
    - No arguments
    - Returns a dictionary of users keyed on user email
    - Each user email must be the key for dictionary entry
    """
    people = people_dict
    return people


def delete_person(_id):
    """
    Contract:
    - Takes in id (unique email)
    - Searches dictionary for id
    - Returns and deletes email if found
    - Returns None if email not in dict
    """
    people = get_people()
    if _id in people:
        del people[_id]
        return _id
    else:
        return None


#TODO: Add roles for later usage when applicable 
def create_person(name: str, affiliation: str, email: str):
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
