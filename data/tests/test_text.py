import data.text as txt


def test_read():
    texts = txt.read()
    assert isinstance(texts, dict)
    for key in texts:
        assert isinstance(key, str) 


def test_read_one():
    assert len(txt.read_one(txt.TEST_KEY)) > 0


def test_read_one_not_found():
    assert txt.read_one('Not a page key!') == {}


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
