from django.db import models
from django.contrib.auth.models import User

class Commit(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Автор')
    user_name = models.CharField(max_length=20, blank=True, default='Аноним', verbose_name='Имя автора')
    description = models.TextField(default='', verbose_name='Комментарий')
    new = models.ForeignKey('New', on_delete=models.CASCADE, verbose_name='Новость')

    def __str__(self):
        return f'Комментарий от {self.user_name} к {self.new}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class New(models.Model):
    title = models.CharField(max_length=1000, verbose_name='Название')
    description = models.TextField(default='', verbose_name='Описание')
    publish = models.BooleanField(default=False, verbose_name='Опубликованно')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Отредактированно')

    def cnt_commit(self):
        return len(Commit.objects.filter(new=self))

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
