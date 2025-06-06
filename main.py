from datetime import datetime, timedelta
import pandas as pd
import os
from matplotlib import pyplot as plt
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import openai


load_dotenv()

class Tarefa:
    def __init__(self, nome, prioridade, prazo):
        self.nome = nome
        self.prioridade = prioridade
        self.prazo = prazo
        self.status = 'Não iniciada'
        self.data_criacao = datetime.now()
        self.horario_inicio = None
        self.tempo_total = None
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
            'data_criacao': self.data_criacao.strftime('%Y-%m-%d %H:%M:%S'),
            'horario_inicio': self.horario_inicio,
            'tempo_total': self.tempo_total
        }])

    def gerar_descricao(self):
        client = openai.Client()
        system_prompt = '''
            Você é um assistente de produtividade atuando como gestor de tarefas. Sua principal função é interpretar títulos de tarefas 
            e gerar descrições completas, claras e objetivas, que ajudem qualquer pessoa a entender rapidamente o que precisa ser feito.
            Seja conciso, mas completo.

            Instruções:
            Evite repetições do título na descrição;
            Escreva sempre com clareza e profissionalismo.
            Escreva a descrição com no máximo 15 palavras
        '''
        prompt = f'Crie uma descrição para a tarefa: {self.nome}'
        
        descricao = client.chat.completions.create(
            messages=[
                {'role' : 'system', 'content' : system_prompt},
                {'role' : 'user', 'content' : prompt}],
            model='gpt-3.5-turbo-0125',
            max_tokens=200,
            temperature=0,
        )

        descricao_resposta = descricao.choices[0].message.content
        return descricao_resposta

    def __str__(self):
        return f'{self.nome} | Prioridade: {self.prioridade} | Prazo: {self.prazo} | Status: {self.status}'


class ListaTarefas:
    def __init__(self):
        if os.path.exists('tarefas.csv'):
            self.tarefas = pd.read_csv('tarefas.csv', index_col=0)
        else:
            self.tarefas = pd.DataFrame(columns=['nome', 'prioridade', 'prazo', 'status', 'descricao', 'data_criacao', 'horario_inicio', 'tempo_total'])

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
        print('=== Tarefa urgente! ===')
        print(f'Tarefa: {tarefas_urgentes.iloc[0]['nome']}') 
        print(f'Prioridade: {tarefas_urgentes.iloc[0]['prioridade']}')
        print(f'Prazo: {tarefas_urgentes.iloc[0]['prazo']}')
        print(f'Status: {tarefas_urgentes.iloc[0]['status']}')
        print('===================')

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
        os.makedirs('img', exist_ok=True)

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
        plt.savefig(f'img/tarefas-por-{coluna}.png')
        return fig

    def plot_progress(self):
        os.makedirs('img', exist_ok=True)

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
        plt.savefig('img/progresso.png')        
        return fig
    
    def exibir_plot(self, fig):
        if fig:
            return fig.show()
        else:
            print('Não foi possível exibir um gráfico')

    def enviar_relatorio_por_email(self, destinatario=None):
        try: 
            tarefas_totais, tarefas_concluidas, tarefas_pendentes,progresso, tempo_medio, tempo_total = self.gerar_estatisticas()

            texto = f'''
Olá, seu relatório de tarefas cehgou!\n
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

            host = 'imap.gmail.com'
            usuario = os.getenv('EMAIL_USUARIO')
            senha = os.getenv('EMAIL_SENHA')

            msg = EmailMessage()
            msg['Subject'] = 'Relatório tarefas'
            msg['From'] = usuario
            msg['To'] = destinatario if destinatario else usuario
                
            msg.set_content(texto)
            msg.add_alternative(texto_html, subtype='html')

            self.plot_tarefas()
            self.plot_tarefas(by_status=False)
            self.plot_progress()

            arquivos = [
                os.path.join('img', 'tarefas-por-prioridade.png'),
                os.path.join('img', 'tarefas-por-status.png'),
                os.path.join('img', 'progresso.png')
            ]
            for arquivo in arquivos:
                with open(arquivo, 'rb') as a:
                    img = a.read()
                    arquivo_nome = a.name
                    msg.add_attachment(img, maintype='image', subtype='png', filename=arquivo_nome)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(usuario, senha)
                smtp.send_message(msg)

            print(f'Email enviado com sucesso para {destinatario}') if destinatario else print('Email enviado com sucesso!')
        except Exception as e:
            print('Erro ao enviar email:', e)


def voltar_ao_menu():
    input('\nDigite algo para voltar ao menu. ')
    limpar_terminal()
    menu()

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def escolher_opcao():
    lista_tarefas = ListaTarefas()
    try: 
        opcao = int(input('Escolha uma opção: '))

        limpar_terminal()
        match opcao:
            case 1:
                nome = input('Digite o nome da tarefa: ')
                while not nome:
                    limpar_terminal()
                    print('Erro! Tente novamente')
                    nome = input('Digite o nome da tarefa: ')
        
                prioridade = input('Digite a prioridade (Alta, Média, Baixa): ').lower().capitalize()
                while prioridade not in ['Alta', 'Média', 'Baixa']:
                    limpar_terminal()
                    print('Erro! Tente novamente.')
                    print(f'Nome: {nome}')
                    prioridade = input('Digite a prioridade (Alta, Média, Baixa): ').lower().capitalize()

                while True:
                    try:
                        prazo = input('Digite o prazo (ex: 2025-12-31): ')
                        prazo = datetime.strptime(prazo, '%Y-%m-%d')
                        break
                    except ValueError:
                        limpar_terminal()
                        print('Formato de data inválido. Tente novamente.')
                        print(f'Nome: {nome}')
                        print(f'Prioridade: {prioridade}')
                    
                tarefa = Tarefa(nome, prioridade, prazo)
                confirm = input(f'Adicionar tarefa: {tarefa} | ?\n[S/N]: ').upper()[0]

                if confirm == 'S':
                    lista_tarefas.adicionar_tarefa(tarefa)
                    print(f'Tarefa "{nome}" adicionada com sucesso!')
                    lista_tarefas.salvar_tarefas()
                elif confirm == 'N':
                    print(f'Tarefa "{nome}" não foi adicionada.')
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
                    n = int(input('Digite número da tarefa que deseja iniciar: '))
                    if 0 <= n < len(lista_tarefas.tarefas):
                        lista_tarefas.iniciar_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print('Tarefa não encontrada.')
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 5:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero}. {tarefa}')
                    n = int(input('Digite número da tarefa que deseja finalizar: '))
                    if 0 <= n < len(lista_tarefas.tarefas):
                        lista_tarefas.finalizar_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print('Tarefa não encontrada.')
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 6:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero}. {tarefa}')
                    n = int(input('Digite número da tarefa que deseja remover: '))
                    if 0 <= n < len(lista_tarefas.tarefas):

                        lista_tarefas.remover_tarefa(lista_tarefas.tarefas['nome'][n])
                        lista_tarefas.salvar_tarefas()
                    else:
                        print('Tarefa não encontrada.')
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 7:
                if not lista_tarefas.tarefas.empty:
                    for numero, tarefa in enumerate(lista_tarefas.tarefas['nome']):
                        print(f'{numero+1}. {tarefa}')
                    n = int(input('Digite número da tarefa que deseja editar: '))
                    if 0 <= n < len(lista_tarefas.tarefas):       
                        print(f'Editando tarefa: {lista_tarefas.tarefas['nome'][n]}')
                        novo_nome = input('Novo nome: ')
                        nova_prioridade = input('Nova prioridade (Alta, Média, Baixa): ')
                        novo_prazo = input('Novo prazo (ex: 2023-12-31): ')
                        novo_prazo = datetime.strptime(novo_prazo, '%Y-%m-%d') if novo_prazo else None
                        lista_tarefas.editar_tarefa(lista_tarefas.tarefas['nome'][n], novo_nome, nova_prioridade, novo_prazo)
                        lista_tarefas.salvar_tarefas()
                    else:
                        print('Tarefa não encontrada.')
                else:
                    print('Nenhuma tarefa cadastrada.')
                voltar_ao_menu()

            case 8:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.selecionar_tarefa_mais_urgente()
                voltar_ao_menu()

            case 9:
                print('Nenhuma tarefa cadastrada.') if lista_tarefas.tarefas.empty else lista_tarefas.exibir_estatisticas()
                voltar_ao_menu()

            case 10:
                if lista_tarefas.tarefas.empty:
                    print('Nenhuma tarefa cadastrada.')   
                else:
                    fig = lista_tarefas.plot_tarefas(by_status=False)
                    lista_tarefas.exibir_plot(fig)
                voltar_ao_menu()

            case 11:
                if lista_tarefas.tarefas.empty:
                    print('Nenhuma tarefa cadastrada.')   
                else:
                    fig = lista_tarefas.plot_tarefas(by_status=True)
                    lista_tarefas.exibir_plot(fig)
                voltar_ao_menu()

            case 12:
                if lista_tarefas.tarefas.empty:
                    print('Nenhuma tarefa cadastrada.')   
                else:
                    fig = lista_tarefas.plot_progress()
                    lista_tarefas.exibir_plot(fig)
                voltar_ao_menu()

            case 13:
                print('Para outro (exemplo@email.com) | Para você (deixe em branco)')
                destinatario = input('Para quem deseja enviar: ')
                limpar_terminal()
                lista_tarefas.enviar_relatorio_por_email(destinatario)
                voltar_ao_menu()

            case 14:
                lista_tarefas.salvar_tarefas()
                limpar_terminal()
                print('=== Volte Sempre ===')

            case _:
                print('Opção inválida. Tente novamente.')
                menu()

    except ValueError:
        print('Entrada inválida. Por favor, insira um número inteiro correspondente à opção do menu.')
        menu()


def menu():
    limpar_terminal()
    print('\n=== Organizador de Tarefas com Prioridades ===')
    print('1. Adicionar Tarefa')
    print('2. Exibir Tarefas por Prioridade')
    print('3. Exibir Tarefas por Status')
    print('4. Iniciar Tarefa')
    print('5. Finalizar Tarefa')
    print('6. Remover Tarefa')
    print('7. Editar Tarefa')
    print('8. Selecionar tarefa mais urgente')
    print('9. Exibir estatísticas')
    print('10. Exbir gráfico Tarefas por Prioridade')
    print('11. Exbir gráfico Tarefas por Status')
    print('12. Exbir gráfico Progresso')
    print('13. Enviar relatório por email')
    print('14. Sair')
    escolher_opcao()


if __name__ == '__main__':
    menu()
