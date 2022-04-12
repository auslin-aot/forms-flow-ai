"""Unit tests for authorization Model."""
from formsflow_api.models import Authorization


def test_new_authorization():
    """
    GIVEN a authorization model
    WHEN a new authorization is created
    THEN check category, identity, resource_id, type defined correctly
    """

    authorization = Authorization(category="Formid authorization", identity="test_user", permissions="ALL", resource_id="12",
    type="ALLOW")
    assert authorization.category == "Formid authorization"
    assert authorization.identity == "test_user"
    assert authorization.resource_id == "12"
    assert authorization.type == "ALLOW"
