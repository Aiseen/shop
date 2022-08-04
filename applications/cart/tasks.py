# import time
#
# from django.core.mail import send_mail
#
# from shop.celery import app
#
#
# @app.task
# def celery_order_mail(email,body):
#     time.sleep(5)
#     full_link = f'Привет,спасибо тебе за заказ \n мы с тобой свяжемс \n {body}'
#
#     send_mail(
#         'From shop project',
#         full_link,
#         'sagynbaevajsen@gmail.com',
#         [email])
