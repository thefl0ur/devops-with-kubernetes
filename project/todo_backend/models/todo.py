from tortoise import fields
from tortoise.models import Model


class TodoModel(Model):
    class Meta:
        table = "todo"

    id = fields.IntField(primary_key=True)
    text: str = fields.CharField(max_length=255)
    is_complete: bool = fields.BooleanField(default=False)
