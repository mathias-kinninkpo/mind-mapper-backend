from bson import ObjectId
from pydantic import BaseModel, Field, root_validator, ValidationError
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValidationError(f'Invalid ObjectId: {v}')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        field_schema = handler(core_schema)
        field_schema.update(type='string')
        return field_schema
