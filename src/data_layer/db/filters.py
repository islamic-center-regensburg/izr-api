from datetime import datetime
from enum import Enum, auto
from typing import Union, Type

from sqlmodel import SQLModel, col

from src.logger.logger import logger


class Operator(Enum):
    EQ = auto()
    IN = auto()
    GT = auto()
    GE = auto()
    LT = auto()
    LE = auto()
    NE = auto()
    CONTAINS = auto()


ValueType = Union[str, list[str], int, list[int], datetime, list[datetime], Enum]


class Filter:
    def __init__(self, attribute: str, operator: Operator, value: ValueType):
        self.attribute: str = attribute
        self.operator: Operator = operator
        self.value = value

    def apply(self, model: Type[SQLModel], select_statement):
        if not hasattr(model, self.attribute):
            logger.error(
                f"Attribute {self.attribute} does not exist in {model.__name__}. Returning select statement."
            )
            return select_statement
        if self.value is None:
            return select_statement
        match self.operator:
            case Operator.EQ:
                return select_statement.where(
                    getattr(model, self.attribute) == self.value
                )
            case Operator.IN:
                return select_statement.where(
                    col(getattr(model, self.attribute)).in_(self.value)
                )
            case Operator.GT:
                return select_statement.where(
                    getattr(model, self.attribute) > self.value
                )
            case Operator.GE:
                return select_statement.where(
                    getattr(model, self.attribute) >= self.value
                )
            case Operator.LT:
                return select_statement.where(
                    getattr(model, self.attribute) < self.value
                )
            case Operator.LE:
                return select_statement.where(
                    getattr(model, self.attribute) <= self.value
                )
            case Operator.NE:
                return select_statement.where(
                    getattr(model, self.attribute) != self.value
                )
            case Operator.CONTAINS:
                return select_statement.where(
                    getattr(model, self.attribute).icontains(self.value)
                )
            case _:
                logger.error(
                    f"Invalid operator: {self.operator}. Returning select statement without filter."
                )
                return select_statement

    @staticmethod
    def from_dict(**kwargs) -> list["Filter"]:
        return [Filter(key, Operator.EQ, kwargs[key]) for key in kwargs]

    @staticmethod
    def get_validity_filters(valid_at: datetime | None) -> list["Filter"]:
        if not valid_at:
            return []
        # Right at the moment of invalidation, the record is still valid, so that we can read all related records that
        # have been valid just before the invalidation. Thus, valid_from < valid_at <= valid_to:
        return [
            Filter(attribute="valid_from", operator=Operator.LT, value=valid_at),
            Filter(attribute="valid_to", operator=Operator.GE, value=valid_at),
        ]
