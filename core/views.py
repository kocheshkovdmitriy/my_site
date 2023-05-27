from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from core.models import New, Commit


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
        return context

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