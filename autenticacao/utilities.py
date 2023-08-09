from django.core.mail import send_mail
from django.conf import settings

def pass_change_email(sent_to, pass_link):
    subject = 'SIACA - Recuperação de Senha'
    message = f'Clique neste link para redefinir sua senha {pass_link}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [sent_to,]
    send_mail( subject, message, email_from, recipient_list )
    return True