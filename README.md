# Organizador de Tarefas

### ✅ Descrição breve do projeto
Organizador de tarefas em **Python** com prioridade e status. Projeto simples voltado para fins didáticos, com o objetivo de aplicar conhecimentos que vou adquirindo. O projeto começa com apenas um programa utilizando conceitos fundamentais da programação orientada a objetos e manipulação de dados, porém tentarei cada vez mais tornar esse projeto "complexo", seja corrigindo erros, assim como trazendo novas funções.
A cada funcionalidade (conhecimentos) nova adicionada, informarei em formato de notas de atualização (patch notes). Entretanto, as modificações para corrigir possíveis erros ou melhora de design, apenas irei comenta-las nos commits. 

### ❓ Por que um organizador de tarefas?
Simples, é um projeto básico e muito bom para aplicar diversos tipos de conhecimentos, ou seja, escalável, seja em OOP, como também em Data Science.



# 📌 Atualizações  
Como dito anteriormente, o objetivo é colocar em prática meus conhecimentos. Assim, fortalecendo meu conhecimento e melhorando meus estudos.  
Então essa parte de **Atualizações**, será onde colocarei em ordem as novas funções adicionadas ao projeto.


## 1. 📊 Gráficos 

**🆕 Função adicionada:** Visualização gráfica de tarefas  
**🧠 Conhecimentos aplicados:**  
- Manipulação de dados com `pandas`  
- Geração e customização de gráficos com `matplotlib`  
- Salvamento de imagens com `plt.savefig()`  

**🔍 Descrição breve:**  
Foram implementadas duas funções para visualizar as tarefas em gráficos: uma exibe a distribuição por status ou prioridade em gráfico de pizza, e a outra mostra o progresso geral em gráfico de barra horizontal. 
Isso facilita a análise visual do andamento e da organização das tarefas.

**🔧 Funçoes adicionas:**

plot_tarfeas()
~~~python
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
~~~
plot_progress()
~~~python
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
~~~


## 2. 📩 Relatórios

**🆕 Função adicionada:** Envio de relatórios por e-mail  
**🧠 Conhecimentos aplicados:**  
- Envio de e-mails com `smtplib` e `email.message`  
- Leitura de variáveis de ambiente com `dotenv`  
- Manipulação de arquivos binários para anexos  

**🔍 Descrição breve:**  
Foi implementada uma função que permite o envio de arquivos de relatório por e-mail de forma automatizada e segura. 
Essa funcionalidade melhora a praticidade do projeto ao facilitar o compartilhamento dos resultados e gráficos gerados.

**🔧 Funçoes adicionas:**

enviar_relatorio_por_email()
~~~python
    def enviar_relatorio_por_email(self, destinatario=None):
        try: 
            load_dotenv()
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
~~~

