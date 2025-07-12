# tests/unit/test_task_repo.py
import pytest
from app.crud.task import TaskRepository
from app.schemas.task import TaskCreate
from app.models.task import Task

@pytest.mark.asyncio
async def test_create_and_get_all(db_session):
    repo = TaskRepository(db_session)
    # создаём задачу
    t_in = TaskCreate(title="foo", description="bar")
    task = await repo.create(t_in, user_id=1)
    assert isinstance(task, Task)
    # получаем список
    tasks = await repo.get_all(user_id=1)
    assert len(tasks) == 1
    assert tasks[0].title == "foo"
