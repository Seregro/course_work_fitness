from sqlalchemy import select
from app.models.profiles import Client

@app.get("/clients")
async def clients_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Client).join(User))
    clients = result.scalars().all()
    
    return templates.TemplateResponse("clients.html", {
        "request": request,
        "clients": clients
    })