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

def test_valid_state_transitions(temp_manuscript):
    # Submitted -> Assign Reviewer -> Ref Review
    new_state = manu.STATE_TABLE[manu_states.SUBMITTED][manu_actions.ASSIGN_REF]['f'](manuscript=temp_manuscript, ref='Reviewer1')
    assert new_state == manu_states.REF_REVIEW
    
    # Ref Review -> Accept -> Copy Edit
    new_state = manu.STATE_TABLE[manu_states.REF_REVIEW][manu_actions.ACCEPT]['f']()
    assert new_state == manu_states.COPY_EDIT
    
    # Ref Review -> Accept with Revision -> Author Revision
    new_state = manu.STATE_TABLE[manu_states.REF_REVIEW][manu_actions.ACCEPT_W_REV]['f']()
    assert new_state == manu_states.AUTHOR_REVISION
    
    # Author Revision -> Done -> Editor Review
    new_state = manu.STATE_TABLE[manu_states.AUTHOR_REVISION][manu_actions.DONE]['f']()
    assert new_state == manu_states.EDITOR_REVIEW
    
    # Editor Review -> Accept -> Copy Edit
    new_state = manu.STATE_TABLE[manu_states.EDITOR_REVIEW][manu_actions.ACCEPT]['f']()
    assert new_state == manu_states.COPY_EDIT
    
    # Copy Edit -> Done -> Author Review
    new_state = manu.STATE_TABLE[manu_states.COPY_EDIT][manu_actions.DONE]['f']()
    assert new_state == manu_states.AUTHOR_REVIEW
    
    # Author Review -> Done -> Formatting
    new_state = manu.STATE_TABLE[manu_states.AUTHOR_REVIEW][manu_actions.DONE]['f']()
    assert new_state == manu_states.FORMATTING
    
    # Formatting -> Done -> Published
    new_state = manu.STATE_TABLE[manu_states.FORMATTING][manu_actions.DONE]['f']()
    assert new_state == manu_states.PUBLISHED
    
    # Submitted -> Reject -> Rejected
    new_state = manu.STATE_TABLE[manu_states.SUBMITTED][manu_actions.REJECT]['f']()
    assert new_state == manu_states.REJECTED
    
    # Withdrawn -> Common Actions -> Withdrawn
    new_state = manu.STATE_TABLE[manu_states.SUBMITTED][manu_actions.WITHDRAW]['f']()
    assert new_state == manu_states.WITHDRAWN


def test_exists():
    if not manu.exists(TEST_MANU_KEY):
        manu.delete(TEST_MANU_KEY)
    manu.create(TEST_TITLE, TEST_DISPLAY_NAME, TEST_ABSTRACT,
                TEST_TEXT, TEST_AUTHOR_FIRST, TEST_AUTHOR_LAST,
                TEST_AUTHOR_EMAIL)
    assert manu.exists(TEST_MANU_KEY)
    manu.delete(TEST_MANU_KEY)


def test_is_valid_manuscript():
    assert manu.is_valid_manuscript('test@example.com') == True
    with pytest.raises(ValueError, match="Invalid email: test@exa"):
        manu.is_valid_manuscript('test@exa')


def test_create():
    if manu.exists(TEST_MANU_KEY):
        manu.delete(TEST_MANU_KEY)
    manu.create(TEST_TITLE, TEST_DISPLAY_NAME,
                TEST_ABSTRACT, TEST_TEXT, 
                TEST_AUTHOR_FIRST, TEST_AUTHOR_LAST,
                TEST_AUTHOR_EMAIL)
    with pytest.raises(ValueError, match="Invalid email: test@exa"):
        manu.create(TEST_TITLE, TEST_DISPLAY_NAME,
                    TEST_ABSTRACT, TEST_TEXT, 
                    TEST_AUTHOR_FIRST, TEST_AUTHOR_LAST,
                    "test@exa")
    assert manu.exists(TEST_MANU_KEY)
    manu.delete(TEST_MANU_KEY)


def test_update_invalid_state(temp_manuscript):
    with pytest.raises(ValueError, match="Invalid state: INV_STATE"):
        manu.update(1, {manu.STATE: "INV_STATE"})

def test_update_invalid_key(temp_manuscript):
    with pytest.raises(ValueError, match="Manuscript with key 2 not found."):
        manu.update(2, {})

def test_update_invalid_email(temp_manuscript):
    with pytest.raises(ValueError, match="Invalid email: test@exa"):
        manu.update(1, {manu.AUTHOR_EMAIL: "test@exa"})

def test_update_valid(temp_manuscript):
    updated = manu.update(1, {manu.AUTHOR_EMAIL: "test@test.org"})
    assert updated[manu.AUTHOR_EMAIL] == "test@test.org"


def test_get_action(temp_manuscript):
    actions = manu.get_actions(manu_states.SUBMITTED)
    assert manu_actions.ASSIGN_REF in actions
    assert manu_actions.REJECT in actions


def test_handle_action(temp_manuscript):
    with pytest.raises(ValueError, match="Manuscript with key 2 not found."):
        manu.handle_action(2, manu_actions.REJECT)
    with pytest.raises(ValueError, match=f'Action {manu_actions.DONE} is not allowed.'):
        manu.handle_action(1, manu_actions.DONE)
    
