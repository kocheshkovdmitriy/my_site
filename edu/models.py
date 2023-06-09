from django.db import models

from users.models import Profile


class Task(models.Model):
    task = models.CharField(max_length=1000, verbose_name='Условие')
    answer = models.CharField(max_length=100, verbose_name='Правильный ответ')
    section = models.ForeignKey('Section', on_delete=models.CASCADE, verbose_name='Раздел', related_name='tasks')

    def __str__(self):
        return 'Задание №:{num}, раздел {section}'.format(
            section=self.section,
            num=self.pk
        )

    class Meta:
        verbose_name = 'Задание'
        verbose_name_plural = 'Задания'


class Test(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема теста')
    tasks_list = models.ManyToManyField('Task', related_name='test')

    def __str__(self):
        return 'Тема: {title}, количесво задани {cnt_task}'.format(
            title=self.title,
            cnt_task=len(self.tasks_list.all())
        )

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Section(models.Model):
    title = models.CharField(max_length=200, verbose_name='Раздел')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

class Answer(models.Model):
    answer = models.CharField(max_length=100, verbose_name='Ответ')
    task = models.ForeignKey('Task', on_delete=models.CASCADE, verbose_name='Задача', related_name='answers')
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест', related_name='answers', blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='answers')
    status = models.BooleanField(verbose_name='статус', default=False)

    def __str__(self):
        return 'Задание №{num}: ваш ответ {answer}. Статус {status}'.format(
            answer=self.answer,
            num=self.task.pk,
            status = 'решено' if self.status else 'нерешено'
        )

    class Meta:
        verbose_name = 'Ответ на задачу'
        verbose_name_plural = 'Ответы на задачи'

class TestAnswer(models.Model):
    test = models.ForeignKey('Test', on_delete=models.CASCADE, verbose_name='Тест', related_name='testanswers')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='testanswers')
    status = models.IntegerField(verbose_name='статус')

    def get_answers(self):
        return Answer.objects.filter(test=self.test, user=self.user)

    def __str__(self):
        return '{user} Тест №{num}. Статус {status}%'.format(
            user=self.user.user.first_name,
            num=self.test.pk,
            status = self.status
        )

    class Meta:
        verbose_name = 'Ответ на тест'
        verbose_name_plural = 'Ответы на тесты'