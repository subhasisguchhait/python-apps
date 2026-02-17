# app/schemas.py
from marshmallow import Schema, fields


class UserCreateSchema(Schema):
    """Validates POST input."""
    full_name = fields.String(required=True)
    email = fields.Email(required=True)


class UserUpdateSchema(Schema):
    """Validates PUT input (partial updates allowed)."""
    full_name = fields.String()
    email = fields.Email()


class UserSchema(Schema):
    """Controls response JSON shape."""
    id = fields.Integer(dump_only=True) # dump_only=True means “never accept this from input, only return it in output” (for id).
    full_name = fields.String()
    email = fields.Email()
