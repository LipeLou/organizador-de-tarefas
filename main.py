from datetime import datetime, timedelta
import pandas as pd
import os
from matplotlib import pyplot as plt

class Tarefa:
    def __init__(self, nome, prioridade, prazo):
        self.nome = nome
        self.prioridade = prioridade
        self.prazo = prazo
        self.status = "Não iniciada"
        self.data_criacao = datetime.now()
        self.horario_inicio = None
        self.tempo_total = None

    def iniciar(self):
        if self.status == "Não iniciada" and self.horario_inicio is None:
            self.horario_inicio = datetime.now()
            self.status = 'Em andamento'
            print(f"Tarefa '{self.nome}' iniciada em {self.horario_inicio}")
        else:
            print(f"A tarefa '{self.nome}' já foi iniciada ou concluída.")

    def finalizar(self):
        if self.horario_inicio:
            self.tempo_total = datetime.now() - self.horario_inicio
            self.status = "Concluída"
            print(f"Tarefa '{self.nome}' finalizada. Tempo total: {self.tempo_total}")
        else:
            print(f"A tarefa '{self.nome}' precisa ser iniciada antes de ser concluída.")

    def editar(self, nome=None, prioridade=None, prazo=None):
        if nome:
            self.nome = nome
        if prioridade:
            self.prioridade = prioridade
        if prazo:
            self.prazo = prazo
        print(f"Tarefa '{self.nome}' foi editada com sucesso.")

    def to_df(self):
        return pd.DataFrame([{
            "nome": self.nome,
            "prioridade": self.prioridade,
            "prazo": self.prazo,
            "status": self.status,
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "horario_inicio": self.horario_inicio,
            "tempo_total": self.tempo_total
        }])

    def __str__(self):
        return f"{self.nome} | Prioridade: {self.prioridade} | Prazo: {self.prazo} | Status: {self.status}"


class ListaTarefas:
    def __init__(self):
        if os.path.exists('tarefas.csv'):
            self.tarefas = pd.read_csv('tarefas.csv', index_col=0)
        else:
            self.tarefas = pd.DataFrame(columns=["nome", "prioridade", "prazo", "status", "data_criacao", "horario_inicio", "tempo_total"])

    def adicionar_tarefa(self, tarefa):
        self.tarefas = pd.concat([self.tarefas, tarefa.to_df()], ignore_index=True)

    def salvar_tarefas(self):
        self.tarefas.to_csv('tarefas.csv')

    def iniciar_tarefa(self, nome):
        if (self.tarefas.loc[self.tarefas['nome'] == nome, 'status'] == 'Não iniciada').any():
            self.tarefas.loc[self.tarefas['nome'] == nome, 'status'] = 'Em andamento'
            self.tarefas.loc[self.tarefas['nome'] == nome, 'horario_inicio'] = datetime.now()
            print(f'Tarefa {nome} iniciada com sucesso!')
        else: 
            print(f'Tarefa {nome} já foi iniciada.')

    def finalizar_tarefa(self, nome):
        if (self.tarefas.loc[self.tarefas['nome'] == nome, 'status'] == 'Em andamento').any():
            self.tarefas.loc[self.tarefas['nome'] == nome, 'status'] = 'Concluída'
            self.tarefas.loc[self.tarefas['nome'] == nome, 'tempo_total'] = datetime.now() - pd.to_datetime(self.tarefas.loc[self.tarefas['nome'] == nome, 'horario_inicio'])
            print(f'Tarefa {nome} concluída com sucesso!')
        else:
            print(f'A tarefa {nome} não pode ser concluída.')

    def editar_tarefa(self, nome, novo_nome, nova_prioridade, novo_prazo):
        if novo_nome:
            self.tarefas.loc[self.tarefas['nome'] == nome, 'nome'] = novo_nome
        if nova_prioridade:
            self.tarefas.loc[self.tarefas['nome'] == nome, 'prioridade'] = nova_prioridade
        if novo_prazo:
            self.tarefas.loc[self.tarefas['nome'] == nome, 'prazo'] = novo_prazo
        print('Tarefa editada com sucesso')

    def exibir_tarefas_por_prioridade(self):
        alta = self.tarefas.loc[self.tarefas['prioridade']=='Alta']
        media = self.tarefas.loc[self.tarefas['prioridade']=='Média']
        baixa = self.tarefas.loc[self.tarefas['prioridade']=='Baixa']

        if not alta.empty:
            print('=== Prioridade Alta ====')
            for idx, row in alta.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")
        if not media.empty:
            print('=== Prioridade Média ====')
            for idx, row in media.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")
        if not baixa.empty:
            print('=== Prioridade Baixa ====')
            for idx, row in baixa.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")

    def exibir_tarefas_por_status(self):
        nao_iniciado = self.tarefas.loc[self.tarefas['status']=="Não iniciada"]
        iniciado = self.tarefas.loc[self.tarefas['status']=='Em andamento']
        concluido = self.tarefas.loc[self.tarefas['status']=='Concluída']

        if not nao_iniciado.empty:
            print('=== Não Iniciadas ====')
            for idx, row in nao_iniciado.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")
        if not iniciado.empty:
            print('=== Em andamento ====')
            for idx, row in iniciado.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")
        if not concluido.empty:
            print('=== Concluídas ====')
            for idx, row in concluido.iterrows():
                print(f"{row['nome']} | Prioridade: {row['prioridade']} | Prazo: {row['prazo']} | Status: {row['status']}")

    def remover_tarefa(self, nome_tarefa):
        if not nome_tarefa in list(self.tarefas['nome']):
            print("Tarefa não encontrada.")
        else:
            self.tarefas = self.tarefas.loc[self.tarefas['nome'] != nome_tarefa]
            print(f"Tarefa '{nome_tarefa}' removida.")

        self.tarefas.reset_index(drop=True, inplace=True)
        self.salvar_tarefas()

    def selecionar_tarefa_mais_urgente(self):
        self.tarefas.loc[self.tarefas['prioridade'] == 'Alta', 'peso_prioridade'] = 3
        self.tarefas.loc[self.tarefas['prioridade'] == 'Média', 'peso_prioridade'] = 2
        self.tarefas.loc[self.tarefas['prioridade'] == 'Baixa', 'peso_prioridade'] = 1

        self.tarefas.loc[self.tarefas['status'] == 'Em andamento', 'peso_status'] = 2
        self.tarefas.loc[self.tarefas['status'] == 'Não iniciada', 'peso_status'] = 3
        self.tarefas.loc[self.tarefas['status'] == 'Concluída', 'peso_status'] = 1

        self.tarefas['peso_urgencia'] = self.tarefas['peso_prioridade'] + self.tarefas['peso_status'] 

        maior_peso = self.tarefas['peso_urgencia'].max()
        tarefas_urgentes = self.tarefas.loc[self.tarefas['peso_urgencia']==maior_peso]

        tarefas_urgentes = tarefas_urgentes.sort_values(by= 'prazo', ascending=True)
        print("=== Tarefa urgente! ===")
        print(f'Tarefa: {tarefas_urgentes.iloc[0]['nome']}') 
        print(f'Prioridade: {tarefas_urgentes.iloc[0]['prioridade']}')
        print(f'Prazo: {tarefas_urgentes.iloc[0]['prazo']}')
        print(f'Status: {tarefas_urgentes.iloc[0]['status']}')
        print("===================")

        self.salvar_tarefas()

    def gerar_estatisticas(self):
        tarefas_totais = self.tarefas.shape[0]
        tarefas_concluidas = self.tarefas.loc[self.tarefas['status'] == 'Concluída'].copy()
        numero_tarefas_concluidas = tarefas_concluidas.shape[0]
        tarefas_pendentes = tarefas_totais - numero_tarefas_concluidas
        progresso = numero_tarefas_concluidas/tarefas_totais * 100
        if numero_tarefas_concluidas == 0:
            tempo_medio = 0
            tempo_total = 0
        else:
            tarefas_concluidas['duracao_horas'] = pd.to_timedelta(tarefas_concluidas['tempo_total']).dt.total_seconds() / 3600
            tempo_medio = tarefas_concluidas['duracao_horas'].mean()
            tempo_total = tarefas_concluidas['duracao_horas'].sum()

        print("======Estatísticas=======")
        print(f'Tarefas Totais: {tarefas_totais}')
        print(f'Tarefas Concluídas: {tarefas_concluidas}')
        print(f'Tarefas Pendentes: {tarefas_pendentes}')
        print(f'Progresso: {round(progresso,2)}%')
        print(f'Tempo médio por trefa: {round(tempo_medio,2)} horas')
        print(f'Tempo total gasto: {round(tempo_total,2)} horas')
        print("===================")

    def plot_tarefas(self, by_status=True):
        coluna = 'status' if by_status else 'prioridade'
        dados = self.tarefas.groupby(coluna)['nome'].count()

        fig, ax = plt.subplots(figsize=(7, 7))
        wedges, texts, autotexts = ax.pie(
            dados,
            labels=dados.index,
            autopct='%1.1f%%',
            explode=[0.01] * len(dados),
            colors=['#FF9800','#4CAF50','#2196F3'],
        )

        for text in texts:
            text.set_fontsize(10)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)

        ax.set_title(f'Distribuição de Tarefas por {coluna.capitalize()}', fontsize=14)
        plt.savefig(f'tarefas-por-{coluna}.png')
        return plt.show()

    def plot_progress(self):
        total = self.tarefas.shape[0]
        concluidas = self.tarefas[self.tarefas['status'] == 'Concluída'].shape[0]
        p_concluidas = (concluidas / total) * 100
        p_nao_concluidas = 100 - p_concluidas

        fig, ax = plt.subplots(figsize=(8, 2))

        ax.barh([''], [p_concluidas], color='g', label=f'Concluído ({p_concluidas:.1f}%)')
        ax.barh([''], [p_nao_concluidas], left=[p_concluidas], color='0.95', label=f'Não Concluído ({p_nao_concluidas:.1f}%)')

        ax.set_xlim(0, 100)
        ax.set_title('Progresso Geral das Tarefas', fontsize=13)
        ax.set_xlabel('Porcentagem')
        ax.get_yaxis().set_visible(False)

        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.savefig('progresso.png')
        return plt.show()



def voltar_ao_menu():
    input('\nDigite algo para voltar ao menu. ')
    limpar_terminal()
    menu()

def limpar_terminal():
    os.system('cls')

def escolher_opcao():
    lista_tarefas = ListaTarefas()
    try: 
        opcao = int(input("Escolha uma opção: "))

        limpar_terminal()
        match opcao:
            case 1:
                nome = input("Digite o nome da tarefa: ")
                prioridade = input("Digite a prioridade (Alta, Média, Baixa): ").lower().capitalize()
                while prioridade not in ['Alta', 'Média', 'Baixa']:
                    print('Tente novamente.')
                    prioridade = input("Digite a prioridade (Alta, Média, Baixa): ").lower().capitalize()
                prazo = input("Digite o prazo (ex: 2023-12-31): ")
                prazo = datetime.strptime(prazo, "%Y-%m-%d")
                tarefa = Tarefa(nome, prioridade, prazo)
                confirm = input(f'Adicionar tarefa: {tarefa} | ?\n[S/N]: ').upper()[0]

                if confirm == 'S':
                    lista_tarefas.adicionar_tarefa(tarefa)
                    print(f"Tarefa '{nome}' adicionada com sucesso!")
                    lista_tarefas.salvar_tarefas()

                elif confirm == 'N':
                    print(f"Tarefa '{nome}' não foi adicionada.")
                voltar_ao_menu()

            case 2:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.exibir_tarefas_por_prioridade()
                voltar_ao_menu()

            case 3:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.exibir_tarefas_por_status()
                voltar_ao_menu()

            case 4:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero}. {tarefa}')
                    n = int(input("Digite número da tarefa que deseja iniciar: "))
                    if n <= len(lista_tarefas.tarefas):
                        lista_tarefas.iniciar_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print("Tarefa não encontrada.")
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 5:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero}. {tarefa}')
                    n = int(input("Digite número da tarefa que deseja finalizar: "))
                    if n <= len(lista_tarefas.tarefas):
                        lista_tarefas.finalizar_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print("Tarefa não encontrada.")
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 6:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero}. {tarefa}')
                    n = int(input("Digite número da tarefa que deseja remover: "))
                    if n <= len(lista_tarefas.tarefas):

                        lista_tarefas.remover_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print("Tarefa não encontrada.")
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 7:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero+1}. {tarefa}')
                    n = int(input("Digite número da tarefa que deseja editar: "))
                    if n <= len(lista_tarefas.tarefas):       
                        print(f'Editando tarefa: {lista_tarefas.tarefas['nome'][n]}')
                        novo_nome = input("Novo nome: ")
                        nova_prioridade = input("Nova prioridade (Alta, Média, Baixa): ")
                        novo_prazo = input("Novo prazo (ex: 2023-12-31): ")
                        novo_prazo = datetime.strptime(novo_prazo, "%Y-%m-%d") if novo_prazo else None
                        lista_tarefas.editar_tarefa(lista_tarefas.tarefas['nome'][n], novo_nome, nova_prioridade, novo_prazo)
                        lista_tarefas.salvar_tarefas()
                    else:
                        print("Tarefa não encontrada.")
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 8:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.selecionar_tarefa_mais_urgente()
                voltar_ao_menu()

            case 9:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.gerar_estatisticas()
                voltar_ao_menu()

            case 10:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.plot_tarefas(by_status=False)
                voltar_ao_menu()

            case 11:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.plot_tarefas(by_status=True)
                voltar_ao_menu()

            case 12:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.plot_progress()
                voltar_ao_menu()

            case 13:
                lista_tarefas.salvar_tarefas()
                limpar_terminal()
                print("=== Volte Sempre ===")

            case _:
                print("Opção inválida. Tente novamente.")
                menu()

    except:
        print("Opção inválida. Tente novamente.")
        menu()


def menu():
    limpar_terminal()
    print("\n=== Organizador de Tarefas com Prioridades ===")
    print("1. Adicionar Tarefa")
    print("2. Exibir Tarefas por Prioridade")
    print("3. Exibir Tarefas por Status")
    print("4. Iniciar Tarefa")
    print("5. Finalizar Tarefa")
    print("6. Remover Tarefa")
    print("7. Editar Tarefa")
    print("8. Selecionar tarefa mais urgente")
    print("9. Exibir estatísticas")
    print("10. Exbir gráfico Tarefas por Prioridade")
    print("11. Exbir gráfico Tarefas por Status")
    print("12. Exbir gráfico Progresso")
    print("13. Sair")
    escolher_opcao()




if __name__ == '__main__':
    menu()
