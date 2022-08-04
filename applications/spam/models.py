from django.db import models


class Contact(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email



#TODO: реализовать отправку спам сообщений всем обьектам из модели Contact.2) При создании товара отправлять сообщение всем \n
# обьектам из модели Contact .3)Развернуть проект с Celery