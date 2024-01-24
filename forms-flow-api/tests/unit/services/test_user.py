"""Tests to assure the User Service."""
from unittest.mock import patch

from formsflow_api.services.factory.keycloak_client_service import (
    KeycloakClientService,
)


def test_keycloak_tenant_users_list(app, client, session):
    """Test tenant users list."""
    with patch(
        "formsflow_api.services.factory.keycloak_client_service.KeycloakClientService.get_tenant_users"
    ) as mock_get:
        # Configure the mock to return a response.
        user_list = [
            {
                "id": "42b46b3b-1fd0-45e4-82d7-2527f7602509",
                "username": "alpha-admin",
                "firstName": "alpha",
                "lastName": "Admin",
                "email": "admin@alpha.formsflow.ai",
                "attributes": {"tenantKey": ["alpha"]},
            },
            {
                "id": "42b46b3b-1fd0-45e4-82d7-2527f7602509",
                "username": "alpha-reviewer",
                "firstName": "alpha",
                "lastName": "reviewer",
                "email": "reviewer@alpha.formsflow.ai",
                "attributes": {"tenantKey": ["alpha"]},
            },
            {
                "id": "42b46b3b-1fd0-45e4-82d7-2527f7602511",
                "username": "alpha-client",
                "firstName": "alpha",
                "lastName": "client",
                "email": "client@alpha.formsflow.ai",
                "attributes": {"tenantKey": ["alpha"]},
            },
            {
                "id": "42b46b3b-1fd0-45e4-82d7-2527f7602543",
                "username": "alpha-designer",
                "firstName": "alpha",
                "lastName": "designer",
                "email": "designer@alpha.formsflow.ai",
                "attributes": {"tenantKey": ["alpha"]},
            },
        ]
        count = len(user_list)
        mock_get.return_value = user_list, count

        assert (
            KeycloakClientService().search_realm_users(
                search=None, page_no=1, limit=5, count=True, role=False
            )[0]
            == user_list
        )
