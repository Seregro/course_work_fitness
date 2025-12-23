from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api import auth, reports, gyms, operations

app = FastAPI(title="Fitness Center DBMS")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(gyms.router)
app.include_router(operations.router)
app.include_router(reports.router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Панель управления фитнес-центром"})