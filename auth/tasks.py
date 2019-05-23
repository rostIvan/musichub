from celery import shared_task


@shared_task
def send_account_activation_email_task(user_email):
    print('Send to ' + user_email)
