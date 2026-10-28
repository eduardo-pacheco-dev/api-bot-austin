from fastapi import APIRouter

from app.api.v1 import ndpd_logs

router = APIRouter()
router.include_router(ndpd_logs.router, prefix="/ndpd-logs", tags=["NDPD Logs"])
