from influxdb_client import InfluxDBClient
from ..config.env import get_influx_settings

def get_influx_client():
    settings = get_influx_settings()
    # Criacao do cliente
    _client = InfluxDBClient(
        url=settings.url,
        token=settings.token,
        org=settings.org,
        verify_ssl=settings.verify_ssl,
    )
    return _client