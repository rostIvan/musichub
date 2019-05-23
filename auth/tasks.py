from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_account_activation(user_email, activation_link):
    print(f'Message sending activation email to {user_email } in progress...')
    send_account_activation_message(user_email, activation_link)
    print('Sent to ' + user_email)


def send_account_activation_message(user_email, activation_link):
    subject = 'Account activation `musichub`'
    text = (f'Click on the next link '
            f'to activate your account => {activation_link}')
    message = EmailMessage(subject, text, to=[user_email])
    message.send()
