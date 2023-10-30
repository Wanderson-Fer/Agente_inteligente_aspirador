from time import sleep

import random
import os


class AgenteAspirador:
    def __init__(self):
        self.energia = 100
        self.bolsa = 0
        self.localizacao = (0, 0)
        self.ambiente = [[0, 1, 0, 0],
                         [1, 0, 0, 1],
                         [0, 0, 1, 0],
                         [1, 0, 0, 0]]
        # Inicializa a Q-table, que armazena valores Q para cada ação em cada estado
        self.q_table = {}
        self.epsilon = 0.3  # Taxa de exploração inicial

    def verificar_sujeira(self):
        x, y = self.localizacao
        return self.ambiente[y][x] == 1

    def aspirar(self):
        x, y = self.localizacao
        self.bolsa += 1
        self.ambiente[y][x] = 0
        print(f"Aspirei sujeira em ({x}, {y}).")

    def mover(self, direcao):
        x, y = self.localizacao
        if direcao == 'cima' and y > 0:
            self.localizacao = (x, y - 1)
        elif direcao == 'baixo' and y < 3:
            self.localizacao = (x, y + 1)
        elif direcao == 'esquerda' and x > 0:
            self.localizacao = (x - 1, y)
        elif direcao == 'direita' and x < 3:
            self.localizacao = (x + 1, y)
        self.energia -= 1

    def voltar_para_casa(self):
        x, y = self.localizacao
        if x > 0:
            while self.localizacao != (0, y):
                self.mover('esquerda')
        if y > 0:
            while self.localizacao != (0, 0):
                self.mover('cima')
        self.energia = 100

    def bolsa_cheia(self):
        return self.bolsa == 10

    def atualizar_q_table(self, state, action, reward, next_state):
        state = str(state)
        if state not in self.q_table:
            self.q_table[state] = [0, 0, 0, 0]  # Q-values for the four possible actions
        if next_state not in self.q_table:
            self.q_table[next_state] = [0, 0, 0, 0]

        max_next_q_value = max(self.q_table[next_state])
        current_q_value = self.q_table[state][action]
        # taxa de aprendizado = 0.2 | taxa de desconto = 0.8
        self.q_table[state][action] = current_q_value + 0.2 * (reward + 0.8 * max_next_q_value - current_q_value)

    def escolher_acao(self):
        state = str(self.localizacao)
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([0, 1, 2, 3])  # Ação aleatória
        else:
            q_values = self.q_table.get(state)
            if q_values:
                return q_values.index(max(q_values))
            else:
                return random.choice([0, 1, 2, 3])

    def sensors(self):
        print(f'posição atual {self.localizacao}\n')
        for line in self.ambiente:
            print(line)

    def quarto_limpo(self):
        for line in self.ambiente:
            for value in line:
                if value:
                    return False

        return True

    def limpar_quarto(self, max_ep=100):
        ep = 0
        while ep < max_ep:
            self.sensors()

            if self.bolsa_cheia():
                self.voltar_para_casa()
            elif self.quarto_limpo():
                print('O quarto foi limpo.')
                print("Objetivo alcançado!")
                break
            elif self.energia > 0:
                action = self.escolher_acao()
                self.mover(['cima', 'baixo', 'esquerda', 'direita'][action])
                next_state = str(self.localizacao)

                if self.verificar_sujeira():
                    self.aspirar()
                    reward = 1
                else:
                    reward = -1

                self.atualizar_q_table(self.localizacao, action, reward, next_state)
            else:
                print('Sem energia...')
                break

            os.system('cls')
            sleep(0.4)  # hehehe

            ep += 1

        else:
            print('Número máximo de épocas alcançados!')


if __name__ == "__main__":
    agente = AgenteAspirador()
    agente.limpar_quarto()
