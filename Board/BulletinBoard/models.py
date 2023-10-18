from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models


class Ad(models.Model):
    type_1 = 'Танки'
    type_2 = 'Хилы'
    type_3 = 'ДД'
    type_4 = 'Торговцы'
    type_5 = 'Гилдмастеры'
    type_6 = 'Квестгиверы'
    type_7 = 'Кузнецы'
    type_8 = 'Кожевники'
    type_9 = 'Зельевары'
    type_10 = 'Мастера заклинаний'
    TYPES = [(type_1, 'Танки'),
             (type_2, 'Хилы'),
             (type_3, 'ДД'),
             (type_4, 'Торговцы'),
             (type_5, 'Гилдмастеры'),
             (type_6, 'Квестгиверы'),
             (type_7, 'Кузнецы'),
             (type_8, 'Кожевники'),
             (type_9, 'Зельевары'),
             (type_10, 'Мастера заклинаний')]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = RichTextUploadingField()
    title = models.CharField(max_length=255)
    creation_time = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=18, choices=TYPES, default=type_1)


    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/ads/{self.id}'

class Response(models.Model):
    resp_ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    resp_author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_time = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, verbose_name='Принято')

    def __str__(self):
        return f'{self.text}'

    def is_accept(self):
        return self.accepted
