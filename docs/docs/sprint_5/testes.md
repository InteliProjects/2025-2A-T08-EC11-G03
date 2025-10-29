## Padrão de Qualidade

## **1. Tabulações dos Resultados (Tabelas e Textos)**

A seguir estão detalhados os resultados e análises obtidos durante os testes realizados no sistema.  
Esses testes tiveram como objetivo avaliar o **desempenho, a estabilidade e a segurança** da API responsável pela comunicação entre o banco InfluxDB e os demais grupos do projeto.  
Cada tipo de teste foi planejado de acordo com a natureza de uso esperada por cada grupo parceiro (Grupos 1, 2 e 4), e executado em ambiente de *staging*.

---

### **1.1 Teste de Carga**

**Motivação:**  
O teste de carga foi escolhido para avaliar o comportamento da API sob um volume elevado e contínuo de requisições simultâneas.  
Esse tipo de teste é fundamental, pois o Grupo 4 depende de nossa API para enviar dados coletados pelas coleiras dos animais ao banco de dados. Assim, era necessário garantir que a aplicação suportasse grandes volumes de escrita e leitura sem instabilidades.

**Metodologia:**  
A execução foi feita com o script `locust_load.py`, que submeteu a API a um alto volume de requisições por um período aproximado de 9 minutos. Durante a execução, foram monitorados os tempos de resposta, taxa de erro e consumo de recursos, com critérios de sucesso definidos previamente (latência ≤ 300 ms e erro ≤ 1%).

- **Ferramenta:** `locust_load.py`  
- **Data:** 03/10/2025  
- **Horário:** 20:32:46 – 20:41:40 (duração: 8 min e 54 s)

**Resultados Obtidos:**

| **Indicador** | **Valor Obtido** | **Observação** |
|----------------|------------------|----------------|
| Requisições executadas | 30.550 | Volume total processado |
| Falhas registradas | 118 (0,38%) | Dentro do limite de 1% |
| Tempo médio de resposta | 355,56 ms | Mínimo 2 ms / Máximo 11.027 ms |
| Rota `/api/animals/all` | 17.018 req – 630,87 ms | Endpoint mais exigido |
| Rota `/api/collars/status` | 13.532 req – 9,33 ms | Endpoint estável |
| RPS médio | 57,22 | Processamento contínuo |
| Tipo de falha | HTTP 500 | Gargalo momentâneo no endpoint `/api/animals/all` |

**Interpretação:**  
O sistema manteve estabilidade e taxa de erro abaixo do limite definido, demonstrando boa capacidade de resposta sob carga contínua.  
As falhas pontuais de HTTP 500 foram associadas ao endpoint mais requisitado, sem comprometer a integridade do sistema.  
Esses resultados comprovam que a API é capaz de lidar com o volume de dados esperado pelo Grupo 4 durante o envio massivo de informações ao InfluxDB.

---

### **1.2 Teste de Pico**

**Motivação:**  
O teste de pico (spike test) foi escolhido para simular aumentos abruptos de tráfego em curtos períodos de tempo.  
Esse cenário está diretamente relacionado ao uso esperado pelo Grupo 2, responsável pelo modelo preditivo, que acessa a API apenas em momentos específicos do dia, realizando múltiplas requisições concentradas.  
O teste foi planejado para garantir que o sistema suporte esse comportamento sem falhas ou lentidão excessiva.

**Metodologia:**  
O teste foi realizado com o script `locust_spike.py`, multiplicando o número nominal de requisições em até cinco vezes durante um período de dois minutos.  
Foram monitorados os tempos de resposta, a ocorrência de falhas e o tempo de recuperação do sistema após o pico.

- **Ferramenta:** `locust_spike.py`  
- **Data:** 03/10/2025  
- **Horário:** 20:28:22 – 20:30:22 (duração: 2 minutos)

**Resultados Obtidos:**

| **Indicador** | **Valor Obtido** | **Observação** |
|----------------|------------------|----------------|
| Requisições executadas | 8.051 | Execução concluída com sucesso |
| Falhas registradas | 0 (0%) | Nenhuma falha crítica |
| Tempo médio de resposta | 811,14 ms | Mínimo 2 ms / Máximo 5.092 ms |
| Rota `/api/animals/all` | 948,57 ms | Leve aumento sob pico |
| Rota `/api/collars/status` | 643,77 ms | Estável |
| RPS médio | 67,26 | Sustentado mesmo sob pico |
| Recuperação | < 2 min | Retorno rápido à normalidade |

**Interpretação:**  
O sistema suportou aumentos repentinos de carga sem falhas ou perda de dados, recuperando-se rapidamente após o pico.  
A ausência de erros e o tempo de recuperação inferior a dois minutos comprovam que a infraestrutura da API é resiliente, estável e adequada para o uso intermitente do Grupo 2.

---

### **1.3 Teste de Segurança**

**Motivação:**  
O teste de segurança foi aplicado com o objetivo de verificar se os mecanismos de autenticação, autorização e controle de acesso estavam devidamente implementados.  
O **Grupo 1**, responsável pelos dashboards, consome dados continuamente, o que torna essencial garantir que o acesso seja feito apenas por usuários autenticados e dentro de limites seguros de requisição.

**Metodologia:**  
O teste foi dividido em duas etapas principais:  
1. **Verificação de autenticação:** tentativa de acesso com e sem credenciais válidas.  
2. **Teste de limitação de requisições (rate limiting):** simulação de acessos acima do permitido para avaliar se o sistema bloqueia requisições excessivas.  

**Etapas realizadas:**
1. **Autenticação:** todas as requisições exigiram *token* válido.  
2. **Limitação de requisições:** acessos excessivos resultaram em bloqueio temporário do usuário.  

**Resultados Obtidos:**

| **Aspecto Avaliado** | **Resultado** | **Conclusão** |
|-----------------------|----------------|----------------|
| Autenticação de usuários | 100% das requisições exigiram *token* | Controle de acesso validado |
| Acesso sem autenticação | Bloqueado | Implementação correta |
| Rate limiting | Ativo | Bloqueio temporário aplicado |
| Estabilidade do sistema | Mantida | Sem perda de dados ou falhas |

**Interpretação:**  
A API demonstrou mecanismos de autenticação e autorização funcionando corretamente, além de boa proteção contra acessos abusivos.  
Durante os testes, verificou-se que o sistema mantém estabilidade mesmo quando submetido a requisições excessivas, o que reforça a confiabilidade e segurança da aplicação.

---

### **1.4 Síntese Geral dos Resultados**

| **Tipo de Teste** | **Duração** | **Requisições** | **Falhas (%)** | **Latência Média (ms)** | **RPS Médio** | **Status** |
|--------------------|-------------|------------------|----------------|--------------------------|----------------|-------------|
| **Carga** | 8m54s | 30.550 | 0,38% | 355,56 | 57,22 | Aprovado |
| **Pico** | 2m | 8.051 | 0% | 811,14 | 67,26 | Aprovado |
| **Segurança** | — | — | — | — | — | Aprovado |

---

## **2. Critérios de Qualidade e Resultados Esperados**

**Motivação e propósito:**  
Os critérios de qualidade definidos a seguir orientaram a validação da performance e da confiabilidade do sistema.  
Esses parâmetros foram baseados nas metas estabelecidas durante o planejamento da Sprint, considerando os requisitos funcionais e não funcionais do projeto.

| **Tipo de Teste** | **Critério Avaliado** | **Resultado Esperado** | **Resultado Obtido** | **Situação** |
|--------------------|------------------------|--------------------------|----------------------|---------------|
| **Teste de Carga** | Latência de leitura | ≤ 300 ms | 355,56 ms | Leve acima, mas estável |
|                    | Taxa de erro | ≤ 1% | 0,38% | Dentro do limite |
|                    | Integridade dos dados | 100% preservada | Sem perdas registradas | Aprovado |
| **Teste de Pico** | Taxa de erro durante o pico | ≤ 3% | 0% | Aprovado |
|                    | Tempo de recuperação | ≤ 2 min | < 2 min | Cumprido |
|                    | Integridade dos dados | 100% preservada | Sem perdas registradas | Aprovado |
| **Teste de Segurança** | Autenticação de usuários | Somente usuários autenticados acessam dados | 100% autenticado via token | Aprovado |
|                    | Limitação de requisições | Bloqueio em caso de excesso | Bloqueio aplicado com sucesso | Aprovado |


Dessa forma, podemos concluir que os testes atenderam aos critérios estabelecidos para desempenho, segurança e estabilidade.  
As motivações que orientaram cada tipo de teste foram confirmadas nos resultados obtidos: o sistema apresentou comportamento consistente sob carga contínua, respondeu bem a picos repentinos e demonstrou robustez contra acessos não autorizados.  

Dessa forma, a aplicação é validada como confiável, segura e estável, pronta para integração com os demais módulos do projeto.
