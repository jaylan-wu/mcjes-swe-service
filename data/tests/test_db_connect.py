import pytest # type: ignore
from unittest.mock import patch
import mongomock # type: ignore
from data.db_connect import connect_db, convert_mongo_id, create, read_one, delete, update, read, read_dict, fetch_all_as_dict, count_documents # type: ignore

@pytest.fixture
def mock_db():
    with patch('data.db_connect.pm.MongoClient', new=mongomock.MongoClient):
        client = connect_db()
        db = client['mcjesDB']
        collection = db['test_collection']
        collection.delete_many({})
        collection.insert_one({"_id": "123", "name": "Test Doc", "value": 42})
        yield db

def test_convert_mongo_id():
    doc = {"_id": 123, "name": "Test Doc"}
    updated_doc = convert_mongo_id(doc)
    assert "_id" in updated_doc
    assert isinstance(updated_doc["_id"], str)
    assert updated_doc["_id"] == "123"

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

def test_update(mock_db):
    update("test_collection", {"_id": "123"}, {"value": 100})
    result = mock_db["test_collection"].find_one({"_id": "123"})
    assert result['value'] == 100

def test_delete(mock_db):
    deleted_count = delete("test_collection", {"_id": "123"})
    assert deleted_count == 1
    result = mock_db["test_collection"].find_one({"_id": "123"})
    assert result is None

def test_read_one(mock_db):
    result = read_one("test_collection", {"_id": "123"})
    assert result is not None
    convert_mongo_id(result)
    assert result['_id'] == "123"
    assert result['name'] == "Test Doc"

def test_read(mock_db):
    results = read("test_collection", no_id=False)
    assert len(results) == 1
    assert results[0]['_id'] == "123"
    assert results[0]['name'] == "Test Doc"

def test_read_dict(mock_db):
    result_dict = read_dict("test_collection", "name")
    assert "Test Doc" in result_dict
    assert result_dict["Test Doc"]["value"] == 42

def test_fetch_all_as_dict(mock_db):
    result_dict = fetch_all_as_dict("name", "test_collection")
    assert "Test Doc" in result_dict
    assert result_dict["Test Doc"]["value"] == 42

def test_count_documents(mock_db):
    count = count_documents("test_collection")
    assert count == 1

def test_count_documents_with_filter(mock_db):
    count = count_documents("test_collection", filt={"name": "Test Doc"})
    assert count == 1

    count_empty = count_documents("test_collection", filt={"name": "Nonexistent"})
    assert count_empty == 0
