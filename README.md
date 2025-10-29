# Amigos da onça
Repositório do grupo 2025-2A-T08-EC11-G03


<p align="center">
<a href= "https://www.inteli.edu.br/"> <img src="https://github.com/Inteli-College/2024-T0008-EC05-G03/assets/85657433/afc793e7-2a20-4207-8832-0c998187c537" alt="Inteli - Instituto de Tecnologia e Liderança" border="0"></a>
</p>

## 🧑‍🎓 | Integrantes:

-  <a href="https://www.linkedin.com/in/antonio-guimar%C3%A3es2005/"> Antônio Guimarães </a>
-  <a href="https://www.linkedin.com/in/cec%C3%ADlia-alonso-gon%C3%A7alves-3aa4bb271/"> Cecília Gonçalves </a>
-  <a href="https://www.linkedin.com/in/eduardo-henrique-dos-santos/"> Eduardo dos Santos </a>
-  <a href="https://www.linkedin.com/in/josevalencar/"> José Alencar </a>
-  <a href="https://www.linkedin.com/in/lidiamariano/"> Lidia Mariano </a>
-  <a href="https://www.linkedin.com/in/luiza-rubim/"> Luiza Rubim </a>
-  <a href="https://www.linkedin.com/in/olincosta/"> Ólin Costa</a>
-  <a href="https://www.linkedin.com/in/rafaelarojas/"> Rafaela Lemos</a>

## 🧑‍🏫 | Professores:

### Orientador(a)
- <a href="https://www.linkedin.com/in/rafaelmatsuyama/"> Rafael Matsuyama </a>

### Instrutores

- <a href="https://www.linkedin.com/in/fabiana-martins-de-oliveira-8993b0b2/"> Fabiana Martins de Oliveira </a>
- <a href="https://www.linkedin.com/in/marcelo-gon%C3%A7alves-phd-a550652/"> Marcelo Gonçalves </a>
- <a href="https://www.linkedin.com/in/murilo-zanini-de-carvalho-0980415b/"> Murilo Zanini de Carvalho </a>
- <a href="https://www.linkedin.com/in/pedroteberga/"> Pedro Teberga </a>
- <a href="https://www.linkedin.com/in/rodrigo-mangoni-nicola-537027158/"> Rodrigo Mangoni Nicola</a>

---

## 📝 | Descrição 

O projeto em parceria com a [Sauá Consultoria Ambiental](https://www.sauaambiental.com.br/) consiste em um sistema de monitoramento de espécies ameaçadas em áreas remotas. Esse monitoramento acompanha as movimentações dos animais de diferentes espécies por meio de coleiras que emitem sinais LoRa (Long Range) e são captados por gateways, que processam esses dados e enviam para a nuvem. Esses dados serão tratados e exibidos em um dashboard interativo para os colaboradores da Sauá, permitindo estratégias mais eficazes de preservação da fauna.
Nosso grupo desenvolveu a parte API, tratamento de dados, pipeline...etc.

Para ler toda a documentação do projeto, [clique aqui](https://inteli-college.github.io/2025-2A-T08-EC11-G03/)

---


##  Estrutura de pastas

```bash
.
├── .github/workflows
├── docs/
│   └── docs
├── src/
└── README.md
```


---

## 💻 | Inicialização

### Pré-requisitos

- Docker (ou, para Windows, WSL + Docker Desktop) instalado

### Passo a passo

1. Para inicializar o projeto, clone o repositório e digite o seguinte comando no diretório ```~/src/```

```bash
git clone git@github.com:Inteli-College/2025-1A-T08-EC09-G03.git
cd 2025-1B-T08-EC10-G01/src/
```

2. Depois, basta buildar e inicializar o sistema dockerizado através do seguinte comando:

```bash
docker-compose up --build
```

---

## 📋 | Histórico de lançamentos

- 0.1.0 - 04/08/2025
 - Análise de impacto ético
 - Canvas proposta de valor
 - Proposta de arquitetura do sistema
 - Requisitos funcionais e não funcionais
 - Entendimento do problema

- 0.2.0 - 18/08/2025
  - Criar Datalake
  - Configuração pipeline ETL
  - Script de carregamento
  - Script de extração
  - Script de transformação
    
- 0.3.0 - 01/09/2025
  - Pipeline de dados
  - Conexão do DataLake
  - Documentação da API
  - Prisma para o banco
  - API para disponibilização dos dados
    
- 0.4.0 - 15/09/2025
  - Reunir dados
  - Finalização da pipeline de dados
  - Banco de dados para armazenar dados do modelo
 
- 0.5.0 - 29/09/2025
  - Testes e documentação dos testes
  - Subir EC2
  - Finalização do projeto

## 📋 Licença/License

<div xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
    <a property="dct:title" rel="cc:attributionURL" href="https://github.com/Inteli-College/2025-2A-T08-EC11-G03">
        Amigos da onça
    </a>
    <span>
        by
    </span>
    <span property="cc:attributionName">
        <a href="https://www.inteli.edu.br/">Inteli</a>, <a href="https://www.linkedin.com/in/antonio-guimar%C3%A3es2005/"> Antônio Guimarães </a>, <a href="https://www.linkedin.com/in/cec%C3%ADlia-alonso-gon%C3%A7alves-3aa4bb271/"> Cecília Gonçalves </a>, <a href="https://www.linkedin.com/in/eduardo-henrique-dos-santos/"> Eduardo dos Santos </a>, <a href="https://www.linkedin.com/in/josevalencar/"> José Alencar </a>, <a href="https://www.linkedin.com/in/lidiamariano/"> Lidia Mariano </a>, <a href="https://www.linkedin.com/in/luiza-rubim/"> Luiza Rubim </a>, <a href="https://www.linkedin.com/in/olincosta/"> Ólin Costa</a>, <a href="https://www.linkedin.com/in/rafaelarojas/"> Rafaela Lemos</a>
    </span> 
    <span>
        is licensed under
    </span>
    <a href="https://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">
        CC BY 4.0
        <img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="Creative Commons"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="Attribution">
    </a>
</div>
