# lib/deserialize.py

from marshmallow import Schema, fields
from pprint import pprint

# schema

class HamsterSchema(Schema):
     name = fields.Str()
     breed = fields.Str()
     dob = fields.Date()
