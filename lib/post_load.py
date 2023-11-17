# lib/post_load.py

from marshmallow import Schema, fields, post_load
from pprint import pprint

# model

class Dog:
    def __init__(self, name, breed, tail_wagging = False):
        self.name = name
        self.breed = breed
        self.tail_wagging = tail_wagging
        
    def give_treat(self):
        self.tail_wagging = True
        
    def scold(self):
        self.tail_wagging = False

# schema

class DogSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    tail_wagging = fields.Boolean()

# deserialize

dog_schema = DogSchema()
dog_json = '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog = dog_schema.loads(dog_json)
print(type(dog))             # => <class 'dict'>
print(isinstance(dog, Dog))  # => False
pprint(dog)                  # => {'breed': 'Beagle', 'name': 'Snuggles', 'tail_wagging': True}