# Health Controller

## Localização
`src/app/controllers/health_controller.py`  
Prefixo aplicado: `/health`  
> Obs: este router ainda não foi incluído no `main.py`.

## Função no projeto
As rotas de saúde são utilizadas para verificar a configuração do ambiente e a conectividade com o InfluxDB.  
São úteis para diagnósticos manuais, integração com sistemas de monitoramento e readiness/liveness probes em ambientes orquestrados.

## GET `/health/env`

### Descrição
Indica, por variável, se as configurações essenciais do InfluxDB estão presentes no ambiente.  
Não expõe valores sensíveis, apenas sinaliza presença ou ausência.

### Resposta
**200 OK** – objeto JSON com flags booleanas:
```json
{
  "INFLUX_URL": true,
  "INFLUX_ORG": true,
  "INFLUX_BUCKET": true,
  "INFLUX_TOKEN": false
}
```

## GET `/health/influx`

### Descrição

Valida as variáveis de ambiente e testa a conectividade com o InfluxDB.
Utiliza `client.health()` quando disponível; caso contrário, faz consulta ao bucket como fallback.

### Respostas

* **200 OK** –

  ```json
  { "status": "pass" }
  ```
* **500 Internal Server Error** –

  * `"Variaveis faltando: …"` se alguma configuração não estiver definida.
  * `"Erro de conexao Influx: …"` em caso de falha ao conectar.


## Conclusão

O Health Controller fornece sinais objetivos sobre o estado da aplicação:

* `/health/env` confirma se o ambiente está corretamente configurado.
* `/health/influx` valida a comunicação real com o InfluxDB.

Essas verificações são fundamentais para operação segura e monitorada do sistema.