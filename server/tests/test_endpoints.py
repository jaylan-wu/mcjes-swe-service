import pytest

from http.client import (
    BAD_REQUEST,
    FORBIDDEN,
    NOT_ACCEPTABLE,
    NOT_FOUND,
    OK,
    SERVICE_UNAVAILABLE,
)

from unittest.mock import patch
# import data classes
import data.people as ppl
from data.texts import Texts

import pytest # type: ignore

# import endpoints, routes, and responses
import server.endpoints as ep
from server.routes import (ENDPOINT_ROUTE, JOURNAL_ROUTE,
                           PEOPLE_ROUTE, TITLE_ROUTE)
from server.responses import (DATE, DATE_RESP, EDITOR, EDITOR_RESP,
                              ENDPOINT_RESP, JOURNAL_NAME,
                              JOURNAL_RESP, TITLE, TITLE_RESP)

TEST_CLIENT = ep.app.test_client()


def test_title():
    resp = TEST_CLIENT.get(ep.TITLE_ROUTE)
    print(f'{ep.TITLE_ROUTE=}')
    resp_json = resp.get_json()
    print(f'{resp_json=}')
    assert ep.TITLE_RESP in resp_json
    assert isinstance(resp_json[ep.TITLE_RESP], str)
    assert len(resp_json[ep.TITLE_RESP]) > 0


def test_journal():
    resp = TEST_CLIENT.get(ep.JOURNAL_ROUTE)
    resp_json = resp.get_json()
    assert ep.JOURNAL_RESP in resp_json


def test_people():
    resp = TEST_CLIENT.get(ep.PEOPLE_ROUTE)
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert ppl.NAME in person


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

@pytest.mark.skip('Skipping because not done.')
def test_texts():
    resp = TEST_CLIENT.get(ep.TEXT_ROUTE)
    resp_json = resp.get_json()
    for _id, text in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert txt.TITLE in text

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

@pytest.mark.skip('Skipping because not done.')
def test_read(mock_read):
    resp = TEST_CLIENT.get(ep.PEOPLE_EP)
    assert resp.status_code == OK
    resp_json = resp.get_json()
    for _id, person in resp_json.items():
        assert isinstance(_id, str)
        assert len(_id) > 0
        assert ppl.NAME in person

@pytest.mark.skip('Skipping because not done.')
def test_read_one(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == OK

@pytest.mark.skip('Skipping because not done.')
def test_read_one_not_found(mock_read):
    resp = TEST_CLIENT.get(f'{ep.PEOPLE_EP}/mock_id')
    assert resp.status_code == NOT_FOUND