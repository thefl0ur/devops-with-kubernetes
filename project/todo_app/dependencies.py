from todo_app.services.todo_backend import TodoBackendService


def get_todo_service() -> TodoBackendService:
    return TodoBackendService()
