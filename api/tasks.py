from fastapi import APIRouter, Depends, HTTPException, status
from dependecies import SessionDep
from schemas.tasks import TaskCreate, TaskRead
from core.jwt_auth import JWTBearer, decode_jwt
from sqlmodel import select
from models.tasks import Task
from models.users import User


router = APIRouter(prefix="/tasks")


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=TaskRead)
async def create_task(task_data: TaskCreate, session: SessionDep, toekn=Depends(JWTBearer())):
    t = decode_jwt(toekn.credentials)
    result = await session.exec(select(User).where(User.id==t['identifier']['id']))
    user_instance = result.first()
    if not user_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
    task = Task(
        title=task_data.title,
        description=task_data.description,
        deadline=task_data.deadline,
        user=user_instance
    )
    task.user = user_instance
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


@router.put('/update/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskRead)
async def update_task(task_data: TaskCreate, task_id, session: SessionDep, token=Depends(JWTBearer())):
    t = decode_jwt(token.credentials)
    user_instance = await session.exec(select(User).where(User.id==t['identifier']['id']))
    user_instance = user_instance.first()
    task_instance = await session.get(Task, task_id)

    if task_instance.user_id != user_instance.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not owner of this task.")
    task_update_data = Task.model_dump(task_data, exclude_unset=True)
    task_instance.sqlmodel_update(task_update_data)

    session.add(task_instance)
    await session.commit()
    await session.refresh(task_instance)
    return task_instance