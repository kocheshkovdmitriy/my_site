import factory
from faker import Factory
from edu import models

factory_ru = Factory.create("ru-RU")


class Section(factory.django.DjangoModelFactory):
    title = factory_ru.word()

    class Meta:
        model = models.Section

class Task(factory.django.DjangoModelFactory):
    task = factory_ru.text()
    answer = factory_ru.word()
    section = factory.SubFactory(Section)

    class Meta:
        model = models.Task


class Test(factory.django.DjangoModelFactory):
    title = factory_ru.word()

    @factory.post_generation
    def tasks_list(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for topping in extracted:
                self.tasks_list.add(topping)

    class Meta:
        model = models.Test


class Answer(factory.django.DjangoModelFactory):
    answer = factory_ru.word()
    task = factory.SubFactory(Task)
    test = factory.SubFactory(Test)
    status = factory_ru.boolean()

    class Meta:
        model = models.Answer







