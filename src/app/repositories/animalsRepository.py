from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone, timedelta

# Correctly import the async client from its submodule and Point from the root
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
from influxdb_client import Point

from ..config.env import get_influx_settings


class AnimalsRepository:
    def __init__(self) -> None:
        self.settings = get_influx_settings()
        # The async client will be created and managed within each method

    async def getAllAnimals(
        self,
        device_ids: Optional[List[str]],
        start_date: Optional[datetime],
        end_date: Optional[datetime],
        cursor: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Asynchronously retrieves telemetry data with dynamic filters.
        """
        # The client is created per-request using an async context manager
        async with InfluxDBClientAsync(
            url=self.settings.url, token=self.settings.token, org=self.settings.org
        ) as client:
            query_api = client.query_api()

            range_start = start_date.isoformat() if start_date else "-30d"
            range_stop_part = f', stop: {end_date.isoformat()}' if end_date else ""

            query_parts = [
                f'from(bucket: "{self.settings.bucket}")',
                f'|> range(start: {range_start}{range_stop_part})',
            ]

            if device_ids:
                device_id_array = ", ".join([f'"{id}"' for id in device_ids])
                query_parts.append(f'|> filter(fn: (r) => contains(value: r.device_id, set: [{device_id_array}]))')

            if cursor:
                query_parts.append(f'|> filter(fn: (r) => r._time < time(v: "{cursor}"))')

            query_parts.extend([
                '|> pivot(rowKey: ["_time", "device_id"], columnKey: ["_field"], valueColumn: "_value")',
                '|> sort(columns: ["_time"], desc: true)',
                f'|> limit(n: {limit})',
            ])

            flux_query = "\n  ".join(query_parts)

            # Await the database query
            tables = await query_api.query(flux_query)
            items: List[Dict[str, Any]] = []
            for table in tables:
                for record in table.records:
                    vals = record.values
                    ts = record.get_time()
                    items.append(
                        {
                            "device_id": vals.get("device_id") or vals.get("deviceId"),
                            "timestamp": ts.isoformat() if ts else str(vals.get("_time")),
                            "battery_voltage": vals.get("battery_voltage"),
                            "battery_level_percent": vals.get("battery_level_percent"),
                            "latitude": vals.get("latitude"),
                            "longitude": vals.get("longitude"),
                            "altitude": vals.get("altitude"),
                            "satellites": vals.get("satellites"),
                            "velocity_min_ms": vals.get("velocity_min_ms"),
                            "velocity_max_ms": vals.get("velocity_max_ms"),
                            "velocity_avg_ms": vals.get("velocity_avg_ms"),
                            "rest_time_minutes": vals.get("rest_time_minutes"),
                            "temperature_c": vals.get("temperature_c"),
                            "humidity_percent": vals.get("humidity_percent"),
                            "pressure_hpa": vals.get("pressure_hpa"),
                            "lora_rssi": vals.get("lora_rssi"),
                        }
                    )
            return items

    async def insertAnimalInfo(self, animal_info: Dict[str, Any]) -> None:
        """
        Asynchronously inserts a new animal telemetry record into InfluxDB after validating the timestamp.
        """
        # --- Timestamp Validation ---
        retention_period_days = 30
        oldest_allowed_date = datetime.now(timezone.utc) - timedelta(days=retention_period_days)
        
        timestamp_to_use = animal_info.get("timestamp")

        if timestamp_to_use:
            # Pydantic already converted it to a datetime object, but we ensure it's timezone-aware for comparison.
            if timestamp_to_use.tzinfo is None:
                timestamp_to_use = timestamp_to_use.replace(tzinfo=timezone.utc)
            
            if timestamp_to_use < oldest_allowed_date:
                raise ValueError(
                    f"Provided timestamp {timestamp_to_use.isoformat()} is outside the "
                    f"{retention_period_days}-day data retention period. "
                    f"The earliest allowed timestamp is {oldest_allowed_date.isoformat()}."
                )
        else:
            # If no timestamp is provided, default to the current time.
            timestamp_to_use = datetime.now(timezone.utc)
        
        # --- End Validation ---

        async with InfluxDBClientAsync(
            url=self.settings.url, token=self.settings.token, org=self.settings.org
        ) as client:
            write_api = client.write_api()

            point = Point("animal_telemetry")
            point.tag("device_id", animal_info.get("device_id"))

            for key, value in animal_info.items():
                if key not in ["device_id", "timestamp"] and value is not None:
                     point.field(key, value)

            point.time(timestamp_to_use)

            # Await the write operation
            await write_api.write(
                bucket=self.settings.bucket,
                record=point
            )

