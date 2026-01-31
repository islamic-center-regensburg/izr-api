from typing import Generic, List, TypeVar
from fastapi import Query
from pydantic import BaseModel, ConfigDict
from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginationMetadata(BaseModel):
    total: int
    page: int
    size: int


class PaginatedResponse(GenericModel, Generic[T]):
    data: List[T]
    metadata: PaginationMetadata


class PaginationBuilder:
    @staticmethod
    def build(
        *,
        items: List[T],
        total: int,
        page: int,
        size: int,
    ) -> PaginatedResponse[T]:
        return PaginatedResponse[T](
            data=items,
            metadata=PaginationMetadata(
                total=total,
                page=page,
                size=size,
            ),
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
