from django.urls import path
from users.views import profile, LoginView, logout_view, register_view, ProfileUpdate

app_name = 'users'


urlpatterns = [
    path('profile/<slug:slug>', profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('profile_update/<slug:slug>', ProfileUpdate.as_view(), name='profile_update'),
]