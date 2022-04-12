"""Test suite for authorization API endpoint."""
import pytest

from tests.utilities.base_test import (
    factory_auth_header,
    get_authorization_request_payload,
)

def test_authorization_creation(app, client, session):
    """Testing authorization create API."""
    token = factory_auth_header()
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = client.post("/authorization", headers=headers, json=get_authorization_request_payload())
    assert response.status_code == 201
    assert response.json.get("id") is not None

def test_authorization_list(app, client, session):
    """Testing authorization listing API."""
    token = factory_auth_header()
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = client.get("/authorization", headers=headers)
    assert response.status_code == 200
    assert response.json is not None

def test_authorization_detail_view(app, client, session):
    """Testing authorization get by id API."""
    token = factory_auth_header()
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = client.post("/authorization", headers=headers, json=get_authorization_request_payload())
    assert response.status_code == 201
    assert response.json.get("id") is not None
    auth_id = response.json.get("id")
    rv = client.get(f"/authorization/{auth_id}", headers=headers)
    assert rv.status_code == 200
    assert rv.json.get("id") == auth_id

def test_authorization_update(app, client, session):
    """Testing authorization update API."""
    token = factory_auth_header()
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = client.post("/authorization", headers=headers, json=get_authorization_request_payload())
    assert response.status_code == 201
    assert response.json.get("id") is not None
    auth_id = response.json.get("id")
    rv = client.put(f"/authorization/{auth_id}", headers=headers, json=get_authorization_request_payload())
    assert rv.status_code == 200

def test_authorization_delete(app, client, session):
    """Testing authorization delete API."""
    token = factory_auth_header()
    headers = {"Authorization": f"Bearer {token}", "content-type": "application/json"}
    response = client.post("/authorization", headers=headers, json=get_authorization_request_payload())
    assert response.status_code == 201
    assert response.json.get("id") is not None
    auth_id = response.json.get("id")
    rv = client.delete(f"/authorization/{auth_id}", headers=headers)
    assert rv.status_code == 200
    rv = client.get(f"/authorization/{auth_id}", headers=headers)
    assert rv.status_code != 200
