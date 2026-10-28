from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, Any

from app.interfaces.repository import BaseRepository
from app.models.ndpd_log import NdpdLog
from app.schemas.ndpd_log import NdpdLogCreate, NdpdLogUpdate


class NdpdLogRepository(BaseRepository[NdpdLog, NdpdLogCreate, NdpdLogUpdate]):
    def __init__(self, db: Session):
        self.db = db

    def create(self, obj_in: NdpdLogCreate) -> NdpdLog:
        db_obj = NdpdLog(**obj_in.model_dump())
        self.db.add(db_obj)
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def get(self, id: int) -> Optional[NdpdLog]:
        return self.db.query(NdpdLog).filter(NdpdLog.id == id).first()

    def get_multi(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> tuple[list[NdpdLog], int]:
        query = self.db.query(NdpdLog)
        
        if filters.get("status"):
            query = query.filter(NdpdLog.status == filters["status"])
        if filters.get("analysis_type"):
            query = query.filter(NdpdLog.analysis_type == filters["analysis_type"])
        if filters.get("user_id"):
            query = query.filter(NdpdLog.user_id == filters["user_id"])
        
        total = query.count()
        items = query.order_by(desc(NdpdLog.created_at)).offset(skip).limit(limit).all()
        return items, total

    def update(self, id: int, obj_in: NdpdLogUpdate) -> Optional[NdpdLog]:
        db_obj = self.db.query(NdpdLog).filter(NdpdLog.id == id).first()
        if not db_obj:
            return None
        
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        self.db.commit()
        self.db.refresh(db_obj)
        return db_obj

    def delete(self, id: int) -> bool:
        db_obj = self.db.query(NdpdLog).filter(NdpdLog.id == id).first()
        if not db_obj:
            return False
        
        self.db.delete(db_obj)
        self.db.commit()
        return True
