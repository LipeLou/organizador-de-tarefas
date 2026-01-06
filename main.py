from datetime import datetime
import os
from dotenv import load_dotenv
from src.tarefa import Tarefa
from src.lista_tarefas import ListaTarefas

load_dotenv()

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
                        print(f'Editando tarefa: {lista_tarefas.tarefas["nome"][n]}')
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
