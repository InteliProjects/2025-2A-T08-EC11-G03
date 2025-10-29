# Pipeline

Esta pipeline foi desenvolvida no **Apache Hop** com o objetivo de consumir dados de uma API geográfica, processá-los e identificar quais registros estão localizados dentro dos limites do território brasileiro.

O fluxo de processamento realiza a coleta, transformação, validação e filtragem dos dados antes da exportação final.

![pipeline](../../static/img/image.png)

---

## Estrutura da Pipeline

### 1. **REST Client**
- **Função:** Consome os dados de uma API externa.
- **Descrição:** Faz uma requisição HTTP para o endpoint configurado e obtém os dados no formato **JSON**.
- **Saída:** Retorna o corpo da resposta da API, que será processado na próxima etapa.

---

### 2. **JSON Input**
- **Função:** Converter a resposta JSON em dados tabulares.
- **Descrição:** Interpreta o conteúdo retornado pela API e transforma os campos em colunas estruturadas.
- **Campos extraídos:** `Latitude`, `Longitude`, `Altitude`.

---

### 3. **Select Values**
- **Função:** Ajustar os tipos de dados e selecionar apenas os campos relevantes.
- **Descrição:** Garante que as colunas estejam no formato correto (por exemplo, `Latitude` e `Longitude` como números decimais) e remove campos desnecessários para as próximas etapas.

---

### 4. **is_inside_brazil (Script)**
- **Função:** Determinar se o ponto geográfico está dentro dos limites do Brasil.
- **Descrição:** Um script personalizado cria uma **flag lógica** (`true`/`false`) com base nas coordenadas.  
  Essa verificação considera os limites geográficos do país (latitude e longitude mínimas e máximas).
- **Saída:** Adiciona uma nova coluna `is_inside_brazil`.

---

### 5. **Filter Rows**
- **Função:** Filtrar registros válidos.
- **Descrição:** Utiliza a flag `is_inside_brazil` para selecionar apenas os registros **dentro do Brasil**.
  - **Verdadeiro:** Envia para a saída final.
  - **Falso:** Pode ser descartado ou enviado para um log de rejeitados.

---

### 6. **CSV File Output**
- **Função:** Exportar os dados processados.
- **Descrição:** Salva os registros válidos em um arquivo **CSV** para uso posterior em análises, dashboards ou integrações.