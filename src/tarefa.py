from datetime import datetime
import pandas as pd
from src.ai_service import gerar_descricao_com_gpt

class Tarefa:
    def __init__(self, nome, prioridade, prazo, descricao=None, status='Não iniciada', data_criacao=None, horario_inicio=None, tempo_total=None):
        self.nome = nome
        self.prioridade = prioridade
        self.prazo = prazo
        self.status = status
        self.data_criacao = data_criacao if data_criacao else datetime.now()
        self.horario_inicio = horario_inicio
        self.tempo_total = tempo_total
        # Se a descrição for passada (ex: carregando do CSV), usa ela. Se não, gera nova.
        if descricao:
            self.descricao = descricao
        else:
            self.descricao = self.gerar_descricao()

    def iniciar(self):
        if self.status == 'Não iniciada' and self.horario_inicio is None:
            self.horario_inicio = datetime.now()
            self.status = 'Em andamento'
            print(f'Tarefa "{self.nome}" iniciada em {self.horario_inicio}')
        else:
            print(f'A tarefa "{self.nome}" já foi iniciada ou concluída.')

    def finalizar(self):
        if self.horario_inicio:
            self.tempo_total = datetime.now() - self.horario_inicio
            self.status = 'Concluída'
            print(f'Tarefa "{self.nome}" finalizada. Tempo total: {self.tempo_total}')
        else:
            print(f'A tarefa "{self.nome}" precisa ser iniciada antes de ser concluída.')

    def editar(self, nome=None, prioridade=None, prazo=None):
        if nome:
            self.nome = nome
        if prioridade:
            self.prioridade = prioridade
        if prazo:
            self.prazo = prazo
        print(f'Tarefa "{self.nome}" foi editada com sucesso.')

    def to_df(self):
        return pd.DataFrame([{
            'nome': self.nome,
            'prioridade': self.prioridade,
            'prazo': self.prazo,
            'status': self.status,
            'descricao': self.descricao,
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S') if isinstance(self.data_criacao, datetime) else self.data_criacao,
            'horario_inicio': self.horario_inicio,
            'tempo_total': self.tempo_total
        }])

    def gerar_descricao(self):
        # Chama o serviço externo
        return gerar_descricao_com_gpt(self.nome)

    def __str__(self):
        return f'{self.nome} | Prioridade: {self.prioridade} | Prazo: {self.prazo} | Status: {self.status}'

