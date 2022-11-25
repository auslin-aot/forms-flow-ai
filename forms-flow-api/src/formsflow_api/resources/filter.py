"""API endpoints for filter resource."""

from http import HTTPStatus
from http.client import BAD_REQUEST

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from formsflow_api_utils.exceptions import BusinessException
from formsflow_api_utils.utils import (
    REVIEWER_GROUP,
    auth,
    cors_preflight,
    profiletime,
)
from marshmallow.exceptions import ValidationError

from formsflow_api.schemas import FilterSchema
from formsflow_api.services import FilterService

filter_schema = FilterSchema()

API = Namespace("Filter", description="Filter APIs")

criteria = API.model(
    "Criteria",
    {
        "CandidateGroup": fields.String(description="Filter task specific to group"),
        "includeAssignedTasks": fields.Boolean(description="Include assigned task"),
    },
)

variable = API.model(
    "Variables",
    {
        "name": fields.String(description="Variable name"),
        "label": fields.String(description="Display name"),
    },
)

properties = API.model(
    "Properties",
    {
        "showUndefinedVariable": fields.Boolean(description="Show undefined variables"),
        "priority": fields.Integer(description="Show undefined variables"),
    },
)

filter = API.model(
    "Filter",
    {
        "name": fields.String(description="Name of the filter"),
        "description": fields.String(description="Description about filter"),
        "criteria": fields.Nested(criteria, description="Filter criteria"),
        "variables": fields.List(
            fields.Nested(variable, description=" Variables shown in the tasks list"),
        ),
        "properties": fields.Nested(properties, description="Properties of filter"),
        "roles": fields.List(
            fields.String(), description="Authorized Roles to the filter"
        ),
        "users": fields.List(
            fields.String(), description="Authorized Users to the filter"
        ),
    },
)
filter_response = API.inherit(
    "Filter response",
    filter,
    {
        "status": fields.String(description="Status of the filter"),
        "tenant": fields.String(description="Authorized Tenant to the filter"),
        "id": fields.Integer(description="Unique id of the filter"),
        "created": fields.DateTime(description="Created time"),
        "modified": fields.DateTime(description="Modified time"),
        "createdBy": fields.String(),
        "modifiedBy": fields.String(),
    },
)


@cors_preflight("GET, POST, OPTIONS")
@API.route("", methods=["GET", "POST", "OPTIONS"])
class FilterResource(Resource):
    """Resource to create and list filter."""

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(
        responses={200: "OK:- Success", 403: "Permission denied"},
        model=[filter_response],
    )
    def get():
        """
        Get all filters.

        List all active filters for requests with ```reviewer permission```.
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                response, status = FilterService.get_all_filters(), HTTPStatus.OK
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except Exception as unexpected_error:
            current_app.logger.warning(unexpected_error)
            raise unexpected_error

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(
        responses={
            201: "Filter created",
            403: "Permission denied",
            400: "Validation Error",
        },
        model=filter_response,
    )
    @API.expect(filter)
    def post():
        """
        Create filter.

        Post a new filter using request body for requests with ```reviewer permission```.
        e.g payload,
        ```
        {
            "name": "Test Task",
            "description": "Filter creation test task",
            "variables":[
                    {
                    "name": "name",
                    "label": "userName"
                    }
                ],
            "criteria": {
                "taskCandidateGroup":"/formsflow/formsflow-reviewer",
                "includeAssignedTasks":true,
                "condition":"ALL"
            },
            "properties": {
                "showUndefinedVariable":false,
                "refresh": false,
                "priority":10
            },
            "users": [],
            "roles": ["/formsflow/formsflow-reviewer"]
        }
        ```
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                filter_data = filter_schema.load(request.get_json())
                response, status = (
                    FilterService.create_filter(filter_data),
                    HTTPStatus.CREATED,
                )
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except ValidationError as error:
            current_app.logger.warning(error)
            response, status = {
                "type": "Bad request error",
                "message": "Invalid request data",
            }, BAD_REQUEST
            return response, status
        except Exception as unexpected_error:
            current_app.logger.warning(unexpected_error)
            raise unexpected_error


@cors_preflight("GET, OPTIONS")
@API.route("/user", methods=["GET", "OPTIONS"])
class UsersFilterList(Resource):
    """Resource to list filters specific to current user."""

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(
        responses={200: "OK:- Success", 403: "Permission denied"},
        model=[filter_response],
    )
    def get():
        """
        List filters of current user.

        Get all active filters of current reviewer user for requests with ```reviewer permission```.
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                response, status = FilterService.get_user_filters(), HTTPStatus.OK
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except Exception as unexpected_error:
            current_app.logger.warning(unexpected_error)
            raise unexpected_error


@cors_preflight("PUT, OPTIONS")
@API.route("/<int:filter_id>", methods=["GET", "PUT", "DELETE", "OPTIONS"])
@API.doc(params={"filter_id": "Filter details corresponding to filter_id"})
class FilterResourceById(Resource):
    """Resource for managing filter by id."""

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(
        responses={200: "OK:- Success", 403: "Permission denied"}, model=filter_response
    )
    def get(filter_id: int):
        """
        Get filter by id.

        Get filter details corresponding to a filter id for requests with ```reviewer permission```.
        : filter_id:- unique id of filter.
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                filter_result = FilterService.get_filter_by_id(filter_id)
                response, status = filter_schema.dump(filter_result), HTTPStatus.OK
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except PermissionError as err:
            response, status = (
                {
                    "type": "Permission Denied",
                    "message": f"Access to filter id - {filter_id} is prohibited.",
                },
                HTTPStatus.FORBIDDEN,
            )
            current_app.logger.warning(err)
            return response, status
        except BusinessException as err:
            current_app.logger.warning(err.error)
            return err.error, err.status_code
        except Exception as unexpected_error:
            current_app.logger.warning(unexpected_error)
            raise unexpected_error

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(
        responses={200: "OK:- Success", 403: "Permission denied"}, model=filter_response
    )
    @API.expect(filter)
    def put(filter_id: int):
        """
        Update filter by id.

        Update filter details corresponding to a filter id for requests with ```reviewer permission```.
        : filter_id:- unique id of filter.
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                filter_data = filter_schema.load(request.get_json())
                filter_result = FilterService.update_filter(filter_id, filter_data)
                response, status = (
                    filter_schema.dump(filter_result),
                    HTTPStatus.OK,
                )
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except PermissionError as err:
            response, status = (
                {
                    "type": "Permission Denied",
                    "message": f"Access to filter id - {filter_id} is prohibited.",
                },
                HTTPStatus.FORBIDDEN,
            )
            current_app.logger.warning(err)
            return response, status
        except BusinessException as err:
            current_app.logger.warning(err)
            error, status = err.error, err.status_code
            return error, status

        except BaseException as submission_err:  # pylint: disable=broad-except
            response, status = {
                "type": "Bad request error",
                "message": "Invalid request data",
            }, HTTPStatus.BAD_REQUEST

            current_app.logger.warning(response)
            current_app.logger.warning(submission_err)

            return response, status

    @staticmethod
    @auth.require
    @profiletime
    @API.doc(responses={200: "OK:- Success", 403: "Permission denied"})
    def delete(filter_id: int):
        """
        Delete filter by id.

        Delete filter corresponding to a filter id for requests with ```reviewer permission```.
        : filter_id:- unique id of filter.
        """
        try:
            if auth.has_role([REVIEWER_GROUP]):
                FilterService.mark_inactive(filter_id=filter_id)
                response, status = "Deleted", HTTPStatus.OK
            else:
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.FORBIDDEN
            return response, status
        except PermissionError as err:
            response, status = (
                {
                    "type": "Permission Denied",
                    "message": f"Access to filter id - {filter_id} is prohibited.",
                },
                HTTPStatus.FORBIDDEN,
            )
            current_app.logger.warning(err)
            return response, status
        except BusinessException as err:
            current_app.logger.warning(err.error)
            return err.error, err.status_code
        except Exception as unexpected_error:
            current_app.logger.warning(unexpected_error)
            raise unexpected_error
