"""This manages Authorization Schema."""

from marshmallow import EXCLUDE, Schema, fields


class VariableSchema(Schema):
    """This class provides the schema for variable."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Exclude unknown fields."""

        unknown = EXCLUDE

    name = fields.Str(required=True)
    label = fields.Str()


class AuthorizationFilterSchema(Schema):
    """This class provides the schema for authorization filter data."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Exclude unknown fields."""

        unknown = EXCLUDE

    title = fields.Str(required=True)
    variables = fields.List(fields.Nested(VariableSchema))
    include_assigned_tasks = fields.Boolean(data_key="includeAssignedTasks")
    assignee = fields.Str()
