from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from users.models import Profile
from users.forms import RegisterForm, AuthUser

from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect


def profile(request, slug):
    profile = get_object_or_404(Profile, slug=slug)
    context = {
        'profile': profile,
        'title': profile.__str__()
    }
    return render(request, 'users/profile.html', context=context)

def logout_view(request):
    logout(request)
    return redirect('/')

class LoginView(View):
    def get(self, request):
        form = AuthUser()
        context = {'form': form}
        return render(request, 'users/auth_user.html', context=context)

    def post(self, request):
        form = AuthUser(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error('__all__', 'Учетная запись не активна.')
            else:
                form.add_error('__all__', 'Неверно введены имя пользователя или пароль.')
        context = {'form': form, 'title': 'авторизация пользователя'}
        return render(request, 'users/auth_user.html', context=context)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            slug = form.cleaned_data.get('username')
            city = form.cleaned_data.get('city')
            school = form.cleaned_data.get('school')
            grade = form.cleaned_data.get('grade')
            Profile.objects.create(user=user, slug=slug, city=city, school=school, grade=grade)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
        else:
            context = {'form': form, 'title': 'регистранция пользователя'}
            return render(request, 'users/reg_user.html', context=context)
    else:
        form = RegisterForm()
        context = {'form': form, 'title': 'регистрация пользователя'}
        return render(request, 'users/reg_user.html', context=context)

class ProfileUpdate(UpdateView):
    model = Profile
    template_name = 'users/profile_update.html'
    fields = ('city', 'school', 'grade', 'tests',)
    context_object_name = 'profile'

    def get_success_url(self):
        return reverse_lazy("users:profile", kwargs={'slug': self.object.slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля'
        return context
