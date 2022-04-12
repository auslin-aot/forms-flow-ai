"""This manages Authorization Database Models."""

from __future__ import annotations

from .base_model import BaseModel
from .db import db


class Authorization(BaseModel, db.Model):
    """This class manages authorization information."""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    identity = db.Column(db.String(100), nullable=False)
    permissions = db.Column(db.String(100), nullable=False)
    resource_id = db.Column(db.String(100), nullable=False)

    @classmethod
    def create_from_dict(cls, authorization_info: dict) -> Authorization:
        """Create new authorization info."""
        if authorization_info:
            authorization = Authorization()
            authorization.category = authorization_info['category']
            authorization.type = authorization_info['type']
            authorization.identity = authorization_info['identity']
            authorization.permissions = authorization_info['permissions']
            authorization.resource_id = authorization_info['resource_id']
            authorization.save()
            return authorization
        return None

    def update(self, mapper_info: dict):
        """Update authorization."""
        self.update_from_dict(
            [
                "category",
                "type",
                "identity",
                "permissions",
                "resource_id",
            ],
            mapper_info,
        )
        self.commit()

    def delete(self):
        """Delete data."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        """Fetch all the authorization."""
        query = cls.query.order_by(cls.id.desc()).all()
        return query

    @classmethod
    def find_authorization_by_id(cls, authorization_id) -> Authorization:
        """Find authorization that matches the provided id."""
        return cls.query.filter(cls.id == authorization_id).first()
