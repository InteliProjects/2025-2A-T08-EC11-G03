from __future__ import annotations

from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime, timezone

# A generic type variable for our data
T = TypeVar("T")


class MetaInfo(BaseModel):
    """Metadata about the API request."""
    request_timestamp_utc: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    limit: int
    device_ids: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class PaginationLinks(BaseModel):
    """HATEOAS-style links for navigating the paginated response."""
    self: str
    next: Optional[str] = None

class PaginatedApiResponse(BaseModel, Generic[T]):
    """
    A standardized, paginated response model following API best practices.
    """
    meta: MetaInfo = Field(..., description="Metadata about the API request.")
    links: PaginationLinks = Field(..., description="Links for navigating through pages of data.")
    count: int = Field(..., description="The number of records in the current page's data list.")
    columns: List[str] = Field(..., description="A list of column names for the data records.")
    data: List[T] = Field(..., description="The actual list of data records for the current page.")


class AnimalTelemetryPayload(BaseModel):
    """
    Defines the structure for the request body when posting new animal telemetry data.
    """
    device_id: str
    timestamp: datetime | None = None
    battery_voltage: float | None = None
    battery_level_percent: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    altitude: float | None = None
    satellites: int | None = None
    velocity_min_ms: float | None = None
    velocity_max_ms: float | None = None
    velocity_avg_ms: float | None = None
    rest_time_minutes: float | None = None
    temperature_c: float | None = None
    humidity_percent: float | None = None
    pressure_hpa: float | None = None
    lora_rssi: float | None = None

    class Config:
        # Pydantic will automatically generate a JSON schema example for the docs
        json_schema_extra = {
            "example": {
                "device_id": "cow-007",
                "timestamp": "2023-10-27T10:00:00Z",
                "latitude": -23.5505,
                "longitude": -46.6333,
                "temperature_c": 25.5,
                "velocity_avg_ms": 1.2,
                "battery_level_percent": 95.5,
            }
        }

