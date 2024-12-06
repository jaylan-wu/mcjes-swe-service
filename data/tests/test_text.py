import pytest
import data.text as txt

ADD_TEXT = "Test Text"

@pytest.fixture(scope='function')
def temp_text():
    text = txt.create(txt.TEST_KEY, 'Home Page', 
            'This is a journal about building API servers.')
    yield text
    try:
        txt.delete(text)
    except:
        print('Text already deleted.')


def test_delete(temp_text):
    txt.delete(temp_text)
    assert not txt.exists(temp_text)


def test_create():
    if txt.exists(ADD_TEXT):
        txt.delete(ADD_TEXT)
    txt.create(ADD_TEXT, 'Test Page', 'This is a test page')
    assert txt.exists(ADD_TEXT)
    txt.delete(ADD_TEXT)


def test_read():
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str) 


def test_read_one(temp_text):
    assert txt.read_one(temp_text) is not None


@pytest.mark.skip('Skipping because not done.')
def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}


@pytest.mark.skip('Skipping because not done.')
def test_update():
    # Initial check to ensure the key exists
    initial_entry = txt.read_one(txt.TEST_KEY)
    assert initial_entry == {txt.TITLE: 'Home Page', txt.TEXT: 'This is a journal about building API servers.'}

    # Update the entry with new title and text
    new_title = 'Updated Home Page'
    new_text = 'Updated journal about building API servers.'
    txt.update(txt.TEST_KEY, new_title, new_text)

    # Check that the update was successful
    updated_entry = txt.read_one(txt.TEST_KEY)
    assert updated_entry[txt.TITLE] == new_title
    assert updated_entry[txt.TEXT] == new_text
