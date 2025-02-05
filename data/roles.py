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

    def is_valid(self, code: str) -> bool:
        """
        A role is valid if it exists in the database
        """
        roles = self.get_roles()
        return code in roles

    def create(self, role_code: str, role: str, is_masthead: bool) -> bool:
        """
        Creates a new role if the key doesn't exist
        """
        roles = self.get_roles()
        if role_code in roles:
            print(f"Role with code {role_code} already exists.")
            return False
        new_role = {self.ROLE_CODE: role_code, self.ROLE: role,
                    self.IS_MASTHEAD: is_masthead}
        dbc.create(self.ROLES_COLLECTION, new_role)
        return role

    def delete(self, role_code: str) -> bool:
        """
        Deletes a role given a key
        """
        return dbc.delete(self.ROLES_COLLECTION,
                          {self.ROLE_CODE: role_code})

    def get_roles(self) -> dict:
        """
        Returns all possible roles and their full details
        """
        roles = dbc.read_dict(self.ROLES_COLLECTION, self.ROLE_CODE)
        print(f'{roles=}')
        return roles

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
        roles = self.get_roles()
        masthead_roles = {code: data["role"] for code, data in roles.items()
                          if data["is_masthead"]}
        return masthead_roles
