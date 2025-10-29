# Ambiente Dockerizado e Integração com Postgres/Prisma

## Introdução
Ambiente completo e containerizado com **FastAPI**, **PostgreSQL** e **Prisma ORM**, mantendo o **InfluxDB** para telemetria histórica. Além disso, adiciona um novo fluxo de **status de coleiras (Collar Status)**, centraliza autenticação com **Cognito** e organiza melhor a base de código (serviços e repositórios).

## Dockerização da API
### Arquivos principais
- **`docker-compose.yml`**
  - Adiciona dois serviços:  
    - `db`: PostgreSQL 16 com volume `pgdata`, healthcheck e variáveis lidas do `.env`.  
    - `api`: build baseado em `src/Dockerfile.api`, dependente do Postgres saudável, expõe porta `8000` e monta `src/` + `prisma/` para hot-reload.  
- **`src/Dockerfile.api`**
  - Usa imagem `python:3.13-slim`.  
  - Instala dependências a partir do `pyproject.toml`.  
  - Copia o schema do Prisma e gera o client (`prisma generate`).  
  - Sobe o Uvicorn com `app.main:app`.  

### Ambiente
- O `.env` é carregado automaticamente em `app/main.py` e `app/config/env.py`, evitando dependências extras como `python-dotenv`.

## PostgreSQL + Prisma
- **Prisma ORM** gera um client Python tipado e assíncrono, permitindo CRUD sem SQL manual.  
- **Schema**: definido em `prisma/schema.prisma`, introduzindo o modelo `CollarStatus`:
  ```prisma
  model CollarStatus {
    id         Int      @id @default(autoincrement())
    coleira_id String   @unique
    prediction String
    created_at DateTime @default(now())
    updated_at DateTime @updatedAt
  }
  ```
- **Migração**: `migration.sql` cria tabelas `animal_metadata` e `collar_statuses`.  
- **Conexão**: `app/utils/db.py` expõe um singleton `Prisma()` com helpers para conectar/desconectar no ciclo de vida do FastAPI (`app/main.py`).  

## Camada de Dados e Negócio
- **Repository**: `collarRepository.py` abstrai queries Prisma (`find_unique`, `find_many`, `create`, `upsert`).  
- **Service**: `collarService.py` aplica regras como paginação cursorizada e prevenção de duplicados.  
- **Schemas**: `collar_schema.py` define modelos Pydantic para request/response:  
  - `CollarStatusCreate` (entrada)  
  - `CollarStatusResponse` (saída com `id`, `created_at`, `updated_at`).  
- **Controller**: `colarController.py` expõe duas rotas:  
  - `GET /collars/status`: lista status com filtros (coleira_id, datas) + paginação cursorizada.  
  - `POST /collars/status`: cria novo status, retorna **409 Conflict** se coleira já existir.  

## Autenticação Cognito
- `app/utils/auth.py` centraliza autenticação:  
  - Busca configurações do Cognito em `env.py`.  
  - Baixa e valida JWKS da AWS.  
  - Exige tokens JWT válidos em todas as rotas sensíveis.  
- Todas as rotas em `colarController` usam `Depends(verify_cognito_token)` para garantir segurança.

## Makefile Atualizado
- Comandos principais:  
  - `make up`: sobe stack (com build).  
  - `make down`: derruba containers.  
  - `make logs`: logs unificados.  
  - `make migrate`: roda `prisma migrate dev` dentro do container API.  
  - `make clean`: remove volume `pgdata` (**operação destrutiva**).  

## Convivência com InfluxDB
- **Telemetria histórica** segue armazenada no InfluxDB (`animalsRepository.py`).  
- **Postgres/Prisma** cobre os **novos dados de status de coleira**.  
- Ambos bancos compartilham variáveis no `.env`, permitindo futura migração gradual.

## Sugestões para Uso
1. Criar um `.env` com `DATABASE_URL` do Postgres e credenciais do Cognito.  
2. Subir stack com `make up`.  
3. Rodar `make migrate` após modificar `schema.prisma`.  
4. Usar as rotas `/api/collars/status` para gerenciar estados de coleira.  

## Conclusão
A aplicação passa a contar com um ambiente totalmente containerizado, simplificando tanto o desenvolvimento quanto a futura implantação em produção.

A integração entre FastAPI, PostgreSQL (via Prisma) e InfluxDB garante flexibilidade para lidar com dados relacionais e temporais, atendendo às novas demandas sem perder o histórico existente.

Além disso, a autenticação centralizada com Cognito reforça a segurança das rotas, enquanto os ajustes no Makefile e na estrutura do código promovem maior padronização e facilidade de manutenção pelo time.

Esse conjunto de melhorias estabelece uma base sólida para evoluções futuras, permitindo que novas funcionalidades sejam incorporadas de forma organizada, escalável e segura.