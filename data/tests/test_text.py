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
    with pytest.raises(ValueError, match="Adding duplicate key='Test Text'"):
        txt.create(ADD_TEXT, 'Test Page', 'This is a test page')
    assert txt.exists(ADD_TEXT)
    txt.delete(ADD_TEXT)


def test_read(temp_text):
    texts = txt.read()
    assert isinstance(texts, dict)
    assert len(texts) > 0
    for key, title in texts.items():
        assert isinstance(key, str)
        assert txt.TITLE in title


def test_read_one(temp_text):
    assert txt.read_one(temp_text) is not None


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') is None


def test_update(temp_text):
    txt.update(temp_text, 'Updated', 'This is an updated page')

def test_update_not_found():
    with pytest.raises(ValueError, 
                       match="Updating non-existent text: key='Not Found Text'"):
        txt.update('Not Found Text', 'Not Found', 'This is not found')
