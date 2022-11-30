from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_mails(subject, message, email_from, recipient_list):
    print("started...")
    send_mail(subject, message, email_from, recipient_list)
    print("sent emails")
    return "Emails sent successfully"
