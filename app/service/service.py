from fastapi import Depends
from service.services import (
    DogService,
    DogWalkerService,
    OrderService,
    BaseService,
)
from database.abstract_database import AbstractDatabase
from database.tortoise_db import (
    get_dog_database,
    get_walker_database,
    get_order_database,
)


def get_dog_service(
    db: AbstractDatabase = Depends(get_dog_database),
) -> BaseService:
    """
    Provides an instance of DogService using the specified database dependency.

    Args:
        db (AbstractDatabase): The database instance for dog-related operations,
        resolved via dependency injection.

    Returns:
        BaseService: An instance of DogService initialized with the provided database.
    """
    return DogService(db)


def get_dog_walker_service(
    db: AbstractDatabase = Depends(get_walker_database),
) -> BaseService:
    """
    Provides an instance of DogWalkerService using the specified database dependency.

    Args:
        db (AbstractDatabase): The database instance for dog walker-related operations,
        resolved via dependency injection.

    Returns:
        BaseService: An instance of DogWalkerService initialized with the provided database.
    """
    return DogWalkerService(db)


def get_order_service(
    db: AbstractDatabase = Depends(get_order_database),
) -> BaseService:
    """
    Provides an instance of OrderService using the specified database dependency.

    Args:
        db (AbstractDatabase): The database instance for order-related operations,
        resolved via dependency injection.

    Returns:
        BaseService: An instance of OrderService initialized with the provided database.
    """
    return OrderService(db)
