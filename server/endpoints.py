"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask  # type: ignore -> , request
from flask_restx import Resource, Api, fields   # type: ignore -> Namespace
from flask_cors import CORS  # type: ignore
from flask import request

import werkzeug.exceptions as wz

# import routes and responses
from server.routes import (ENDPOINT_ROUTE, HELLO_ROUTE, JOURNAL_ROUTE,
                           PEOPLE_ROUTE, TEXT_ROUTE, TITLE_ROUTE)
from server.responses import (DATE, DATE_RESP, EDITOR, EDITOR_RESP,
                              ENDPOINT_RESP, HELLO_RESP, JOURNAL_NAME,
                              JOURNAL_RESP, MASTHEAD_RESP, TITLE, TITLE_RESP)

# import data classes
import data.people as ppl
import data.text as txt

app = Flask(__name__)
CORS(app)
api = Api(app)

# Define the PEOPLE_EP constant for consistency
PEOPLE_EP = PEOPLE_ROUTE


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
        if ret is None:
            return {"Message": "Person not found"}, HTTPStatus.NOT_FOUND
        return {"Message": ret}, HTTPStatus.OK


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


MESSAGE = 'Message'
RETURN = 'return'


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.String,
})


@api.route(f'{PEOPLE_ROUTE}/create')
class PeopleCreate(Resource):
    """
    Add a person to the journal db.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def put(self):
        """
        Add a person.
        """
        try:
            name = request.json.get(ppl.NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create(name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


@api.route(f'{PEOPLE_ROUTE}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {MASTHEAD_RESP: ppl.get_masthead()}


@api.route(TEXT_ROUTE)
class Texts(Resource):
    """
    The purpose of this is to class is to return all texts
    """
    def get(self):
        """
        Retrieve all people
        """
        return txt.read()


@api.route(f'{TEXT_ROUTE}/<_id>')
class Text(Resource):
    """
    The purpose of this is to return a single text
    """
    def get(self, _id):
        """
        Obtains id(KEY) and get a text from library with read_one.
        """
        ret = txt.read_one(_id)
        return {'Message': ret}


@api.route('/people/<string:email>/addRole/<string:role>')
class AddRole(Resource):
    def put(self, email, role):
        try:
            person = ppl.get_person(email)
        except ValueError:
            mssg = f"{person} not found, please create the person first"
            return {"message": mssg}, 404
        try:
            ppl.add_role(email, role)
        except KeyError as err:
            return {"message": err}, 404
        return {"message": f"Role '{role}' added to {email}"}


@api.route('/people/<string:email>/removeRole/<string:role>')
class RemoveRole(Resource):
    def put(self, email, role):
        try:
            person = ppl.get_person(email)
        except ValueError:
            mssg = f"{person} not found"
            return {"message": mssg}, 404
        try:
            ppl.remove_role(email, role)
        except KeyError:
            return {"message": f"{role} doesn't exist"}, 404
        return {"message": f"Role '{role}' removed from {email}"}


TITLE_UPDATE_FIELDS = api.model('UpdateJournalTitle', {
    'title': fields.String(description="The new title of the journal"),
    'editor': fields.String(description="The new editor of the journal"),
    'date': fields.String(description="The new publication date of journal")
})


@api.route(f'{TITLE_ROUTE}/update')
class UpdateJournalTitle(Resource):
    """
    Update the journal title, editor, and publication date.
    """
    @api.expect(TITLE_UPDATE_FIELDS)
    @api.response(HTTPStatus.OK, 'Title updated successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Invalid input')
    def post(self):
        """
        Update journal title information.
        """
        try:
            # Declare globals at the beginning of the function
            global TITLE, EDITOR, DATE
            new_title = request.json.get('title', TITLE)
            new_editor = request.json.get('editor', EDITOR)
            new_date = request.json.get('date', DATE)
            # Update global variables or database records
            TITLE = new_title
            EDITOR = new_editor
            DATE = new_date
            return {
                "message": "Journal title updated successfully",
                TITLE_RESP: TITLE,
                EDITOR_RESP: EDITOR,
                DATE_RESP: DATE
            }, HTTPStatus.OK
        except Exception as err:
            return {"message": f"Update Failed: {err}"}, HTTPStatus.BAD_REQUEST
