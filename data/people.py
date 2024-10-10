"""
In this module, we interface with the People Datatype
"""

# data fields
NAME = 'name'
ROLES = 'roles'
AFFILIATION = 'affiliation'
EMAIL = 'email'

# testing variables (TODO add more emails)
JW_EMAIL = 'jw6639@nyu.edu'
DEL_EMAIL = 'delete@nyu.edu'

people_dict = {
    JW_EMAIL: {
        NAME: 'Jaylan Wu',
        ROLES: [],
        AFFILIATION: 'New York University',
        EMAIL: JW_EMAIL,
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


# TODO fill out following functions
def delete_person():
    return


def create_person():
    return
