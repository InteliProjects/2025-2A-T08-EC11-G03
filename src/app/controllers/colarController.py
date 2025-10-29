from __future__ import annotations

from typing import Any, Dict, Optional
from datetime import datetime
from urllib.parse import urlencode

from fastapi import APIRouter, HTTPException, Query, Request, Body, status, Depends

from app.services.collarService import CollarService
from app.schemas.schemas import PaginatedApiResponse, MetaInfo, PaginationLinks
from app.schemas.collar_schema import CollarStatusCreate, CollarStatusResponse
from app.utils.auth import verify_cognito_token
router = APIRouter(
    prefix="/collars",
    tags=["Collar Status"],
)


@router.get(
    "/status",
    response_model=PaginatedApiResponse[Dict[str, Any]],
    summary="List collar statuses (all or by coleira_id) with cursor pagination",
    dependencies=[Depends(verify_cognito_token)],
)
async def get_collar_statuses(
    request: Request,
    coleira_id: Optional[str] = Query(None, description="Filter by a specific coleira_id."),
    start_date: Optional[datetime] = Query(None, description="Start datetime (ISO 8601) for created_at filter."),
    end_date: Optional[datetime] = Query(None, description="End datetime (ISO 8601) for created_at filter."),
    cursor: Optional[str] = Query(None, description="Cursor for the next page (stringified last `id`)."),
    limit: int = Query(100, ge=1, le=1000, description="Max rows per page."),
) -> PaginatedApiResponse[Dict[str, Any]]:
    """
    Single route that returns:
      - All statuses (default), or
      - Only a specific collar when `coleira_id` is provided,
    using descending `id` cursor pagination (like your animals endpoint).
    """
    service = CollarService()
    try:
        items = await service.getCollarStatuses(
            coleira_id=coleira_id,
            start_date=start_date,
            end_date=end_date,
            cursor=cursor,
            limit=limit,
        )

        # Build cursor for next page
        next_cursor: Optional[str] = None
        if len(items) == limit:
            last_id = items[-1].get("id")
            if last_id is not None:
                next_cursor = str(last_id)

        base_url = str(request.url.replace(query=None))

        query_params = {
            "limit": limit,
            "coleira_id": coleira_id,
            "start_date": start_date.isoformat() if start_date else None,
            "end_date": end_date.isoformat() if end_date else None,
        }
        query_params = {k: v for k, v in query_params.items() if v is not None}

        self_params = query_params.copy()
        if cursor:
            self_params["cursor"] = cursor
        self_link = f"{base_url}?{urlencode(self_params, doseq=True)}"

        next_link = None
        if next_cursor:
            next_params = query_params.copy()
            next_params["cursor"] = next_cursor
            next_link = f"{base_url}?{urlencode(next_params, doseq=True)}"

        links = PaginationLinks(self=self_link, next=next_link)
        meta = MetaInfo(
            limit=limit,
            device_ids=None,
            start_date=start_date,
            end_date=end_date,
        )
        columns = list(items[0].keys()) if items else []

        return PaginatedApiResponse(
            meta=meta,
            links=links,
            count=len(items),
            columns=columns,
            data=items,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/status",
    response_model=CollarStatusResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new collar status",
)
async def create_collar_status(
    payload: CollarStatusCreate = Body(...),
    _claims: dict = Depends(verify_cognito_token),
) -> CollarStatusResponse:
    """
    Creates a new status record for a given `coleira_id`.

    - If a status for this `coleira_id` already exists, returns **409 Conflict**.
    """
    service = CollarService()
    new_status = await service.create_status(payload)
    if not new_status:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Status for coleira_id '{payload.coleira_id}' already exists.",
        )
    return new_status
