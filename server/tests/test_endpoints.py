import pytest  # type: ignore

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch

# import endpoints, routes, and responses
import server.endpoints as ep
from server.routes import Routes
from server.responses import Responses

# import data classes
from data.people import People
from data.texts import Texts

# object instances for servers
routes = Routes()
responses = Responses()

# object instances for data
txts = Texts()
ppl = People()

# instantiate the test_client
TEST_CLIENT = ep.app.test_client()


def test_endpoints_get():
    resp = TEST_CLIENT.get(routes.ENDPOINTS)
    resp_json = resp.get_json()
    assert responses.ENDPOINTS in resp_json


def test_journal_get():
    resp = TEST_CLIENT.get(routes.JOURNAL)
    resp_json = resp.get_json()
    assert responses.JOURNAL in resp_json


def test_manuscripts_get():
    resp = TEST_CLIENT.get(routes.MANUSCRIPTS)
    resp_json = resp.get_json()
    assert responses.MANUSCRIPTS in resp_json


def test_people():
    resp = TEST_CLIENT.get(routes.PEOPLE)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert ppl.FIRST_NAME in person


@pytest.mark.skip('Skipping because not done.')
def test_person():
    # Use an existing person for the test
    person_id = ppl.CW_EMAIL
    expected_person = ppl.people_dict[person_id]
    
    # Make a GET request to retrieve the person
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_ROUTE}/{person_id}')
    resp_json = resp.get_json()

    # Check if the status code is 200 (OK)
    assert resp.status_code == OK, f"Unexpected status code: {resp.status_code}"
    assert 'Message' in resp_json, "Response does not contain 'Message' key"

    person = resp_json['Message']

    # Validate the response data
    assert isinstance(person, dict), "Person data is not a dictionary"
    assert person[ppl.NAME] == expected_person[ppl.NAME], "Name mismatch"
    assert person[ppl.EMAIL] == expected_person[ppl.EMAIL], "Email mismatch"
    assert person[ppl.AFFILIATION] == expected_person[ppl.AFFILIATION], "Affiliation mismatch"
    assert person[ppl.ROLES] == expected_person[ppl.ROLES], "Roles mismatch"


def test_texts():
    resp = TEST_CLIENT.get(routes.TEXTS)
    resp_json = resp.get_json()
    for _id, text in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert txts.TITLE in text


@pytest.mark.skip('Skipping because not done.')
def test_text():
    text_key = txt.TEST_KEY
    resp = TEST_CLIENT.get(f'{ep.TEXT_ROUTE}/{text_key}')
    resp_json = resp.get_json()

    assert resp.status_code == 200
    assert 'Message' in resp_json

    text = resp_json['Message']

    assert isinstance(text, dict)
    assert txt.TITLE in text
    assert 'title' in text
    assert isinstance(text['title'], str)
