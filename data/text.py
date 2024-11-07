KEY = 'key'
TITLE = 'title'
TEXT = 'text'
EMAIL = 'email'

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

# Functions to work on


def create(key: str, title: str, text: str):
    if key not in text_dict:
        text_dict[key] = {TITLE: title, TEXT: text}
    else:
        print(f'Key {key} already exists. Use update() to modify it.')


def delete(key: str, title: str):
    if key in text_dict:
        del text_dict[key]
    else:
        print(f'Key {key} does not exist. Use create() to create it.')


def update(key: str, title: str, text: str):
    """
    Updates an existing entry in the text_dict with a new title and text.
    If the key does not exist, it informs the user.
    """
    if key in text_dict:
        text_dict[key][TITLE] = title
        text_dict[key][TEXT] = text
        print(f'Key {key} has been updated.')
    else:
        print(f'Key {key} does not exist. Use create() to add it first.')


def read():
    """
    Our contract:
        - No arguments.
        - Returns a dictionary of texts keyed on page keys
    """
    text = text_dict
    return text


def read_one(key: str) -> dict:
    # This should take a key and return the page dictionary
    # for that key. Return an empty dictionary of key not found.
    result = {}
    if key in text_dict:
        result = text_dict[key]
    return result


def main():
    print(read())


if __name__ == '__main__':
    main()
