"""
This module contains the custom types for the application.
"""
import datetime
from typing import Annotated, List, Type, TypeVar, Union

from pydantic import BaseModel, BeforeValidator, RootModel

Number = Union[int, float]
OpStr = Union[str, None]
OpInt = Union[int, None]
OpFloat = Union[float, None]
OpNumber = Union[int, float, None]
OpList = Union[list, None]


def coerce_dt_or_dttm_to_str(data: datetime.date | datetime.datetime | str | None) -> str | None:
    if isinstance(data, datetime.date):
        return str(data)
    if isinstance(data, datetime.datetime):
        return data.isoformat()
    return data


def coerce_number_to_str(data: int | float | None) -> str | None:
    if isinstance(data, (int, float)):
        return str(data)
    return data


def coerce_bytes_to_str(data: bytes | None) -> str | None:
    if isinstance(data, bytes):
        return str(data)
    return data


OpCoercedBytes = Annotated[str | None, BeforeValidator(coerce_bytes_to_str)]
OpCoercedStr = Annotated[str | int | float | None, BeforeValidator(coerce_dt_or_dttm_to_str)]
CoercedDtOrDttm = Annotated[str | datetime.date | datetime.datetime, BeforeValidator(coerce_dt_or_dttm_to_str)]
OpCoercedDtOrDttm = CoercedDtOrDttm | None


T = TypeVar("T", bound=BaseModel)


def create_batch_model(base_model: Type[T]) -> Type[BaseModel]:
    coerced_row = Annotated[base_model, BeforeValidator(lambda row: dict(row))]  # type: ignore  #(figure out why)

    class BatchModel(RootModel):
        root: List[coerced_row]

        def __iter__(self):
            return iter(self.root)

        def __len__(self):
            return len(self.root)

        def __getitem__(self, item):
            return self.root[item]

        class Config:
            arbitrary_types_allowed = True
            populate_by_name = True
            json_encoders = {
                datetime.datetime: lambda dt: dt.isoformat(),
            }

    return BatchModel
