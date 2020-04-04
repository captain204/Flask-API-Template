from marshmallow import Schema, fields, pre_load
from marshmallow import validate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from passlib.apps import custom_app_context as password_context
import re




orm = SQLAlchemy()
ma = Marshmallow()


class ResourceAddUpdateDelete():   
    def add(self, resource):
        orm.session.add(resource)
        return orm.session.commit()

    def update(self):
        return orm.session.commit()

    def delete(self, resource):
        orm.session.delete(resource)
        return orm.session.commit()




class User(orm.Model, ResourceAddUpdateDelete):
    id = orm.Column(orm.Integer, primary_key=True)
    name = orm.Column(orm.String(50), unique=True, nullable=False)
    password_hash = orm.Column(orm.String(120), nullable=False)
    creation_date = orm.Column(orm.TIMESTAMP,server_default=orm.func.current_timestamp(), nullable=False)

    def verify_password(self, password):
        return password_context.verify(password, self.password_hash)

    def check_password_strength_and_hash_if_ok(self, password):
        if len(password) < 8:
            return 'The password is too short. Please, specify a password with at least 8 characters.', False
        if len(password) > 32:
            return 'The password is too long. Please, specify a password with no more than 32 characters.', False

        if re.search(r'[A-Z]', password) is None:
            return 'The password must include at least one uppercase letter.', False

        if re.search(r'[a-z]', password) is None:
            return 'The password must include at least one lowercase letter.', False

        if re.search(r'\d', password) is None:
            return 'The password must include at least one number.', False

        if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~"+r'"]',password) is None:
            return 'The password must include at least one symbol.', False

        self.password_hash = password_context.hash(password)
        return '', True

    def __init__(self, name):
        self.name = name




class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,validate=validate.Length(3))
    password = fields.String(required=True,validate=validate.Length(6))
    url = ma.URLFor('api.userresource',id='<id>',_external=True)

    