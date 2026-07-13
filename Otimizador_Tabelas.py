import numpy as np

class OtimizadorTabela:
    def __init__(self, num_times: int):
    
        if num_times % 2 != 0:
            raise ValueError("O número de times deve ser par.")
            
        self.num_times = num_times
        self.num_rodadas_turno = num_times - 1
        self.num_rodadas_total = self.num_rodadas_turno * 2
        
    
        self.matriz_rivalidade = np.zeros((num_times, num_times), dtype=int)
        
        self.vetor_datas = []

    def gerar_solucao_inicial(self) -> np.ndarray:
        
        tabela = np.zeros((self.num_times, self.num_rodadas_total), dtype=int)
        times = list(range(1, self.num_times + 1))
        
        for rodada in range(self.num_rodadas_turno):
            for i in range(self.num_times // 2):
                time_a = times[i]
                time_b = times[self.num_times - 1 - i]
                
                if (rodada % 2 == 0):
                    tabela[time_a - 1][rodada] = time_b       
                    tabela[time_b - 1][rodada] = -time_a      
                else:
                    tabela[time_a - 1][rodada] = -time_b      
                    tabela[time_b - 1][rodada] = time_a       
                    
            times.insert(1, times.pop())
            
        for rodada in range(self.num_rodadas_turno):
            rodada_returno = rodada + self.num_rodadas_turno
            for i in range(self.num_times):
                tabela[i][rodada_returno] = -tabela[i][rodada]
                
        return tabela

    def calcular_penalidades(self, tabela: np.ndarray) -> int:
        penalidade_total = 0
        
        # Definição dos Pesos
        peso_seguranca_regional = 1000  
        peso_descanso_curto = 10        
        peso_inatividade = 5            
        peso_sequencia_fora = 5      
        
        for i in range(self.num_times):
            sequencia_visitante = 0
            for rodada in range(self.num_rodadas_total):
                if tabela[i][rodada] < 0:
                    sequencia_visitante += 1
                    if sequencia_visitante > 2:
                        penalidade_total += peso_sequencia_fora
                else:
                    sequencia_visitante = 0
                    
        for rodada in range(self.num_rodadas_total):
            mandantes = []
            for time in range(self.num_times):
                if tabela[time][rodada] > 0:
                    mandantes.append(time)
                    
            for i in range(len(mandantes)):
                for j in range(i + 1, len(mandantes)):
                    time_a = mandantes[i]
                    time_b = mandantes[j]
                    if self.matriz_rivalidade[time_a][time_b] == 1:
                        penalidade_total += peso_seguranca_regional

        if len(self.vetor_datas) == self.num_rodadas_total:
            for i in range(self.num_times):
                ultima_data_jogada = -1
                
                for rodada in range(self.num_rodadas_total):
                    if tabela[i][rodada] != 0:
                        data_atual = self.vetor_datas[rodada]
                        
                        if ultima_data_jogada != -1:
                            dias_descanso = data_atual - ultima_data_jogada
                            
                            if dias_descanso < 3:
                                penalidade_total += peso_descanso_curto
                            elif dias_descanso > 7:
                                penalidade_total += peso_inatividade
                                
                        ultima_data_jogada = data_atual
                        
        return penalidade_total

    def gerar_vizinhos_swap_rodadas(self, tabela_atual: np.ndarray) -> list:
       
        vizinhos = []
        for r1 in range(self.num_rodadas_total):
            for r2 in range(r1 + 1, self.num_rodadas_total):
                tabela_vizinha = np.copy(tabela_atual)
                tabela_vizinha[:, [r1, r2]] = tabela_vizinha[:, [r2, r1]]
                
                vizinhos.append({
                    "tabela": tabela_vizinha,
                    "movimento": f"Swap Rodadas: {r1} e {r2}"
                })
        return vizinhos

    def gerar_vizinhos_swap_mandante(self, tabela_atual: np.ndarray) -> list:
        vizinhos = []
        jogos_processados = set() 
        
        for time in range(self.num_times):
            for rodada in range(self.num_rodadas_total):
                adversario = abs(tabela_atual[time][rodada])
                id_jogo = tuple(sorted([time + 1, adversario])) + (rodada,)
                
                if id_jogo not in jogos_processados:
                    jogos_processados.add(id_jogo)
                    tabela_vizinha = np.copy(tabela_atual)
                    
                    tabela_vizinha[time][rodada] *= -1
                    tabela_vizinha[adversario - 1][rodada] *= -1
                    
                    vizinhos.append({
                        "tabela": tabela_vizinha,
                        "movimento": f"Swap Mandante: Time {id_jogo[0]} vs Time {id_jogo[1]} na Rodada {rodada}"
                    })
        return vizinhos

    def otimizar(self, max_iteracoes_sem_melhoria: int = 50, tamanho_tabu: int = 15) -> tuple[np.ndarray, int]:
    
        solucao_atual = self.gerar_solucao_inicial()
        melhor_solucao_global = np.copy(solucao_atual)
        
        custo_atual = self.calcular_penalidades(solucao_atual)
        melhor_custo_global = custo_atual
        
        lista_tabu = []
        iteracoes_estagnadas = 0
        
        print(f"Iniciando Busca Tabu\nCusto da Tabela Inicial: {melhor_custo_global}")
        
        while iteracoes_estagnadas < max_iteracoes_sem_melhoria and melhor_custo_global > 0:
            vizinhos_rodadas = self.gerar_vizinhos_swap_rodadas(solucao_atual)
            vizinhos_mandantes = self.gerar_vizinhos_swap_mandante(solucao_atual)
            todos_vizinhos = vizinhos_rodadas + vizinhos_mandantes
            
            melhor_vizinho_local = None
            menor_custo_local = float('inf')
            assinatura_escolhida = None
            
            for vizinho in todos_vizinhos:
                tabela_candidata = vizinho["tabela"]
                custo_candidato = self.calcular_penalidades(tabela_candidata)
                
                assinatura = tabela_candidata.tobytes()
                is_tabu = assinatura in lista_tabu
                criterio_aspiracao = custo_candidato < melhor_custo_global
                
                if not is_tabu or criterio_aspiracao:
                    if custo_candidato < menor_custo_local:
                        menor_custo_local = custo_candidato
                        melhor_vizinho_local = tabela_candidata
                        assinatura_escolhida = assinatura
            
            if melhor_vizinho_local is None:
                print("Preso em mínimo local irreversível")
                break
                
            solucao_atual = melhor_vizinho_local
            custo_atual = menor_custo_local
            
            lista_tabu.append(assinatura_escolhida)
            if len(lista_tabu) > tamanho_tabu:
                lista_tabu.pop(0) 
                
            if custo_atual < melhor_custo_global:
                melhor_custo_global = custo_atual
                melhor_solucao_global = np.copy(solucao_atual)
                iteracoes_estagnadas = 0 
                print(f"Melhoria encontrada! \nNovo Custo: {melhor_custo_global}")
            else:
                iteracoes_estagnadas += 1 
                
        print(f"\nBusca Finalizada. \nCusto da Melhor Tabela: {melhor_custo_global}")
        return melhor_solucao_global, melhor_custo_global

if __name__ == "__main__":
    NUM_TIMES = 4 
    otimizador = OtimizadorTabela(NUM_TIMES)
    

    otimizador.matriz_rivalidade[0][1] = 1
    otimizador.matriz_rivalidade[1][0] = 1
    
   
    otimizador.vetor_datas = [1, 2, 5, 15, 18, 21]
    
    print("-" * 60)
    print(f"ESTADO INICIAL: {NUM_TIMES} Equipes, {otimizador.num_rodadas_total} Rodadas")
    print("Legenda: +ID = Mandante | -ID = Visitante")
    print("-" * 60)
    
    solucao_base = otimizador.gerar_solucao_inicial()
    print("Matriz Gerada pelo Método do Polígono:")
    print(solucao_base)
    print("\n")
    
    melhor_tabela, penalidade_final = otimizador.otimizar(
        max_iteracoes_sem_melhoria=30, 
        tamanho_tabu=10
    )
    
    print("-" * 60)
    print("TABELA OTIMIZADA FINAL")
    print(melhor_tabela)
    print("-" * 60)