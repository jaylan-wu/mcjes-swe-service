"""
This file contains all of the endpoints for our flask app.
"""
from http import HTTPStatus

from flask import Flask, request  # type: ignore
from flask_restx import Resource, Api, fields   # type: ignore -> Namespace
from flask_cors import CORS  # type: ignore
from flask_bcrypt import Bcrypt  # type: ignore
from flask_jwt_extended import JWTManager, create_access_token  # type: ignore
# from flask_jwt_extended import jwt_required, get_jwt_identity  # type: ignore
from werkzeug.security import generate_password_hash  # type: ignore
from werkzeug.security import check_password_hash  # type: ignore
import werkzeug.exceptions as wz  # type: ignore
import requests  # type: ignore
import re  # type: ignore

# import server classes
from server.routes import Routes
from server.responses import Responses

# import data classes
from data.people import People
from data.roles import Roles
from data.texts import Texts
from data.manuscripts import Manuscripts

# import security
# import security.security as sec

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
bcrypt = Bcrypt(app)
app.config['JWT_SECRET_KEY'] = 'mcjes_jwt'
jwt = JWTManager(app)

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


@api.route(f'{routes.DEVELOPER}{routes.LOGS}{routes.ERROR}/<_username>')
class ErrorLog(Resource):
    """
    Developer tool to fetch the application error log from PythonAnywhere.
    """
    def get(self, _username):
        """
        Retrieves error log from the PythonAnywhere server file system.
        """
        token = 'b8d7afc890b6e0462c12f3d1f27bf2fb0bac0921'

        log_path = f'/var/log/{_username}.pythonanywhere.com.error.log'
        url = 'https://www.pythonanywhere.com/api/v0/user/' + \
            f'{_username}/files/path{log_path}'

        headers = {
            'Authorization': f'Token {token}'
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            split_logs = re.split(r'(?=\d{4}-\d{2}-\d{2})', response.text)
            log_entries = [entry.strip() for entry
                           in split_logs if entry.strip()]
            return {'ErrorLog': log_entries[:20]}, HTTPStatus.OK
        else:
            return {
                'error': f"Error {response.status_code}",
                'details': response.content.decode('utf-8')
            }, response.status_code


USER_REGISTER_FLDS = api.model('UserRegister', {
    ppl.FIRST_NAME: fields.String(required=True),
    ppl.LAST_NAME: fields.String(required=True),
    ppl.EMAIL: fields.String(required=True),
    ppl.PASSWORD: fields.String(required=True),
    ppl.AFFILIATION: fields.String,
    ppl.ROLES: fields.List(fields.String(required=True)),
})


USER_LOGIN_FLDS = api.model('UserLogin', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})


@api.route(routes.REGISTER)
class Register(Resource):
    """
    This class is used to register a new user
    """
    @api.expect(USER_REGISTER_FLDS)
    def post(self):
        """
        Registers a new user
        """
        data = request.get_json()
        first_name = data.get(ppl.FIRST_NAME)
        last_name = data.get(ppl.LAST_NAME)
        email = data.get(ppl.EMAIL)
        password = data.get(ppl.PASSWORD)
        # affiliation = data.get(ppl.AFFILIATION)
        roles = data.get(ppl.ROLES)
        if ppl.read_one(email):
            return {MESSAGE: "User already exists"}, 400
        password_hash = generate_password_hash(password)
        ppl.create(first_name, last_name, email, password_hash,
                   "NYU", roles)
        return {MESSAGE: "User registered successfully"}, 201


@api.route(routes.LOGIN)
class Login(Resource):
    @api.expect(USER_LOGIN_FLDS)
    def post(self):
        """Logs in a user and returns an access token"""
        data = request.get_json()
        email = data.get(ppl.EMAIL)
        password = data.get(ppl.PASSWORD)
        user = ppl.read_one(email)
        if not user:
            return {MESSAGE: "User does not exists"}, 401
        if check_password_hash(user[ppl.PASSWORD], password):
            access_token = create_access_token(identity=email)
            return {
                'access_token': access_token,
                'user': {
                    'first_name': user[ppl.FIRST_NAME],
                    'last_name': user[ppl.LAST_NAME],
                    'email': user[ppl.EMAIL],
                    'affiliation': user[ppl.AFFILIATION],
                    'roles': user.get(ppl.ROLES, ['Viewer'])
                    }
            }, 200
        else:
            return {MESSAGE: "Wrong Password"}, 401


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
        return manu.read()

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
                return {{MESSAGE: f"Manuscript action executed: {response}"},
                        HTTPStatus.OK}
            except ValueError as e:
                return {MESSAGE: str(e)}, HTTPStatus.BAD_REQUEST
        else:
            updated_manu = manu.update(int(_manukey), data)
            if updated_manu is None:
                return {MESSAGE: "Manuscript not found"}, HTTPStatus.NOT_FOUND
        return ({MESSAGE: "Manuscript updated successfully"}, HTTPStatus.OK)

    def delete(self, _manukey):
        """
        Deletes a manuscript from the database using their manu_key
        """
        success = manu.delete(_manukey)
        if not success:
            return {MESSAGE: "Manuscript not found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: 'Manuscript deleted successfully'}, HTTPStatus.OK


MANU_ACTION_FLDS = api.model('ManuscriptActionEntry', {
    manu.ACTION: fields.String,
})


@api.route(f'{routes.MANUSCRIPTS}{routes.ACTION}/<_manukey>')
class ManuscriptAction(Resource):
    """
    The purpose of this class is to submit a manuscript action
    """
    @api.expect(MANU_CREATE_FLDS)
    def put(self, _manukey):
        """
        Updates a manuscript state through its action
        """
        data = request.get_json()
        try:
            response = manu.handle_action(int(_manukey), data[manu.ACTION])
            return {{MESSAGE: f"Manuscript action executed: {response}"},
                    HTTPStatus.OK}
        except ValueError as e:
            return {MESSAGE: str(e)}, HTTPStatus.BAD_REQUEST


@api.route(f'{routes.MANUSCRIPTS}{routes.PEOPLE}/<_email>')
class ManuscriptByEmail(Resource):
    """
    The purpose of this class is to fetch manuscripts under a single email
    """
    def get(self, _email):
        """
        Retrieves a group of manuscripts using their emails
        """
        manu_with_email = []
        manuscripts = manu.read()
        for _id, manuscript in manuscripts.items():
            if manuscript[manu.AUTHOR_EMAIL] == _email:
                manu_with_email.append(manuscript)
        if len(manu_with_email) == 0:
            return {MESSAGE: "No Manuscripts Found"}, HTTPStatus.NOT_FOUND
        else:
            return {MESSAGE: manu_with_email}, HTTPStatus.OK


PEOPLE_CREATE_FLDS = api.model('AddNewPeopleEntry', {
    ppl.FIRST_NAME: fields.String,
    ppl.LAST_NAME: fields.String,
    ppl.EMAIL: fields.String,
    ppl.PASSWORD: fields.String,
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
            password = request.json.get(ppl.PASSWORD)
            role = request.json.get(ppl.ROLES)
            person = ppl.create(first_name, last_name,
                                email, password,
                                affiliation, role)
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
        # kwargs = {sec.LOGIN_KEY: 'any key for now'}
        # if not sec.is_permitted(sec.PEOPLE, sec.DELETE, _user_id, **kwargs):
        #     raise wz.Forbidden('This user does not have authorization.')
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


TEXT_CREATE_FLDS = api.model('AddNewTextEntry', {
    txts.KEY: fields.String,
    txts.TITLE: fields.String,
    txts.TEXT: fields.String,
})


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

    @api.expect(TEXT_CREATE_FLDS)
    def post(self):
        """
        Add a text to the journal db.
        """
        try:
            key = request.json.get(txts.KEY)
            title = request.json.get(txts.TITLE)
            content = request.json.get(txts.TEXT)
            text = txts.create(key, title, content)
            return {
                MESSAGE: 'Text added!',
                RETURN: text,
            }, HTTPStatus.CREATED
        except Exception as err:
            raise wz.NotAcceptable(f'Could not add text: {err}')


@api.route(f'{routes.TEXTS}/<_key>')
class Text(Resource):
    """
    This class is a resource to manage text-related requests.
    This is for a single text.
    """

    def get(self, _key):
        """
        Obtains a key and retrieves a text from library with read_one
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
        if success:
            return {MESSAGE: "Text not found"}, HTTPStatus.NOT_FOUND
        return {MESSAGE: 'Text deleted successfully'}, HTTPStatus.OK

    @api.expect(TEXT_CREATE_FLDS)
    def put(self, _key):
        """
        Updates a text's details in the database using their _key
        """
        data = request.get_json()
        title = data.get(txts.TITLE)
        content = data.get(txts.TEXT)
        if not data:
            return {"Message": "Invalid data"}, HTTPStatus.BAD_REQUEST
        updated_text = txts.update(_key, title, content)
        if updated_text is None:
            return {"Message": "Text not found"}, HTTPStatus.NOT_FOUND
        return ({"Message": "Text updated successfully",
                 "Person": updated_text}, HTTPStatus.OK)
