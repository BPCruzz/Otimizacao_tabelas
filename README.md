# Otimização de Tabelas de Campeonatos ⚽📅

Este repositório contém a implementação do Trabalho Prático 1 (TP1) para a disciplina de **Tópicos Especiais em Algoritmos (Otimização Heurística)** do Instituto Federal de Minas Gerais (IFMG) - Campus Ouro Branco.

## Sobre o Projeto

O projeto visa resolver o **Problema de Programação de Torneios** (*Sports League Scheduling Problem*) aplicado ao contexto crônico do calendário do futebol brasileiro. Através da metaheurística de **Busca Tabu**, o algoritmo busca gerar e otimizar a tabela do campeonato, minimizando o desgaste físico dos atletas e respeitando restrições rígidas de segurança pública e formato da competição.

## 👤 Autor
* **Bryan Parreiras Cruz** - Estudante de Sistemas de Informação

## Modelagem da Solução

### Função Objetivo
Minimizar a variação do tempo de descanso ideal dos elencos. A função aplica uma penalidade que cresce de forma acentuada sempre que uma equipe é forçada a jogar com menos de 3 dias de descanso ou acaba ficando mais de 7 dias inativa.

### Restrições
* **Rígidas (Hard Constraints):**
  * Preservação rigorosa do formato *Double Round-Robin* (todas as equipes têm obrigatoriamente que se enfrentar duas vezes, uma em casa e outra fora).
  * **Segurança Regional:** Equipes com forte rivalidade da mesma cidade ou região não devem atuar como mandantes na mesma data, visando não sobrecarregar a segurança pública.
* **Flexíveis (Soft Constraints):**
  * **Gestão de Mando de Campo:** Minimização do número de vezes que uma equipe é forçada a realizar jogos consecutivos na condição de visitante (idealmente não ultrapassando o limite de duas viagens consecutivas).

### Representação e Vizinhança
A tabela é modelada utilizando uma matriz bidimensional onde as linhas representam as equipes e as colunas representam as rodadas (datas). Os movimentos aplicados na Busca Tabu para encontrar melhores tabelas incluem:
* **Swap de Rodadas:** Inversão completa da disposição de todos os jogos entre duas datas.
* **Swap de Mandante:** Troca isolada do mando de campo em um jogo específico para corrigir infrações locais (como as da Segurança Regional).

## Como Funciona o Algoritmo
A Busca Tabu testa milhares de configurações silenciosamente, avaliando o custo através da função objetivo e aplicando os movimentos descritos. Utiliza uma **Lista Tabu** para evitar ficar presa em ótimos locais. O processo contínuo visa reduzir o custo operacional (ex: reduzindo penalidades na ordem de 1000 pontos) até encontrar uma solução ótima ou o limite de iterações sem melhorias globais ser alcançado.

## Referências Bibliográficas
A modelagem e os conceitos extraídos baseiam-se em:
1. HAMIEZ, J.-P.; HAO, J.-K. (2001). *Solving the sports league scheduling problem with tabu search*. Local Search for Planning and Scheduling, Springer.
2. RASMUSSEN, R. V.; TRICK, M. A. (2008). *Round robin scheduling – a survey*. European Journal of Operational Research.