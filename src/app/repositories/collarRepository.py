from __future__ import annotations

from typing import List, Optional, Dict, Any
from datetime import datetime
from prisma import Prisma
from prisma.models import CollarStatus
from app.utils.db import get_prisma


class CollarRepository:
    """
    Data Access Layer for CollarStatus on Postgres (Prisma).
    """

    def __init__(self) -> None:
        self.db: Prisma = get_prisma()  # connection managed by FastAPI lifespan

    async def get_by_collar_id(self, coleira_id: str) -> Optional[CollarStatus]:
        """
        Fetch a single row by unique coleira_id.
        Requires `coleira_id` to be @unique in schema.prisma.
        """
        return await self.db.collarstatus.find_unique(
            where={"coleira_id": coleira_id}
        )
        # If coleira_id is NOT unique, use:
        # return await self.db.collarstatus.find_first(where={"coleira_id": coleira_id})

    async def list_statuses(
        self,
        coleira_id: Optional[str],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        cursor: Optional[int],
        limit: int,
    ) -> List[CollarStatus]:
        """
        Returns a page of collar statuses filtered by optional coleira_id and date range.
        Cursor is the last seen `id` (descending).
        """
        where: Dict[str, Any] = {}
        if coleira_id:
            where["coleira_id"] = coleira_id

        if start_date or end_date:
            created_at: Dict[str, Any] = {}
            if start_date:
                created_at["gte"] = start_date
            if end_date:
                created_at["lte"] = end_date
            where["created_at"] = created_at

        args: Dict[str, Any] = {
            "where": where or None,
            "order": {"id": "desc"},
            "take": limit,
        }
        if cursor is not None:
            args["cursor"] = {"id": cursor}
            args["skip"] = 1

        return await self.db.collarstatus.find_many(**args)

    async def create(self, data: Dict[str, Any]) -> CollarStatus:
        """
        Creates a new status row.
        """
        return await self.db.collarstatus.create(data=data)

    async def upsert_by_collar_id(self, coleira_id: str, data: Dict[str, Any]) -> CollarStatus:
        """
        Idempotent write helper using unique coleira_id.
        """
        return await self.db.collarstatus.upsert(
            where={"coleira_id": coleira_id},
            data={"create": data, "update": data},
        )
