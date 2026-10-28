from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from app.db.session import get_db
from app.services.ndpd_log_service import NdpdLogService
from app.services.telegram_service import build_ndpd_log_message, send_telegram_message
from app.schemas.ndpd_log import NdpdLogCreate, NdpdLogUpdate, NdpdLogResponse, NdpdLogListResponse

router = APIRouter()


@router.post(
    "/",
    response_model=NdpdLogResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar log de análise NDPD",
    description="Cria um novo registro de log de análise NDPD",
)
def create_ndpd_log(
    ndpd_log: NdpdLogCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    service = NdpdLogService(db)
    log = service.create(ndpd_log)
    background_tasks.add_task(send_telegram_message, build_ndpd_log_message(log))
    return log


@router.get(
    "/",
    response_model=NdpdLogListResponse,
    summary="Listar logs de análise NDPD",
    description="Lista logs com paginação e filtros",
)
def list_ndpd_logs(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(10, ge=1, le=100, description="Número de registros por página"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por status"),
    analysis_type: Optional[str] = Query(None, description="Filtrar por tipo de análise"),
    user_id: Optional[str] = Query(None, description="Filtrar por ID do usuário"),
    db: Session = Depends(get_db),
):
    service = NdpdLogService(db)
    items, total = service.get_multi(
        skip=skip,
        limit=limit,
        status=status_filter,
        analysis_type=analysis_type,
        user_id=user_id,
    )
    return NdpdLogListResponse(total=total, items=items, page=skip // limit + 1, size=limit)


@router.get(
    "/{log_id}",
    response_model=NdpdLogResponse,
    summary="Buscar log de análise NDPD por ID",
    description="Retorna um log específico pelo ID",
)
def get_ndpd_log(log_id: int, db: Session = Depends(get_db)):
    service = NdpdLogService(db)
    log = service.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log de análise NDPD não encontrado")
    return log


@router.put(
    "/{log_id}",
    response_model=NdpdLogResponse,
    summary="Atualizar log de análise NDPD",
    description="Atualiza todos os campos de um log existente",
)
def update_ndpd_log(log_id: int, ndpd_log_update: NdpdLogUpdate, db: Session = Depends(get_db)):
    service = NdpdLogService(db)
    log = service.update(log_id, ndpd_log_update)
    if not log:
        raise HTTPException(status_code=404, detail="Log de análise NDPD não encontrado")
    return log


@router.patch(
    "/{log_id}",
    response_model=NdpdLogResponse,
    summary="Atualizar parcialmente log de análise NDPD",
    description="Atualiza parcialmente um log existente",
)
def patch_ndpd_log(log_id: int, ndpd_log_update: NdpdLogUpdate, db: Session = Depends(get_db)):
    service = NdpdLogService(db)
    log = service.update(log_id, ndpd_log_update)
    if not log:
        raise HTTPException(status_code=404, detail="Log de análise NDPD não encontrado")
    return log


@router.delete(
    "/{log_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Deletar log de análise NDPD",
    description="Remove um log de análise NDPD",
)
def delete_ndpd_log(log_id: int, db: Session = Depends(get_db)):
    service = NdpdLogService(db)
    success = service.delete(log_id)
    if not success:
        raise HTTPException(status_code=404, detail="Log de análise NDPD não encontrado")
    return None
