"""
In this module, we interface with the People Datatype.
This is for general People collection that we have in
the database. This is NOT for account management.
"""
import data.db_connect as dbc

from data.roles import Roles
from data.utilities import Utilities

# Instantiate Roles object
rls = Roles()
util = Utilities()


class People:
    def __init__(self):
        self.PEOPLE_COLLECTION = 'people'

        # Instance Variables for Field Names
        self.FIRST_NAME = 'first_name'
        self.LAST_NAME = 'last_name'
        self.AFFILIATION = 'affiliation'
        self.EMAIL = 'email'
        self.ROLES = 'roles'

    def exists(self, email: str) -> bool:
        """
        Check if an instance of a person exists
        """
        return bool(self.read_one(email))

    def is_valid_person(self, email: str, roles: list) -> bool:
        """
        Checks if an instance of a person would be a valid person to add
        if they have a valid email or if the role exists.
        """
        if not util.is_valid_email(email):
            raise ValueError(f'Invalid email: {email}')
        for role in roles:
            if not rls.exists(role):
                raise ValueError(f'Invalid role: {role}')
        return True

    def create(self, first_name: str, last_name: str,
               affiliation: str, email: str, roles: list):
        """
        Creates a new instance of a person if email doesn't exist.
        Takes: first_name, last_name, email, affiliation, roles [list]
        """
        if self.exists(email):
            raise ValueError(f'Adding duplicate: {email=}')
        if self.is_valid_person(email, roles):
            person = {self.FIRST_NAME: first_name, self.LAST_NAME: last_name,
                      self.AFFILIATION: affiliation, self.EMAIL: email,
                      self.ROLES: roles}
            dbc.create(self.PEOPLE_COLLECTION, person)
            return email

    def delete(self, email: str):
        """
        Deletes a person given an email
        """
        return dbc.delete(self.PEOPLE_COLLECTION, {self.EMAIL: email})

    def read(self) -> dict:
        """
        Returns a dictionary of all people keyed on emails
        """
        people = dbc.read_dict(self.PEOPLE_COLLECTION, self.EMAIL)
        return people

    def read_one(self, email: str) -> dict:
        """
        Returns an instance of a person given an email
        """
        return dbc.read_one(self.PEOPLE_COLLECTION, {self.EMAIL: email})

    def update(self, first_name: str, last_name: str,
               affiliation: str, email: str, roles: list):
        """
        Updates an existing person
        Raises ValueError if the person does not exist
        """
        if not self.exists(email):
            raise ValueError(f'Updating non-existent person: {email=}')
        if self.is_valid_person(email, roles):
            person = dbc.update(self.PEOPLE_COLLECTION,
                                {self.EMAIL: email},
                                {self.FIRST_NAME: first_name,
                                 self.LAST_NAME: first_name,
                                 self.AFFILIATION: affiliation,
                                 self.EMAIL: email, self.ROLES: roles})
            return person

    def has_role(self, person: dict, role: str) -> bool:
        """
        Returns a boolean given if a person has a role
        """
        if role in person.get(self.ROLES):
            return True
        return False

    def get_masthead(self) -> dict:
        """
        Returns dictionary where keys are masthead role names and values are
        dictionaries of people with those roles.
        """
        masthead = {}
        mh_roles = rls.get_masthead_roles()
        for mh_role, role_name in mh_roles.items():
            people_w_role = []
            people = self.read()
            for _id, person in people.items():
                if self.has_role(person, mh_role):
                    people_w_role.append(person)
            masthead[role_name] = people_w_role
        return masthead
