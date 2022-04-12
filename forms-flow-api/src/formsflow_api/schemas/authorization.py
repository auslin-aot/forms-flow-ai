"""This manages authorization Response Schema."""

from marshmallow import EXCLUDE, Schema, fields


class AuthorizationSchema(Schema):
    """This class manages authorization response schema."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Exclude unknown fields in the deserialized output."""

        unknown = EXCLUDE

    id = fields.Int()
    category = fields.Str()
    type = fields.Str()
    identity = fields.Str()
    permissions = fields.Str()
    resource_id = fields.Str(data_key="resourceId")
