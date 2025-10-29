import requests
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Importamos a nova função em vez do objeto 'settings'
from ..config.env import get_cognito_settings

# Chamamos a função para obter as configurações do Cognito
cognito_settings = get_cognito_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Exceções (sem alteração) ---
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
EXPIRED_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
    headers={"WWW-Authenticate": "Bearer"},
)

# --- Configuração do Cognito (agora usa o objeto cognito_settings) ---
JWKS_URL = f"https://cognito-idp.{cognito_settings.aws_region}.amazonaws.com/{cognito_settings.user_pool_id}/.well-known/jwks.json"
ISSUER = f"https://cognito-idp.{cognito_settings.aws_region}.amazonaws.com/{cognito_settings.user_pool_id}"

try:
    jwks_response = requests.get(JWKS_URL)
    jwks_response.raise_for_status()
    jwks = jwks_response.json()
except requests.RequestException as e:
    raise RuntimeError(f"Could not fetch Cognito JWKS: {e}") from e

# --- Função de Verificação de Token (agora usa o objeto cognito_settings) ---
async def verify_cognito_token(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"], "kid": key["kid"], "use": key["use"],
                    "n": key["n"], "e": key["e"],
                }
                break
        
        if not rsa_key:
            raise CREDENTIALS_EXCEPTION

        payload = jwt.decode(
            token,
            rsa_key,
            algorithms=["RS256"],
            audience=cognito_settings.app_client_id, # <-- MUDANÇA AQUI
            issuer=ISSUER,
        )
        
        if payload.get("token_use") != "access":
             raise CREDENTIALS_EXCEPTION

        return payload

    except jwt.ExpiredSignatureError:
        raise EXPIRED_TOKEN_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION