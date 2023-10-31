import typing

import pydantic


class CreateAdv(pydantic.BaseModel):
    heading: str
    description: str
    creator: str


class UpdateAdv(pydantic.BaseModel):
    heading: typing.Optional[str]
    description: typing.Optional[str]


