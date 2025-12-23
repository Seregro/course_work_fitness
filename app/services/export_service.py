import pandas as pd
import json
from io import BytesIO, StringIO
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.visit_log import VisitLog

async def export_visits_report(db: AsyncSession, format: str):
    result = await db.execute(select(VisitLog))
    visits = result.scalars().all()
    
    data = [
        {"id": v.id, "client_id": v.client_id, "check_in": str(v.check_in), "check_out": str(v.check_out)} 
        for v in visits
    ]
    
    if format == "json":
        return json.dumps(data, indent=4), "application/json"
    
    df = pd.DataFrame(data)
    if format == "csv":
        output = StringIO()
        df.to_csv(output, index=False)
        return output.getvalue(), "text/csv"
    
    if format == "xlsx":
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue(), "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"