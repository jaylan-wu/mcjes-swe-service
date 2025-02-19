"""
This file contains all of the endpoints for our flask app.
"""
from http import HTTPStatus

from flask import Flask, request  # type: ignore -> , request
from flask_restx import Resource, Api, fields   # type: ignore -> Namespace
from flask_cors import CORS  # type: ignore
import werkzeug.exceptions as wz  # type: ignore

# import server classes
from server.routes import Routes
from server.responses import Responses

# import data classes
from data.people import People
from data.roles import Roles
from data.texts import Texts
from data.manuscripts import Manuscripts

# object instances for servers
routes = Routes()
responses = Responses()

# object instances for data
txts = Texts()
rls = Roles()
ppl = People()
manu = Manuscripts()

# Start Flask App
app = Flask(__name__)
CORS(app)
api = Api(app)


@api.route(routes.ENDPOINTS)
class Endpoints(Resource):
    """
    This class serves as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        Retrieves a sorted list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {responses.ENDPOINTS: endpoints}


@api.route(routes.JOURNAL)
class Journal(Resource):
    """
    This class handles creating, reading, updating
    and deleting the journal title.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        """
        return {
            responses.JOURNAL: 'Journal of NYU SWE',
            responses.TITLE: 'MCJES',
            responses.EDITOR: 'Max, Cheyenne, Jaylan, Eduardo, & Sadaat',
        }


@api.route(routes.PEOPLE)
class People(Resource):
    """
    This class is a resource to manage people-related requests.
    This is for multiple amounts of people.
    """
    def get(self):
        """
        Retrieve all people
        """
        return ppl.read()


@api.route(f'{routes.PEOPLE}/<_email>')
class Person(Resource):
    """
    The purpose of this class is have REST API a single person.
    """
    def get(self, _email):
        """
        Obtains _email and gets person from database with read_one.
        """
        ret = ppl.read_one(_email)
        if ret is None:
            return {"Message": "Person not found"}, HTTPStatus.NOT_FOUND
        return {"Message": ret}, HTTPStatus.OK

    @api.response(HTTPStatus.NOT_FOUND, 'Person not found')
    @api.response(HTTPStatus.NO_CONTENT, 'Person deleted successfully')
    def delete(self, _email):
        """
        Deletes a person from the database using their _email
        """
        success = ppl.delete(_email)
        if not success:
            return {"Message": "Person not found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: 'Person deleted successfully', RETURN: success}

    def put(self, _email):
        """
        Updates a person's details in the database using their _email
        """
        data = request.get_json()
        if not data:
            return {"Message": "Invalid data"}, HTTPStatus.BAD_REQUEST
        updated_person = ppl.update(_email, data)
        if updated_person is None:
            return {"Message": "Person not found"}, HTTPStatus.NOT_FOUND
        return ({"Message": "Person updated successfully",
                 "Person": updated_person}, HTTPStatus.OK)


MESSAGE = 'Message'
RETURN = 'return'


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.FIRST_NAME: fields.String,
    ppl.LAST_NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String),
})


@api.route(f'{routes.PEOPLE}/create')
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
            first_name = request.json.get(ppl.FIRST_NAME)
            last_name = request.json.get(ppl.LAST_NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            ret = ppl.create(first_name, last_name, affiliation, email, role)
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: '
                                   f'{err=}')
        return {
            MESSAGE: 'Person added!',
            RETURN: ret,
        }


@api.route(f'{routes.PEOPLE}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {responses.MASTHEAD: ppl.get_masthead()}


@api.route(routes.TEXTS)
class Texts(Resource):
    """
    This class is a resource to manage text-related requests.
    This is for multiple amounts of texts.
    """
    def get(self):
        """
        Retrieve all texts
        """
        return txts.read()


@api.route(f'{routes.TEXTS}/<_id>')
class Text(Resource):
    """
    The purpose of this is to return a single text given a text key
    """
    def get(self, _id):
        """
        Obtains id(KEY) and get a text from library with read_one.
        """
        ret = txts.read_one(_id)
        return {'Message': ret}


@api.route(routes.MANUSCRIPTS)
class Manuscripts(Resource):
    """
    This class is a resource to manage manuscript-related requests.
    This is for multiple amounts of manuscripts.
    """
    def get(self):
        """
        Retrieve all manuscripts
        """
        return manu.read()
