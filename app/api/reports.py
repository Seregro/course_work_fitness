from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from app.services.export_service import export_visits_report
from app.api.deps import RoleChecker
from app.models.user import UserRole

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/visits")
async def get_report(
    format: str = Query(..., regex="^(json|csv|xlsx)$"),
    db: AsyncSession = Depends(get_db),
    _ = Depends(RoleChecker([UserRole.ADMIN, UserRole.STAFF]))
):
    content, media_type = await export_visits_report(db, format)
    return Response(content=content, media_type=media_type)