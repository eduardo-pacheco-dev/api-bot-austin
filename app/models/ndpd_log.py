from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func

from app.db.base_class import Base


class NdpdLog(Base):
    __tablename__ = "ndpd_logs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    analysis_type = Column(String(100), nullable=False, index=True)
    input_data = Column(JSON, nullable=True)
    result_data = Column(JSON, nullable=True)
    status = Column(String(50), nullable=False, default="pending", index=True)
    user_id = Column(String(100), nullable=True, index=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
