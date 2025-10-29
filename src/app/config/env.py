import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    # Best-effort local .env loader to avoid external deps
    candidates = [
        Path(__file__).resolve().parents[3] / ".env",  # repo root
        Path(__file__).resolve().parents[2] / ".env",  # src root
        Path(__file__).resolve().parents[1] / ".env",  # app dir
    ]
    for p in candidates:
        if p.exists():
            try:
                with p.open("r", encoding="utf-8") as fh:
                    for line in fh:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            v = v.strip().strip('"').strip("'")
                            os.environ.setdefault(k.strip(), v)
            except Exception:
                pass
            break


_load_dotenv()


@dataclass(frozen=True)
class InfluxSettings:
    url: str
    org: str
    bucket: str
    token: str
    verify_ssl: str


def get_influx_settings() -> InfluxSettings:
    url = os.getenv("INFLUX_URL", "")
    org = os.getenv("INFLUX_ORG", "")
    bucket = os.getenv("INFLUX_BUCKET", "")
    token = os.getenv("INFLUX_TOKEN", "")
    verify_ssl = os.getenv("")
    # print(f'Token: ${token}')
    # print(f'Token: ${url}')
    # print(f'Token: ${org}')
    # print(f'Token: ${bucket}')
    return InfluxSettings(url=url, org=org, bucket=bucket, token=token, verify_ssl=verify_ssl)

@dataclass(frozen=True)
class CognitoSettings:
    """Dataclass para armazenar as configurações do Cognito."""
    aws_region: str
    user_pool_id: str
    app_client_id: str

def get_cognito_settings() -> CognitoSettings:
    """Lê as variáveis de ambiente do Cognito e retorna um objeto CognitoSettings."""
    aws_region = os.getenv("AWS_REGION", "")
    user_pool_id = os.getenv("COGNITO_USER_POOL_ID", "")
    app_client_id = os.getenv("COGNITO_APP_CLIENT_ID", "")
    
    if not all([aws_region, user_pool_id, app_client_id]):
        raise ValueError("Uma ou mais variáveis de ambiente do Cognito não estão definidas.")

    return CognitoSettings(
        aws_region=aws_region,
        user_pool_id=user_pool_id,
        app_client_id=app_client_id
    )