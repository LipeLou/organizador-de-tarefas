import openai

def gerar_descricao_com_gpt(titulo_tarefa):
    try:
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
        prompt = f'Crie uma descrição para a tarefa: {titulo_tarefa}'
        
        descricao = client.chat.completions.create(
            messages=[
                {'role' : 'system', 'content' : system_prompt},
                {'role' : 'user', 'content' : prompt}],
            model='gpt-3.5-turbo-0125',
            max_tokens=200,
            temperature=0,
        )

        return descricao.choices[0].message.content
    except Exception as e:
        print(f"Erro ao gerar descrição com IA: {e}")
        return "Descrição não gerada automaticamente."

