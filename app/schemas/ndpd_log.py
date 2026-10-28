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


class NdpdLogCreate(NdpdLogBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Análise NDPD #001",
                "description": "Análise de padrões de tráfego",
                "analysis_type": "traffic_analysis",
                "input_data": {"period": "2026-10", "filters": ["source"]},
                "status": "pending",
                "user_id": "user_123"
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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "completed",
                "result_data": {"findings": ["pattern_1"], "score": 0.95}
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
