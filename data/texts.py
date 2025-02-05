"""
In this module, we interface with the Texts Datatype.
This is for large static pieces of text that we keep
in the database.
"""
import data.db_connect as dbc


class Texts:
    def __init__(self):
        self.TEXTS_COLLECTION = 'texts'

        # Instance Variables for Field Names
        self.KEY = 'key'
        self.TITLE = 'title'
        self.TEXT = 'text'

    def exists(self, key: str) -> bool:
        """
        Checks if an instance exists using a key
        """
        return bool(self.read_one(key))

    def create(self, key: str, title: str, text: str):
        """
        Creates a new instance of a text if key does not exist
        """
        if self.exists(key):
            raise ValueError(f'Adding duplicate: {key=}')
        new_text = {self.KEY: key, self.TITLE: title, self.TEXT: text}
        dbc.create(self.TEXTS_COLLECTION, new_text)
        return key

    def delete(self, key: str):
        """
        Deletes a text given a key
        """
        dbc.delete(self.TEXTS_COLLECTION, {self.KEY: key})

    def read(self) -> dict:
        """
        Returns a dictionary of all texts keyed on text keys
        """
        texts = dbc.read_dict(self.TEXTS_COLLECTION, self.KEY)
        return texts

    def read_one(self, key: str) -> dict:
        """
        Returns an instance of a text given a key
        """
        return dbc.read_one(self.TEXTS_COLLECTION, {self.KEY: key})

    def update(self, key: str, title: str, text: str):
        """
        Updates an existing entry with a new title and text.
        Raises ValueError if the key does not exist.
        """
        if not self.exists(key):
            raise ValueError(f'Updating non-existent text: {key=}')
        ret = dbc.update(self.TEXTS_COLLECTION, {self.KEY: key},
                         {self.KEY: key, self.TITLE: title, self.TEXT: text})
        print(f'{ret=}')
        return key
