import pytest # type: ignore

from data.manuscripts import ManuscriptStates, ManuscriptActions, Manuscripts

# Instantiate Manuscript Objects
manu_states = ManuscriptStates()
manu_actions = ManuscriptActions()
manuscripts = Manuscripts()

# Manuscript States Tests
def test_get_states():
    assert manu_states.get_states() == manu_states.VALID_STATES

def test_is_valid_state():
    for state in manu_states.get_states():
        assert manu_states.is_valid_state(state) is True
    assert manu_states.is_valid_state('NOT') is False

# Manuscript Actions Tests
