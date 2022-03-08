from flask_marshmallow import Marshmallow

marshmallow_obj = Marshmallow()


'''
Schema - The main component of Marshmallow is a Schema. 
A schema defines the rules that guides deserialization, called load, 
and serialization, called dump.

Serialization (Schema.dump()) - Serialize objects by passing them to your schema’s dump method, 
which returns the formatted result (here, JSON). Used for responding a user with an api.
To serialize, we converted data from Python to JSON.

Deserialization (Schema.load()) - Opposite of serialization. To deserialize, we are converting JSON data to SQLAlchemy objects. 
When deserializing objects from the SQLite database, Marshmallow automatically converts the serialized data to a native Python object.
Used to post a json payload to a respective resource.

As a nice alternative to reqparse, schema.load() raises a ValidationError error when invalid data are passed in. 
To access the dictionary of val errors use ValidationError.messages attr.

Fields - simply attributes/ columns in our database.

p.s - these notes are taken from marshmallow documentation. IT'S AWESOME!
'''