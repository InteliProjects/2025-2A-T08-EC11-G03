# Requisitos

O presente projeto tem como objetivo o desenvolvimento de um sistema de monitoramento inteligente da fauna silvestre, integrando tecnologias de edge computing para uso em áreas remotas. A solução será composta por uma API e um dashboard interativo, permitindo a visualização da localização dos animais rastreados, emissão de alertas, análise de informações e integração com o banco de dados da Sauá Consultoria Ambiental.

Nesta seção, serão apresentados os requisitos funcionais e não funcionais definidos para o projeto, que orientam seu desenvolvimento e servirão como base para validação e testes da solução.

# Requisistos funcionais

Requisitos funcionais são as especificações que descrevem as funcionalidades que um sistema deve executar. Eles detalham o que o sistema precisa fazer, ou seja, as ações, tarefas e comportamentos necessários para satisfazer as necessidades do usuário. Em sua essência, requisitos funcionais definem as regras de negócio e as características que tornam o sistema útil. Eles respondem diretamente à pergunta "O que o sistema faz?".

Por exemplo, um requisito funcional para um sistema de e-commerce seria "O sistema deve permitir que o usuário adicione produtos ao carrinho de compras". Outro exemplo seria "O sistema deve calcular o total da compra, incluindo impostos e frete". Tais especificações constituem o cerne da aplicação, determinando as tarefas específicas que ela foi projetada para realizar.

Com base nisso, esta solução conta com os seguintes requisitos funcionais:

| **Nº do RF** | **Título**                            | **Descrição**                                                                                                  | **Casos de Teste**                                                                         |
| ------------ | ------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| RF-01        | Interação com o mapa                  | O sistema deve permitir que o usuário interaja com o mapa, aplicando zoom, movimentação e seleção de áreas.    | Acessar o mapa, aplicar zoom, mover o mapa e selecionar pontos para verificar a interação. |
| RF-02        | Localização em tempo real             | O sistema deve apresentar em tempo real a última coordenada de rastreio do animal.                             | Verificar se a coordenada exibida corresponde ao último dado recebido do animal.           |
| RF-03        | API para integração com gráfico       | O sistema deve disponibilizar uma API que permita integração com o gráfico de movimentação.                    | Realizar requisição à API e validar se os dados retornados podem ser usados no gráfico.    |
| RF-04        | Integração com banco de dados da Sauá | A API deve possibilitar integração com o banco de dados da Sauá Consultoria Ambiental.                         | Testar a comunicação da API com o banco de dados e validar inserção e leitura de dados.    |
| RF-05        | Identificação visual de animais       | O mapa do sistema deve disponibilizar colorações diferentes para identificação de cada animal rastreado.       | Adicionar múltiplos animais e verificar se cada um possui cor distinta no mapa.            |
| RF-06        | Alerta de baixa bateria               | O sistema deve apresentar informações de alerta quando a bateria do dispositivo de rastreamento estiver baixa. | Simular nível baixo de bateria e verificar se o alerta é exibido corretamente.             |
| RF-07        | Alarme de inatividade prolongada      | O sistema deve emitir um alarme caso o animal permaneça muito tempo em um mesmo local.                         | Simular localização fixa por período prolongado e verificar se o alarme é emitido.         |
| RF-08        | Cadastro de novos animais             | O sistema deve permitir o cadastro de novos animais a serem rastreados.                                        | Realizar cadastro de um novo animal e confirmar se aparece no sistema e no mapa.           |

# Requisitos não funcionais

Os requisitos não funcionais definem como o sistema deve se comportar, em vez de especificar funções ou comportamentos específicos. Diferentemente dos requisitos funcionais, que descrevem o que o sistema faz, os requisitos não funcionais se concentram em características de qualidade, como desempenho, segurança, usabilidade, confiabilidade e compatibilidade.

Esses requisitos são essenciais para garantir que o sistema atenda às expectativas dos usuários e funcione de forma eficiente, segura e confiável em diferentes condições de operação. Exemplos comuns incluem tempo de resposta aceitável, disponibilidade, tolerância a falhas, compatibilidade com dispositivos móveis e facilidade de manutenção.

Com base nisso, esta solução conta com os seguintes requisitos funcionais:

| **Nº do RNF** | **Título**                       | **Descrição**                                                                                                                                 | **Casos de Teste**                                                                                                                               |
| ------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| RNF-01        | Tempo de Resposta                | O sistema deve responder às requisições da API em até 1 segundo em condições normais de operação.                                             | Medir o tempo de resposta da API para diferentes tipos de requisições e verificar se está ≤ 1s.                                                  |
| RNF-02        | Disponibilidade                  | A API e o dashboard devem manter disponibilidade mínima de 99% durante o período de operação.                                                 | Monitorar uptime por 30 dias.                                                                                                                    |
| RNF-03        | Segurança de Comunicação         | Toda comunicação entre dashboard, API e banco de dados deve ser criptografada via protocolo HTTPS/TLS.                                        | Acessar o sistema e verificar se apenas conexões HTTPS são aceitas e se o certificado é válido.                                                  |
| RNF-04        | Escalabilidade                   | O sistema deve suportar adição de novos animais e usuários sem perda perceptível de desempenho.                                               | Cadastrar dezenas de novos animais e usuários e medir tempo de resposta e estabilidade do sistema.                                               |
| RNF-05        | Compatibilidade e Responsividade | O dashboard deve funcionar corretamente em desktops, tablets e smartphones, adaptando-se automaticamente ao dispositivo.                      | Testar visualização e funcionalidade em diferentes navegadores e tamanhos de tela.                                                               |
| RNF-06        | Usabilidade da Interface         | A interface deve ser intuitiva e apresentar informações com cores, ícones e legendas claras para fácil interpretação.                         | Realizar testes com usuários e medir facilidade de uso e compreensão das informações exibidas.                                                   |
| RNF-07        | Tolerância a Falhas              | O sistema deve continuar operando de forma limitada mesmo que algum componente, como a API ou o banco de dados, apresente falhas temporárias. | Simular indisponibilidade parcial de serviços e verificar se o sistema mantém funções críticas ativas, como visualização de dados já carregados. |

## Conclusão

Nesta seção, foram apresentados os requisitos funcionais e não funcionais do sistema, detalhando tanto o que o sistema deve fazer quanto como ele deve se comportar.

Os requisitos funcionais descrevem as funcionalidades essenciais, como interação com o mapa, rastreio em tempo real, integração com APIs e cadastro de animais, garantindo que o sistema atenda às necessidades dos usuários e cumpra seus objetivos principais.

Já os requisitos não funcionais tratam das características de qualidade, como desempenho, disponibilidade, segurança, escalabilidade e usabilidade, assegurando que o sistema seja confiável, eficiente e fácil de utilizar em diferentes condições de operação.

A definição e criação desses requisitos é de extrema importância para orientar o desenvolvimento, a implementação de testes e a validação do sistema, garantindo que ele atenda tanto às expectativas dos usuários quanto aos padrões de qualidade esperados.

# Bibliografia:

[1] Pressman, Roger S.; Maxim, Bruce R. Engenharia de Software: Uma Abordagem Profissional. O livro aborda o processo de engenharia de software de forma abrangente, dedicando seções importantes à elicitação e especificação de requisitos.

[2] Sommerville, Ian. Engenharia de Software. Esta obra é um clássico na área e oferece uma visão detalhada sobre a importância dos requisitos no ciclo de vida do desenvolvimento de software, diferenciando entre requisitos funcionais e não funcionais.

[3] Wiegers, Karl E.; Beatty, Joy. Software Requirements. Este livro é amplamente reconhecido como uma das melhores referências para a prática de gerenciamento de requisitos, com foco em técnicas e boas práticas para sua definição, documentação e validação.
