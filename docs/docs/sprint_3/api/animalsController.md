# Animals Controller

## Localização
`src/app/controllers/animalsController.py`  
Prefixo aplicado no app: `/api`

## Função no projeto
O Animals Controller é responsável por expor as operações de leitura e escrita relacionadas à telemetria de animais.  
Atualmente, implementa:
- Leitura paginada e filtrada de registros de telemetria (`GET /animals/all`).  
- Inserção de novos registros (`POST /animals/info`).  

## GET `/api/animals/all`

### Descrição
Retorna leituras de telemetria pivotadas, com suporte a filtros por dispositivo e janela temporal.  
O resultado é paginado e contém metadados (HATEOAS com links de navegação).

### Parâmetros de Query
- `device_ids`: lista de strings *(opcional)*  
  Pode ser enviada repetindo a chave (`device_ids=A&device_ids=B`).  
- `start_date`: datetime ISO 8601 *(opcional)*  
  Define o início da janela temporal (ex.: `2024-10-01T00:00:00Z`).  
- `end_date`: datetime ISO 8601 *(opcional)*  
  Define o fim da janela temporal.  
- `cursor`: datetime ISO 8601 *(opcional)*  
  Timestamp do último item da página anterior. A consulta retorna registros com `_time` **anterior** a esse valor.  
- `limit`: inteiro *(padrão: 100, mínimo: 1, máximo: 1000)*  
  Tamanho máximo da página.  

### Estrutura de Resposta
**200 OK** – Objeto no formato `PaginatedApiResponse[Dict[str, Any]]`, com os campos:  
- `meta`: informações da requisição (ex.: `request_timestamp_utc`, `limit`, filtros aplicados).  
- `links`: URLs de navegação (`self` e `next`, se houver próxima página).  
- `count`: quantidade de itens na página.  
- `columns`: chaves do primeiro registro (schema dinâmico).  
- `data`: lista de registros pivotados (campos como `device_id`, `timestamp`, `latitude`, `battery_voltage`, etc.).  

**500 Internal Server Error** – erro ao consultar o backend ou exceção de serviço.  

### Exemplo de Requisição
```bash
curl "http://localhost:5000/api/animals/all?device_ids=onca-001&start_date=2024-10-01T00:00:00Z&limit=50"
```

## POST `/api/animals/info`

### Descrição

Insere um novo registro de telemetria para um animal.
O corpo da requisição segue o schema `AnimalTelemetryPayload`.

### Corpo da Requisição

Exemplo:

```json
{
  "device_id": "onca-001",
  "timestamp": "2025-09-10T15:30:00Z",
  "latitude": -19.12345,
  "longitude": -57.12345,
  "battery_voltage": 3.7,
  "temperature_c": 36.5
}
```

### Regras de Negócio

* `device_id` é obrigatório.
* `timestamp` deve estar dentro da retenção de 30 dias; caso não informado, será usado o horário atual (UTC).

### Respostas

* **201 Created** –

  ```json
  { "status": "success", "message": "Animal info inserted successfully." }
  ```
* **500 Internal Server Error** – falha de validação ou escrita no InfluxDB.
  A mensagem segue o padrão:

  ```json
  { "detail": "Failed to insert animal info: <detalhes do erro>" }
  ```

## Conclusão

O Animals Controller concentra as operações relacionadas à telemetria: leitura filtrada e paginada dos dados históricos e inserção de novas medições.
Essa abordagem facilita tanto o consumo em dashboards quanto a evolução de regras de negócio ligadas à coleta de dados.