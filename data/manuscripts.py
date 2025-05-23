'''
In this file, we interface with the Manuscript Datatype.
This is will handle our FSM actions for our Manuscripts as
well as holding all the necessary fields.
'''
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
        self.AUTHOR_REVIEW = 'Author Review'
        self.AUTHOR_REVISION = 'Author Revision'
        self.COPY_EDIT = 'Copy Edit'
        self.EDITOR_REVIEW = 'Editor Review'
        self.FORMATTING = 'Formatting'
        self.PUBLISHED = 'Published'
        self.REF_REVIEW = 'Referee Review'
        self.REJECTED = 'Rejected'
        self.SUBMITTED = 'Submitted'
        self.WITHDRAWN = 'Withdrawn'

        self.VALID_STATES = [
            self.AUTHOR_REVIEW,
            self.AUTHOR_REVISION,
            self.COPY_EDIT,
            self.EDITOR_REVIEW,
            self.FORMATTING,
            self.PUBLISHED,
            self.REF_REVIEW,
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
        self.ACCEPT = 'Accept'
        self.ACCEPT_W_REV = 'Accept with Revisions'
        self.ASSIGN_REF = 'Assign Referee'
        self.REMOVE_REF = 'Remove Referee'
        self.SUBMIT_REV = 'Submit Revisions'
        self.DONE = 'Done'
        self.REJECT = 'Rejected'
        self.WITHDRAW = 'Withdrawn'

        self.VALID_ACTIONS = [
            self.ACCEPT,
            self.ACCEPT_W_REV,
            self.ASSIGN_REF,
            self.REMOVE_REF,
            self.SUBMIT_REV,
            self.DONE,
            self.REJECT,
            self.WITHDRAW,
        ]

    def get_actions(self) -> list:
        return self.VALID_ACTIONS

    def is_valid_action(self, action: str) -> bool:
        return action in self.VALID_ACTIONS

    def assign_ref(self, manuscript: dict, ref: str = None, **kwargs) -> str:
        manu = Manuscripts()
        ref = ref or kwargs.get("ref") or manuscript.get("ref")
        if not ref:
            raise ValueError("Referee email is required to assign a referee.")
        if ref not in manuscript[manu.REFEREES]:
            manuscript[manu.REFEREES].append(ref)
            dbc.update(
                manu.MANUSCRIPTS_COLLECTION,
                {manu.MANU_KEY: manuscript[manu.MANU_KEY]},
                {manu.REFEREES: manuscript[manu.REFEREES]}
            )
        return manu.STATES.REF_REVIEW

    def remove_ref(self, manuscript: dict, ref: str) -> str:
        manu = Manuscripts()
        if ref in manuscript[manu.REFEREES]:
            manuscript[manu.REFEREES].remove(ref)
        if len(manuscript[manu.REFEREES]) > 0:
            return manu.STATES.REF_REVIEW
        else:
            return manu.STATES.SUBMITTED


class Manuscripts:
    def __init__(self):
        self.MANUSCRIPTS_COLLECTION = 'manuscripts'

        # Helper Objects
        self.STATES = ManuscriptStates()
        self.ACTIONS = ManuscriptActions()

        # Instance Variables for Field Names
        self.MANU_KEY = 'manuscript_key'  # hidden unique ID
        self.TITLE = 'title'
        self.DISPLAY_NAME = 'display_name'
        self.ABSTRACT = 'abstract'
        self.TEXT = 'text'
        self.AUTHOR_FIRST = 'author_first_name'
        self.AUTHOR_LAST = 'author_last_name'
        self.AUTHOR_EMAIL = 'author_email'
        self.EDITOR = 'editor'
        self.REFEREES = 'referees'
        self.STATE = 'state'
        self.ACTION = 'action'
        self.CURRENT_ACTIONS = 'current_actions'

        # State Table
        self.FUNC = 'f'

        self.COMMON_ACTIONS = {
            self.ACTIONS.WITHDRAW: {
                self.FUNC: lambda **kwargs: self.STATES.WITHDRAWN,
            }
        }

        self.STATE_TABLE = {
            self.STATES.SUBMITTED: {
                self.ACTIONS.ASSIGN_REF: {
                    self.FUNC: self.ACTIONS.assign_ref
                },
                self.ACTIONS.REJECT: {
                    self.FUNC: lambda **kwargs: self.STATES.REJECTED,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.REF_REVIEW: {
                self.ACTIONS.ASSIGN_REF: {
                    self.FUNC: self.ACTIONS.assign_ref
                },
                self.ACTIONS.REMOVE_REF: {
                    self.FUNC: self.ACTIONS.remove_ref
                },
                self.ACTIONS.SUBMIT_REV: {
                    self.FUNC: self.ACTIONS.assign_ref
                },
                self.ACTIONS.ACCEPT: {
                    self.FUNC: lambda **kwargs: self.STATES.COPY_EDIT,
                },
                self.ACTIONS.ACCEPT_W_REV: {
                    self.FUNC: lambda **kwargs: self.STATES.AUTHOR_REVISION,
                },
                self.ACTIONS.REJECT: {
                    self.FUNC: lambda **kwargs: self.STATES.REJECTED,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.AUTHOR_REVISION: {
                self.ACTIONS.DONE: {
                    self.FUNC: lambda **kwargs: self.STATES.EDITOR_REVIEW,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.EDITOR_REVIEW: {
                self.ACTIONS.ACCEPT: {
                    self.FUNC: lambda **kwargs: self.STATES.COPY_EDIT,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.COPY_EDIT: {
                self.ACTIONS.DONE: {
                    self.FUNC: lambda **kwargs: self.STATES.AUTHOR_REVIEW,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.AUTHOR_REVIEW: {
                self.ACTIONS.DONE: {
                    self.FUNC: lambda **kwargs: self.STATES.FORMATTING,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.FORMATTING: {
                self.ACTIONS.DONE: {
                    self.FUNC: lambda **kwargs: self.STATES.PUBLISHED,
                },
                **self.COMMON_ACTIONS,
            },
            self.STATES.REJECTED: {
                **self.COMMON_ACTIONS,
            },
            self.STATES.WITHDRAWN: {
                **self.COMMON_ACTIONS,
            },
            self.STATES.PUBLISHED: {
                **self.COMMON_ACTIONS,
            },
        }

    def exists(self, manu_key: int) -> bool:
        '''
        Check if an instance of a manuscripts exists
        '''
        return bool(self.read_one(manu_key))

    def is_valid_manuscript(self, author_email: str):
        '''
        Checks if an instance of a manuscript would be a valid
        manuscript to add on whether if they have a valid email
        '''
        if not util.is_valid_email(author_email):
            raise ValueError(f'Invalid email: {author_email}')
        return True

    def create(self, title: str, display_name: str, abstract: str, text: str,
               author_fn: str, author_ln: str, author_email: str):
        '''
        Creates a new instance of a person if email doesn't exist.
        Takes: first_name, last_name, email, affiliation, roles [list]
        '''
        manu_key = len(self.read()) + 1
        if self.is_valid_manuscript(author_email):
            manuscript = {self.MANU_KEY: manu_key, self.TITLE: title,
                          self.DISPLAY_NAME: display_name,
                          self.ABSTRACT: abstract, self.TEXT: text,
                          self.AUTHOR_FIRST: author_fn,
                          self.AUTHOR_LAST: author_ln,
                          self.AUTHOR_EMAIL: author_email,
                          self.REFEREES: [], self.EDITOR: None,
                          self.STATE: self.STATES.SUBMITTED,
                          self.CURRENT_ACTIONS:
                          self.get_actions(self.STATES.SUBMITTED,)}
            dbc.create(self.MANUSCRIPTS_COLLECTION, manuscript)
            return manuscript

    def delete(self, manu_key: int):
        '''
        Deletes a manuscript given a manu_key
        '''
        return dbc.delete(self.MANUSCRIPTS_COLLECTION,
                          {self.MANU_KEY: manu_key})

    def read(self) -> dict:
        '''
        Returns a dictionary of all manuscripts keyed on manuscript keys
        '''
        manuscripts = dbc.read_dict(self.MANUSCRIPTS_COLLECTION, self.MANU_KEY)
        return manuscripts

    def read_one(self, manu_key: int) -> dict:
        '''
        Returns an instance of a manuscript given an manu_key
        '''
        return dbc.read_one(self.MANUSCRIPTS_COLLECTION,
                            {self.MANU_KEY: manu_key})

    def update(self, manu_key: int, data: dict):
        '''
        Updates an existing manuscript with the provided fields.
        '''
        if not self.exists(manu_key):
            raise ValueError(f'Manuscript with key {manu_key} not found.')
        if self.AUTHOR_EMAIL in data:
            if not util.is_valid_email(data[self.AUTHOR_EMAIL]):
                raise ValueError(f'Invalid email: {data[self.AUTHOR_EMAIL]}')
        if self.STATE in data:
            if not self.STATES.is_valid_state(data[self.STATE]):
                raise ValueError(f'Invalid state: {data[self.STATE]}')
        dbc.update(self.MANUSCRIPTS_COLLECTION,
                   {self.MANU_KEY: manu_key}, data)
        return self.read_one(manu_key)

    def get_actions(self, state: str) -> list:
        return list(self.STATE_TABLE.get(state, {}).keys())

    def handle_action(
        self,
        manu_key: int,
        action: str,
        payload: dict = None
    ) -> str:
        manuscript = self.read_one(manu_key)
        if not manuscript:
            raise ValueError(f'Manuscript with key {manu_key} not found.')
        state = manuscript[self.STATE]
        if action not in self.STATE_TABLE[state]:
            raise ValueError(f'Action {action} is not allowed.')

        new_state_func = self.STATE_TABLE[state][action][self.FUNC]

        if payload:
            manuscript.update(payload)

        if callable(new_state_func):
            new_state = new_state_func(
                manuscript=manuscript,
                **(payload or {})
            )
        else:
            new_state = new_state_func

        dbc.update(
            self.MANUSCRIPTS_COLLECTION,
            {self.MANU_KEY: manu_key},
            {
                self.STATE: new_state,
                self.CURRENT_ACTIONS: self.get_actions(new_state)
            }
        )
        return new_state
