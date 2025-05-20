from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from bot.db import Task, get_db
from typing_extensions import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


app = FastAPI()


app.mount('/static', StaticFiles(directory='web/static'), name='static')
templates = Jinja2Templates(directory='web/templates')


@app.get('/admin/tasks')
async def list_tasks(request: Request, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(
        select(Task)\
        .order_by(Task.user_id)\
        .order_by(Task.created_at)
    )
    tasks = result.scalars().all()
    return templates.TemplateResponse('tasks.html',
                                    {'request': request,
                                    'tasks': tasks})





