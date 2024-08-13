from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from uuid import UUID

from tortoise import Model
from tortoise.contrib.pydantic import (
    PydanticModel,
)
from pydantic import BaseModel

TM = TypeVar("TM", bound=Model)
TT = TypeVar("TT", bound=PydanticModel)

ModelType = TypeVar("ModelType")


class AbstractDatabase(Generic[ModelType], ABC):
    @abstractmethod
    async def fetch_all_data(
        self,
        page: int,
        size: int,
    ) -> dict[str, list | int]:
        """
        Fetch all rows from the database with pagination.

        Args:
            page (int): The page number to retrieve.
            size (int): The number of rows per page.

        Returns:
            dict[str, list[TableType] | int]: A dictionary containing pagination information and a list of results.
        """
        raise NotImplementedError

    @abstractmethod
    async def fetch_single_row(self, row_id: UUID) -> ModelType:
        """
        Fetch a single row from the database by its ID.

        Args:
            row_id (UUID): The unique identifier of the row.

        Returns:
            ModelType: The row matching the given ID.

        Raises:
            HTTPException: If the row does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def insert_row(self, instance: BaseModel) -> UUID:
        """
        Insert a new row into the database.

        Args:
            instance (instance_type): The data for the new row.

        Returns:
            UUID: The unique identifier of the newly inserted row.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_row(self, row_id: UUID, instance: BaseModel) -> None:
        """
        Update an existing row in the database.

        Args:
            row_id (UUID): The unique identifier of the row to update.
            instance (instance_type): The updated data for the row.

        Raises:
            HTTPException: If the row does not exist.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_row(self, row_id: UUID) -> None:
        """
        Delete a row from the database by its ID.

        Args:
            row_id (UUID): The unique identifier of the row to delete.

        Raises:
            HTTPException: If the row does not exist.
        """
        raise NotImplementedError
