# Animals Service

## Localização
`src/app/services/animalsService.py`

## Função no projeto
O **AnimalsService** é a camada intermediária entre os **controllers** e o **AnimalsRepository**.  
Sua função é orquestrar as regras de negócio, aplicar validações/normalizações quando necessário e delegar a persistência ou consulta dos dados ao repositório.  
Isso garante separação de responsabilidades:  
- Controllers ficam focados na comunicação HTTP.  
- Repository lida diretamente com o InfluxDB.  
- Service atua como ponto único de regras de negócio e evolução.

## Métodos implementados

### `async getAllAnimals(device_ids, start_date, end_date, cursor, limit) -> List[Dict[str, Any]]`

**Descrição**  
Executa a leitura de telemetria de animais, aplicando filtros opcionais e retornando registros de forma paginada.  
O método delega a consulta ao repositório, que constrói a query Flux no InfluxDB.

**Parâmetros**  
- `device_ids`: lista de identificadores de dispositivos *(opcional)*.  
- `start_date`: datetime *(opcional)* — início da janela de consulta.  
- `end_date`: datetime *(opcional)* — fim da janela de consulta.  
- `cursor`: string datetime *(opcional)* — marca o último registro da página anterior; retorna apenas registros anteriores a esse timestamp.  
- `limit`: inteiro *(obrigatório, default: 100, min: 1, max: 1000)* — número máximo de registros a retornar por página.  

**Retorno**  
- Lista de dicionários representando os registros pivotados de telemetria.  
- Cada registro inclui campos como `device_id`, `timestamp`, coordenadas, métricas ambientais e de bateria.  

### `async postAnimalInfo(animal_info: Dict[str, Any]) -> None`

**Descrição**  
Recebe um dicionário com os dados validados pelo schema `AnimalTelemetryPayload` e delega a escrita ao repositório.  
O método em si não aplica validações próprias: a validação de timestamp e retenção de 30 dias ocorre no repositório.

**Parâmetros**  
- `animal_info`: dicionário com os campos da telemetria (ex.: `device_id`, `timestamp`, `latitude`, `longitude`, `battery_voltage`, etc.).  

**Retorno**  
- **None**. O método não retorna dados úteis, apenas garante a chamada ao repositório.  
- Em caso de falha, uma exceção é propagada para o controller.  

## Tratamento de erros
- O service não captura exceções internamente.  
- Exceções do repositório (como falha de validação do `timestamp` ou erro de escrita no InfluxDB) são propagadas ao controller.  
- Os controllers convertem essas falhas em respostas HTTP adequadas (`500 Internal Server Error`).  

## Importância e potencial de evolução
Mesmo com lógica simples no estado atual, o **AnimalsService** é essencial para a arquitetura:  
- **Centralização de regras**: local adequado para incluir validações adicionais, normalização de campos e logs de auditoria.  
- **Escalabilidade**: permite evoluir com filtros mais sofisticados (ex.: por região ou espécie) sem acoplar controllers ao repositório.  
- **Testabilidade**: ao permitir injeção de mocks do repositório, facilita testes unitários.  

## Conclusão
O **AnimalsService** garante que a lógica de negócios do projeto esteja desacoplada das camadas de comunicação HTTP e acesso a dados.  
Ele organiza o fluxo entre controllers e repositórios, tornando a aplicação mais robusta, escalável e fácil de manter.