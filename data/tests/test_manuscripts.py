import pytest # type: ignore

from data.manuscripts import ManuscriptStates, ManuscriptActions, Manuscripts

# Instantiate Manuscript Objects
manu_states = ManuscriptStates()
manu_actions = ManuscriptActions()
manu = Manuscripts()

# Test Manuscript Variables
TEST_MANU_KEY = 1
TEST_TITLE = 'Manuscript Title'
TEST_DISPLAY_NAME = 'Manuscripts'
TEST_ABSTRACT = 'Abstract'
TEST_TEXT = 'Text'
TEST_AUTHOR_FIRST = 'Jane'
TEST_AUTHOR_LAST = 'Doe'
TEST_AUTHOR_EMAIL = 'janedoe@nyu.edu'

@pytest.fixture(scope='function')
def temp_manuscript():
    manuscript = manu.create(TEST_TITLE, TEST_DISPLAY_NAME,
                             TEST_ABSTRACT, TEST_TEXT, 
                             TEST_AUTHOR_FIRST, TEST_AUTHOR_LAST,
                             TEST_AUTHOR_EMAIL)
    yield manuscript
    try:
        manu.delete(TEST_MANU_KEY)
    except:
        print('Manuscript already deleted.')

# Manuscript States Tests
def test_get_states():
    assert manu_states.get_states() == manu_states.VALID_STATES

def test_is_valid_state():
    for state in manu_states.get_states():
        assert manu_states.is_valid_state(state) is True
    assert manu_states.is_valid_state('NOT') is False

# Manuscript Actions Tests
def test_get_actions():
    assert manu_actions.get_actions() == manu_actions.VALID_ACTIONS

def test_is_valid_action():
    for action in manu_actions.get_actions():
        assert manu_actions.is_valid_action(action) is True
    assert manu_actions.is_valid_action('NOT') is False

def test_assign_ref(temp_manuscript):
    manu_actions.assign_ref(temp_manuscript, 'Temp Ref')
    assert temp_manuscript[manu.REFEREES] == ['Temp Ref']

def test_remove_ref(temp_manuscript):
    manu_actions.remove_ref(temp_manuscript, 'Temp Ref')
    assert temp_manuscript[manu.REFEREES] == []
    manu_actions.assign_ref(temp_manuscript, 'Temp Ref')
    manu_actions.assign_ref(temp_manuscript, 'Temp Ref 2')
    assert manu_actions.remove_ref(temp_manuscript, 'Temp Ref') == manu.STATES.REF_REVIEW
    assert temp_manuscript[manu.REFEREES] == ['Temp Ref 2']

# Manuscript Tests
def test_common_actions():
    action_func = manu.COMMON_ACTIONS[manu.ACTIONS.WITHDRAW][manu.FUNC]
    result = action_func()
    assert result == manu.STATES.WITHDRAWN

def test_exists():
    if not manu.exists(TEST_MANU_KEY):
        manu.delete(TEST_MANU_KEY)
    manu.create(TEST_TITLE, TEST_DISPLAY_NAME, TEST_ABSTRACT,
                TEST_TEXT, TEST_AUTHOR_FIRST, TEST_AUTHOR_LAST,
                TEST_AUTHOR_EMAIL)
    assert manu.exists(TEST_MANU_KEY)
    manu.delete(TEST_MANU_KEY)
