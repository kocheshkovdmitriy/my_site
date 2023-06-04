
from django.contrib.auth.models import User
from django.db.models import Count, Case, When, F
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from core.models import New, Commit
from core import forms

import users.models
import users.filters
import edu.models


def about(request):
    return render(request=request, template_name='core/about.html')


class TitleMixin():
    title = None

    def get_title(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        return context


class NewList(TitleMixin, ListView):
    model = New
    template_name = 'core/list_news.html'
    context_object_name = 'news'
    title = 'Новости'


class NewDetail(DetailView):
    model = New
    template_name = 'core/detail_new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object'].title
        context['commits'] = Commit.objects.filter(new_id=context['object'].pk)
        context['form'] = forms.CommitForm()
        return context

    def post(self, request, **kwargs):
        object = self.get_object()
        data = {'user_name': request.POST.get('user_name', ''),
                'description': request.POST['description'],
                'new': object}
        if not request.user.is_anonymous:
            data['user'] = request.user
            data['user_name'] = request.user.first_name
        Commit.objects.create(**data)
        return redirect(reverse('core:detail_new', kwargs=kwargs))


class NewCreate(TitleMixin, CreateView):
    model = New
    template_name = 'core/new_create.html'
    fields = '__all__'
    title = 'Создание новости'
    success_url = reverse_lazy("core:list_news")


class NewUpdate(TitleMixin, UpdateView):
    model = New
    template_name = 'core/new_update.html'
    fields = '__all__'
    title = 'Редактирование новости'

    def get_success_url(self):
        return reverse_lazy("core:detail_new", kwargs={'pk': self.object.pk})


class NewDelete(TitleMixin, DeleteView):
    model = New
    template_name = 'core/new_delete.html'
    title = 'Удаление новости'
    success_url = reverse_lazy("core:list_news")


class ListStudents(View):
    def get(self, request):
        context = self.get_context_data()
        return render(request, 'core/list_students.html', context=context)

    def get_context_data(self):
        cnt_tasks = edu.models.Task.objects.all().count()
        context = {'students': self.get_queryset().annotate(
                completed_tasks=Count(Case(When(answers__status=True, then=1))),
                statistic_tasks=F('completed_tasks') * 100 / cnt_tasks,
                completed_tests=Count(Case(When(testanswers__status=True, then=1)))
            ),
            'filters': self.get_filters(),
        }
        return context

    def get_filters(self):
        return users.filters.ProfileFilter(self.request.GET)

    def get_queryset(self):
        return self.get_filters().qs