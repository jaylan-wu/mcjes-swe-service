"""
In this module, we create a utilities object that
allows us to reuse functions that are commonly used
throughout the repository.
"""
import re


class Utilities:
    def __init__(self):
        self.VALID_CHARS = '[A-Za-z0-9_.]'

    def is_valid_email(self, email: str) -> bool:
        """
        Takes in an email as a string and returns true
        if it is a valid email
        """
        pattern = f'^{self.VALID_CHARS}+@[A-Za-z0-9.-]+\\.[A-Za-z]{{2,3}}$'
        return re.match(pattern, email) is not None
