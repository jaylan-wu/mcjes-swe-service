"""
In this module, we interface with the Roles Datatype.
These roles are provided to people and determine the
permissions that are alloted to a person.
Roles should be unchanged.
"""
import data.db_connect as dbc


class Roles:
    def __init__(self):
        self.ROLES_COLLECTION = 'roles'

        # Instance Variables for Data Fields
        self.ROLE_CODE = 'role_code'
        self.ROLE = 'role'
        self.IS_MASTHEAD = 'is_masthead'

    def exists(self, role_code: str) -> bool:
        """
        A role is valid if it exists in the database
        """
        return bool(self.read_one(role_code))

    def create(self, role_code: str, role: str, is_masthead: bool) -> str:
        """
        Creates a new role if the key doesn't exist
        """
        if self.exists(role_code):
            raise ValueError(f'Adding duplicate: {role_code=}')
        new_role = {self.ROLE_CODE: role_code, self.ROLE: role,
                    self.IS_MASTHEAD: is_masthead}
        dbc.create(self.ROLES_COLLECTION, new_role)
        return role_code

    def delete(self, role_code: str) -> bool:
        """
        Deletes a role given a key
        """
        return dbc.delete(self.ROLES_COLLECTION,
                          {self.ROLE_CODE: role_code})

    def read(self) -> dict:
        """
        Returns all possible roles and their full details
        """
        roles = dbc.read_dict(self.ROLES_COLLECTION, self.ROLE_CODE)
        return roles

    def read_one(self, role_code: str) -> dict:
        """
        Returns an instance of a role given a role_code
        """
        return dbc.read_one(self.ROLES_COLLECTION, {self.ROLE_CODE: role_code})

    def get_role_codes(self) -> list:
        """
        Returns a list of all possible role codes
        """
        roles = dbc.read_dict(self.ROLES_COLLECTION, self.ROLE_CODE)
        return list(roles.keys())

    def get_masthead_roles(self) -> dict:
        """
        Returns a dictionary of masthead roles
        """
        roles = self.read()
        masthead_roles = {code: data["role"] for code, data in roles.items()
                          if data["is_masthead"]}
        return masthead_roles
