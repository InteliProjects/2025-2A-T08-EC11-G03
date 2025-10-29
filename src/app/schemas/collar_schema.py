# src/app/schemas/collar_schemas.py

from pydantic import BaseModel, Field
from datetime import datetime

class CollarStatusBase(BaseModel):
    """Base schema with shared fields."""
    coleira_id: str = Field(..., example="C001-A", description="The unique identifier for the collar.")
    # --- FIELD RENAMED HERE ---
    prediction: str = Field(..., example="resting", description="The predicted behavior of the animal (e.g., 'resting', 'grazing', 'walking').")


class CollarStatusCreate(CollarStatusBase):
    """Schema for creating a new prediction record via a POST request."""
    # --- JSON SCHEMA EXTRA ADDED HERE ---
    class Config:
        json_schema_extra = {
            "example": {
                "coleira_id": "C001-A",
                "prediction": "grazing"
            }
        }


class CollarStatusResponse(CollarStatusBase):
    """Schema for API responses, including database-generated fields."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True