import uuid
from fastapi import APIRouter, status, Depends
from api.v1.dog.models import (
    DogReturnModel,
    DogModel,
    IDModel,
)
from database.models import DogTable
from models.paginated_params import (
    PaginatedParams,
    PaginationResponse,
)
from service.service import get_dog_service

dogs_router = APIRouter(prefix="/api/v1/dogs", tags=["dogs"])


@dogs_router.get(
    "/",
    response_model=PaginationResponse,
    status_code=status.HTTP_200_OK,
    description="List of all dogs",
)
async def get_all_dogs(
    service=Depends(get_dog_service),
    query_params: PaginatedParams = Depends(),
) -> dict:
    """
    Retrieve a paginated list of all dogs.

    Args:
        query_params (PaginatedParams): Pagination parameters including page number and page size.
        service (DogService): Dependency for dog-related operations.

    Returns:
        PaginateResponse: A response model containing the list of dogs and pagination information.
    """
    return await service.get_all(query_params)


@dogs_router.get(
    "/{dog_id}/",
    response_model=DogReturnModel,
    status_code=status.HTTP_200_OK,
    description="Read a single dog",
)
async def get_single_dog(
    dog_id: uuid.UUID,
    service=Depends(get_dog_service),
) -> DogTable:
    """
    Retrieve a single dog's details by its ID.

    Args:
        dog_id (uuid.UUID): The unique identifier of the dog.
        service (DogService): Dependency for dog-related operations.

    Returns:
        DogTable: The details of the requested dog.
    """
    return await service.get_single(dog_id)


@dogs_router.post(
    "/",
    response_model=IDModel,
    status_code=status.HTTP_201_CREATED,
    description="Create new dog",
)
async def create_dog(
    dog: DogModel,
    service=Depends(get_dog_service),
) -> dict:
    """
    Create a new dog entry in the database.

    Args:
        dog (Dog): The data for the new dog.
        service (DogService): Dependency for dog-related operations.

    Returns:
        dict: The unique identifier of the newly created dog.
    """
    return await service.create(dog)


@dogs_router.put(
    "/{dog_id}/",
    status_code=status.HTTP_200_OK,
    description="Update dog",
)
async def update_dog(
    dog_id: uuid.UUID,
    dog: DogModel,
    service=Depends(get_dog_service),
):
    """
    Update the details of an existing dog.

    Args:
        dog_id (uuid.UUID): The unique identifier of the dog to be updated.
        dog (Dog): The updated data for the dog.
        service (DogService): Dependency for dog-related operations.

    Returns:
        None: No content is returned.
    """
    return await service.update(row_id=dog_id, new_instance=dog)


@dogs_router.delete(
    "/{dog_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete dog",
)
async def delete_dog(
    dog_id: uuid.UUID,
    service=Depends(get_dog_service),
):
    """
    Delete a dog entry from the database.

    Args:
        dog_id (uuid.UUID): The unique identifier of the dog to be deleted.
        service (DogService): Dependency for dog-related operations.

    Returns:
        None: No content is returned.
    """
    return await service.delete(row_id=dog_id)
