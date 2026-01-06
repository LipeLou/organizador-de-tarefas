import streamlit as st
import pandas as pd
from datetime import datetime, date
from src.tarefa import Tarefa
from src.lista_tarefas import ListaTarefas

# Configuração da Página
st.set_page_config(page_title="Organizador de Tarefas", page_icon="📝", layout="wide")

def main():
    st.title("📝 Organizador de Tarefas")
    
    lista = ListaTarefas()

    # Sidebar para Menu e Funcionalidades Extras
    st.sidebar.title("Menu")
    menu = ["Dashboard", "Minhas Tarefas", "Nova Tarefa"]
    choice = st.sidebar.selectbox("Navegação", menu)

    st.sidebar.divider()
    
    # Download CSV
    st.sidebar.header("📂 Dados")
    if not lista.tarefas.empty:
        csv = lista.tarefas.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button(
            label="Baixar Tarefas (CSV)",
            data=csv,
            file_name='tarefas.csv',
            mime='text/csv',
        )
    
    st.sidebar.divider()

    # Envio de Relatório
    st.sidebar.header("📧 Relatório")
    with st.sidebar.form("form_email"):
        destinatario = st.text_input("Email do destinatário", placeholder="seu@email.com")
        enviar_btn = st.form_submit_button("Enviar Relatório")
        
        if enviar_btn:
            if destinatario:
                with st.spinner('Gerando e enviando relatório...'):
                    lista.enviar_relatorio_por_email(destinatario)
                st.success("Relatório enviado!")
            else:
                st.warning("Por favor, digite um email.")

    if choice == "Dashboard":
        st.header("📊 Dashboard")
        
        # Métricas
        if not lista.tarefas.empty:
            total, concluidas, pendentes, progresso, tempo_medio, tempo_total = lista.gerar_estatisticas()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total de Tarefas", total)
            col2.metric("Concluídas", concluidas)
            col3.metric("Pendentes", pendentes)
            col4.metric("Progresso", f"{progresso:.1f}%")

            st.divider()

            # Gráficos
            col_graf1, col_graf2 = st.columns(2)
            
            with col_graf1:
                st.subheader("Por Status")
                fig_status = lista.plot_tarefas(by_status=True)
                if fig_status:
                    st.pyplot(fig_status)
            
            with col_graf2:
                st.subheader("Por Prioridade")
                fig_prio = lista.plot_tarefas(by_status=False)
                if fig_prio:
                    st.pyplot(fig_prio)

            st.subheader("Progresso Geral")
            fig_prog = lista.plot_progress()
            if fig_prog:
                st.pyplot(fig_prog)
        else:
            st.info("Nenhuma tarefa cadastrada para exibir estatísticas.")

    elif choice == "Minhas Tarefas":
        st.header("📋 Minhas Tarefas")
        
        if not lista.tarefas.empty:
            # Filtros
            filtro_status = st.multiselect("Filtrar por Status", options=lista.tarefas['status'].unique(), default=lista.tarefas['status'].unique())
            filtro_prio = st.multiselect("Filtrar por Prioridade", options=lista.tarefas['prioridade'].unique(), default=lista.tarefas['prioridade'].unique())
            
            df_filtrado = lista.tarefas[
                (lista.tarefas['status'].isin(filtro_status)) & 
                (lista.tarefas['prioridade'].isin(filtro_prio))
            ]
            
            st.dataframe(df_filtrado, use_container_width=True)

            # Ações Rápidas (Expander para operações em tarefas específicas)
            with st.expander("Gerenciar Tarefa Específica"):
                tarefas_nomes = lista.tarefas['nome'].tolist()
                tarefa_selecionada = st.selectbox("Selecione uma tarefa", tarefas_nomes)
                
                if tarefa_selecionada:
                    dados_tarefa = lista.tarefas[lista.tarefas['nome'] == tarefa_selecionada].iloc[0]
                    st.write(f"**Status Atual:** {dados_tarefa['status']}")
                    
                    col_b1, col_b2, col_b3 = st.columns(3)
                    
                    if col_b1.button("Iniciar Tarefa"):
                        lista.iniciar_tarefa(tarefa_selecionada)
                        lista.salvar_tarefas()
                        st.success(f"Tarefa '{tarefa_selecionada}' iniciada!")
                        st.rerun()
                    
                    if col_b2.button("Concluir Tarefa"):
                        lista.finalizar_tarefa(tarefa_selecionada)
                        lista.salvar_tarefas()
                        st.success(f"Tarefa '{tarefa_selecionada}' concluída!")
                        st.rerun()

                    if col_b3.button("Remover Tarefa"):
                        lista.remover_tarefa(tarefa_selecionada)
                        st.warning(f"Tarefa '{tarefa_selecionada}' removida!")
                        st.rerun()

        else:
            st.info("Nenhuma tarefa cadastrada.")

    elif choice == "Nova Tarefa":
        st.header("➕ Nova Tarefa")
        
        with st.form("form_nova_tarefa"):
            nome = st.text_input("Nome da Tarefa")
            prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])
            col_d1, col_d2 = st.columns(2)
            data_prazo = col_d1.date_input("Data do Prazo", min_value=date.today())
            hora_prazo = col_d2.time_input("Horário do Prazo", value=datetime.now().time())
            
            submitted = st.form_submit_button("Cadastrar Tarefa")
            
            if submitted:
                if nome:
                    prazo_combinado = datetime.combine(data_prazo, hora_prazo)
                    nova_tarefa = Tarefa(nome, prioridade, prazo_combinado)
                    lista.adicionar_tarefa(nova_tarefa)
                    lista.salvar_tarefas()
                    st.success(f"Tarefa '{nome}' cadastrada com sucesso!")
                    # Descrição gerada automaticamente pela IA (aviso)
                    st.info(f"Descrição gerada via IA: {nova_tarefa.descricao}")
                else:
                    st.error("O nome da tarefa é obrigatório.")

if __name__ == '__main__':
    main()
