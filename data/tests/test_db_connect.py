import pytest # type: ignore
from unittest.mock import patch
import mongomock # type: ignore
from data.db_connect import connect_db, create, read_one, delete, update, read, read_dict, fetch_all_as_dict, count_documents # type: ignore

@pytest.fixture
def mock_db():
    with patch('data.db_connect.pm.MongoClient', new=mongomock.MongoClient):
        client = connect_db()
        db = client['mcjesDB']
        collection = db['test_collection']
        collection.delete_many({})
        collection.insert_one({"_id": "123", "name": "Test Doc", "value": 42})
        yield db

def test_create(mock_db):
    doc = {"_id": "456", "name": "New Doc", "value": 99}
    create("test_collection", doc)
    result = mock_db["test_collection"].find_one({"_id": "456"})
    assert result is not None
    assert result['name'] == "New Doc"

def test_read_one(mock_db):
    result = read_one("test_collection", {"_id": "123"})
    assert result is not None
    assert result['name'] == "Test Doc"