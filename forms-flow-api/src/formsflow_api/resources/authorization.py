"""API endpoints for managing authorization resource."""

from http import HTTPStatus

from flask import current_app, request
from flask_restx import Namespace, Resource

from formsflow_api.utils import auth, cors_preflight, profiletime

from formsflow_api.schemas import AuthorizationSchema
from formsflow_api.services import AuthorizationService

API = Namespace("Authorization", description="Authorization")


@cors_preflight("GET,POST,OPTIONS")
@API.route("", methods=["GET", "POST", "OPTIONS"])
class AuthorizationResource(Resource):
    """Resource for managing authorization."""

    @staticmethod
    @auth.require
    @profiletime
    def get():
        """Get all authorization details."""
        
        return (
            AuthorizationService.get_all_authorization(),
            HTTPStatus.OK,
        )

    @staticmethod
    @auth.require
    @profiletime
    def post():
        """Post a new authorization using the request body.

        : category:- Category of the authorization
        : identity:- Identity of the User/Group/Role
        : permissions:- Permissions (All/Read/Update/Delete/..)
        : resourceId:- Resource id for authorization (formid/*)
        : type:- Type of access (allow/deny)
        """
        authorization_json = request.get_json()

        try:
            authorization_schema = AuthorizationSchema()
            dict_data = authorization_schema.load(authorization_json)
            response, status = AuthorizationService.create_authorization(dict_data), HTTPStatus.CREATED
        except BaseException as authorization_err:  # pylint: disable=broad-except
            response, status = {
                "type": "Bad request error",
                "message": "Invalid authorization request passed",
            }, HTTPStatus.BAD_REQUEST
            current_app.logger.info(response)
            current_app.logger.info(authorization_err)
        return response, status


@cors_preflight("GET,PUT,DELETE,OPTIONS")
@API.route("/<int:authorization_id>", methods=["GET", "PUT", "DELETE", "OPTIONS"])
class AuthorizationResourceById(Resource):
    """Resource for getting authorization by id."""

    @staticmethod
    @auth.require
    @profiletime
    def get(authorization_id: int):
        """Get authorization by id.

        : authorization_id:- List the authorization for particular authorization_id
        """
        return (
            AuthorizationService.get_authorization_by_id(authorization_id=authorization_id),
            HTTPStatus.OK,
        )

    @staticmethod
    @auth.require
    @profiletime
    def put(authorization_id: int):
        """Update authorization details.

        : authorization_id:- Update the authorization for particular authorization_id
        """
        application_json = request.get_json()

        try:
            schema = AuthorizationSchema()
            dict_data = schema.load(application_json)
            response, status = AuthorizationService.update_authorization(
                authorization_id=authorization_id, data=dict_data
            ), HTTPStatus.OK
        except KeyError as err:
            response, status = {
                "type": "Invalid request data",
                "message": f"Invalid authorization id - {authorization_id}",
            }, HTTPStatus.BAD_REQUEST
            current_app.logger.info(err)
        except BaseException as authorization_err:  # pylint: disable=broad-except
            response, status = {
                "type": "Bad Request Error",
                "message": "Invalid request passed",
            }, HTTPStatus.BAD_REQUEST
            current_app.logger.info(authorization_err)
        return response, status

    @staticmethod
    @auth.require
    @profiletime
    def delete(authorization_id: int):
        """Delete authorization by id.

        : authorization_id:- Delete authorization by id.
        """
        try:
            AuthorizationService.delete_authorization(authorization_id=authorization_id)
            response, status = (
                f"Deleted ID {authorization_id}",
                HTTPStatus.OK,
            )
        except BaseException as err:  # pylint: disable=broad-except
            response, status = (
                {
                    "type": "Invalid request data",
                    "message": f"Invalid authorization id - {authorization_id}",
                },
                HTTPStatus.BAD_REQUEST,
            )

            current_app.logger.info(response)
            current_app.logger.info(err)
        return response, status
