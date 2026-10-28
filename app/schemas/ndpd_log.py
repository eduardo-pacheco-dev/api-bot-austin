from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Any


class NdpdLogBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Título do log de análise", example="Análise NDPD #001")
    description: str | None = Field(None, description="Descrição detalhada da análise", example="Análise de padrões de tráfego")
    analysis_type: str = Field(..., min_length=1, max_length=100, description="Tipo de análise", example="traffic_analysis")
    input_data: dict[str, Any] | None = Field(None, description="Dados de entrada para análise")
    result_data: dict[str, Any] | None = Field(None, description="Resultado da análise")
    status: str = Field(default="pending", max_length=50, description="Status da análise", example="completed")
    user_id: str | None = Field(None, max_length=100, description="ID do usuário responsável", example="user_123")
    error_message: str | None = Field(None, description="Mensagem de erro caso falhe")
    
    # NDPD fields
    site_id: str | None = Field(None, max_length=100, description="Site ID", example="SITE-001")
    report: str | None = Field(None, max_length=255, description="Report", example="REL-2026-001")
    oc: str | None = Field(None, max_length=100, description="Ordem Complexa", example="OC-12345")
    so: str | None = Field(None, max_length=100, description="Service Order", example="OS-67890")
    item_name: str | None = Field(None, max_length=255, description="Item name", example="Cabo de rede CAT6")
    quantity_approved: float | None = Field(None, ge=0, description="Approved quantity", example=10.0)
    quantity_pending: float | None = Field(None, ge=0, description="Pending quantity", example=5.0)
    quantity_rejected: float | None = Field(None, ge=0, description="Rejected quantity", example=2.0)
    quantity_total: float | None = Field(None, ge=0, description="Total quantity", example=17.0)
    rejection_reason: str | None = Field(None, description="Rejection reason", example="Not in accordance with specifications")
    event_datetime: datetime | None = Field(None, description="Event datetime")


class NdpdLogCreate(NdpdLogBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "NDPD Analysis #001",
                "description": "Item receipt analysis",
                "analysis_type": "receipt",
                "status": "pending",
                "site_id": "SITE-001",
                "report": "REL-2026-001",
                "oc": "OC-12345",
                "so": "OS-67890",
                "item_name": "Cabo de rede CAT6",
                "quantity_approved": 10.0,
                "quantity_pending": 5.0,
                "quantity_rejected": 2.0,
                "quantity_total": 17.0,
                "rejection_reason": None,
                "event_datetime": "2026-10-28T17:00:00"
            }
        }
    )


class NdpdLogUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    analysis_type: str | None = Field(None, min_length=1, max_length=100)
    input_data: dict[str, Any] | None = None
    result_data: dict[str, Any] | None = None
    status: str | None = Field(None, max_length=50)
    user_id: str | None = Field(None, max_length=100)
    error_message: str | None = None
    
    site_id: str | None = Field(None, max_length=100)
    report: str | None = Field(None, max_length=255)
    oc: str | None = Field(None, max_length=100)
    so: str | None = Field(None, max_length=100)
    item_name: str | None = Field(None, max_length=255)
    quantity_approved: float | None = Field(None, ge=0)
    quantity_pending: float | None = Field(None, ge=0)
    quantity_rejected: float | None = Field(None, ge=0)
    quantity_total: float | None = Field(None, ge=0)
    rejection_reason: str | None = None
    event_datetime: datetime | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "approved",
                "quantity_approved": 15.0,
                "quantity_pending": 2.0,
                "quantity_rejected": 0.0,
                "rejection_reason": None
            }
        }
    )


class NdpdLogResponse(NdpdLogBase):
    id: int = Field(..., description="ID do log", example=1)
    created_at: datetime = Field(..., description="Data de criação")
    updated_at: datetime = Field(..., description="Data de última atualização")

    model_config = ConfigDict(from_attributes=True)


class NdpdLogListResponse(BaseModel):
    total: int = Field(..., description="Total de registros", example=10)
    items: list[NdpdLogResponse] = Field(..., description="Lista de logs")
    page: int = Field(..., description="Página atual", example=1)
    size: int = Field(..., description="Itens por página", example=10)
