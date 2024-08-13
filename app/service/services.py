from uuid import UUID

from api.v1.dog.models import DogModel
from api.v1.order.models import OrderReturnModel
from api.v1.walker.models import DogWalkerModel
from typing import Generic, TypeVar
from database.models import (
    DogTable,
    DogWalkerTable,
    OrderTable,
)
from database.abstract_database import (
    AbstractDatabase,
)
from models.paginated_params import (
    PaginatedParams,
)
from tortoise import Model
from pydantic import BaseModel


TModel = TypeVar("TModel", bound=BaseModel)
TTable = TypeVar("TTable", bound=Model)


class BaseService(Generic[TModel, TTable]):
    """
    A base service class that provides standard CRUD operations for a given model and database.

    Attributes:
        _database (AbstractDatabase): The database instance used for data operations.
    """

    def __init__(self, database: AbstractDatabase):
        """
        Initializes the BaseService with a specific database instance.

        Args:
            database (AbstractDatabase): The database instance to use for data operations.
        """
        self._database = database

    async def get_all(
        self,
        query_params: PaginatedParams,
    ) -> dict[str, list[TTable] | int]:
        """
        Retrieve all records with pagination.

        Args:
            query_params (PaginatedParams): The pagination parameters (page number and size).

        Returns:
            Dict[str, List[TTable] | int]: A dictionary containing the paginated results and metadata.
        """
        return await self._database.fetch_all_data(
            page=query_params.page,
            size=query_params.size,
        )

    async def get_single(self, row_id: UUID) -> TTable:
        """
        Retrieve a single record by its unique identifier.

        Args:
            row_id (UUID): The unique identifier of the record.

        Returns:
            TTable: The record matching the provided ID.
        """
        return await self._database.fetch_single_row(row_id=row_id)

    async def create(self, instance: TModel) -> dict[str, UUID]:
        """
        Create a new record in the database.

        Args:
            instance (TModel): The data to be inserted as a new record.

        Returns:
            Dict[str, UUID]: A dictionary containing the unique identifier of the newly created record.
        """
        instance_id: UUID = await self._database.insert_row(instance)
        return {"id": instance_id}

    async def update(self, row_id: UUID, new_instance: TModel) -> None:
        """
        Update an existing record in the database.

        Args:
            row_id (UUID): The unique identifier of the record to be updated.
            new_instance (TModel): The new data to update the record with.

        Returns:
            None
        """
        await self._database.update_row(row_id=row_id, instance=new_instance)

    async def delete(self, row_id: UUID) -> None:
        """
        Delete a record from the database by its unique identifier.

        Args:
            row_id (UUID): The unique identifier of the record to be deleted.

        Returns:
            None
        """
        await self._database.delete_row(row_id=row_id)


class DogService(BaseService[DogModel, DogTable]):
    """
    A service class for managing dog-related operations.
    Inherits standard CRUD operations from BaseService.
    """

    pass


class DogWalkerService(BaseService[DogWalkerModel, DogWalkerTable]):
    """
    A service class for managing dog walker-related operations.
    Inherits standard CRUD operations from BaseService.
    """

    pass


class OrderService(BaseService[OrderReturnModel, OrderTable]):
    """
    A service class for managing order-related operations.
    Inherits standard CRUD operations from BaseService.
    """

    pass
