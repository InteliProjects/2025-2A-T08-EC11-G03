from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Query, Body, status, Request, Depends

from ..services.animalsService import AnimalsService
from ..schemas.schemas import PaginatedApiResponse, AnimalTelemetryPayload, MetaInfo, PaginationLinks
from ..utils.auth import verify_cognito_token
router = APIRouter()


@router.get(
    "/animals/all",
    response_model=PaginatedApiResponse[Dict[str, Any]],
    dependencies=[Depends(verify_cognito_token)],
)
async def get_animals_all(
    request: Request,
    device_ids: Optional[List[str]] = Query(None, description="Lista de device_id para filtrar."),
    start_date: Optional[datetime] = Query(None, description="Data de início para o filtro (ISO 8601)."),
    end_date: Optional[datetime] = Query(None, description="Data de fim para o filtro (ISO 8601)."),
    cursor: Optional[str] = Query(None, description="Cursor para a próxima página (timestamp ISO 8601 do último item)."),
    limit: int = Query(100, ge=1, le=1000, description="Quantidade máxima de linhas a retornar por página."),
) -> PaginatedApiResponse[Dict[str, Any]]:
    """
    Retorna os dados de telemetria de forma paginada.
    """
    # Seu código original permanece o mesmo aqui.
    service = AnimalsService()
    try:
        items = await service.getAllAnimals(
            device_ids=device_ids,
            start_date=start_date,
            end_date=end_date,
            cursor=cursor,
            limit=limit
        )

        # (... resto do seu código de paginação ...)
        next_cursor = None
        if len(items) == limit:
            last_item = items[-1]
            if 'timestamp' in last_item and last_item['timestamp']:
                next_cursor = last_item['timestamp']

        base_url = str(request.url.replace(query=None))
        
        query_params = {
            "limit": limit,
            "device_ids": device_ids,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}

        self_link_params = query_params.copy()
        if cursor:
            self_link_params['cursor'] = cursor
        
        self_link = f"{base_url}?{urlencode(self_link_params, doseq=True)}"
        
        next_link = None
        if next_cursor:
            next_link_params = query_params.copy()
            next_link_params['cursor'] = next_cursor
            next_link = f"{base_url}?{urlencode(next_link_params, doseq=True)}"

        links = PaginationLinks(self=self_link, next=next_link)
        meta = MetaInfo(
            limit=limit,
            device_ids=device_ids,
            start_date=start_date,
            end_date=end_date
        )
        columns = list(items[0].keys()) if items else []

        return PaginatedApiResponse(
            meta=meta,
            links=links,
            count=len(items),
            columns=columns,
            data=items
        )

    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))


@router.post(
    "/animals/info",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, str]
)
async def post_animal_info(
    payload: AnimalTelemetryPayload = Body(...),
    _claims: dict = Depends(verify_cognito_token),
) -> Dict[str, str]:
    """
    Insere um novo registro de telemetria para um animal.
    """
    # Exemplo: Você poderia usar as 'claims' para registrar qual usuário fez a inserção
    # cognito_username = _claims.get("username")
    # print(f"Dados inseridos pelo usuário: {cognito_username}")
    
    service = AnimalsService()
    try:
        animal_info_dict = payload.model_dump(exclude_unset=True)
        await service.postAnimalInfo(animal_info_dict)
        return {"status": "success", "message": "Animal info inserted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert animal info: {str(e)}")
