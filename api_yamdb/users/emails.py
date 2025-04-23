from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(email, confirmation_code):
    """
    Отправляет письмо с кодом подтверждения
    на указанный адрес электронной почты.
    """
    subject = 'Ваш код подтверждения для регистрации на Yamdb'
    message = f'Ваш код подтверждения: {confirmation_code}'
    recipient_list = [email]

    send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
    )
