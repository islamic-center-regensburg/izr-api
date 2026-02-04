import re
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Optional, Type, Union

from sqlalchemy import distinct
from sqlalchemy.sql.functions import func
from sqlmodel import Session, SQLModel, select

from src.core.db.filters import Filter
from src.core.db.order_by import OrderBy
from src.core.exceptions import DoesNotExistInDatabaseException

ResourceId = Union[int, str]


@dataclass
class Join:
    model: Type[SQLModel]
    condition: Any
    filters: list[Filter] = field(default_factory=list)

    def get_valid_filters(self) -> list[Filter]:
        return [f for f in self.filters if f.value is not None]


class DatabaseRepository:
    def __init__(self, db: Session):
        self.__db: Session = db

    def get_session(self):
        return self.__db

    def get_by_id[T: SQLModel](self, model: Type[T], id: ResourceId) -> T:
        record = self.__db.get(model, id)
        if not record:
            raise DoesNotExistInDatabaseException(
                f"Record of {model.__name__} with id {id} does not exist in database."
            )
        return record

    def get_all[T: SQLModel](
        self,
        model: Type[T],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[Union[OrderBy, list[OrderBy]]] = None,
        filters: list[Filter] | None = None,
        **kwargs,
    ) -> list[T]:
        filters = deepcopy(filters)
        if filters is None:
            filters = []
        if order_by is None:
            order_by = []
        elif order_by and not isinstance(order_by, list):
            order_by = [order_by]
        if order_by == [] and (limit or offset):
            order_by = [OrderBy(attribute="id", descending=False)]
        filters += Filter.from_dict(**kwargs)
        select_statement = select(model)
        select_statement = self.__apply_filters(model, filters, select_statement)
        select_statement = self.__order_by(model, select_statement, order_by)
        return list(self.__db.exec(select_statement.offset(offset).limit(limit)).all())

    def count(self, model: Type[SQLModel], filters: list[Filter] | None = None) -> int:
        filters = filters or []
        select_statement = select(func.count()).select_from(model)
        select_statement = self.__apply_filters(model, filters, select_statement)
        return self.__db.exec(select_statement).one()

    def get_last[T: SQLModel](
        self, model: Type[T], filters: list[Filter] | None = None, **kwargs
    ) -> Optional[T]:
        order_by = None
        if hasattr(model, "valid_from"):
            order_by = OrderBy(attribute="valid_from", descending=True)
        elif hasattr(model, "created_at"):
            order_by = OrderBy(attribute="created_at", descending=True)
        elif hasattr(model, "id"):
            order_by = OrderBy(attribute="id", descending=True)
        try:
            return self.get_all(
                model, offset=0, limit=1, order_by=order_by, filters=filters, **kwargs
            )[0]
        except IndexError:
            return None

    def get_valid[T: SQLModel](
        self,
        model: Type[T],
        filters: list[Filter] | None = None,
        **kwargs,
    ) -> T:
        filters = filters or []
        validity_filters: list[Filter] = Filter.get_validity_filters(datetime.now(UTC))
        try:
            records = self.get_all(model, filters=filters + validity_filters, **kwargs)
            if not records:
                raise DoesNotExistInDatabaseException(
                    f"No record of {model.__name__} found on database."
                )
            elif len(records) > 1:
                raise Exception(
                    f"Multiple records of {model.__name__} found on database."
                )
            else:
                return records[0]
        except Exception as e:
            raise e

    @staticmethod
    def __apply_filters(model: Type[SQLModel], filters: list[Filter], select_statement):
        for _filter in filters:
            select_statement = _filter.apply(model, select_statement)
        return select_statement

    @staticmethod
    def __order_by(model: Type[SQLModel], select_statement, order_by: list[OrderBy]):
        if not order_by and hasattr(model, "created_at"):
            order_by = [OrderBy(attribute="created_at")]
        if order_by:
            for ob in order_by:
                match ob.descending:
                    case True:
                        select_statement = select_statement.order_by(
                            getattr(model, ob.attribute).desc()
                        )
                    case False:
                        select_statement = select_statement.order_by(
                            getattr(model, ob.attribute)
                        )
        return select_statement

    def create[T: SQLModel](self, record: T) -> T:
        self.__db.add(record)
        self.__db.commit()
        self.__db.refresh(record)
        return record

    def create_linked_records[T: SQLModel](
        self, record: SQLModel, linked_records: list[T], link_model: Type[SQLModel]
    ) -> list[T]:
        if not (
            getattr(record, "id", None)
            and all(
                getattr(linked_record, "id", None) for linked_record in linked_records
            )
        ):
            raise ValueError("Record and linked records must have an 'id' attribute.")
        record_id = record.id  # pyright: ignore [reportAttributeAccessIssue]
        if not linked_records:
            return []
        for linked_record in linked_records:
            linked_record_id = linked_record.id  # pyright: ignore [reportAttributeAccessIssue]
            try:
                # noinspection PyTypeChecker
                self.get_by_id(linked_records[0].__class__, linked_record_id)
            except DoesNotExistInDatabaseException:
                self.create(linked_record)
            link_record = link_model(
                **{
                    f"{self.__get_record_name(record)}_id": record_id,
                    f"{self.__get_record_name(linked_record)}_id": linked_record_id,
                }
            )
            self.create(link_record)
        return linked_records

    def get_all_linked_to[T: SQLModel](
        self,
        model: Type[T],
        link_model: Type[SQLModel],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        order_by: Optional[Union[OrderBy, list[OrderBy]]] = None,
        model_filters: list[Filter] | None = None,
        link_model_filters: list[Filter] | None = None,
        **kwargs,
    ) -> list[T]:
        if model_filters is None:
            model_filters = []
        if link_model_filters is None:
            link_model_filters = []
        if order_by is None:
            order_by = []
        elif order_by and not isinstance(order_by, list):
            order_by = [order_by]
        model_filters += Filter.from_dict(
            **{attr: kwargs[attr] for attr in kwargs if hasattr(model, attr)}
        )
        link_model_filters += Filter.from_dict(
            **{attr: kwargs[attr] for attr in kwargs if hasattr(link_model, attr)}
        )
        # noinspection PyTypeChecker
        select_statement = select(model).join(
            link_model,
            getattr(model, "id")
            == getattr(link_model, f"{self.get_model_name(model)}_id"),
        )
        select_statement = self.__apply_filters(
            link_model, link_model_filters, select_statement
        )
        select_statement = self.__apply_filters(model, model_filters, select_statement)
        select_statement = self.__order_by(model, select_statement, order_by)
        select_statement = select_statement.distinct()
        return list(self.__db.exec(select_statement.offset(offset).limit(limit)).all())

    @staticmethod
    def __get_record_name(record: SQLModel) -> str:
        pattern = re.compile(r"(?<!^)(?=[A-Z])")
        name = pattern.sub("_", record.__class__.__name__).lower()
        name = name.replace("_table", "")
        return name

    @staticmethod
    def get_model_name(model: Type[SQLModel]) -> str:
        pattern = re.compile(r"(?<!^)(?=[A-Z])")
        name = pattern.sub("_", model.__name__).lower()
        if name.endswith("_table"):
            name = name[:-6]
        return name

    def update[T: SQLModel](self, record: T) -> T:
        try:
            record_id = record.id  # pyright: ignore [reportAttributeAccessIssue]
            # noinspection PyTypeChecker
            existing_record = self.get_by_id(record.__class__, record_id)
        except DoesNotExistInDatabaseException:
            raise DoesNotExistInDatabaseException
        for attribute in record.__dict__:
            if attribute == "id" or attribute.startswith("_"):
                continue
            setattr(existing_record, attribute, getattr(record, attribute))
        self.create(existing_record)
        return existing_record

    def delete(self, model: Type[SQLModel], id: ResourceId) -> None:
        try:
            self.__db.delete(self.get_by_id(model, id))
        except DoesNotExistInDatabaseException:
            raise DoesNotExistInDatabaseException
        self.__db.commit()

    def delete_all(
        self, model: Type[SQLModel], filters: list[Filter] | None = None, **kwargs
    ):
        if filters is None:
            filters = []
        filters += Filter.from_dict(**kwargs)
        select_statement = select(model)
        select_statement = self.__apply_filters(model, filters, select_statement)
        records = self.__db.exec(select_statement).all()
        for record in records:
            self.__db.delete(record)
        self.__db.commit()

    def get_with_join[T: SQLModel](
        self,
        model: type[T],
        joins: list[Join],
        filters: list[Filter] | None = None,
        offset: int | None = None,
        limit: int | None = None,
        order_by: OrderBy | list[OrderBy] | None = None,
        *,
        distinct: bool = False,
    ) -> list[T]:
        filters = filters or []
        order_by = order_by or []
        if order_by and not isinstance(order_by, list):
            order_by = [order_by]
        if order_by == [] and (limit or offset):
            order_by = [OrderBy(attribute="id", descending=False)]

        filters = [f for f in filters if f.value is not None]
        select_statement = select(model)
        for join in joins:
            select_statement = select_statement.join(join.model, join.condition)
            select_statement = self.__apply_filters(
                join.model, join.get_valid_filters(), select_statement
            )
        select_statement = self.__apply_filters(model, filters, select_statement)
        select_statement = self.__order_by(model, select_statement, order_by)

        if distinct:
            select_statement = select_statement.distinct()

        return list(self.__db.exec(select_statement.offset(offset).limit(limit)).all())

    def count_with_join[T: SQLModel](
        self, model: type[T], joins: list[Join], filters: list[Filter] | None = None
    ) -> int:
        if not hasattr(model, "id"):
            raise ValueError(
                f"Model {model.__name__} must have an 'id' attribute for counting."
            )

        filters = filters or []
        filters = [f for f in filters if f.value is not None]

        select_statement = select(func.count(distinct(model.id))).select_from(model)  # pyright: ignore [reportAttributeAccessIssue]
        for join in joins:
            select_statement = select_statement.join(join.model, join.condition)
            select_statement = self.__apply_filters(
                join.model, join.get_valid_filters(), select_statement
            )
        select_statement = self.__apply_filters(model, filters, select_statement)

        return self.__db.exec(select_statement).one()
