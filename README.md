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
Foram implementadas duas funções para visualizar as tarefas em gráficos: uma exibe a distribuição por status ou prioridade em gráfico de pizza, e a outra mostra o progresso geral em gráfico de barra horizontal. Isso facilita a análise visual do andamento e da organização das tarefas.

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

## 📩 Envio de ralatórios por email

**🚧 Em andamento... 🚧**
