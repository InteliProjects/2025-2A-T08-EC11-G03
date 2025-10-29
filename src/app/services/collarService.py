# app/services/collarService.py
from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

from app.repositories.collarRepository import CollarRepository
from app.schemas.collar_schema import CollarStatusCreate
from prisma.models import CollarStatus


class CollarService:
    """
    Business logic layer for collar statuses.
    Mirrors AnimalsService pattern: optional repo injection, defaults to internal repo.
    """
    def __init__(self, repository: CollarRepository | None = None) -> None:
        self.repository = repository or CollarRepository()

    async def getCollarStatuses(
        self,
        coleira_id: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        cursor: Optional[str],
        limit: int,
    ) -> List[Dict[str, Any]]:
        """
        Returns a page of statuses as list[dict] (keeps parity with animals service).
        - `cursor` is a stringified `id` (descending pagination).
        """
        cursor_id: Optional[int] = int(cursor) if cursor is not None else None

        rows: List[CollarStatus] = await self.repository.list_statuses(
            coleira_id=coleira_id,
            start_date=start_date,
            end_date=end_date,
            cursor=cursor_id,
            limit=limit,
        )

        # Map Prisma model -> dict (like animals maps Influx row -> dict)
        items: List[Dict[str, Any]] = []
        for r in rows:
            items.append(
                {
                    "id": r.id,
                    "coleira_id": r.coleira_id,
                    "prediction": r.prediction,
                    "created_at": r.created_at.isoformat() if r.created_at else None,
                    "updated_at": r.updated_at.isoformat() if r.updated_at else None,
                }
            )
        return items

    async def create_status(self, status_create: CollarStatusCreate) -> Optional[CollarStatus]:
        """
        Creates a new collar status if one doesn't already exist for `coleira_id`.
        Returns None if duplicate found (controller turns that into 409).
        """
        existing = await self.repository.get_by_collar_id(status_create.coleira_id)
        if existing:
            return None
        data = status_create.model_dump()
        return await self.repository.create(data)

    # optional: idempotent write if you decide to expose it later
    async def upsert_status(self, status_create: CollarStatusCreate) -> CollarStatus:
        data = status_create.model_dump()
        return await self.repository.upsert_by_collar_id(status_create.coleira_id, data)
