from __future__ import annotations

import os
from typing import Dict

from fastapi import APIRouter, HTTPException

from ..config.env import get_influx_settings


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/env")
def env_status() -> Dict[str, bool]:
    s = get_influx_settings()
    return {
        "INFLUX_URL": bool(s.url),
        "INFLUX_ORG": bool(s.org),
        "INFLUX_BUCKET": bool(s.bucket),
        "INFLUX_TOKEN": bool(s.token),
    }


@router.get("/influx")
def influx_status() -> Dict[str, str]:
    s = get_influx_settings()
    missing = [k for k, v in {
        "INFLUX_URL": s.url,
        "INFLUX_ORG": s.org,
        "INFLUX_BUCKET": s.bucket,
        "INFLUX_TOKEN": s.token,
    }.items() if not v]
    if missing:
        raise HTTPException(status_code=500, detail=f"Variaveis faltando: {', '.join(missing)}")

    try:
        from influxdb_client import InfluxDBClient
        client = InfluxDBClient(url=s.url, token=s.token, org=s.org)
        try:
            # Prefer health() if available
            health = client.health()
            status = getattr(health, "status", None) or str(health)
        except Exception:
            # Fallback try listing the bucket
            client.buckets_api().find_bucket_by_name(s.bucket)
            status = "pass"
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexao Influx: {e}")

