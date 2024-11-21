"""Example of Pydantic model with conversion to JSON schema

See: https://docs.pydantic.dev/latest/concepts/json_schema/#generating-json-schema
"""

import json
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.config import ConfigDict


class FooBar(BaseModel):
    count: int
    size: float | None = None


class Gender(str, Enum):
    male = "male"
    female = "female"
    other = "other"
    not_given = "not_given"


class MainModel(BaseModel):
    """
    This is the description of the main model
    """

    model_config = ConfigDict(title="Main")

    foo_bar: FooBar
    gender: Annotated[Gender | None, Field(alias="Gender")] = None
    snap: int = Field(
        default=42,
        title="The Snap",
        description="this is the value of snap",
        gt=30,
        lt=50,
    )


main_model_schema = MainModel.model_json_schema()  # (1)!
print(json.dumps(main_model_schema, indent=2))  # (2)!
