import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

def enviar_email_relatorio(destinatario, assunto, corpo_texto, corpo_html, anexos=[]):
    load_dotenv()
    usuario = os.getenv('EMAIL_USUARIO')
    senha = os.getenv('EMAIL_SENHA')
    
    if not usuario or not senha:
        print("Credenciais de email não configuradas no .env")
        return

    destinatario_final = destinatario if destinatario else usuario

    try:
        msg = EmailMessage()
        msg['Subject'] = assunto
        msg['From'] = usuario
        msg['To'] = destinatario_final
            
        msg.set_content(corpo_texto)
        msg.add_alternative(corpo_html, subtype='html')

        for arquivo_path in anexos:
            if os.path.exists(arquivo_path):
                with open(arquivo_path, 'rb') as a:
                    img = a.read()
                    arquivo_nome = os.path.basename(arquivo_path)
                    msg.add_attachment(img, maintype='image', subtype='png', filename=arquivo_nome)
            else:
                print(f"Arquivo anexo não encontrado: {arquivo_path}")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(usuario, senha)
            smtp.send_message(msg)

        print(f'Email enviado com sucesso para {destinatario_final}')
    except Exception as e:
        print('Erro ao enviar email:', e)

