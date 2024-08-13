from enum import Enum

from tortoise import fields
from tortoise.models import Model


CHAR_FIELD_LEN = 50


class IDModel(Model):
    id = fields.UUIDField(primary_key=True)

    class Meta:
        abstract = True


class DateTimeModel(Model):
    created = fields.DatetimeField(auto_now_add=True, null=False)
    updated = fields.DatetimeField(auto_now=True, null=False)

    class Meta:
        abstract = True


class DogTable(IDModel, DateTimeModel):
    apartment = fields.IntField(null=False)
    name = fields.CharField(max_length=CHAR_FIELD_LEN, null=False)
    breed = fields.CharField(
        max_length=CHAR_FIELD_LEN,
        null=False,
        default="",
    )
    active = fields.BooleanField(default=True, null=False)

    class Meta:
        ordering = ["name", "breed"]
        table = "dogs"

    def __str__(self):
        return f"{self.name} - {self.breed}"


class DogWalkerTable(IDModel, DateTimeModel):
    name = fields.CharField(max_length=CHAR_FIELD_LEN, null=False)
    surname = fields.CharField(max_length=CHAR_FIELD_LEN, null=False)
    active = fields.BooleanField(default=True, null=False)

    class Meta:
        ordering = ["active", "name"]
        table = "dog_walkers"

    def __str__(self):
        return f"{self.name} {self.surname}"


class OrderStatus(Enum):
    planned = "Запланирована"
    in_progress = "В процессе"
    success = "Завершена"
    cancel = "Отменена"


class OrderTable(IDModel, DateTimeModel):
    walk_at = fields.DatetimeField(null=False)
    dog: fields.ForeignKeyRelation[DogTable] | None = fields.ForeignKeyField(
        "models.DogTable",
        related_name="orders",
        on_delete=fields.SET_NULL,
        null=True,
    )
    walker: fields.ForeignKeyRelation[DogWalkerTable] | None = fields.ForeignKeyField(
        "models.DogWalkerTable",
        related_name="orders",
        on_delete=fields.SET_NULL,
        null=True,
    )
    status = fields.CharEnumField(
        OrderStatus,
        null=False,
        default=OrderStatus.planned,
    )

    class Meta:
        ordering = ["walk_at"]
        table = "orders"
        unique_together = (
            ("walk_at", "walker"),
            ("walk_at", "dog"),
        )

    def __str__(self):
        return f"{self.walk_at} {self.walker}, {self.dog}"
