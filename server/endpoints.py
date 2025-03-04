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

# Helper Variables
MESSAGE = 'Message'
RETURN = 'Return'


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


MANU_CREATE_FLDS = api.model('AddNewManuscriptEntry', {
    manu.TITLE: fields.String,
    manu.DISPLAY_NAME: fields.String,
    manu.ABSTRACT: fields.String,
    manu.TEXT: fields.String,
    manu.AUTHOR_FIRST: fields.String,
    manu.AUTHOR_LAST: fields.String,
    manu.AUTHOR_EMAIL: fields.String,
    manu.ACTION: fields.String,
})


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
        return {responses.MANUSCRIPTS: manu.read()}

    @api.response(HTTPStatus.CREATED, 'Manuscript added!')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def post(self):
        """
        Add a manuscript to the journal db.
        """
        try:
            title = request.json.get(manu.TITLE)
            disp_name = request.json.get(manu.DISPLAY_NAME)
            abstract = request.json.get(manu.ABSTRACT)
            text = request.json.get(manu.TEXT)
            author_first = request.json.get(manu.AUTHOR_FIRST)
            author_last = request.json.get(manu.AUTHOR_LAST)
            author_email = request.json.get(manu.AUTHOR_EMAIL)
            manu.create(title, disp_name, abstract, text,
                        author_first, author_last, author_email)
            return {MESSAGE: 'Manuscript added!'}, HTTPStatus.CREATED
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add manuscript: {err}')


@api.route(f'{routes.MANUSCRIPTS}/<_manukey>')
class Manuscript(Resource):
    """
    The purpose of this class is have REST API a single manuscript.
    """
    def get(self, _manukey):
        """
        Retrieves a manuscript using their unique manuscript key
        """
        manuscript = manu.read_one(int(_manukey))
        print(manuscript)
        if manuscript is None:
            return {MESSAGE: "Manuscript Not Found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: manuscript}, HTTPStatus.OK

    @api.response(HTTPStatus.CREATED, 'Manuscript Updated!')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(MANU_CREATE_FLDS)
    def put(self, _manukey):
        """
        Updates a manuscript using their unique manuscript key
        """
        data = request.get_json()
        if not data:
            return {MESSAGE: "Invalid data"}, HTTPStatus.BAD_REQUEST
        if manu.ACTION in data:
            try:
                response = manu.handle_action(int(_manukey), data[manu.ACTION])
                return {MESSAGE: f"Manuscript action executed: {response}"}, HTTPStatus.OK
            except ValueError as e:
                return {MESSAGE: str(e)}, HTTPStatus.BAD_REQUEST
        else:
            updated_manu = ppl.update(int(_manukey), data)
            if updated_manu is None:
                return {MESSAGE: "Manuscript not found"}, HTTPStatus.NOT_FOUND
        return ({MESSAGE: "Manuscript updated successfully"}, HTTPStatus.OK)


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.FIRST_NAME: fields.String,
    ppl.LAST_NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String),
})


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

    @api.response(HTTPStatus.CREATED, 'Person Added!')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not acceptable')
    @api.expect(PEOPLE_CREATE_FLDS)
    def post(self):
        """
        Add a person to the journal db.
        """
        try:
            first_name = request.json.get(ppl.FIRST_NAME)
            last_name = request.json.get(ppl.LAST_NAME)
            affiliation = request.json.get(ppl.AFFILIATION)
            email = request.json.get(ppl.EMAIL)
            role = request.json.get(ppl.ROLES)
            person = ppl.create(first_name, last_name,
                                affiliation, email, role)
            return {
                MESSAGE: 'Person added!',
                RETURN: person,
            }, HTTPStatus.CREATED
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add person: {err}')


@api.route(f'{routes.PEOPLE}/<_email>')
class Person(Resource):
    """
    The purpose of this class is to have REST API a single person.
    """
    def get(self, _email):
        """
        Obtains _email and gets person from database with read_one.
        """
        person = ppl.read_one(_email)
        if person is None:
            return {"Message": "Person Not Found"}, HTTPStatus.NOT_FOUND
        return {"Message": person}, HTTPStatus.OK

    def delete(self, _email):
        """
        Deletes a person from the database using their _email
        """
        success = ppl.delete(_email)
        if not success:
            return {MESSAGE: "Person not found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: 'Person deleted successfully'}, HTTPStatus.OK

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


@api.route(f'{routes.PEOPLE}/masthead')
class Masthead(Resource):
    """
    Get a journal's masthead.
    """
    def get(self):
        return {responses.MASTHEAD: ppl.get_masthead()}


@api.route(routes.ROLES)
class Roles(Resource):
    """
    This class is a resource to manage role-related requests.
    This is for multiple amounts of roles.
    """
    def get(self):
        """
        Retrieve all roles
        """
        return rls.read()


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


@api.route(f'{routes.TEXTS}/<_key>')
class Text(Resource):
    """
    The purpose of this is to return a single text given a text key
    """
    def get(self, _key):
        """
        Obtains ey and retrieves a text from library with read_one
        """
        text = txts.read_one(_key)
        if text is None:
            return {MESSAGE: "Text Not Found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: text}, HTTPStatus.OK

    def delete(self, _key):
        """
        Deletes a text from the database using their key
        """
        success = txts.delete(_key)
        if not success:
            return {MESSAGE: "Text not found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: 'Text deleted successfully'}, HTTPStatus.OK
