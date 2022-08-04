from django.core.mail import send_mail


def order_mail(email,body):
    full_link = f'Привет,спасибо тебе за заказ \n мы с тобой свяжемс \n {body}'

    send_mail(
        'From shop project',
        full_link,
        'sagynbaevajsen@gmail.com',
        [email])
