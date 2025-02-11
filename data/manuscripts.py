"""
In this file, we interface with the Manuscript Datatype.
This is will handle our FSM actions for our Manuscripts as
well as holding all the necessary fields.
"""
import data.db_connect as dbc
from data.utilities import Utilities

# instantiate utilities object
util = Utilities()


class ManuscriptStates:
    '''
    In this class, we manage the possible states a manuscript
    could be in.
    '''
    def __init__(self):
        # Instance Variables for Manuscript States
        self.AUTHOR_REV = 'AUR'
        self.COPY_EDIT = 'CED'
        self.IN_REF_REV = 'REF'
        self.REJECTED = 'REJ'
        self.SUBMITTED = 'SUB'
        self.WITHDRAWN = 'WIT'

        self.VALID_STATES = [
            self.AUTHOR_REV,
            self.COPY_EDIT,
            self.IN_REF_REV,
            self.REJECTED,
            self.SUBMITTED,
            self.WITHDRAWN,
        ]

    def get_states(self) -> list:
        return self.VALID_STATES

    def is_valid_state(self, state: str) -> bool:
        return state in self.VALID_STATES


class ManuscriptActions:
    '''
    In this class, we manage the possible actions that could
    be applied to a manuscript depending on the state it is in.
    This is where the FSM should be held
    '''
    def __init__(self):
        # Instance Variables for Manuscript States
        self.ACCEPT = 'ACC'
        self.ASSIGN_REF = 'ARF'
        self.DELETE_REF = 'DRF'
        self.DONE = 'DON'
        self.REJECT = 'REJ'
        self.WITHDRAW = 'WIT'

        self.VALID_ACTIONS = [
            self.ACCEPT,
            self.ASSIGN_REF,
            self.DELETE_REF,
            self.DONE,
            self.REJECT,
            self.WITHDRAW,
        ]

    def get_actions(self) -> list:
        return self.VALID_ACTIONS

    def is_valid_action(self, action: str) -> bool:
        return action in self.VALID_ACTIONS


class Manuscripts:
    def __init__(self):
        self.MANUSCRIPTS_COLLECTION = 'manuscripts'

        # Instance Variables for Field Names
        self.MANU_KEY = 'manuscript_key'  # hidden unique ID
        self.TITLE = 'title'
        self.DISPLAY_NAME = 'display_name'
        self.ABSTRACT = 'abstract'
        self.TEXT = 'text'
        self.AUTHOR = 'author'
        self.AUTHOR_EMAIL = 'author_email'
        self.REFEREES = 'referees'
        self.EDITOR = 'editor'
        self.STATE = 'state'
        self.REPORT = 'report'
        self.VERDICT = 'verdict'

    def exists(self, manu_key: str) -> bool:
        """
        Check if an instance of a manuscripts exists
        """
        return bool(self.read_one(manu_key))

    def is_valid_manuscript(self, author_email: str):
        # TODO: fill out validity function
        pass

    def create(self, title: str, display_name: str, abstract: str, text: str,
               author: str, author_email: str):
        # TODO: fill out create function
        pass

    def read(self) -> dict:
        """
        Returns a dictionary of all manuscripts keyed on manuscript keys
        """
        manuscripts = dbc.read_dict(self.MANUSCRIPTS_COLLECTION, self.MANU_KEY)
        return manuscripts

    def read_one(self, manu_key: str) -> dict:
        """
        Returns an instance of a manuscript given an manu_key
        """
        return dbc.read_one(self.MANUSCRIPTS_COLLECTION,
                            {self.MANU_KEY: manu_key})

    def update(self, title: str, display_name: str, abstract: str, text: str,
               author: str, author_email: str):
        # TODO: fill out update function
        pass
