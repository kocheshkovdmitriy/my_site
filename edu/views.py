from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from edu import models
from edu import filters
from edu import forms


class TitleMixin():
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class TestList(TitleMixin, ListView):
    model = models.Test
    template_name = 'edu/list_tests.html'
    context_object_name = 'tests'
    title = 'Каталог тестов'

    def get_filters(self):
        return filters.TestFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.get_filters()
        return context


class TaskList(TitleMixin, ListView):
    model = models.Task
    template_name = 'edu/list_tasks.html'
    context_object_name = 'tasks'
    title = 'Каталог заданий'

    def get_filters(self):
        return filters.TaskFilter(self.request.GET)
    
    def get_queryset(self):
        return self.get_filters().qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filters'] = self.get_filters()
        return context


class TestDetail(DetailView):
    model = models.Test
    template_name = 'edu/detail_test.html'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        return context


class TaskDetail(DetailView):
    model = models.Task
    template_name = 'edu/detail_task.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].__str__()
        return context


class TaskCreate(CreateView):
    model = models.Task
    template_name = 'edu/task_create.html'
    fields = '__all__'
    title = 'Создание задачи'
    success_url = reverse_lazy("edu:list_tasks")


class TaskUpdate(TitleMixin, UpdateView):
    model = models.Task
    template_name = 'edu/task_update.html'
    fields = '__all__'
    title = 'Изменение задачи'

    def get_success_url(self):
        return reverse_lazy("edu:detail_task", kwargs={'pk': self.object.pk})


class TaskDelete(TitleMixin, DeleteView):
    model = models.Task
    template_name = 'edu/task_delete.html'
    title = 'Удаление задачи'
    success_url = reverse_lazy("edu:list_tasks")


class TestCreateView(View):
    def post(self, request):
        if request.POST.get('create_test'):
            list_task_id = dict(request.POST).get('list_task_id')
            if list_task_id:
                new_test = models.Test.objects.create(title=request.POST["title"])
                new_test.tasks_list.set(models.Task.objects.filter(pk__in=list_task_id))
                print(new_test)
                return redirect(reverse('edu:detail_test', kwargs={'pk': new_test.pk}))
        context = self.get_context_data(request)
        if request.POST.get('create_task'):
            new_task = models.Task.objects.create(
                task=request.POST.get('task'),
                answer=request.POST.get('answer'),
                section_id=int(request.POST.get('section'))
            )
            context['list_task_id'].append(str(new_task.pk))
        if request.POST.get('add_task'):
            form = forms.TaskForm()
            context['form_task'] = form
        return render(request, 'edu/test_create.html', context=context)

    def get(self, request):
        context = self.get_context_data(request)
        return render(request, 'edu/test_create.html', context=context)

    def get_filters(self):
        return filters.TaskFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs

    def get_context_data(self, request):
        context = {'tasks': self.get_queryset(),
                   'filters': self.get_filters(),
                   'title': 'Создание теста',
                   'list_task_id': dict(request.POST).get('list_task_id', [])}
        return context