from pydantic import BaseModel, ValidationError
from errors import HttpException


class CreateAd(BaseModel):
    title: str
    description: str


def validate_create_ad(json_data):
    try:
        schema = CreateAd(**json_data)
        return schema.dict()
    except ValidationError as error:
        print(error.errors())
        raise HttpException(status_code=400, message=error.errors())


class CreateOwner(BaseModel):
    name: str


def validate_create_owner(json_data):
    try:
        schema = CreateOwner(**json_data)
        return schema.dict()
    except ValidationError as error:
        print(error.errors())
        raise HttpException(status_code=400, message=error.errors())
