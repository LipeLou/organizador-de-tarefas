import os
import pandas as pd
from datetime import datetime
from src.plot_service import plotar_pizza_tarefas, plotar_progresso, exibir_plot
from src.email_service import enviar_email_relatorio

class ListaTarefas:
    def __init__(self, arquivo_csv='tarefas.csv'):
        self.arquivo_csv = arquivo_csv
        if os.path.exists(self.arquivo_csv):
            self.tarefas = pd.read_csv(self.arquivo_csv, index_col=0)
            # Garantir que colunas de data sejam datetime, se necessário, mas pandas geralmente lê como object/string.
            # Conversões podem ser feitas sob demanda.
        else:
            self.tarefas = pd.DataFrame(columns=['nome', 'prioridade', 'prazo', 'status', 'descricao', 'data_criacao', 'horario_inicio', 'tempo_total'])

    def adicionar_tarefa(self, tarefa):
        self.tarefas = pd.concat([self.tarefas, tarefa.to_df()], ignore_index=True)

    def salvar_tarefas(self):
        self.tarefas.to_csv(self.arquivo_csv)

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
            # Recupera horario_inicio e converte para datetime se for string
            inicio = pd.to_datetime(self.tarefas.loc[self.tarefas['nome'] == nome, 'horario_inicio'])
            self.tarefas.loc[self.tarefas['nome'] == nome, 'tempo_total'] = datetime.now() - inicio
            print(f'Tarefa {nome} concluída com sucesso!')
        else:
            print(f'A tarefa {nome} não pode ser concluída.')

    def editar_tarefa(self, nome, novo_nome, nova_prioridade, novo_prazo):
        mask = self.tarefas['nome'] == nome
        if novo_nome:
            self.tarefas.loc[mask, 'nome'] = novo_nome
        if nova_prioridade:
            self.tarefas.loc[mask, 'prioridade'] = nova_prioridade
        if novo_prazo:
            self.tarefas.loc[mask, 'prazo'] = novo_prazo
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
        nao_iniciado = self.tarefas.loc[self.tarefas['status']=='Não iniciada']
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
            print('Tarefa não encontrada.')
        else:
            self.tarefas = self.tarefas.loc[self.tarefas['nome'] != nome_tarefa]
            print(f'Tarefa "{nome_tarefa}" removida.')

        self.tarefas.reset_index(drop=True, inplace=True)
        self.salvar_tarefas()

    def selecionar_tarefa_mais_urgente(self):
        # Cria colunas temporárias para cálculo, mas idealmente não devia alterar o self.tarefas permanentemente com essas colunas auxiliares se não for o objetivo.
        # No código original altera. Vou manter o comportamento.
        
        self.tarefas.loc[self.tarefas['prioridade'] == 'Alta', 'peso_prioridade'] = 3
        self.tarefas.loc[self.tarefas['prioridade'] == 'Média', 'peso_prioridade'] = 2
        self.tarefas.loc[self.tarefas['prioridade'] == 'Baixa', 'peso_prioridade'] = 1

        self.tarefas.loc[self.tarefas['status'] == 'Em andamento', 'peso_status'] = 2
        self.tarefas.loc[self.tarefas['status'] == 'Não iniciada', 'peso_status'] = 3
        self.tarefas.loc[self.tarefas['status'] == 'Concluída', 'peso_status'] = 1

        self.tarefas['peso_urgencia'] = self.tarefas['peso_prioridade'] + self.tarefas['peso_status'] 

        if self.tarefas.empty:
             print('Nenhuma tarefa para analisar.')
             return

        maior_peso = self.tarefas['peso_urgencia'].max()
        tarefas_urgentes = self.tarefas.loc[self.tarefas['peso_urgencia']==maior_peso]

        tarefas_urgentes = tarefas_urgentes.sort_values(by= 'prazo', ascending=True)
        print('=== Tarefa urgente! ===')
        print(f'Tarefa: {tarefas_urgentes.iloc[0]["nome"]}') 
        print(f'Prioridade: {tarefas_urgentes.iloc[0]["prioridade"]}')
        print(f'Prazo: {tarefas_urgentes.iloc[0]["prazo"]}')
        print(f'Status: {tarefas_urgentes.iloc[0]["status"]}')
        print('===================')

        self.salvar_tarefas()

    def gerar_estatisticas(self):
        tarefas_totais = self.tarefas.shape[0]
        tarefas_concluidas = self.tarefas.loc[self.tarefas['status'] == 'Concluída'].copy()
        numero_tarefas_concluidas = tarefas_concluidas.shape[0]
        tarefas_pendentes = tarefas_totais - numero_tarefas_concluidas
        progresso = (numero_tarefas_concluidas/tarefas_totais * 100) if tarefas_totais > 0 else 0
        
        if numero_tarefas_concluidas == 0:
            tempo_medio = 0
            tempo_total = 0
        else:
            tarefas_concluidas['duracao_horas'] = pd.to_timedelta(tarefas_concluidas['tempo_total']).dt.total_seconds() / 3600
            tempo_medio = tarefas_concluidas['duracao_horas'].mean()
            tempo_total = tarefas_concluidas['duracao_horas'].sum()

        return tarefas_totais, numero_tarefas_concluidas, tarefas_pendentes, progresso, tempo_medio, tempo_total

    def exibir_estatisticas(self):
        tarefas_totais, numero_tarefas_concluidas, tarefas_pendentes, progresso, tempo_medio, tempo_total = self.gerar_estatisticas()
        print('======Estatísticas=======')
        print(f'Tarefas Totais: {tarefas_totais}')
        print(f'Tarefas Concluídas: {numero_tarefas_concluidas}')
        print(f'Tarefas Pendentes: {tarefas_pendentes}')
        print(f'Progresso: {round(progresso,2)}%')
        print(f'Tempo médio por tarefa: {round(tempo_medio,2)} horas')
        print(f'Tempo total gasto: {round(tempo_total,2)} horas')
        print('=========================')

    def plot_tarefas(self, by_status=True):
        return plotar_pizza_tarefas(self.tarefas, by_status)

    def plot_progress(self):
        return plotar_progresso(self.tarefas)
    
    def exibir_plot(self, fig):
        exibir_plot(fig)

    def enviar_relatorio_por_email(self, destinatario=None):
        tarefas_totais, tarefas_concluidas, tarefas_pendentes, progresso, tempo_medio, tempo_total = self.gerar_estatisticas()

        texto = f'''
Olá, seu relatório de tarefas chegou!\n
Seu progresso neste projeto é de {round(progresso, 1)}%.\n
O número total de tarefas é: {tarefas_totais}.\n
Destas, {tarefas_concluidas} foram concluídas e {tarefas_pendentes} estão pendentes.\n
O tempo médio em cada tarefa é {round(tempo_medio, 2)} horas e o tempo total executando as tarefas é de {round(tempo_total, 2)} horas.\n
Seguem anexos os gráficos de estatísticas.
'''

        texto_html = f'''
                <html>
                <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; color: #333333; padding: 20px;">
                    <div style="max-width: 600px; margin: auto; background-color: #ffffff; border: 1px solid #dddddd; border-radius: 8px; padding: 20px;">
                    <h2 style="color: #2c3e50;">Relatório de Tarefas</h2>
                    <p style="font-size: 16px;">Olá, seu relatório de tarefas chegou!</p>
                    <p style="font-size: 16px; line-height: 1.6;">
                        Seu progresso neste projeto é de <strong>{round(progresso, 1)}%</strong>.<br>
                        O número total de tarefas é: <strong>{tarefas_totais}</strong>.<br>
                        Destas, <strong>{tarefas_concluidas}</strong> foram concluídas e <strong>{tarefas_pendentes}</strong> estão pendentes.<br>
                        O tempo médio em cada tarefa é <strong>{round(tempo_medio, 2)} horas</strong> e o tempo total executando as tarefas é de <strong>{round(tempo_total, 2)} horas</strong>.
                    </p>
                    <p style="font-size: 16px;">Seguem anexos os gráficos de estatísticas.</p>
                    </div>
                </body>
                </html>
                '''
        
        # Gera e salva os gráficos
        self.plot_tarefas(by_status=True)
        self.plot_tarefas(by_status=False)
        self.plot_progress()

        arquivos_anexos = [
            os.path.join('img', 'tarefas-por-prioridade.png'),
            os.path.join('img', 'tarefas-por-status.png'),
            os.path.join('img', 'progresso.png')
        ]

        enviar_email_relatorio(destinatario, 'Relatório tarefas', texto, texto_html, arquivos_anexos)

