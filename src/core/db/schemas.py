from datetime import datetime
from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel
from sqlmodel import SQLModel

T = TypeVar("T")


class PaginatedList(GenericModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int


class PaginationBuilder:
    @staticmethod
    def build(
        *,
        items: List[T],
        total: int,
        page: int,
        size: int,
    ) -> PaginatedList[T]:
        return PaginatedList[T](
            items=items,
            total=total,
            page=page,
            size=size,
        )


class PageParams(BaseModel):
    # lets FastAPI read it from query params via Depends(PageParams)
    model_config = ConfigDict(from_attributes=True)

    page: int = Query(1, ge=1, description="Page number (1-based)")
    size: int = Query(10, ge=1, le=100, description="Page size (max 100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


class BaseQueryParams(SQLModel):
    valid_at: datetime | None = Query(
        None, description="Filter records valid at this datetime"
    )
    sort: list[str] | None = Query(
        None,
        description="List of fields to sort by, prefix with '-' for descending (e.g. ['name', '-created_at'])",
    )
