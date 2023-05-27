from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=40, unique=True, db_index=True, verbose_name='url')
    city = models.CharField(max_length=40, blank=True, verbose_name='Город проживания')
    school = models.CharField(max_length=200, blank=True, verbose_name='Школа')
    grade = models.IntegerField(default=0, blank=True, verbose_name='Класс')
    tests = models.ManyToManyField('edu.Test', blank=True, verbose_name='Тесты')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'profile_slug': self.slug})

    def __str__(self):
        return "{name} {second_name}".format(
            name=self.user.first_name,
            second_name=self.user.last_name
        )

    class Meta:
        verbose_name = 'Профиль ользователя'
        verbose_name_plural = 'Профили пользователей'


