# lib/load_only_dump_only.py

from marshmallow import Schema, fields, post_load
from datetime import datetime
from pprint import pprint

# model

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.created_at = datetime.now()

# schema 

class UserSchema(Schema):
    name = fields.Str()
    password = fields.Str(load_only=True)         #read-only/deserialized 
    created_at = fields.DateTime(dump_only=True)  #write-only/serialized

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

user_schema = UserSchema()

user_data = {"name": "Lua",  "password": "secret"}   # created_at is dump_only

user =  user_schema.load( user_data  )   

pprint(user_schema.dumps(user))                      # password is load_only
# => '{"name": "Lua", "created_at": "2023-11-11T10:56:55.898190"}'

