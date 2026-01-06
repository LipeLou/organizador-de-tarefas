import matplotlib.pyplot as plt
import os

def plotar_pizza_tarefas(df_tarefas, by_status=True):
    os.makedirs('img', exist_ok=True)

    coluna = 'status' if by_status else 'prioridade'
    dados = df_tarefas.groupby(coluna)['nome'].count()

    if dados.empty:
        print("Sem dados para plotar.")
        return None

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, texts, autotexts = ax.pie(
        dados,
        labels=dados.index,
        autopct='%1.1f%%',
        explode=[0.01] * len(dados),
        colors=['#FF9800','#4CAF50','#2196F3'] if len(dados) <= 3 else None, # Ajuste simples para cores
    )

    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)

    ax.set_title(f'Distribuição de Tarefas por {coluna.capitalize()}', fontsize=14)
    plt.savefig(f'img/tarefas-por-{coluna}.png')
    return fig

def plotar_progresso(df_tarefas):
    os.makedirs('img', exist_ok=True)

    total = df_tarefas.shape[0]
    if total == 0:
        return None
        
    concluidas = df_tarefas[df_tarefas['status'] == 'Concluída'].shape[0]
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

def exibir_plot(fig):
    if fig:
        return fig.show()
    else:
        print('Não foi possível exibir um gráfico')

