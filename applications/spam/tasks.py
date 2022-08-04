from django.core.mail import send_mail


def spam_attack():
    full_link = f'Здравствуйте'

    send_mail(
        'from spam',
        full_link,

    )