from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Integer()
    nickname = fields.String()


class UserParams(Schema):
    nickname = fields.String(required=True)
