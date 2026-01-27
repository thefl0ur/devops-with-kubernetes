from typing import TYPE_CHECKING

from tortoise.contrib.pydantic import PydanticModel, pydantic_model_creator

from todo_backend.models import TodoModel


if TYPE_CHECKING:  # pragma: nocoverage

    class TodoSchema(TodoModel, PydanticModel):  # type:ignore[misc]
        pass
else:
    TodoSchema = pydantic_model_creator(TodoModel, name="TodoSchema")
