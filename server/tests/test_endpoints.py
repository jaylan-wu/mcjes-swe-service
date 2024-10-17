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

import pytest # type: ignore

# import endpoints, routes, and responses
import server.endpoints as ep
from server.routes import (ENDPOINT_ROUTE, HELLO_ROUTE, JOURNAL_ROUTE,
                           PEOPLE_ROUTE, TITLE_ROUTE)
from server.responses import (DATE, DATE_RESP, EDITOR, EDITOR_RESP,
                              ENDPOINT_RESP, HELLO_RESP, JOURNAL_NAME,
                              JOURNAL_RESP, TITLE, TITLE_RESP)

TEST_CLIENT = ep.app.test_client()


def test_hello():
    resp = TEST_CLIENT.get(ep.HELLO_ROUTE)
    resp_json = resp.get_json()
    assert ep.HELLO_RESP in resp_json


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
