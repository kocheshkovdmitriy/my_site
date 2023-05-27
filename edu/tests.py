from django.test import TestCase, Client
from django.urls import reverse
from edu import  factories, models


class TaskTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.section = factories.Section()
        self.task1 = factories.Task(section = self.section)
        self.task2 = factories.Task()
        self.task3 = factories.Task()

    def test_list_task(self):
        response = self.client.get(reverse('edu:list_tasks'))
        self.assertEqual(response.status_code, 200)

    def test_filter_task(self):
        response = self.client.get(reverse('edu:list_tasks') + f'?section_id={self.section.pk}')
        self.assertEqual(response.status_code, 200)
        cnt = response.content.decode().count('Задание №:')
        temp = f'Задание №:{self.task1.pk}'
        self.assertTrue(temp in response.content.decode() and cnt == 1)

    def test_detail_task(self):
        response = self.client.get(reverse('edu:detail_task', kwargs={'pk': self.task1.pk}))
        self.assertEqual(response.status_code, 200)
        temp = f'id задачи: {self.task1.pk}'
        self.assertTrue(temp in response.content.decode())
        temp = f'id задачи: {self.task2.pk}'
        self.assertFalse(temp in response.content.decode())

    def test_create_task(self):
        data = {"task": 'решите 2 + 2 =', "answer": '4', "section": factories.Section().pk}
        response = self.client.post(path=reverse("edu:task_create"), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_task = models.Task.objects.filter(task=data['task']).first()
        self.assertListEqual([data['task'], data['answer'], data['section']], [new_task.task, new_task.answer, new_task.section.pk])

    def test_update_task(self):
        task = models.Task.objects.all().first()
        data = {"task": 'отредактировано', "answer": task.answer, "section": task.section.pk}
        response = self.client.post(path=reverse("edu:task_update", kwargs={'pk': task.pk}), data=data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_task = models.Task.objects.filter(pk=task.pk).first()
        self.assertListEqual([data['task'], data['answer'], task.section.pk], [new_task.task, new_task.answer, new_task.section.pk])

    def test_delete_task(self):
        task = models.Task.objects.all().last()
        response = self.client.post(path=reverse("edu:task_delete", kwargs={'pk': task.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
        new_task = models.Task.objects.filter(pk=task.pk).first()
        self.assertTrue(new_task is None)