import uuid

from fastapi import APIRouter, status, Depends
from api.v1.order.models import (
    OrderReturnModel,
    OrderUpdateModel,
    NewOrder,
)
from models.paginated_params import (
    PaginatedParams,
    PaginationResponse,
)
from service.service import get_order_service

order_router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@order_router.get(
    "/",
    response_model=PaginationResponse,
    status_code=status.HTTP_200_OK,
    description="List of all orders",
)
async def get_orders(
    service=Depends(get_order_service),
    query_params: PaginatedParams = Depends(),
):
    return await service.get_all(query_params)


@order_router.get(
    "/{order_id}/",
    response_model=OrderReturnModel,
    status_code=status.HTTP_200_OK,
    description="Read a single order",
)
async def get_order(
    order_id: uuid.UUID,
    service=Depends(get_order_service),
):
    return await service.get_single(order_id)


@order_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    description="Create new dog walker",
)
async def create_order(
    order: NewOrder,
    service=Depends(get_order_service),
):
    return await service.create(order)


@order_router.put(
    "/{order_id}/",
    status_code=status.HTTP_200_OK,
    description="Update dog walker",
)
async def update_order(
    order_id: uuid.UUID,
    new_order: OrderUpdateModel,
    service=Depends(get_order_service),
):
    return await service.update(row_id=order_id, new_instance=new_order)


@order_router.delete(
    "/{order_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete dog walker",
)
async def delete_order(
    order_id: uuid.UUID,
    service=Depends(get_order_service),
):
    return await service.delete(row_id=order_id)
