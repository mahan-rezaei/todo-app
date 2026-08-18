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


@router.get('/list', status_code=status.HTTP_200_OK, response_model=list[TaskRead])
async def tasks_list(session: SessionDep):
    tasks = await session.exec(select(Task))
    return tasks


@router.get('/user-list', status_code=status.HTTP_200_OK, response_model=list[TaskRead])
async def user_tasks_list(session: SessionDep, token=Depends(JWTBearer())):
    t = decode_jwt(token.credentials)
    user_tasks = await session.exec(select(Task).where(Task.user_id==t['identifier']['id']))
    return user_tasks


@router.put('/update/{task_id}', status_code=status.HTTP_200_OK, response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate, session: SessionDep, token=Depends(JWTBearer())):
    t = decode_jwt(token.credentials)
    user_instance = await session.exec(select(User).where(User.id==t['identifier']['id']))
    user_instance = user_instance.first()
    task_instance = await session.get(Task, task_id)

    if task_instance.user_id != user_instance.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not owner of this task.")
    task_update_data = task_data.model_dump(exclude_unset=True)
    task_instance.sqlmodel_update(task_update_data)

    session.add(task_instance)
    await session.commit()
    await session.refresh(task_instance)
    return task_instance


@router.delete('/delete/{task_id}', status_code=status.HTTP_200_OK)
async def delete_task(task_id: int, session: SessionDep, token=Depends(JWTBearer())):
    t = decode_jwt(token.credentials)
    result = await session.exec(select(Task).where(Task.id==task_id, Task.user_id==t['identifier']['id']))
    task = result.first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="task not found.")
    await session.delete(task)
    await session.commit()
    return {'detail': "task deleted successfully."}

    

@router.get('/finish/{task_id}', status_code=status.HTTP_200_OK)
async def finish_task(task_id: int, session: SessionDep, token=Depends(JWTBearer())):
    pass