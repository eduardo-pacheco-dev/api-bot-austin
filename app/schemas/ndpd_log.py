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
    
    # Campos NDPD
    site_id: str | None = Field(None, max_length=100, description="ID do site", example="SITE-001")
    relatorio: str | None = Field(None, max_length=255, description="Relatório", example="REL-2026-001")
    oc: str | None = Field(None, max_length=100, description="Ordem de Compra", example="OC-12345")
    os: str | None = Field(None, max_length=100, description="Ordem de Serviço", example="OS-67890")
    nome_item: str | None = Field(None, max_length=255, description="Nome do item", example="Cabo de rede CAT6")
    quantidade_aprovada: float | None = Field(None, ge=0, description="Quantidade aprovada", example=10.0)
    quantidade_pendente: float | None = Field(None, ge=0, description="Quantidade pendente", example=5.0)
    quantidade_reprovada: float | None = Field(None, ge=0, description="Quantidade reprovada", example=2.0)
    quantidade_total: float | None = Field(None, ge=0, description="Quantidade total", example=17.0)
    motivo_reprovacao: str | None = Field(None, description="Motivo da reprovação", example="Não conforme especificação")
    data_hora: datetime | None = Field(None, description="Data e hora da análise")


class NdpdLogCreate(NdpdLogBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Análise NDPD #001",
                "description": "Análise de item recebimento",
                "analysis_type": "recebimento",
                "status": "pendente",
                "site_id": "SITE-001",
                "relatorio": "REL-2026-001",
                "oc": "OC-12345",
                "os": "OS-67890",
                "nome_item": "Cabo de rede CAT6",
                "quantidade_aprovada": 10.0,
                "quantidade_pendente": 5.0,
                "quantidade_reprovada": 2.0,
                "quantidade_total": 17.0,
                "motivo_reprovacao": None,
                "data_hora": "2026-10-28T17:00:00"
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
    relatorio: str | None = Field(None, max_length=255)
    oc: str | None = Field(None, max_length=100)
    os: str | None = Field(None, max_length=100)
    nome_item: str | None = Field(None, max_length=255)
    quantidade_aprovada: float | None = Field(None, ge=0)
    quantidade_pendente: float | None = Field(None, ge=0)
    quantidade_reprovada: float | None = Field(None, ge=0)
    quantidade_total: float | None = Field(None, ge=0)
    motivo_reprovacao: str | None = None
    data_hora: datetime | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "aprovado",
                "quantidade_aprovada": 15.0,
                "quantidade_pendente": 2.0,
                "quantidade_reprovada": 0.0,
                "motivo_reprovacao": None
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
