"""Test suite for Import API endpoint."""

import json
import io
from werkzeug.datastructures import FileStorage
from formsflow_api_utils.utils import CREATE_DESIGNS
from tests.utilities.base_test import get_token
from unittest.mock import patch, MagicMock

def form_workflow_data():
    """Form workflow json."""
    return {
        "forms": [
            {
                "formTitle": "testform156",
                "formDescription": "",
                "anonymous": "false",
                "type": "main",
                "content": {
                    "title": "testform156",
                    "name": "testform156",
                    "path": "testform156",
                    "type": "form",
                    "display": "form",
                    "tags": ["common"],
                    "isBundle": "false",
                    "access": [
                        {
                            "type": "read_all",
                            "roles": [
                                "66d93e5986f02eb25448d611",
                                "66d93e5986f02eb25448d5f1",
                                "66d93e5986f02eb25448d608",
                            ],
                        },
                    ],
                    "submissionAccess": [
                        {"roles": ["628f0edf19cebb9cea4f1226"], "type": "create_all"},
                        {"roles": ["628f0edf19cebb9cea4f1232"], "type": "read_all"},
                        {"roles": ["628f0edf19cebb9cea4f1232"], "type": "update_all"},
                        {
                            "roles": [
                                "628f0edf19cebb9cea4f1226",
                                "628f0edf19cebb9cea4f1232",
                            ],
                            "type": "delete_all",
                        },
                        {"roles": ["628f0ee019cebb9cea4f1236"], "type": "create_own"},
                        {"roles": ["628f0ee019cebb9cea4f1236"], "type": "read_own"},
                        {"roles": ["628f0ee019cebb9cea4f1236"], "type": "update_own"},
                        {"roles": ["628f0edf19cebb9cea4f1232"], "type": "delete_own"},
                    ],
                    "owner": "66d93e5986f02eb25448d68f",
                    "components": [
                        {
                            "label": "Text Field",
                            "labelPosition": "top",
                            "placeholder": "",
                            "description": "",
                            "tooltip": "",
                            "prefix": "",
                            "suffix": "",
                            "widget": {"type": "input"},
                            "inputMask": "",
                            "displayMask": "",
                            "allowMultipleMasks": "false",
                            "customClass": "",
                            "tabindex": "",
                            "autocomplete": "",
                            "hidden": "false",
                            "hideLabel": "false",
                            "showWordCount": "false",
                            "showCharCount": "false",
                            "mask": "false",
                            "autofocus": "false",
                            "spellcheck": "true",
                            "disabled": "false",
                            "tableView": "true",
                            "modalEdit": "false",
                            "multiple": "false",
                            "persistent": "true",
                            "inputFormat": "plain",
                            "protected": "false",
                            "dbIndex": "false",
                            "case": "",
                            "truncateMultipleSpaces": "false",
                            "encrypted": "false",
                            "redrawOn": "",
                            "clearOnHide": "true",
                            "customDefaultValue": "",
                            "calculateValue": "",
                            "calculateServer": "false",
                            "allowCalculateOverride": "false",
                            "validateOn": "change",
                            "validate": {
                                "required": "false",
                                "pattern": "",
                                "customMessage": "",
                                "custom": "",
                                "customPrivate": "false",
                                "json": "",
                                "minLength": "",
                                "maxLength": "",
                                "strictDateValidation": "false",
                                "multiple": "false",
                                "unique": "false",
                            },
                            "unique": "false",
                            "errorLabel": "",
                            "errors": "",
                            "key": "textField",
                            "tags": [],
                            "properties": {},
                            "conditional": {
                                "show": "null",
                                "when": "null",
                                "eq": "",
                                "json": "",
                            },
                            "customConditional": "",
                            "logic": [],
                            "attributes": {},
                            "overlay": {
                                "style": "",
                                "page": "",
                                "left": "",
                                "top": "",
                                "width": "",
                                "height": "",
                            },
                            "type": "textfield",
                            "input": "true",
                            "refreshOn": "",
                            "dataGridLabel": "false",
                            "addons": [],
                            "inputType": "text",
                            "id": "eabmhto",
                            "defaultValue": "null",
                        },
                        {
                            "type": "button",
                            "label": "Submit",
                            "key": "submit",
                            "size": "md",
                            "block": "false",
                            "action": "submit",
                            "disableOnInvalid": "true",
                            "theme": "primary",
                            "input": "true",
                            "placeholder": "",
                            "prefix": "",
                            "customClass": "",
                            "suffix": "",
                            "multiple": "false",
                            "defaultValue": "null",
                            "protected": "false",
                            "unique": "false",
                            "persistent": "false",
                            "hidden": "false",
                            "clearOnHide": "true",
                            "refreshOn": "",
                            "redrawOn": "",
                            "tableView": "false",
                            "modalEdit": "false",
                            "dataGridLabel": "true",
                            "labelPosition": "top",
                            "description": "",
                            "errorLabel": "",
                            "tooltip": "",
                            "hideLabel": "false",
                            "tabindex": "",
                            "disabled": "false",
                            "autofocus": "false",
                            "dbIndex": "false",
                            "customDefaultValue": "",
                            "calculateValue": "",
                            "calculateServer": "false",
                            "widget": {"type": "input"},
                            "attributes": {},
                            "validateOn": "change",
                            "validate": {
                                "required": "false",
                                "custom": "",
                                "customPrivate": "false",
                                "strictDateValidation": "false",
                                "multiple": "false",
                                "unique": "false",
                            },
                            "conditional": {"show": "null", "when": "null", "eq": ""},
                            "overlay": {
                                "style": "",
                                "left": "",
                                "top": "",
                                "width": "",
                                "height": "",
                            },
                            "allowCalculateOverride": "false",
                            "encrypted": "false",
                            "showCharCount": "false",
                            "showWordCount": "false",
                            "properties": {},
                            "allowMultipleMasks": "false",
                            "addons": [],
                            "leftIcon": "",
                            "rightIcon": "",
                            "id": "ehluayb",
                        },
                        {
                            "label": "applicationId",
                            "customClass": "",
                            "addons": [],
                            "modalEdit": "false",
                            "persistent": "true",
                            "protected": "false",
                            "dbIndex": "false",
                            "encrypted": "false",
                            "redrawOn": "",
                            "customDefaultValue": "",
                            "calculateValue": "",
                            "calculateServer": "false",
                            "key": "applicationId",
                            "tags": [],
                            "properties": {},
                            "logic": [],
                            "attributes": {},
                            "overlay": {
                                "style": "",
                                "page": "",
                                "left": "",
                                "top": "",
                                "width": "",
                                "height": "",
                            },
                            "type": "hidden",
                            "input": "true",
                            "placeholder": "",
                            "prefix": "",
                            "suffix": "",
                            "multiple": "false",
                            "unique": "false",
                            "hidden": "false",
                            "clearOnHide": "true",
                            "refreshOn": "",
                            "tableView": "false",
                            "labelPosition": "top",
                            "Description": "",
                            "errorLabel": "",
                            "tooltip": "",
                            "hideLabel": "false",
                            "tabindex": "",
                            "disabled": "false",
                            "autofocus": "false",
                            "widget": {"type": "input"},
                            "validateOn": "change",
                            "validate": {
                                "required": "false",
                                "custom": "",
                                "customPrivate": "false",
                                "strictDateValidation": "false",
                                "multiple": "false",
                                "unique": "false",
                            },
                            "conditional": {"show": "null", "when": "null", "eq": ""},
                            "allowCalculateOverride": "false",
                            "showCharCount": "false",
                            "showWordCount": "false",
                            "allowMultipleMasks": "false",
                            "inputType": "hidden",
                            "id": "em1y8gd",
                            "defaultValue": "",
                            "dataGridLabel": "false",
                            "description": "",
                        },
                        {
                            "label": "applicationStatus",
                            "addons": [],
                            "customClass": "",
                            "modalEdit": "false",
                            "defaultValue": "null",
                            "persistent": "true",
                            "protected": "false",
                            "dbIndex": "false",
                            "encrypted": "false",
                            "redrawOn": "",
                            "customDefaultValue": "",
                            "calculateValue": "",
                            "calculateServer": "false",
                            "key": "applicationStatus",
                            "tags": [],
                            "properties": {},
                            "logic": [],
                            "attributes": {},
                            "overlay": {
                                "style": "",
                                "page": "",
                                "left": "",
                                "top": "",
                                "width": "",
                                "height": "",
                            },
                            "type": "hidden",
                            "input": "true",
                            "tableView": "false",
                            "placeholder": "",
                            "prefix": "",
                            "suffix": "",
                            "multiple": "false",
                            "unique": "false",
                            "hidden": "false",
                            "clearOnHide": "true",
                            "refreshOn": "",
                            "dataGridLabel": "false",
                            "labelPosition": "top",
                            "Description": "",
                            "errorLabel": "",
                            "tooltip": "",
                            "hideLabel": "false",
                            "tabindex": "",
                            "disabled": "false",
                            "autofocus": "false",
                            "widget": {"type": "input"},
                            "validateOn": "change",
                            "validate": {
                                "required": "false",
                                "custom": "",
                                "customPrivate": "false",
                                "strictDateValidation": "false",
                                "multiple": "false",
                                "unique": "false",
                            },
                            "conditional": {"show": "null", "when": "null", "eq": ""},
                            "allowCalculateOverride": "false",
                            "showCharCount": "false",
                            "showWordCount": "false",
                            "allowMultipleMasks": "false",
                            "inputType": "hidden",
                            "id": "e6z1qd9",
                            "description": "",
                        },
                    ],
                    "created": "2024-09-05T06:33:02.367Z",
                    "modified": "2024-09-05T06:33:02.385Z",
                },
            }
        ],
        "workflows": [
            {
                "processKey": "Defaultflow",
                "processName": "Default Flow",
                "type": "main",
                "content": '<?xml version="1.0" encoding="UTF-8"?>\n<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:camunda="http://camunda.org/schema/1.0/bpmn" xmlns:di="http://www.omg.org/spec/DD/20100524/DI" xmlns:modeler="http://camunda.org/schema/modeler/1.0" id="Definitions_1gblxi8" targetNamespace="http://bpmn.io/schema/bpmn" exporter="Camunda Modeler" exporterVersion="4.12.0" modeler:executionPlatform="Camunda Platform" modeler:executionPlatformVersion="7.15.0">\n  <bpmn:process id="Defaultflow" name="Default Flow" isExecutable="true">\n    <bpmn:startEvent id="StartEvent_1" name="Default Flow Started">\n      <bpmn:outgoing>Flow_09rbji4</bpmn:outgoing>\n    </bpmn:startEvent>\n    <bpmn:task id="Audit_Task_Executed" name="Execute Audit Task">\n      <bpmn:extensionElements>\n        <camunda:executionListener event="start">\n          <camunda:script scriptFormat="javascript">execution.setVariable(\'applicationStatus\', \'Completed\');</camunda:script>\n        </camunda:executionListener>\n        <camunda:executionListener class="org.camunda.bpm.extension.hooks.listeners.BPMFormDataPipelineListener" event="start">\n          <camunda:field name="fields">\n            <camunda:expression>["applicationId","applicationStatus"]</camunda:expression>\n          </camunda:field>\n        </camunda:executionListener>\n        <camunda:executionListener class="org.camunda.bpm.extension.hooks.listeners.ApplicationStateListener" event="end" />\n      </bpmn:extensionElements>\n      <bpmn:incoming>Flow_09rbji4</bpmn:incoming>\n      <bpmn:outgoing>Flow_0klorcg</bpmn:outgoing>\n    </bpmn:task>\n    <bpmn:sequenceFlow id="Flow_09rbji4" sourceRef="StartEvent_1" targetRef="Audit_Task_Executed">\n      <bpmn:extensionElements>\n        <camunda:executionListener event="take">\n          <camunda:script scriptFormat="javascript">execution.setVariable(\'applicationStatus\', \'New\');</camunda:script>\n        </camunda:executionListener>\n        <camunda:executionListener class="org.camunda.bpm.extension.hooks.listeners.ApplicationStateListener" event="take" />\n      </bpmn:extensionElements>\n    </bpmn:sequenceFlow>\n    <bpmn:endEvent id="Event_1ws2h5w" name="Default Flow Ended">\n      <bpmn:incoming>Flow_0klorcg</bpmn:incoming>\n    </bpmn:endEvent>\n    <bpmn:sequenceFlow id="Flow_0klorcg" sourceRef="Audit_Task_Executed" targetRef="Event_1ws2h5w" />\n  </bpmn:process>\n  <bpmndi:BPMNDiagram id="BPMNDiagram_1">\n    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Defaultflow">\n      <bpmndi:BPMNEdge id="Flow_0klorcg_di" bpmnElement="Flow_0klorcg">\n        <di:waypoint x="370" y="117" />\n        <di:waypoint x="432" y="117" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNEdge id="Flow_09rbji4_di" bpmnElement="Flow_09rbji4">\n        <di:waypoint x="215" y="117" />\n        <di:waypoint x="270" y="117" />\n      </bpmndi:BPMNEdge>\n      <bpmndi:BPMNShape id="_BPMNShape_StartEvent_2" bpmnElement="StartEvent_1">\n        <dc:Bounds x="179" y="99" width="36" height="36" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="166" y="142" width="62" height="27" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Activity_1qmqqen_di" bpmnElement="Audit_Task_Executed">\n        <dc:Bounds x="270" y="77" width="100" height="80" />\n      </bpmndi:BPMNShape>\n      <bpmndi:BPMNShape id="Event_1ws2h5w_di" bpmnElement="Event_1ws2h5w">\n        <dc:Bounds x="432" y="99" width="36" height="36" />\n        <bpmndi:BPMNLabel>\n          <dc:Bounds x="419" y="142" width="62" height="27" />\n        </bpmndi:BPMNLabel>\n      </bpmndi:BPMNShape>\n    </bpmndi:BPMNPlane>\n  </bpmndi:BPMNDiagram>\n</bpmn:definitions>\n',
            }
        ],
        "rules": [],
        "authorizations": [
            {
                "APPLICATION": {
                    "resourceId": "66d9509e86f02eb25448d75b",
                    "resourceDetails": {},
                    "roles": [],
                    "userName": None,
                },
                "DESIGNER": {
                    "resourceId": "66d9509e86f02eb25448d75b",
                    "resourceDetails": {},
                    "roles": [],
                    "userName": None,
                },
                "FORM": {
                    "resourceId": "66d9509e86f02eb25448d75b",
                    "resourceDetails": {},
                    "roles": [],
                    "userName": None,
                },
            }
        ],
    }


def create_file(form_content):
    """Create a file-like object."""
    return FileStorage(
        stream=io.BytesIO(form_content.encode("utf-8")),
        filename="response_export-1.json",
        content_type="application/json",
    )


def test_import(app, client, session, jwt, mock_redis_client):
    """Testing import."""

    token = get_token(jwt, role=CREATE_DESIGNS, username="designer")
    headers = {
        "Authorization": f"Bearer {token}",
    }

    with patch("requests.post") as mock_post:
        # Create a mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"form":{"majorVersion": 1,"minorVersion": 0}, "workflow":{"majorVersion": 3,"minorVersion": 4}}'
        mock_post.return_value = mock_response
        # Prepare the file content
        form_content = json.dumps(form_workflow_data())
        file = create_file(form_content)

        # input form-data
        form_data = {
            "file": file,
            "data": json.dumps(
                {
                    "importType": "new",
                    "action": "validate",
                }
            ),
        }

        # Send the POST request with form-data
        response = client.post("/import", data=form_data, headers=headers)

        # Assertions to validate the response
        assert response.status_code == 200
        assert response.json is not None
        assert len(response.json["form"]) is not None
        assert response.json["form"]["majorVersion"] == 1
        assert response.json["form"]["minorVersion"] == 0
        assert len(response.json["workflow"]) is not None
        assert response.json["workflow"]["majorVersion"] == 1
        assert response.json["workflow"]["minorVersion"] == 0
