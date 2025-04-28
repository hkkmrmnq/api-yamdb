from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_email(email, accoun_activation_token):
    """
    Отправляет письмо с кодом подтверждения
    на указанный адрес электронной почты.
    """
    subject = 'Токен для активации аккунта на Yamdb'
    message = (
        'Токен для активации Вашего '
        f'аккунта на Yamdb: {accoun_activation_token}'
    )
    recipient_list = [email]

    send_mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        subject=subject,
        message=message,
        recipient_list=recipient_list,
    )
