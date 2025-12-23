from fastapi import FastAPI
from app.api import auth, reports, views, operations 

app = FastAPI(title="Fitness Pro System")

app.include_router(auth.router)
app.include_router(reports.router)
app.include_router(operations.router)
app.include_router(views.router)