"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
# from http import HTTPStatus

from flask import Flask  # , request
from flask_restx import Resource, Api  # Namespace, fields
from flask_cors import CORS

# import werkzeug.exceptions as wz

# import data classes
import data.people as ppl

app = Flask(__name__)
CORS(app)
api = Api(app)

ENDPOINT_EP = '/endpoints'
ENDPOINT_RESP = 'Available endpoints'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
TITLE_EP = '/title'
TITLE_RESP = 'Title'
TITLE = 'The Journal of API Technology'
EDITOR_RESP = 'Editor'
EDITOR = 'ejc369@nyu.edu'
DATE_RESP = 'Date'
DATE = '2024-09-24'
JOURNAL_EP = '/journal'
JOURNAL_NAME = 'mcjes'
JOURNAL_RESP = 'Journal Name'
PEOPLE_EP = '/people'


@api.route(HELLO_EP)
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


@api.route(ENDPOINT_EP)
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
        return {"Available endpoints": endpoints}


@api.route(TITLE_EP)
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


@api.route(JOURNAL_EP)
class JournalName(Resource):
    """
    The purpose of this class is to return Journal Name
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {JOURNAL_RESP: JOURNAL_NAME}


# TODO add endpoints for people
# need GET all people, GET single person, DEL single person
@api.route(PEOPLE_EP)
class People(Resource):
    """
    TODO edit comment
    """
    def get(self):
        return


@api.route(f'{PEOPLE_EP}/<_id>')
class Person(Resource):
    """
    TODO edit comment
    """
    def get(self, _id):
        return


@api.route(f'{PEOPLE_EP}/delete/<_id>')
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
