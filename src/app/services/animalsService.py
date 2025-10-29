from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

from ..repositories.animalsRepository import AnimalsRepository


class AnimalsService:
    def __init__(self, repository: AnimalsRepository | None = None) -> None:
        self.repository = repository or AnimalsRepository()

    async def getAllAnimals(
        self,
        device_ids: Optional[List[str]],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        cursor: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        # Await the call to the async repository method
        return await self.repository.getAllAnimals(
            device_ids=device_ids,
            start_date=start_date,
            end_date=end_date,
            cursor=cursor,
            limit=limit
        )

    async def postAnimalInfo(self, animal_info: Dict[str, Any]) -> None:
        """
        Receives a dictionary of animal info and passes it to the repository to be inserted.
        """
        # Await the call to the async repository method
        return await self.repository.insertAnimalInfo(animal_info)

