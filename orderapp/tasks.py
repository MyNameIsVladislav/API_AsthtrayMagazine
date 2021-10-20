from django.core.mail import send_mail

from core.celery import app
from core.settings import EMAIL_HOST_USER


@app.task
def send_email_success(email):
    send_mail('Successful', 'Оплата прошла успешно! Ожидайте доставки!', EMAIL_HOST_USER, [email],)
