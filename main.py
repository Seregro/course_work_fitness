from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api import auth, reports

app = FastAPI(title="Fitness Pro System")

templates = Jinja2Templates(directory="templates")

app.include_router(auth.router)
app.include_router(reports.router)

@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})