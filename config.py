from fastapi import FastAPI
from api import users, tasks


app = FastAPI()


app.include_router(users.router, tags=['Users'])
app.include_router(tasks.router, tags=['Tasks'])