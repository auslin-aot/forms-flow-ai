"""API endpoints for managing anonymous applications."""

from http import HTTPStatus

from flask import current_app, request
from flask_restx import Namespace, Resource, fields
from formsflow_api_utils.utils import (
    ANONYMOUS_USER,
    cors_preflight,
    profiletime,
)

from formsflow_api.models import FormProcessMapper
from formsflow_api.schemas import ApplicationSchema
from formsflow_api.services import ApplicationService

API = Namespace("Public", description="Public api endpoints")

application_create_model = API.model(
    "Application Create",
    {
        "formId": fields.String(),
        "submissionId": fields.String(),
        "formUrl": fields.String(),
    },
)

application_base_model = API.model(
    "Application Create Response",
    {
        "applicationStatus": fields.String(),
        "created": fields.String(),
        "createdBy": fields.String(),
        "formId": fields.String(),
        "formProcessMapperId": fields.String(),
        "id": fields.Integer(),
        "modified": fields.String(),
        "modifiedBy": fields.String(),
        "processInstanceId": fields.String(),
        "submissionId": fields.String(),
    },
)

check_response = API.model("Check Status", {
    "is_anonymous": fields.Boolean(),
    "status": fields.String()
})

@cors_preflight("POST,OPTIONS")
@API.route("/application/create", methods=["POST", "OPTIONS"])
class ApplicationAnonymousResourcesByIds(Resource):
    """Resource for anonymous application creation."""

    @staticmethod
    @profiletime
    @API.doc(body=application_create_model)
    @API.response(201, "CREATED:- Successful request.", model=application_base_model)
    @API.response(
        400,
        "BAD_REQUEST:- Invalid request.",
    )
    def post():
        """Post a new anonymous application using the request body."""
        application_json = request.get_json()
        try:
            application_schema = ApplicationSchema()
            dict_data = application_schema.load(application_json)
            mapper = FormProcessMapper.find_form_by_form_id(dict_data["form_id"])
            is_anonymous = mapper.is_anonymous
            status = mapper.status
            if not is_anonymous or status != "active":
                response, status = {
                    "type": "Authorization error",
                    "message": "Permission denied",
                }, HTTPStatus.UNAUTHORIZED
                return response, status

            dict_data["created_by"] = ANONYMOUS_USER
            application = ApplicationService.create_application(
                data=dict_data, token=None
            )
            response, status = application_schema.dump(application), HTTPStatus.CREATED
            return response, status
        except BaseException as application_err:  # pylint: disable=broad-except
            response, status = {
                "type": "Bad request error",
                "message": "Invalid application request passed",
            }, HTTPStatus.BAD_REQUEST
            current_app.logger.warning(response)
            current_app.logger.warning(application_err)
            return response, status


@cors_preflight("GET,OPTIONS")
@API.route("/form/<string:form_id>", methods=["GET", "OPTIONS"])
class AnonymousResourceById(Resource):
    """Resource to check form is Anonymous and published."""

    @staticmethod
    @profiletime
    @API.response(200, "OK:- Successful request.", model=check_response)
    @API.response(
        400,
        "BAD_REQUEST:- Invalid request.",
    )
    def get(form_id: str):
        """Get form by form id and return is_anonymous and published status."""
        try:
            mapper = FormProcessMapper.find_form_by_form_id(form_id)
            response, status = {
                "is_anonymous": bool(mapper.is_anonymous),
                "status": mapper.status,
            }, HTTPStatus.OK
        except BaseException as application_err:  # pylint: disable=broad-except
            response, status = {
                "type": "Bad request error",
                "message": "Invalid application request passed",
            }, HTTPStatus.BAD_REQUEST
            current_app.logger.warning(response)
            current_app.logger.warning(application_err)
        return response, status
