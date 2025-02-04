'''
This file contains all the fields of a manuscript datatype
'''

TITLE = 'title'
DISP_NAME = 'disp_name'
ABSTRACT = 'abstract'
TEXT = 'text'
AUTHOR = 'author'
AUTHOR_EMAIL = 'author_email'
REFEREES = 'referees'
EDITOR = 'editor'
STATE = 'state'
REPORT = 'report'
VERDICT = 'verdict'

TEST_FLD_NM = TITLE
TEST_FLD_DISP_NM = 'Title'


FIELDS = {
    TITLE: {
        DISP_NAME: TEST_FLD_DISP_NM,
    },
}


def get_flds() -> dict:
    return FIELDS


def get_fld_names() -> list:
    return list(FIELDS.keys())


def get_disp_name(fld_nm: str) -> dict:
    fld = FIELDS.get(fld_nm)
    if isinstance(fld, dict):  # Ensure the field is a dictionary
        return fld.get(DISP_NAME, None)  # Return the display name if it exists
    return None  # Return None if the field is invalid or not a dictionary


def main():
    print(f'{get_flds()=}')


if __name__ == '__main__':
    main()
