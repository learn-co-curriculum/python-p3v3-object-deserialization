# Deserialization : Code-Along

## Learning Goals

- Use the marshmallow library to deserialize an input dictionary to a Python
  class instance.
- Filter fields as `load_only` or `dump_only`.
- Define custom `function` and `method` fields to compute values during
  serialization.

---

## Key Vocab

- **Serialization**: a process to convert programmatic data such as a Python
  object to a sequence of bytes that can be shared with other programs,
  computers, or networks.
- **Deserialization**: the reverse process, converting input data back to
  programmatic data.

---

## Introduction

Serialization is a technique for converting data such as a Python class instance
to a series of bytes. Deserialization is the reverse process, converting the
byte stream back to a Python class instance or some other application-level data
structure.

We've seen how to use the `marshmallow` library to serialize object state using
the `dump()` or `dumps()` methods, which respectively produce a dictionary and
JSON-encoded string. In this lesson, we'll use the `load()` and `loads()`
methods to perform the reverse process of deserialization, creating a Python
class instance from input data formatted as either a dictionary or a
JSON-encoded string.

## Setup

This lesson is a code-along, so fork and clone the repo.

Run `pipenv install` to install the dependencies and `pipenv shell` to enter
your virtual environment before running your code.

```console
$ pipenv install
$ pipenv shell
```

---

## Deserialization

With serialization, we **dump** object state as output data in a format that is
easy to share such as a dictionary or string. You can view deserialization as
the reverse, where we **load** input data formatted as a dictionary or string
into a more complex Python data structure such as a class instance. However,
before we deserialize to a class instance, we'll first see how to serialize to
simpler data type such as a dictionary. It may seem odd to deserialize a
dictionary to a dictionary, but it is the first step in the process.
Deserialization to an object includes a post-loading step that we'll explore
later in the lesson.

Within the `lib` directory, you'll find the file `deserialize.py` that defines a
marshmallow schema named `HamsterSchema`. The file does not include a hamster
model class, since we won't be creating model objects just yet.

```py
# lib/deserialize.py

from marshmallow import Schema, fields
from pprint import pprint

# schema

class HamsterSchema(Schema):
     name = fields.Str()
     breed = fields.Str()
     dob = fields.Date()
```

The `load()` method validates and deserializes an input dictionary to an
application-level data structure. By default, `load()` returns a dictionary of
field names mapped to deserialized values. We'll explore what happens if there
are validation errors in a separate lesson.

Update the code as shown below to create a schema instance, along with an input
dictionary that contains key-value pairs for each field defined in the schema.
We can then call the `load()` method on the schema, passing the input dictionary
as a parameter. The `load()` method validates that the contents of the input
dictionary (i.e. the dictionary key-value pairs correspond to the field types
specified in the schema), and then returns a new dictionary as the method
result.

```py
# validate and deserialize an input dictionary to an output dictionary
# of field names mapped to deserialized values with the load() method.

hamster_schema = HamsterSchema()
hamster_dict = {"name" : "Fluffernutter", "breed": "Roborovski", "dob" : "2014-08-11"}
result = hamster_schema.load(hamster_dict)
print(type(result)) # => <class 'dict'>
pprint(result)      #
# => {'breed': 'Roborovski',
# =>  'dob': datetime.date(2014, 8, 11),
# =>  'name': 'Fluffernutter'}
```

The output should display the deserialized data in a dictionary format. The
pretty-printing function `pprint` displays the dictionary across multiple lines
if there is too much content to fit on one line. Notice the `dob` field has been
converted from the `datetime` input string "2014-08-11 into an object
`datetime.date(2014, 8, 11)`.

```console
$ python lib/deserialize.py
<class 'dict'>
{'breed': 'Roborovski',
 'dob': datetime.date(2014, 8, 11),
 'name': 'Fluffernutter'}
<class 'dict'>
```

We can use the `loads()` method to deserialize using as input a JSON-encoded
string. Update the code to add the following, noticing the variable
`hamster_json` is assigned to a string, not a dictionary:

```py
# validate and deserialize a JSON-encoded string to an output dictionary
# of field names mapped to deserialized values with the loads() method.

hamster_json = '{"name": "Wiggles", "breed": "Siberian", "dob": "2020-01-30"}'
result_2 = hamster_schema.loads(hamster_json)
print(type(result_2))  # => <class 'dict'>
pprint(result_2)
# => {'breed': 'Siberian',
# =>  'dob': datetime.date(2020, 1, 30),
# =>  'name': 'Wiggles'}
```

The `loads()` method returns a dictionary as a result as seen in the output.

```console
$ python lib/deserialize.py
...
<class 'dict'>
{'breed': 'Siberian',
 'dob': datetime.date(2020, 1, 30),
 'name': 'Wiggles'}
```

## Deserializing a collection

A collection can be deserialized by passing `many=True`, either when
instantiating the schema or as an extra parameter passed to the `load()` or
`loads()` methods. The result of deserialization is a list of dictionaries.

Update the code to deserialize a collection as shown below by passing a list of
dictionaries along with `many=True` as parameters to the `load()`: method.

```py
# deserialize a list of dictionaries

hamster_1 = {"name": "Nibbles", "breed": "European",  "dob": "2018-04-30"}
hamster_2 = {"name": "Snuggles", "breed": "Chinese", "dob": "2023-10-07"}
hamster_list = [hamster_1, hamster_2]
result_3 = hamster_schema.load(hamster_list, many = True)
print(type(result_3))  # => <class 'list'>
pprint(result_3)       # list of dictionaries
# => [{'breed': 'European', 'dob': datetime.date(2018, 4, 30), 'name': 'Nibbles'},
# =>  {'breed': 'Chinese', 'dob': datetime.date(2023, 10, 7), 'name': 'Snuggles'}]
```

We can also deserialize a JSON-encoded string containing an array of objects
using the `loads()` method. Let's pass the parameter `many=True` when creating
the schema to demonstrate that option. Add the following code and confirm the
output:

```py
# deserialize a JSON array

hamster_1 = '{"name": "Honey", "breed": "Turkish", "dob": "2009-06-03"}'
hamster_2 = '{"name": "Squeaky", "breed": "Winter White", "dob": "2022-12-31"}'
hamsters  = f'[{hamster_1}, {hamster_2}]'   #string contains JSON array of objects
hamster_schema_many = HamsterSchema(many=True)
result_4 = hamster_schema_many.loads(hamsters)
print(type(result_4))  # => <class 'list'>
pprint(result_4)       # list of dictionaries
# => [{'breed': 'Turkish', 'dob': datetime.date(2009, 6, 3),'name': 'Honey'},
# =>  {'breed': 'White White', 'dob': datetime.date(2022, 12, 31), 'name': 'Squeaky'}]
```

### Deserializing to objects (post-load)

To deserialize to an object, we need to define a method of the schema and
decorate it with `@post_load`. The method receives a dictionary of deserialized
data.

Open `lib/post_load.py`. The file defines a model class named `Dog`, along a
schema named `DogSchema`. If you run the current version of the code, the
`loads` method returns a dictionary, not a `Dog` instance, since by default the
method returns a dictionary data structure. The call to `pprint` displays the
dictionary contents.

```py
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
```

We can deserialize to an object by defining a method in the schema and
decorating it with ` @post_load`. The method receives a dictionary of
deserialized data. Update the `DogSchema` as shown to add this method:

```py
class DogSchema(Schema):
    name = fields.Str()
    breed = fields.Str()
    tail_wagging = fields.Boolean()

    # take a dictionary of deserialized data and return a model instance
    @post_load
    def make_dog(self, data, **kwargs):
        return Dog(**data)
```

If you run the code, you'll see the output reflects that a `Dog` instance was
returned from loading:

```console
$ python lib/post_load.py
<class '__main__.Dog'>
True
<__main__.Dog object at 0x102e1c910>
```

Let's update the comments to reflect the correct output.

```py
print(type(dog))             # => <class 'dict'>
print(isinstance(dog, Dog))  # => True
pprint(dog)                  # => <models.Dog object at 0x102c28d90>
```

Now that we've deserialized to a `Dog` object, we can invoke the methods
`scold()` and `give_treat()` to change the object's state. We'll also use the
`dumps()` method to serialize the object and confirm the state changes.

```py
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

    # take a dictionary of deserialized data and return a model instance
    @post_load
    def make_dog(self, data, **kwargs):
        return Dog(**data)

# deserialize to a class instance by defining a @post_load method in the schema

dog_schema = DogSchema()
dog_json = '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog = dog_schema.loads(dog_json)
print(type(dog))             # => <class 'dict'>
print(isinstance(dog, Dog))  # => True
pprint(dog)                  # => <models.Dog object at 0x102c28d90>

# call instance methods to change object state, deserialize to JSON using dumps()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog.scold()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": false}'
dog.give_treat()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

### Load-only and Dump-Only Fields

We may want define fields that are "load-only" (used during deserialization) or
"dump_only" (used during serialization).

For example, consider the `User` model show below.  
The constructor takes parameters for the `name` and `password`. However,
`created_at` is computed as the current timestamp and not passed as a parameter.

```py
class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.created_at = datetime.now()
```

We want values for `name` and `password` when we deserialize input data to
create a `User` instance, but we don't need a value for `created_at` since it is
computed. We probably do not want to include `password` when we serialize the
object state since that value should not be shared.

The parameter `load_only=True` is used to indicate a schema field should be used
during deserialization but not serialization, while `dump_only=True` indicates
the field should be serialized but not used during deserialization. By default,
a field is defined as `load_only=False` and `dump_only=False`, meaning it will
be used for serialization and deserialization.

Consider the code in `lib/load_only_dump_only.py`.

- The `name` field is used for both serialization and deserialization.
- The `password` field is loaded/deserialized, but is not dumped/serialized.
- The `created_at` field is not loaded/deserialized, but is dumped/serialized.

```py
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
```

Run the code to confirm the output

```console
$ python lib/load_only_dump_only.py
'{"name": "Lua", "created_at": "2023-11-15T07:30:30.660156"}'
```

---

---

## Custom Fields

You can create a custom field beyond the builtin field types. This is often done
during serialization to compute a value from other fields. We will look at two
options for creating a custom field (1) defining a `function` field, and (2)
defining a `method` field.

Consider the code in `lib/custom_field.py`. A cat has fields `name`, `dob`, and
`favorite_toys`.

```py
# lib/custom_field.py

from marshmallow import Schema, fields, post_load
from datetime import date
from pprint import pprint

# model

class Cat:
    def __init__(self, name, dob, favorite_toys = []):
        self.name = name
        self.dob = dob
        self.favorite_toys = favorite_toys

# schema

class CatSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    dob = fields.Date(format="%Y-%m-%d")
    favorite_toys = fields.List(fields.Str())

    @post_load
    def make_cat(self, data, **kwargs):
        return Cat(**data)

schema = CatSchema()

#deserialize
cat_1 = schema.load({"name": "Meowie", "dob": "2020-11-28", "favorite_toys": ["ball", "squeaky mouse"]})
cat_2 = schema.load({"name": "Whiskers", "dob": "2015-4-15", "favorite_toys": []})

#serialize
pprint(schema.dump(cat_1))
# => {'age': 2,
# =>  'dob': '2020-11-28',
# =>  'favorite_toys': ['ball', 'squeaky mouse']}

pprint(schema.dump(cat_2))
# => {'age': 8,
# => 'dob': '2015-04-15',
# => 'favorite_toys': []}
```

Running the code produces the expected output:

```console
{'dob': '2020-11-28',
 'favorite_toys': ['ball', 'squeaky mouse'],
 'name': 'Meowie'}
{'dob': '2015-04-15', 'favorite_toys': [], 'name': 'Whiskers'}
```

Suppose we would like to include in the serialized output two more fields:

- `likes_toys` : a boolean that is true if the list of favorite toys is not
  empty
- `age` : an integer calculated using the date of birth and the current date.

These fields will not be included during loading, since they can be calculated
from the other fields. While we could update the model class to calculate them,
we can also just update the schema to compute them during serialization.

We can use define `likes_toys` using the class `fields.Function` as shown below.
We pass a callable from which to compute the value. The function must take a
single argument `obj` which is the object to be serialized.

```py
likes_toys = fields.Function(lambda obj : len(obj.favorite_toys) > 0, dump_only = True)
```

The calculation for the `age` field doesn't necessarily work as a simple lambda
expression, so we'll implement that field using the class `fields.Method` as
shown:

```py
    age = fields.Method("calculate_age", dump_only = True)

    def calculate_age(self, obj):
        today = date.today()
        return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))

```

Update the code to add the `likes_toys` function and `age` method fields to the
schema:

```py
# lib/custom_field.py

from marshmallow import Schema, fields, post_load
from datetime import date
from pprint import pprint

# model

class Cat:
    def __init__(self, name, dob, favorite_toys = []):
        self.name = name
        self.dob = dob
        self.favorite_toys = favorite_toys

# schema

class CatSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    dob = fields.Date(format="%Y-%m-%d")
    favorite_toys = fields.List(fields.Str())
    likes_toys = fields.Function(lambda obj : len(obj.favorite_toys) > 0, dump_only = True)
    age = fields.Method("calculate_age", dump_only = True)

    def calculate_age(self, obj):
        today = date.today()
        return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))

    @post_load
    def make_cat(self, data, **kwargs):
        return Cat(**data)

schema = CatSchema()

#deserialize
cat_1 = schema.load({"name": "Meowie", "dob": "2020-11-28", "favorite_toys": ["ball", "squeaky mouse"]})
cat_2 = schema.load({"name": "Whiskers", "dob": "2015-4-15", "favorite_toys": []})

#serialize
pprint(schema.dump(cat_1))
# => {'age': 2,
# =>  'dob': '2020-11-28',
# =>  'favorite_toys': ['ball', 'squeaky mouse'],
# =>  'likes_toys': True,
# =>  'name': 'Meowie'}

pprint(schema.dump(cat_2))
# => {'age': 8,
# => 'dob': '2015-04-15',
# => 'favorite_toys': [],
# => 'likes_toys': False,
# => 'name': 'Whiskers'}
```

Now we see `age` and `likes_toys` included in the serialized output:

```console
{'age': 2,
 'dob': '2020-11-28',
 'favorite_toys': ['ball', 'squeaky mouse'],
 'likes_toys': True,
 'name': 'Meowie'}
{'age': 8,
 'dob': '2015-04-15',
 'favorite_toys': [],
 'likes_toys': False,
 'name': 'Whiskers'}
```

## Conclusion

This lesson has covered quite a few concepts involving deserialization:

- The schema `load()` method validates and deserializes an input dictionary.
- The schema `loads()` method validates and deserializes a JSON-encoded string.
- By default, `load()` and `loads()` return a dictionary of field names mapped
  to deserialized values.
- A schema can deserialize a collection by passing the parameter `many=True` to
  either the schema constructor or the schema loading methods.
- To deserialize to an object, we decorate a schema method with `@post_load`,
  and implement the method to take a dictionary of deserialized data and return
  a model instance from the deserialized data.
- The parameter `load_only=True` is used to indicate a schema field should be
  used during deserialization but not serialization, while `dump_only=True`
  indicates the field should be serialized but not used during deserialization.
- By default, a field is defined as `load_only=False` and `dump_only=False`,
  meaning it will be used for both serialization and deserialization.
- Custom fields can be created using `fields.Function` and `fields.Method`
  types.

## Solution Code

```py
# lib/deserialize.py

from marshmallow import Schema, fields
from pprint import pprint

# schema

class HamsterSchema(Schema):
     name = fields.Str()
     breed = fields.Str()
     dob = fields.Date()


# validate and deserialize an input dictionary to an output dictionary
# of field names mapped to deserialized values with the load() method.

hamster_schema = HamsterSchema()
hamster_dict = {"name" : "Fluffernutter", "breed": "Roborovski", "dob" : "2014-08-11"}
result = hamster_schema.load(hamster_dict)
print(type(result)) # => <class 'dict'>
pprint(result)      #
# => {'breed': 'Roborovski dwarf',
# =>  'dob': datetime.date(2014, 8, 11),
# =>  'name': 'Fluffernutter'}

# validate and deserialize a JSON-encoded string to an output dictionary
# of field names mapped to deserialized values with the loads() method.

hamster_json = '{"name": "Wiggles", "breed": "Siberian", "dob": "2020-01-30"}'
result_2 = hamster_schema.loads(hamster_json)
print(type(result_2))  # => <class 'dict'>
pprint(result_2)
# => {'breed': 'Siberian',
# =>  'dob': datetime.date(2020, 1, 30),
# =>  'name': 'Wiggles'}

# deserialize a list of dictionaries

hamster_1 = {"name": "Nibbles", "breed": "European",  "dob": "2018-04-30"}
hamster_2 = {"name": "Snuggles", "breed": "Chinese", "dob": "2023-10-07"}
hamster_list = [hamster_1, hamster_2]
result_3 = hamster_schema.load(hamster_list, many = True)
print(type(result_3))  # => <class 'list'>
pprint(result_3)       # list of dictionaries
# => [{'breed': 'European', 'dob': datetime.date(2018, 4, 30), 'name': 'Nibbles'},
# =>  {'breed': 'Chinese', 'dob': datetime.date(2023, 10, 7), 'name': 'Snuggles'}]

# deserialize a JSON array

hamster_1 = '{"name": "Honey", "breed": "Turkish", "dob": "2009-06-03"}'
hamster_2 = '{"name": "Squeaky", "breed": "Winter White", "dob": "2022-12-31"}'
hamsters  = f'[{hamster_1}, {hamster_2}]'   #string contains JSON array of objects
hamster_schema_many = HamsterSchema(many=True)
result_4 = hamster_schema_many.loads(hamsters)
print(type(result_4))  # => <class 'list'>
pprint(result_4)       # list of dictionaries
# => [{'breed': 'Turkish', 'dob': datetime.date(2009, 6, 3),'name': 'Honey'},
# =>  {'breed': 'White White', 'dob': datetime.date(2022, 12, 31), 'name': 'Squeaky'}]
```

```py
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

    # take a dictionary of deserialized data and return a model instance
    @post_load
    def make_dog(self, data, **kwargs):
        return Dog(**data)

# deserialize to a class instance by defining a @post_load method in the schema

dog_schema = DogSchema()
dog_json = '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog = dog_schema.loads(dog_json)
print(type(dog))             # => <class 'dict'>
print(isinstance(dog, Dog))  # => True
pprint(dog)                  # => <models.Dog object at 0x102c28d90>

# call instance methods to change object state, deserialize to JSON using dumps()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
dog.scold()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": false}'
dog.give_treat()
pprint(dog_schema.dumps(dog))   # => '{"name": "Snuggles", "breed": "Beagle", "tail_wagging": true}'
```

```py
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
```

```py
# lib/custom_field.py

from marshmallow import Schema, fields, post_load
from datetime import date
from pprint import pprint

# model

class Cat:
    def __init__(self, name, dob, favorite_toys = []):
        self.name = name
        self.dob = dob
        self.favorite_toys = favorite_toys

# schema

class CatSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "Name is required."})
    dob = fields.Date(format="%Y-%m-%d")
    favorite_toys = fields.List(fields.Str())
    likes_toys = fields.Function(lambda obj : len(obj.favorite_toys) > 0, dump_only = True)
    age = fields.Method("calculate_age", dump_only = True)

    def calculate_age(self, obj):
        today = date.today()
        return today.year - obj.dob.year - ((today.month, today.day) < (obj.dob.month, obj.dob.day))

    @post_load
    def make_cat(self, data, **kwargs):
        return Cat(**data)

schema = CatSchema()

#deserialize
cat_1 = schema.load({"name": "Meowie", "dob": "2020-11-28", "favorite_toys": ["ball", "squeaky mouse"]})
cat_2 = schema.load({"name": "Whiskers", "dob": "2015-4-15", "favorite_toys": []})

#serialize
pprint(schema.dump(cat_1))
# => {'age': 2,
# =>  'dob': '2020-11-28',
# =>  'favorite_toys': ['ball', 'squeaky mouse'],
# =>  'likes_toys': True,
# =>  'name': 'Meowie'}

pprint(schema.dump(cat_2))
# => {'age': 8,
# => 'dob': '2015-04-15',
# => 'favorite_toys': [],
# => 'likes_toys': False,
# => 'name': 'Whiskers'}
```

---

## Resources

- [marshmallow](https://pypi.org/project/marshmallow/)
- [marshmallow quickstart](https://marshmallow.readthedocs.io/en/stable/quickstart.html)
