import pytest
from data.texts import Texts

# Test variables
TEST_KEY = 'HomePage'
TEST_TITLE = 'Home Page'
TEST_TEXT = 'This is a journal about building API servers.'

# Instantiate txts object for testing
txts = Texts()

@pytest.fixture(scope='function')
def temp_text():
    text = txts.create(TEST_KEY, TEST_TITLE, TEST_TEXT)
    yield text
    try:
        txts.delete(text)
    except:
        print('Text already deleted.')


def test_exists():
    # Assert that the instance doesn't exist
    assert not txts.exists(TEST_KEY)
    # Create an instance and assert its existence
    txts.create(TEST_KEY, TEST_TITLE, TEST_TEXT)
    assert txts.exists(TEST_KEY)
    # Delete the instnace and assert that its deleted
    txts.delete(TEST_KEY)
    assert not txts.exists(TEST_KEY)


def test_create():
    if txts.exists(TEST_KEY):
        txts.delete(TEST_KEY)
    txts.create(TEST_KEY, TEST_TITLE, TEST_TEXT)
    with pytest.raises(ValueError, match="Adding duplicate: key='HomePage'"):
        txts.create(TEST_KEY, TEST_TITLE, TEST_TEXT)
    assert txts.exists(TEST_KEY)
    txts.delete(TEST_KEY)


def test_delete(temp_text):
    txts.delete(temp_text)
    assert not txts.exists(temp_text)


def test_read(temp_text):
    texts = txts.read()
    assert isinstance(texts, dict)
    assert len(texts) > 0
    for key, title in texts.items():
        assert isinstance(key, str)
        assert txts.TITLE in title


def test_read_one(temp_text):
    assert txts.read_one(temp_text) is not None


def test_read_one_not_found():
    assert txts.read_one('Not a page key!') is None


def test_update(temp_text):
    txts.update(temp_text, 'Updated', 'This is an updated page')
    test_text = txts.read_one(temp_text)
    assert test_text[txts.TITLE] == 'Updated'


def test_update_not_found():
    with pytest.raises(ValueError, match="Updating non-existent text: key='NotFoundText'"):
        txts.update('NotFoundText', 'Not Found', 'This is not found')
