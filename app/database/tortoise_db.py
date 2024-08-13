from uuid import UUID
from fastapi.exceptions import HTTPException
from fastapi import status
from typing import Type, Generic, TypeVar
from database.abstract_database import (
    AbstractDatabase,
)
from database import models
from tortoise import exceptions as tort_exc
from tortoise import Model
from tortoise.queryset import QuerySet
from tortoise.contrib.pydantic import (
    pydantic_model_creator,
    pydantic_queryset_creator,
    PydanticListModel,
)
from pydantic import BaseModel
from functools import wraps
from api.v1.order.models import OrderUpdateModel

ModelType = TypeVar("ModelType", bound=Model)


def _exists(func):
    """
    Decorator that wraps a database operation function to handle exceptions.

    If a record does not exist or there is an integrity error, the decorator will catch
    the exception and raise an appropriate HTTPException.

    Args:
        func: The function to be wrapped.

    Returns:
        The wrapped function result if no exceptions are raised.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except tort_exc.DoesNotExist as ex:
            table = "Record"
            if ex.model and hasattr(ex.model, "Meta") and hasattr(ex.model.Meta, "table"):
                table = ex.model.Meta.table[:-1].title().replace("_", " ")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{table} with such id does not exist".format(table=table),
            )
        except tort_exc.IntegrityError as ie:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"IntegrityError: {ie}",
            )

    return wrapper


class DogDatabase(AbstractDatabase, Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the database instance with a specific Tortoise ORM model.

        Args:
            model (Type[TM]): The Tortoise ORM model class to use for database operations.
        """
        self._model = model
        self._pydantic = pydantic_model_creator(model)
        self._pydantic_list = pydantic_queryset_creator(model)

    async def fetch_all_data(
        self,
        page: int,
        size: int,
    ) -> dict[str, list[ModelType] | int]:
        """
        Fetch all rows from the database with pagination.

        Args:
            page (int): The page number to retrieve.
            size (int): The number of rows per page.

        Returns:
            dict[str, list[TT] | int]: A dictionary containing pagination information and a list of rows.
        """
        total_count: int = await self._model.all().count()
        total_pages: int = (total_count + size - 1) // size
        offset: int = (page - 1) * size
        queryset: QuerySet = self._model.all().offset(offset).limit(size)
        instances: PydanticListModel = await self._pydantic_list.from_queryset(queryset)
        return {
            "page_number": page,
            "size": size,
            "total_pages": total_pages,
            "total_result": total_count,
            "result": instances.model_dump(),
        }

    @_exists
    async def fetch_single_row(self, row_id: UUID) -> ModelType:
        """
        Fetch a single row from the database by its ID.

        Args:
            row_id (UUID): The unique identifier of the row.

        Returns:
            TM: The row matching the given ID.
        """
        return await self._model.get(id=row_id)

    async def insert_row(self, instance: BaseModel) -> UUID:
        """
        Insert a new row into the database.

        Args:
            instance (TT): The data for the new row.

        Returns:
            UUID: The unique identifier of the newly inserted row.
        """
        row: ModelType = await self._model.create(**instance.model_dump())
        await row.save()
        return row.id  # type: ignore[attr-defined]

    @_exists
    async def update_row(self, row_id: UUID, instance: BaseModel) -> None:
        """
        Update an existing row in the database.

        Args:
            row_id (UUID): The unique identifier of the row to update.
            instance (TT): The updated data for the row.
        """
        row: ModelType = await self._model.get(id=row_id)
        await row.update_from_dict(instance.model_dump())
        await row.save()

    @_exists
    async def delete_row(self, row_id: UUID) -> None:
        """
        Delete a row from the database by its ID.

        Args:
            row_id (UUID): The unique identifier of the row to delete.
        """
        row: ModelType = await self._model.get(id=row_id)
        await row.delete()


class DogWalkerDatabase(DogDatabase, Generic[ModelType]):
    pass


class OrderDatabase(DogDatabase, Generic[ModelType]):
    @_exists
    async def insert_row(self, instance: OrderUpdateModel) -> UUID:
        """
        Insert a new row into the database.

        Args:
            instance (TT): The data for the new row.

        Returns:
            UUID: The unique identifier of the newly inserted row.
        """
        dog: models.DogTable = await models.DogTable.get(id=instance.dog)
        walker: models.DogWalkerTable = await models.DogWalkerTable.get(
            id=instance.walker,
        )
        row: ModelType = await self._model.create(
            dog=dog,
            walker=walker,
            **instance.model_dump(exclude={"dog", "walker"}),
        )
        await row.save()
        return row.id  # type: ignore[attr-defined]

    @_exists
    async def update_row(
        self,
        row_id: UUID,
        instance: OrderUpdateModel,
    ) -> None:
        """
        Update an existing row in the database.

        Args:
            row_id (UUID): The unique identifier of the row to update.
            instance (TT): The updated data for the row.
        """
        row: ModelType = await self._model.get(id=row_id)
        dog: models.DogTable = await models.DogTable.get(id=instance.dog)
        walker: models.DogWalkerTable = await models.DogWalkerTable.get(
            id=instance.walker,
        )
        dict_for_update = instance.model_dump(exclude={"dog", "walker"})
        dict_for_update["dog"] = dog
        dict_for_update["walker"] = walker
        row.update_from_dict(dict_for_update)
        await row.save()


async def get_dog_database() -> AbstractDatabase:
    """
    Dependency to provide an instance of DogDatabase.

    Returns:
        AbstractDatabase: An instance of DogDatabase.
    """
    return DogDatabase[models.DogTable](models.DogTable)


async def get_walker_database() -> AbstractDatabase:
    """
    Dependency to provide an instance of DogWalkerDatabase.

    Returns:
        AbstractDatabase: An instance of DogWalkerDatabase.
    """
    return DogWalkerDatabase[models.DogWalkerTable](models.DogWalkerTable)


async def get_order_database() -> AbstractDatabase:
    """
    Dependency to provide an instance of OrderDatabase.

    Returns:
        AbstractDatabase: An instance of OrderDatabase.
    """
    return OrderDatabase[models.OrderTable](models.OrderTable)
