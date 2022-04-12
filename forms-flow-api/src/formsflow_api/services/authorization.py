"""This exposes application authorization service."""
from http import HTTPStatus

from formsflow_api.models import Authorization
from formsflow_api.schemas import AuthorizationSchema

from formsflow_api.exceptions import BusinessException

authorization_schema = AuthorizationSchema()


class AuthorizationService:
    """This class manages authorization service."""

    @staticmethod
    def create_authorization(data):
        """Create new Authorization."""
        authorization = Authorization.create_from_dict(data)
        return authorization_schema.dump(authorization)

    @staticmethod
    def get_all_authorization():
        """Get authorization."""
        authorization = Authorization.find_all()
        return authorization_schema.dump(authorization, many=True)

    @staticmethod
    def get_authorization_by_id(authorization_id):
        """Get authorization by id."""
        authorization = Authorization.find_authorization_by_id(authorization_id=authorization_id)
        if authorization:
            return authorization_schema.dump(authorization)
        raise BusinessException("Invalid authorization id", HTTPStatus.BAD_REQUEST)

    @staticmethod
    def update_authorization(authorization_id, data):
        """Update Authorization."""
        authorization = Authorization.find_authorization_by_id(
            authorization_id=authorization_id
        )
        if authorization:
            authorization.update(data)
            return authorization_schema.dump(authorization)
        raise KeyError("Invalid authorization id", HTTPStatus.BAD_REQUEST)

    @staticmethod
    def delete_authorization(authorization_id):
        """Delete data by id."""
        authorization = Authorization.find_authorization_by_id(authorization_id=authorization_id)
        if authorization:
            authorization.delete()
            return authorization_id
        raise BusinessException("Invalid authorization id", HTTPStatus.BAD_REQUEST)
