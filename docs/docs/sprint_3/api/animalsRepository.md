# Animals Repository

## Localização
`src/app/repositories/animalsRepository.py`

## Função no projeto
O **AnimalsRepository** é a camada de acesso a dados responsável por interagir diretamente com o **InfluxDB**.  
Seu papel é executar consultas e escritas usando a linguagem **Flux**, isolando os detalhes técnicos de conexão e persistência das demais camadas da aplicação.  
Dessa forma, controllers e services não precisam lidar com a complexidade do banco de séries temporais.

## Métodos implementados

### `async getAllAnimals(device_ids, start_date, end_date, cursor, limit) -> List[Dict[str, Any]]`

**Descrição**  
Executa a leitura dos registros de telemetria de animais.  
A consulta aplica filtros dinâmicos de dispositivo e intervalo temporal, além de paginação baseada em cursor, retornando os resultados pivotados.

**Parâmetros**  
- `device_ids`: lista de identificadores de dispositivos *(opcional)*.  
- `start_date`: datetime *(opcional)* — início da janela de consulta (default: últimos 30 dias).  
- `end_date`: datetime *(opcional)* — fim da janela de consulta.  
- `cursor`: string datetime *(opcional)* — retorna apenas registros com `_time` **anterior** ao cursor.  
- `limit`: inteiro *(obrigatório)* — número máximo de registros a retornar por página.  

**Consulta Flux** (construída dinamicamente):  
```flux
from(bucket: "<bucket>")
  |> range(start: <start|“-30d”>[, stop: <end>])
  |> filter(... device_ids ...)           // quando informado
  |> filter(fn: (r) => r._time < time(v: "<cursor>"))  // quando cursor informado
  |> pivot(rowKey: ["_time","device_id"], columnKey: ["_field"], valueColumn: "_value")
  |> sort(columns: ["_time"], desc: true)
  |> limit(n: <limit>)
```

**Retorno**

* Lista de dicionários JSON, cada um representando um registro de telemetria pivotado.
* Campos previstos (podem variar conforme o schema do bucket):

  * Identificação: `device_id`, `timestamp`.
  * Energia: `battery_voltage`, `battery_level_percent`.
  * Localização: `latitude`, `longitude`, `altitude`, `satellites`.
  * Dinâmica: `velocity_min_ms`, `velocity_max_ms`, `velocity_avg_ms`, `rest_time_minutes`.
  * Ambiente: `temperature_c`, `humidity_percent`, `pressure_hpa`, `lora_rssi`.

**Exemplo de resposta**

```json
[
  {
    "device_id": "onca-001",
    "timestamp": "2025-09-10T15:30:00Z",
    "battery_voltage": 3.7,
    "battery_level_percent": 87,
    "latitude": -19.12345,
    "longitude": -57.12345,
    "altitude": 150,
    "satellites": 8,
    "temperature_c": 36.5,
    "humidity_percent": 72,
    "pressure_hpa": 1012,
    "lora_rssi": -85
  }
]
```

### `async insertAnimalInfo(animal_info: Dict[str, Any]) -> None`

**Descrição**
Insere um novo registro de telemetria no InfluxDB.
Antes da escrita, aplica validações de retenção e ajuste de timestamp.

**Regras de negócio**

* **Retenção**: rejeita registros com `timestamp` anterior a 30 dias da data atual.
* **Timezone**: converte timestamps *naive* para UTC.
* **Default**: quando não informado, o `timestamp` é definido como `now()` em UTC.

**Escrita no InfluxDB**

* **Measurement**: `animal_telemetry`.
* **Tag**: `device_id`.
* **Fields**: todos os demais atributos do registro (quando não nulos).
* `point.time(timestamp)` e `write(bucket, record=point)` são usados para persistência.

**Retorno**

* **None**. Em caso de falha, uma exceção é lançada e propagada para o service/controller.

## Tratamento de erros

* Falhas de conexão ou configuração do InfluxDB disparam exceções.
* Falhas de validação de timestamp (fora da retenção de 30 dias) resultam em erro propagado ao controller, que retorna `500 Internal Server Error`.

## Importância e potencial de evolução

O **AnimalsRepository** é o ponto de contato com o InfluxDB e desempenha papel fundamental na robustez do sistema:

* **Centraliza a lógica de acesso a dados**, evitando duplicação em outros módulos.
* **Garante consistência** na forma de consultar e gravar informações de telemetria.
* **Facilita manutenção** ao encapsular a lógica de Flux em um único local.
* **Possibilita evolução** para estratégias de particionamento, caching ou ajustes de performance em consultas de larga escala.

## Conclusão

O **AnimalsRepository** abstrai toda a complexidade do InfluxDB, entregando dados organizados e validando inserções antes da escrita. A implementação assegura que a camada de negócio (services) e a camada de exposição (controllers) trabalhem com dados consistentes, sem precisar lidar diretamente com detalhes do banco de séries temporais.