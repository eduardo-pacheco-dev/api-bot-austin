from sqlalchemy.orm import Session
from typing import Optional

from app.repositories.ndpd_log_repository import NdpdLogRepository
from app.schemas.ndpd_log import NdpdLogCreate, NdpdLogUpdate
from app.models.ndpd_log import NdpdLog


class NdpdLogService:
    def __init__(self, db: Session):
        self.repository = NdpdLogRepository(db)

    def create(self, ndpd_log: NdpdLogCreate) -> NdpdLog:
        return self.repository.create(ndpd_log)

    def get(self, log_id: int) -> Optional[NdpdLog]:
        return self.repository.get(log_id)

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        analysis_type: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[NdpdLog], int]:
        filters = {}
        if status:
            filters["status"] = status
        if analysis_type:
            filters["analysis_type"] = analysis_type
        if user_id:
            filters["user_id"] = user_id
        return self.repository.get_multi(skip=skip, limit=limit, **filters)

    def update(self, log_id: int, ndpd_log_update: NdpdLogUpdate) -> Optional[NdpdLog]:
        return self.repository.update(log_id, ndpd_log_update)

    def delete(self, log_id: int) -> bool:
        return self.repository.delete(log_id)
