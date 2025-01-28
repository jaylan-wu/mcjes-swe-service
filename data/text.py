import data.db_connect as dbc

TEXT_COLLECTION = 'text'

KEY = 'key'
TITLE = 'title'
TEXT = 'text'

TEST_KEY = 'HomePage'
SUBM_KEY = 'SubmissionsPage'
DEL_KEY = 'DeletePage'

text_dict = {
    TEST_KEY: {
        TITLE: 'Home Page',
        TEXT: 'This is a journal about building API servers.',
    },
    SUBM_KEY: {
        TITLE: 'Submissions Page',
        TEXT: 'All submissions must be original work in Word format.',
    },
    DEL_KEY: {
        TITLE: 'Delete Page',
        TEXT: 'This is a text to delete.',
    },
}


def create(key: str, title: str, text: str):
    if exists(key):
        raise ValueError(f'Adding duplicate {key=}')
    text = {KEY: key, TITLE: title, TEXT: text}
    dbc.create(TEXT_COLLECTION, text)
    return key


def delete(key: str):
    dbc.delete(TEXT_COLLECTION, {KEY: key})


def exists(key: str) -> bool:
    return read_one(key)


def read() -> dict:
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of texts keyed on page keys
    """
    texts = dbc.read_dict(TEXT_COLLECTION, KEY)
    return texts


def read_one(key: str) -> dict:
    return dbc.read_one(TEXT_COLLECTION, {KEY: key})


def update(key: str, title: str, text: str):
    """
    Updates an existing entry in the text_dict with a new title and text.
    If the key does not exist, it informs the user.
    """
    if not exists(key):
        raise ValueError(f'Updating non-existent text: {key=}')
    ret = dbc.update(TEXT_COLLECTION, {KEY: key},
                     {KEY: key, TITLE: title, TEXT: text})
    print(f'{ret=}')
    return key


def main():
    print(read())


if __name__ == '__main__':
    main()
