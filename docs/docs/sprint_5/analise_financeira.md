# Análise financeira

## **Introdução**

A presente análise financeira tem como objetivo avaliar a **viabilidade econômica da implementação do módulo de engenharia de dados** do projeto de **monitoramento de animais silvestres**, desenvolvido pelo grupo 3 para a Sauá Consultoria Ambiental. Este módulo é responsável por viabilizar o **processamento, integração e disponibilização dos dados coletados pelos dispositivos de GPS-telemetria** produzidos pelo grupo 4, utilizando tecnologias de **pipeline, armazenamento em nuvem e segurança de dados**.

O foco desta análise é estimar os custos de **desenvolvimento do pipeline de dados**, responsável pela **sanitização, armazenamento e distribuição dos dados ambientais**, bem como os custos da **infraestrutura em nuvem e do desenvolvimento da API** que permitirá o acesso a esses dados por meio de painéis e dashboards de monitoramento.  
Além disso, será avaliado o **retorno financeiro e operacional** esperado, considerando o impacto do projeto sobre a redução de custos em pesquisas de biodiversidade e o fortalecimento da posição estratégica da Sauá no setor ambiental.

---

## **Análise Financeira: Protótipo (PoC) – Engenharia de Dados**

Para esta prova de conceito (PoC), consideraremos um período de **3 meses**, tempo estimado para o desenvolvimento e testes do pipeline de dados e da API de distribuição. A análise inclui os custos de **mão de obra técnica**, **infraestrutura em nuvem** e **licenças de software**.

---

### **Desenvolvimento de Software e Engenharia de Dados: Custo da Mão de Obra**

| **Função** | **Quantidade** | **Meses** | **Salário Mensal (R$)** | **Valor Final (R$)** | **Fonte** |
|-------------|----------------|-----------|--------------------------|----------------------|-----------|
| Engenheiro de Dados | 2 | 3 | 9.100,00 | 54.600,00 | Glassdoor |
| Engenheiro de Software Backend | 1 | 3 | 8.200,00 | 24.600,00 | Vagas |
| Engenheiro DevOps / Cloud | 1 | 3 | 9.000,00 | 27.000,00 | Glassdoor |
| Cientista de Dados (para modelos de IA/ML) | 1 | 3 | 10.000,00 | 30.000,00 | QueroBolsa |
| Gestor de Projeto Técnico | 1 | 3 | 5.500,00 | 16.500,00 | Vagas |
| **Total** |  |  |  | **R$ 152.700,00** |  |

**Observação:** As médias salariais foram baseadas em dados atualizados de portais de emprego brasileiros. Os valores já consideram encargos e benefícios.  

---

### **Custos de Infraestrutura em Nuvem (Cloud)**

A infraestrutura em nuvem será essencial para hospedar os serviços de processamento de dados, banco de dados e API. Abaixo, estimam-se os custos com base em valores médios das plataformas **AWS**, **Azure** e **Google Cloud**, para o período de 3 meses.

| **Serviço** | **Quantidade/Descrição** | **Valor/Mês (R$)** | **Valor Final (3 meses)** |
|--------------|--------------------------|---------------------|---------------------------|
| Computação | 3 instâncias de máquinas virtuais (4 vCPUs, 16GB RAM) | R$ 1.600,00 | R$ 4.800,00 |
| Armazenamento | 1 TB SSD para dados brutos e tratados | R$ 0,25/GB = R$ 250,00 | R$ 750,00 |
| Rede | 2 TB de transferência de dados | R$ 0,10/GB = R$ 204,80 | R$ 614,40 |
| Banco de Dados Relacional (PostgreSQL gerenciado) | 500 GB | R$ 500,00 | R$ 1.500,00 |
| Banco NoSQL (para dados IoT) | 500 GB | R$ 400,00 | R$ 1.200,00 |
| Monitoramento e Logs | CloudWatch / DataDog | R$ 200,00 | R$ 600,00 |
| API Gateway + Balanceamento de Carga | AWS API Gateway / Nginx Load Balancer | R$ 500,00 | R$ 1.500,00 |
| Pipelines ETL (Dataflow / Airflow / Lambda) | 3 pipelines automatizadas | R$ 800,00 | R$ 2.400,00 |
| IA/ML (Treinamento de modelos de predição de rotas animais) | GPUs temporárias (spot instances) | R$ 1.200,00 | R$ 3.600,00 |
| **Total** |  |  | **R$ 16.964,40** |

**Observação:** Os valores incluem impostos e taxas de uso variáveis estimadas em 18%.  

---

### **Custos de Licenciamento e Ferramentas de Desenvolvimento**

| **Descrição** | **Quantidade** | **Valor Unitário (R$)** | **Valor Final (R$)** | **Fonte** |
|----------------|----------------|--------------------------|----------------------|------------|
| Licenças GitHub Pro / Colaboração | 5 usuários | R$ 40,00/mês | R$ 600,00 | GitHub |
| Power BI Pro (Painel de Visualização) | 2 usuários | R$ 100,00/mês | R$ 600,00 | Microsoft |
| Ferramentas de Observabilidade (DataDog) | 1 instância | R$ 300,00/mês | R$ 900,00 | DataDog |
| **Total** |  |  | **R$ 2.100,00** |  |

---

### **Custo Total do Protótipo – Engenharia de Dados**

| **Descrição** | **Valor (R$)** |
|----------------|----------------|
| Custos relacionados à mão de obra | R$ 152.700,00 |
| Custos relacionados à infraestrutura em nuvem | R$ 16.964,40 |
| Custos relacionados a licenças e ferramentas | R$ 2.100,00 |
| **Custo Total para Implementação (PoC)** | **R$ 171.764,40** |

---

## **Valor Final: Margem de Lucro + Impostos da Nota Fiscal**

A margem de lucro projetada será de **10%**, considerando a natureza experimental da PoC e a possibilidade de retorno a médio prazo via contratos de manutenção e evolução tecnológica. Além disso, é considerado o **imposto de emissão de nota fiscal (18%)**, utilizando o **método de cálculo “por dentro”**.

| **Descrição** | **Lucro (10%)** | **Custo + Lucro (R$)** | **Imposto (18%) “por dentro”** | **Valor Final (R$)** |
|----------------|-----------------|------------------------|-------------------------------|----------------------|
| Custo Total (PoC) | R$ 17.176,44 | R$ 188.940,84 | R$ 41.406,60 | **R$ 230.347,44** |

---

## **ROI (Retorno Sobre o Investimento)**

O ROI é uma métrica essencial para determinar o potencial de retorno financeiro e estratégico do investimento realizado.

```math
ROI = (Receita − Custo) / Custo × 100
```

- **Receita estimada:** R$ 350.000,00 (considerando a venda do sistema e 1 ano de manutenção técnica a instituições de pesquisa e órgãos ambientais)  
- **Custo total:** R$ 230.347,44  

```math
ROI = (350.000 - 230.347,44) / 230.347,44 × 100 = 51,9%
```

🔹 **Interpretação:**  
Um ROI de **51,9%** indica **alta viabilidade econômica** e **potencial de lucro significativo**, reforçando o valor estratégico do projeto para a Sauá e seus parceiros de pesquisa.

---

## **Análise de Viabilidade Financeira**

A implementação da pipeline de dados e API para monitoramento de fauna representa **um investimento inicial moderado**, mas com alto potencial de retorno, tanto econômico quanto científico. Entre os benefícios esperados:

- **Redução de custos operacionais** para projetos de monitoramento ambiental.  
- **Maior acesso a dados de biodiversidade**, fortalecendo políticas públicas e projetos de conservação.  
- **Fortalecimento da imagem da Sauá** como empresa inovadora no uso de IA, IoT e cloud para sustentabilidade.  
- **Escalabilidade comercial**, com possibilidade de ofertar o sistema como SaaS (Software as a Service) para múltiplas instituições.

---

## **Conclusão**

A análise financeira do módulo de engenharia de dados demonstra que o projeto é **tecnicamente viável e financeiramente atrativo**, com **ROI positivo** e forte **potencial de impacto ambiental e de mercado**.  
Com um **investimento total estimado de R$ 230.347,44**, a PoC permitirá validar o funcionamento do pipeline de dados, da API e da infraestrutura de nuvem, estabelecendo a base tecnológica para o monitoramento automatizado da fauna silvestre.

O sucesso dessa fase fortalecerá a posição da **Sauá Consultoria Ambiental** como referência nacional em **tecnologia aplicada à conservação da biodiversidade**, alinhando-se plenamente aos objetivos estratégicos da organização.