import uuid

from faker import Faker
from api.v1.order.models import OrderStatus

fake = Faker(locale="ru")

fake_order_data = []

basic_response = {
    "page_number": 1,
    "size": 10,
    "total_pages": 0,
    "total_result": 0,
    "result": [],
}
fake_incorrect_order_data: dict = {
    "1": {
        "status": OrderStatus.planned.value,
        "walk_at": "2024-02-12 10:00:00",
    },
    "2": {
        "status": OrderStatus.planned.value,
        "walk_at": "3030-02-12 05:00:00",
    },
    "3": {
        "status": OrderStatus.planned.value,
        "walk_at": "3030-02-12 23:00:00",
    },
    "4": {
        "status": 125,
        "walk_at": "3024-02-12 17:00:00",
    },
    "5": {
        "status": OrderStatus.planned.value,
        "walk_at": "3030-02-12 17:25:00",
    },
    "6": {
        "status": OrderStatus.planned.value,
        "walk_at": "3030-02-12 17:30:00",
    },
}
for row in fake_incorrect_order_data.values():
    row["dog"] = str(uuid.uuid4())
    row["walker"] = str(uuid.uuid4())

for num in range(1, 4):
    fake_order_data.append(
        {
            "dog": None,
            "walker": None,
            "status": OrderStatus.planned.value,
            "walk_at": "2030-0{}-12 21:30:10.820691".format(num),
        },
    )
