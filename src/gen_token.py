import hashlib
import base64
import requests
from urllib.parse import urlencode, urlparse, parse_qs
import secrets

# --- CONFIGURAÇÃO ---
#
# VERIFIQUE E AJUSTE ESTES VALORES PARA CORRESPONDER EXATAMENTE
# À URL QUE FUNCIONOU PARA VOCÊ!
#
COGNITO_DOMAIN = "https://us-east-1q9wbq5s06.auth.us-east-1.amazoncognito.com"
CLIENT_ID = "6g80ths4a0i2907gsooe9bp7ev"
# A URI para a qual o Cognito te redireciona. DEVE ser igual à do console da AWS.
REDIRECT_URI = "https://localhost:8000/auth" 
# Os escopos que você configurou no Cognito.
SCOPES = "openid phone email"
# --------------------

def generate_pkce_verifier_and_challenge():
    """Gera um par de verificador e desafio para o fluxo PKCE."""
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    challenge_bytes = base64.urlsafe_b64encode(digest)
    code_challenge = challenge_bytes.decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def main():
    """
    Guia o usuário para obter um access_token manualmente.
    """
    # --- Parte 1: Gerar a URL de Login ---
    print("\n--- PARTE 1: Gerar URL de Login ---")
    
    # Geramos o PKCE para segurança. O 'verifier' será usado na Parte 2.
    code_verifier, code_challenge = generate_pkce_verifier_and_challenge()
    
    auth_url_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPES,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }
    # Usamos o endpoint padrão /oauth2/authorize
    authorize_url = f"{COGNITO_DOMAIN}/oauth2/authorize?{urlencode(auth_url_params)}"
    
    print("\n[AÇÃO NECESSÁRIA]")
    print("1. Copie a URL abaixo e cole no seu navegador.")
    print("2. Faca o login (com o Google, etc.).")
    print("3. O navegador sera redirecionado para 'localhost'. Copie a URL completa da barra de enderecos.\n")
    print("URL de Login:")
    print(f"==> {authorize_url}\n")
    
    # --- Parte 2: Capturar o 'code' e obter o Token ---
    
    # Pedimos ao usuário para colar a URL que ele copiou do navegador
    redirected_url = input("Cole a URL completa de redirecionamento aqui e pressione Enter:\n")
    
    try:
        # Extraímos o parâmetro 'code' da URL colada
        parsed_url = urlparse(redirected_url)
        authorization_code = parse_qs(parsed_url.query)['code'][0]
        print(f"\n[+] Codigo de autorizacao extraido com sucesso: {authorization_code[:15]}...")
    except (KeyError, IndexError):
        print("\n[!] Erro: Nao foi possivel encontrar o parametro 'code' na URL fornecida. Tente novamente.")
        return

    print("\n--- PARTE 2: Trocando o Código pelo Access Token ---")
    token_endpoint = f"{COGNITO_DOMAIN}/oauth2/token"
    token_payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI, # Precisa ser a mesma da requisição inicial
        'code_verifier': code_verifier # Prova que a requisição é legítima
    }

    try:
        response = requests.post(token_endpoint, data=token_payload)
        response.raise_for_status()
        
        tokens = response.json()
        access_token = tokens.get('access_token')

        print("\n" + "="*50)
        print("  TOKEN OBTIDO COM SUCESSO!")
        print("="*50)
        print(f"\nAccess Token: \n{access_token}\n")
        return access_token

    except requests.exceptions.HTTPError as err:
        print("\n[!] Erro ao obter o token:")
        print(f"    Status Code: {err.response.status_code}")
        print(f"    Resposta: {err.response.json()}")

if __name__ == "__main__":
    main()