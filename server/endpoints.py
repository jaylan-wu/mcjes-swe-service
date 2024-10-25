"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus

from flask import Flask  # type: ignore -> , request
from flask_restx import Resource, Api   # type: ignore -> Namespace, fields
from flask_cors import CORS  # type: ignore

# import werkzeug.exceptions as wz

# import routes and responses
from server.routes import (ENDPOINT_ROUTE, HELLO_ROUTE, JOURNAL_ROUTE,
                           PEOPLE_ROUTE, TEXT_ROUTE, TITLE_ROUTE)
from server.responses import (DATE, DATE_RESP, EDITOR, EDITOR_RESP,
                              ENDPOINT_RESP, HELLO_RESP, JOURNAL_NAME,
                              JOURNAL_RESP, TITLE, TITLE_RESP)

# import data classes
import data.people as ppl
import data.text as txt

app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route(ENDPOINT_ROUTE)
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {ENDPOINT_RESP: endpoints}


@api.route(HELLO_ROUTE)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {HELLO_RESP: 'world'}


@api.route(TITLE_ROUTE)
class JournalTitle(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title.
    """
    def get(self):
        """
        Retrieve the journal title.
        """
        return {
            TITLE_RESP: TITLE,
            EDITOR_RESP: EDITOR,
            DATE_RESP: DATE,
        }


@api.route(JOURNAL_ROUTE)
class JournalName(Resource):
    """
    The purpose of this class is to return Journal Name
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {JOURNAL_RESP: JOURNAL_NAME}


@api.route(PEOPLE_ROUTE)
class People(Resource):
    """
    The purpose of this is to class is to return all people
    """
    def get(self):
        """
        Retrieve all people
        """
        return ppl.read()


@api.route(f'{PEOPLE_ROUTE}/<_id>')
class Person(Resource):
    """
    The purpose of this is to return a single person.
    """
    def get(self, _id):
        """
        Obtains id(email) and gets person from library with read_one.
        """
        ret = ppl.read_one(_id)
        return {'Message': ret}


@api.route(f'{PEOPLE_ROUTE}/delete/<_id>')
class PersonDelete(Resource):
    """
    The purpose of this is to Delete a single person.
    """
    def delete(self, _id):
        """
        Obtains id(email) and deletes using delete_person.
        """
        ret = ppl.delete_person(_id)
        return {'Message': ret}


@api.route(TEXT_ROUTE)
class Text(Resource):
    """
    The purpose of this is to class is to return all people
    """
    def get(self):
        """
        Retrieve all people
        """
        return txt.read()
