from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional

from app.models.ndpd_log import NdpdLog
from app.schemas.ndpd_log import NdpdLogCreate, NdpdLogUpdate


class NdpdLogCRUD:
    @staticmethod
    def create(db: Session, ndpd_log: NdpdLogCreate) -> NdpdLog:
        db_obj = NdpdLog(**ndpd_log.model_dump())
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def get(db: Session, log_id: int) -> Optional[NdpdLog]:
        return db.query(NdpdLog).filter(NdpdLog.id == log_id).first()

    @staticmethod
    def get_multi(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        analysis_type: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> tuple[list[NdpdLog], int]:
        query = db.query(NdpdLog)
        
        if status:
            query = query.filter(NdpdLog.status == status)
        if analysis_type:
            query = query.filter(NdpdLog.analysis_type == analysis_type)
        if user_id:
            query = query.filter(NdpdLog.user_id == user_id)
        
        total = query.count()
        items = query.order_by(desc(NdpdLog.created_at)).offset(skip).limit(limit).all()
        return items, total

    @staticmethod
    def update(db: Session, log_id: int, ndpd_log_update: NdpdLogUpdate) -> Optional[NdpdLog]:
        db_obj = db.query(NdpdLog).filter(NdpdLog.id == log_id).first()
        if not db_obj:
            return None
        
        update_data = ndpd_log_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @staticmethod
    def delete(db: Session, log_id: int) -> bool:
        db_obj = db.query(NdpdLog).filter(NdpdLog.id == log_id).first()
        if not db_obj:
            return False
        
        db.delete(db_obj)
        db.commit()
        return True
