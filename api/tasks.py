from fastapi import APIRouter
from dependecies import SessionDep
from schemas.tasks import TaskCreate


router = APIRouter(prefix="/tasks")


@router.post('/create')
async def create_task(task_data: TaskCreate, session: SessionDep):
    pass