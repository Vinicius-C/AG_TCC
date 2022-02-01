import numpy as np

from AGUtil import AGUtil
from Individuo import Individuo


class AG(AGUtil):
    # Intervalo de Frequência que será gerado a curva
    intervalo_curva = None
    # Passos na geração da curva
    passos_curva = None
    # Passo que começa a banda da antena
    passo_comeco_banda = None
    # Passo que termina a banda da antena
    passo_fim_banda = None

    # Array contendo a curva com funcionamento ideal de absorção
    curva_referencia_a = []
    # Array contendo a curva com funcionamento ideal de transmissão
    curva_referencia_t = []
    # Array contendo a curva com funcionamento ideal de reflexão
    curva_referencia_r = []

    # Array contendo a curva com pesos para faixas de frequência para usar no fitness da absorção
    pesos = []

    # Fitness Última Geração
    ultimo_fitness = None
    # Faixa de Operação da Antena
    faixa_antena = None
    # Modo (1-TE, 2-TM)
    modo = None
    # Angulo de Incidencia
    angulo_incidencia = None
    # Tamanho da Geracao
    tamanho_geracao = None
    # Taxa de Mutação
    taxa_mutacao = None
    # Taxa de Crossover
    ultrapassagem_crossover = None
    # Quantidade de Selecionados
    n_selecionados = None
    # Geração
    geracao = []
    # Rank Weight
    rank_weight = []
    # Quantidade de Filhos por Casal
    n_filhos = None
    # Característica a Ser Otimizada(r - Reflexão, t - Transmissão, a - Absorção)
    otimizacao = None
    # Ag com 100% de liberdade sobre o substrato
    busca_dieletrico = None
    # Permissividade relativa
    # Essa variável existirá quando o dielétrico for definido
    er = None
    # Permeabilidade relativa
    # Essa variável existirá quando o dielétrico for definido
    ur = None
    # Intervalo de frequencia para ocorrer Salisbury's Screen
    # Essa variável existirá quando o dielétrico for definido,
    # assim limitando o intervalo de busca do ag sobre a largura do dielétrico
    intervalo_salisbury = None
    # Limite inferior de l para ocorrer Salisbury's Screen
    # Essa variável existirá quando o dielétrico for definido
    l_inf = None
    # Limite superior de l para ocorrer Salisbury's Screen
    # Essa variável existirá quando o dielétrico for definido
    l_sup = None

    # Dados da espira passa-faixa selecionada anteriormente
    espira_passa_faixa = None
    dados = None

    def __init__(self):
        super().__init__()

    def nova_geracao(self, funcao_fitness, funcao_crossover):
        # Selecionar melhores
        selecionados = []
        # Setar o início da lista de fitness dos selecionados com 9999
        fitness_selecionados = [9999999]
        # Para cada indivíduo verificar se ele se encaixa na lista de selecionados (Quando esse for menor que algum
        # dos n indivíduos já selecionados, encaixar este indivíduo na posição do que ele é menor)
        for j in range(self.tamanho_geracao):
            #print(str(funcao_fitness(self.geracao[j])["fitness"]))
            fitness_j = funcao_fitness(self.geracao[j])["fitness"]
            for k in range(self.n_selecionados):
                if fitness_j < fitness_selecionados[k]:
                    selecionados.insert(k, self.geracao[j])
                    fitness_selecionados.insert(k, fitness_j)
                    break
                    # Se for maior que um da lista de selecionados já pode pausar
                elif len(fitness_selecionados) <= k + 1:
                    break
                    # Se não existir mais para comparar já pode pausar

        if len(selecionados) == 0:
            for j in range(self.tamanho_geracao):
                #print(str(self.geracao[j].p))
                fitness_j = funcao_fitness(self.geracao[j])["fitness"]
                for k in range(self.n_selecionados):
                    if fitness_j < fitness_selecionados[k]:
                        selecionados.insert(k, self.geracao[j])
                        fitness_selecionados.insert(k, fitness_j)
                        break
                        # Se for maior que um da lista de selecionados já pode pausar
                    elif len(fitness_selecionados) <= k + 1:
                        break
                        # Se não existir mais para comparar já pode pausar

        # Substituir geração
        self.geracao = selecionados

        for l in range(self.tamanho_geracao - len(selecionados)):
            # Selecionar pelo rank weighting macho e fêmea
            macho = self.selecionar_mate(selecionados, len(selecionados))
            femea = self.selecionar_mate(selecionados, len(selecionados))

            # Gera o filho
            filho = funcao_crossover(macho, femea)
            filho.mutacao(self.taxa_mutacao, self.busca_dieletrico, self.l_inf, self.l_sup,
                          self.intervalo_salisbury, self.angulo_incidencia, self.dados)

            self.geracao.append(filho)

        return selecionados[0]

    def set_geracao(self, funcao_gerar):
        self.geracao = []
        for j in range(self.tamanho_geracao):
            self.geracao.append(funcao_gerar())

    def crossover(self, n, macho, femea):
        # Ultrapassagem do crossover, assim será possivel o filho ter um valor fora do intervalo dos pais
        n = n

        p = AGUtil.combinar_real(
            n,
            np.array(self.dados["INTERVALO_P_PRIMEIRO_ESPIRA_VALIDO"]),
            macho.p,
            femea.p
        )

        d = AGUtil.combinar_real(
            n,
            np.array(self.dados["INTERVALO_D/P_PRIMEIRO_ESPIRA_VALIDO"]) * p,
            macho.d,
            femea.d
        )

        w = AGUtil.combinar_real(
            n,
            np.array(self.dados["INTERVALO_W/D_PRIMEIRO_ESPIRA_VALIDO"]) * d,
            macho.w,
            femea.w
        )

        r = AGUtil.combinar_real(
            n,
            self.dados["INTERVALO_R_PRIMEIRO_ESPIRA_VALIDO"],
            macho.r,
            femea.r
        )

        resultado = Individuo()
        resultado.set_espira_quadrada(d, w, p, r)

        return resultado
