# Previsão de Vendas - Rede de Farmácias Rossmann

![find map](../img/rossmann.png)

A Rossmann é uma rede de farmácias que opera em mais de 3.000 lojas em 7 países europeus, empregando cerca de 56 mil colaboradores. A empresa disponibilizou dados de vendas de suas filiais na plataforma [Kaggle](https://www.kaggle.com/competitions/rossmann-store-sales/overview), contendo mais de 1 milhão de registros com 18 características únicas para cada venda.
# 1. Problema de Negócio
O Chief Financial Officer (CFO) da Rossmann deseja reformar as lojas da rede de farmácias, visando melhorar a estrutura e o atendimento ao público. Para isso, ele informou aos gerentes que precisa receber a previsão de receita das próximas 6 semanas de cada loja, a fim de determinar o valor a ser investido em cada uma delas.

Atualmente, as previsões são feitas individualmente por cada gerente de loja, resultando em variações significativas devido a fatores distintos que influenciam os resultados, como promoções, competição por clientes, feriados e sazonalidade. O processo de cálculo é manual, o que torna os resultados ainda mais inconsistentes.

O objetivo deste projeto é auxiliar o CFO na tomada de decisões, fornecendo previsões automáticas para cada loja e permitindo que ele consulte essas previsões através de um Bot no aplicativo Telegram.

# 2. Premissas de Negócio
Para construir a solução, as seguintes premissas foram consideradas:
* A consulta da previsão de vendas estará disponível 24/7 e será acessível via aplicativo do Telegram. O CFO digitará o código da loja e receberá como resposta o valor da previsão para as próximas 6 semanas.
* A previsão considerará apenas as lojas que tiveram vendas superiores a 0 nos dados disponíveis.
* Os dias em que as lojas estiveram fechadas serão excluídos da previsão.
* Lojas sem informações sobre competidores próximos terão a distância fixada em 200.000 metros.

## 2.1. Descrição dos Dados
| Atributo                          | Descrição                                                                                                                                             |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| Store                             | Identificador único de cada loja                                                                                                                      |
| Date                              | Data em que ocorreu o evento de venda                                                                                                                 |
| DayOfWeek                         | Variável numérica que representa o dia da semana                                                                                                      |
| Sales                             | Valor de vendas do dia                                                                                                                                |
| Customers                         | Quantidade de clientes na loja no dia                                                                                                                 |
| Open                              | Indicador para loja aberta = 1 ou fechada = 0                                                                                                         |
| StateHoliday                      | Indica se o dia é feriado de estado. a = Feriado público, b = Feriado de páscoa, c = Natal, 0 = Não há feriado                                        |
| SchoolHoliday                     | Indica se a loja foi ou não fechada durante o feriado escolar                                                                                         |
| StoreType                         | Indica o modelo de lojas. Pode variar entre a, b, c, d                                                                                                |
| Assortment                        | Indica o nível de variedade de produtos: a = básico, b = extra, c = estendido                                                                         |
| CompetitionDistance               | Distância (em metros) para o competidor mais próximo                                                                                                  |
| CompetitionOpenSince [Month/Year] | Indica o ano e mês em que o competidor mais próximo abriu                                                                                             |
| Promo                             | Indica se a loja está com alguma promoção ativa no dia                                                                                                |
| Promo2                            | Indica se a loja deu continuidade na promoção: 0 = loja não está participando, 1 = loja participando                                                  |
| Promo2Since [Year/Week]           | Descreve o ano e semana de quando a loja começa a a promoção extendida                                                                                |
| PromoInterval                     | Descreve os meses em que a loja iniciou a promo2, ex.: "Feb,May,Aug,Nov" significa que a loja iniciou as promoções estendidas em cada um desses meses |

# 3. Estratégia da Solução
Para garantir uma entrega rápida e eficiente da primeira solução, com o objetivo de trazer valor para a empresa e permitir decisões ágeis por parte do CFO, foi adotado o método CRISP-DS.

![Mapa Mental](../img/crisp_ds.png)

O método CRISP-DS é composto por 9 etapas cíclicas, em que a cada iteração dessas etapas, o resultado de negócio é aprimorado, buscando entregas cada vez mais rápidas e de maior qualidade, com maior precisão. Isso possibilita que as equipes que utilizarão os resultados desenvolvidos tenham um produto minimamente utilizável já na primeira entrega, e que seja aprimorado ao longo do tempo.

## Passos do CRISP-DS:
1. **Problema de Negócio:** Esta etapa tem como objtive receber o problema de negócio que será resolvido. É nesta etapa que é recebido a pergutna ou o pedido feito pelo dono do problema, que no caso deste projeto, é o CFO da rede Rossmann.

2. **Entendimento de Negócio:** Esta etapa tem como objetivo entender a dor do dono do problema e qual a sua real necessidade. Nesta etapa podem surgir protótipos da solução para validar com o dono do problema o que ele deseja como solução. 

3. **Coleta de Dados:** Esta etapa tem como objetivo realizar a coleta dos dados, buscando eles nas tabelas do(s) banco(s) de dados da empresa. 

4. **Limpeza dos Dados:** Esta etapa tem como objetivo remover toda e qualquer sujeira nos dados. Um dado sujo pode ser entendido como um dado que irá atrapalhar a performance final do algoritmo de Machine Learning. Tomando o cuidado entender bem o fenômeno que está sendo estudado para que não sejam removidos dados importantes para a modelagem do problema.

5. **Exploração dos Dados:** Esta etapa tem como objetivo entender os dados e como eles se relacionam entre si. Normalmente, são criadas hipóteses acionáveis de negócio que são posteriormente validadas utilizando técnicas de análise de dados. Além da criação de novas *features* que serão utilizadas na etapa de Modelagem de Dados.

6. **Modelagem dos Dados:** Esta etapa tem como objetivo preparar os dados para que eles sejam utilizados pelos algoritmos de Machine Learning. É nesta etapa que são feitos as transformações e *encodign* dos dados, a fim de facilitar o aprendizado do algoritmo utilizado.

7. **Aplicação de Algoritmos de Machine Learning:** Esta etapa tem como objetivo selecionar e aplicar algoritmos de Machine Learning nos dados preparados nas etapas anteriores. É nesta etapa que são selecionados os algoritmos e feito a comparação de performance enetre eles, para selecionar o algoritmos que melhor performou como algoritmo final.

8. **Avaliação de Performance:** Esta etapa tem como objetivo verificar a performance do algoritmo selecionado na etapa anterior com os resultados atuais, ou *base line* atual. Neste momento é feito a tradução da performance do algoritmo para perfomance de negócio. Ou seja, quanto a solução criada tratrá de retorno financeiro para a empresa. Caso a performance seja aceitável, o algoritmo é publicado e é retornado para a etapa de entendimento de negócio novamente, a fim entender melhor possíveis lacunas e assim melhorar a performance do algoritmo selecionado. Caso a performance não seja aceitável, o algoritmo não é publicado e é retornado para a etapa de entendimento de negócio para fazer uma nova iteração e assim melhorar a performance da solução.

9. **Publicação da Solução:** Esta etapa tem como objetivo publicar o algoritmo selecionado, deixando publico e utilizável a solução criada.

## 3.1. Produto Final
Foi combinado com o CFO que seria entregue um Bot dentro do aplicativo Telegram, facilitando assim que o CFO verifique a previsão das lojas independente do local em que ele esteja.

Além disso, no processo de criação do produto final, será criado uma API que será utilizada para retornar as previsões das lojas. Essa API irá utilizar o modelo de Machine Learning desenvolvido para realizar a previsão.

## 3.2. Ferramentas Utilizadas
Para criar a solução, foram utilizadas as seguintes ferramentas:
- Linguagem de Programação Python versão 3.8.13
- Versionador de código Git
- Aplicação Jupyter Notebook para prototipar a solução
- Serviço de Hospedagem em Nuvem
- Técnicas de manipulação de dados utilizando a linguagem de programação Python
- Técnicas de redução de dimensionalidade e seleção de atributos
- Algoritmos de Machine Learning da biblioteca [scikit-learn](https://scikit-learn.org/stable/) da linguagem de programação Python

# 4. Top 3 Insights
Foi criado um Mindmap para ajudar na construção de Hipóteses, a fim de facilitar e delimitar o escopo da etapa de análise exploratória.

![](api/img/mind_map.png)

Através do Mindmap, foram geradas 19 hipóteses de negócio. Dessas, 12 foram selecionadas para validação, confirmando premissas da equipe de negócios e do responsável pelo problema. Além disso, foram gerados insights relevantes para ambos os grupos.

Dos 12 hipóteses verificadas, destacaram-se três principais insights.

## Insight 1: Lojas Abertas durante o feriado de Natal deveriam vender mais
**Hipótese Falsa:** Lojas que ficam abertas durante o feriado de natal não vendem mais em comparação a outros feriados

![](api/img/hip_1.png)

## Insight 2: Lojas Deveriam vender mais depois do dia 10 de cada mês
**Hipótese Verdadeira:** Lojas realmente vendem mais depois do dia 10 de cada mês

![](api/img/hip_2.png)

## Insight 3: Lojas deveriam vender mais no segundo semestre do ano
**Hipótese Falsa:** Lojas vendem MENOS no segundo semestre do ano

![](api/img/hip_3.png)

# 5. Modelos de Machine Learning
No primeiro ciclo do projeto, foram selecionados cinco algoritmos para teste, visando identificar o algoritmo com melhor desempenho e custo de implementação. Nessa etapa inicial, optou-se pela simplicidade, considerando que era o primeiro ciclo do projeto e o objetivo principal era entregar uma solução mínima utilizável para a equipe de negócios e polo CFO.

Os algotitmos selecionados foram:
- Avarege Model
- Linear Regression
- Linear Regression - Lasso
- Random Forest Regressor
- XGBRegressor

Após a seleção dos algoritmos, procedemos com o treinamento e teste de cada um deles para avaliar sua performance. Além disso, utilizamos o método de seleção de features * [Boruta](https://mbq.github.io/Boruta/) para identificar as variáveis mais relevantes e impactantes na base de dados. 

# 6. Seleção do Modelo de Machine Learning
## 6.1. Esolha da Métrica
Na escolha entre os algoritmos, utilizamos a métrica ***MAPE (Mean Absolute Percentage Error)***, que é uma medida de erro que expressa a porcentagem média do erro em relação ao valor real. Optamos por essa métrica porque ela é mais compreensível para a equipe de negócios e o CEO, uma vez que fornece uma representação percentual do erro em relação ao valor médio. Dessa forma, é mais fácil interpretar e comunicar o desempenho dos algoritmos selecionados.

## 6.2. Métricas dos Algoritmos
Após os testes inicias, obtivemos os seguintes resultados:

| Nome do Modelo            |         MAE |     MAPE |        RMSE |
| :------------------------ | ----------: | -------: | ----------: |
| Avarege Model             | 1354.800353 | 0.455051 | 1835.135542 |
| Linear Regression         | 1867.089774 | 0.292694 | 2671.049215 |
| Linear Regression - Lasso | 1891.704880 | 0.289106 | 2744.451735 |
| Random Forest Regressor   |  679.893818 | 0.099967 | 1011.038517 |
| XGBRegressor              |  865.126662 | 0.124905 | 1278.187883 |

## 6.3. Métricas dos Algoritmos - *Cross Validation*

Após testar os algoritmos selecionados, utilizamos a técnica de ***Cross Validation*** para validar os resultados e garantir a real performance de cada modelo utilizado. No nosso caso, como estávamos lidando com uma série temporal, aplicamos uma forma específica de ***Cross Validation*** que leva em consideração a ordem cronológica dos dados durante o treinamento dos algoritmos.Significa que respeitamos a sequência temporal em que os dados foram coletados ou registrados. Isso é importante quando estamos trabalhando com séries temporais, onde a ordem dos eventos é relevante. Essa abordagem nos permite obter uma avaliação mais precisa do desempenho dos modelos ao longo do tempo.

![](api/img/cross_validation.png)

Com esse método de validação, foram obtidas as seguintes performances:

| Nome do Modelo                |             MAE CV |       MAPE CV |            RMSE CV |
| :---------------------------- | -----------------: | ------------: | -----------------: |
| Linear Regression             | 2081.73 +/- 295.63 |  0.3 +/- 0.02 | 2952.52 +/- 468.37 |
| Linear Regression Regularized |  2116.38 +/- 341.5 | 0.29 +/- 0.01 | 3057.75 +/- 504.26 |
| Random Forest Regressor       |  837.66 +/- 218.22 | 0.12 +/- 0.02 | 1255.81 +/- 318.76 |
| XGBoost Regressor             | 1045.83 +/- 182.93 | 0.14 +/- 0.02 |  1509.2 +/- 260.07 |

## 6.4. Escolha do Modelo
Embora o algoritmo ***Random Fores Regressor*** tenha sido o algoritmo que melhor performou, foi optado pelo algoritmo ***XGBosst Regressor*** nesta etapa. 
- Primeiro, porque o erro entre esses dois algoritmos é pequeno.
- segundo porque o tempo de treinamento do ***XGBoost Regressor*** é mais rápido se comparado ao algoritmo ***Random Fores Regressor***. 
- Terceiro porque o modelo final treinado pelo algoritmo ***XGBoost Regressor*** ocupa menos espaço que o algoritmo ***Random Fores Regressor***, deixando assim o uso de servidores em nuvem mais baratos.

## 6.5. Ajuste de Hiperparâmetros
Foi o utilizado a técnica de ***Random Search*** para fazer a busca dos melhores hyperparâmetros. Os testes realizados foram os seguintes:

| Tentativa |             MAE CV |       MAPE CV |            RMSE CV |
| :-------: | -----------------: | ------------: | -----------------: |
|  Teste 1  | 1298.59 +/- 145.92 | 0.18 +/- 0.01 | 1876.77 +/- 183.35 |
|  Teste 2  |  805.51 +/- 136.41 | 0.11 +/- 0.01 | 1178.01 +/- 207.34 |
|  Teste 3  |   1047.9 +/- 138.9 | 0.15 +/- 0.01 | 1509.67 +/- 188.21 |
|  Teste 4  |  806.21 +/- 129.75 | 0.11 +/- 0.01 | 1173.31 +/- 200.39 |
|  Teste 5  | 1028.34 +/- 126.16 | 0.14 +/- 0.01 | 1472.95 +/- 162.73 |
|  Teste 6  | 1521.97 +/- 165.69 | 0.21 +/- 0.01 | 2204.28 +/- 210.19 |
|  Teste 7  |  1307.5 +/- 132.12 | 0.18 +/- 0.01 | 1896.64 +/- 182.21 |
|  Teste 8  |  889.96 +/- 123.96 | 0.12 +/- 0.01 | 1278.13 +/- 179.34 |
|  Teste 9  |  797.98 +/- 155.47 | 0.11 +/- 0.01 |  1157.82 +/- 228.1 |
| Teste 10  |  1081.47 +/- 115.4 | 0.15 +/- 0.01 | 1546.74 +/- 159.11 |

Sendo que os parâmetros do **Teste 4** foram os selecionados como os melhores parâmetros para o treinamento do modelo.

## 6.6. Performance do Modelo
Como podemos observar nos dois primeiro gráficos abaixo, o modelo selecionado obteve uma performance aceitável, visto que conseguiu entender e reproduzir o padrão de vendas ao longo dos anos estudados.

Já nos dois últimos gráficos, podemos observar uma distribuição normal a cerca das previsões, o que nos inidica um bom resultado do modelo selecionado, além de podermos verificar a distribuição dos erros do modelo.

![](api/img/performance.png)

# 7. Resultado de Negócio
Com o modelo selecionado e treinado, obtivemos a seguinte performance de negócio para as 5 melhores lojas:

| ID da Loja |     Previsões |  Pior Cenário | Melhor Cenário |       MAE |   MAPE |
| :--------- | ------------: | ------------: | -------------: | --------: | -----: |
| 259        | \$ 542,261.00 | \$ 541,643.54 |  \$ 542,878.46 | \$ 617.46 | 0.0483 |
| 990        | \$ 235,996.80 | \$ 235,689.77 |  \$ 236,303.82 | \$ 307.03 | 0.0485 |
| 1089       | \$ 378,721.16 | \$ 378,205.41 |  \$ 379,236.90 | \$ 515.75 | 0.0488 |
| 1097       | \$ 440,957.44 | \$ 440,370.68 |  \$ 441,544.20 | \$ 586.76 | 0.0541 |
| 667        | \$ 314,811.66 | \$ 314,324.37 |  \$ 315,298.95 | \$ 487.29 | 0.0551 |


Um ponto importante de ressaltar, é que houveram algumas lojas que não obtiveram bons resultados, e que em uma próxima iteração deve ser tratadas individualmente para verificar qual pode ser o problema para essas lojas. As 5 piores lojas tiveram a seguinte performance:


| ID da Loja |     Previsões |  Pior Cenário | Melhor Cenário |         MAE |  MAPE |
| :--------- | ------------: | ------------: | -------------: | ----------: | ----: |
| 292        | \$ 103,891.24 | \$ 100,561.08 |  \$ 107,221.41 | \$ 3,330.17 | 0.562 |
| 909        | \$ 237,516.14 | \$ 229,953.85 |  \$ 245,078.43 | \$ 7,562.29 | 0.511 |
| 876        | \$ 206,953.81 | \$ 202,905.53 |  \$ 211,002.09 | \$ 4,048.28 | 0.316 |
| 722        | \$ 353,882.56 | \$ 351,866.71 |  \$ 355,898.42 | \$ 2,015.85 | 0.268 |
| 274        | \$ 195,549.67 | \$ 194,157.14 |  \$ 196,942.21 | \$ 1,392.54 | 0.244 |


Como resultado final, temos os seguintes cenários:

| Cenários       |           Valores |
| :------------- | ----------------: |
| Previsão Feita | \$ 285,901,376.00 |
| Pior Cenário   | \$ 285,158,456.49 |
| Melhor Cenário | \$ 286,644,307.44 |

## 7.1. Distribuição das Previsões por Loja
![](api/img/business_performance.png)


# 8. Conclusões
Conforme pôde ser verificado, o projeto resolveu o problema inicial, que era a previsão de faturamento das lojas feitas de forma manual por seus gerentes.

Outro ponto importante de destacar é que com a solução criada, o CFO pode agora consultar as lojas de forma automática utilizando o BOT criado, dando mais agilidade na tomada de decisão.

# 9. Lições Aprendidas
* Priorizar tarefas e soluções
* Desenvolver soluções de forma cíclica, entregando assim resultado mais rapidamente
* Construção de um BOT para o aplicativo de mensagens Telegram, afim de agilizar o acesso à informações.

# 10. Próximos Passos

* Realizar uma investigação detalhada para identificar as causas das previsões inadequadas em algumas lojas.
* Explorar a inclusão de diferentes algoritmos durante a próxima fase de treinamento, com o objetivo de aprimorar a precisão das previsões.
* Desenvolver uma aplicação web usando o framework Streamlit, permitindo que os gerentes das lojas acessem e visualizem as previsões de forma fácil e intuitiva.
* Implementar testes unitários abrangentes para validar a funcionalidade das classes e funções desenvolvidas.
* Identificar e criar novas variáveis (features) que possam contribuir para melhorar o desempenho do modelo atual e futuros modelos de previsão.
* Aplicar técnicas avançadas de programação para otimizar a eficiência e o desempenho da solução.

* Investigar a razão de algumas lojas estarem com previsões ruins
* Selecionar outros algoritmos para treinamento no próximo ciclo, a fim de buscar uma solução que melhore o desempenho da previsão
* Criar uma apllicação Web utilizando o framework Streamlit para dar acesso Web às previsões para os gerentes das lojas.
* Implementar testes unitários nas classes e funções produzidas.
* Criar novas *Features* para tentar melhorar a perfomance do modelo atual e de modelos futuros.
* Aplicar técnicas de programação para melhorar o desempenho da solução criada.
