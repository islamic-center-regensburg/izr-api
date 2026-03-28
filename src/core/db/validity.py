from abc import ABC, abstractmethod
from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP
from sqlmodel import Field, SQLModel


class VersionedSQLModel(SQLModel, ABC):
    valid_from: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_type=TIMESTAMP(timezone=True),  # type: ignore[arg-type]
        nullable=False,
        description="Valid from date time in UTC",
    )
    valid_to: datetime = Field(
        default=datetime(9999, 12, 31, tzinfo=UTC),
        sa_type=TIMESTAMP(timezone=True),  # type: ignore[arg-type]
        nullable=False,
        description="Valid to date time in UTC",
    )
    update_reason: str | None = Field(default=None)

    @classmethod
    @abstractmethod
    def get_business_key_fields(cls) -> set[str]:
        pass

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "__abstractmethods__") and not cls.__abstractmethods__:
            invalid = [
                name
                for name in cls.get_business_key_fields()
                if name not in cls.model_fields
            ]
            if invalid:
                msg = (
                    f"Invalid business key fields in class '{cls.__name__}': {invalid}"
                )
                raise ValueError(msg)
