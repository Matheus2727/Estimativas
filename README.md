# Estimativas

> O objetivo do programa é ler uma base de dados de um arquivo excel e implementar metodos para realizar estimativas sobre o comportamento desses dados. O método de interpolação 
de Newton gera um polinomio interpolador para tentar reproduzir o comportamento dos dados (uma curva que passa por todos os pontos) e portante pode ser útil para determinar 
valores dentro do intervalo de dados (o polinomio pode variar de acordo com o input desejado, mesmo sem alterar a base de dados). O método de minimos quadrados gera um polinomio 
que não necessariamente cruza os pontos da base de dados, mas tenta minimizar os erros em relação a esses pontos, nesse caso o programa está equipado com regressão linear, entao 
gerará uma reta que melhor se ajusta aos pontos e portanto pode ser útil em previsões.

## Objetivos futuros:

As proximas atualizações do projeto terão como objetivo trazer as seguintes features:

- [ ] Novas opções de mínimos quadrados (polinomios de maior grau, curva exponencial, etc)
- [ ] Implementação de suporte para bancos SQL
- [ ] Melhorias na geração do polinomio interpolador do método de Newton

## Pré-requisitos

* São necessarias as versões mais recentes de: python, pygame, matplotlib e pandas
* Sistema operacional: Windows
