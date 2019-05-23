from celery import shared_task


@shared_task
def send_email_account_activation_task(user_email):
    print('Send to ' + user_email)
