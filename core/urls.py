from django.urls import path
from core import views

app_name = 'core'


urlpatterns = [
    path('', views.NewList.as_view(), name='list_news'),
    path('new/<int:pk>', views.NewDetail.as_view(), name='detail_new'),
    path('about/', views.about, name='about'),
    path('new_create/', views.NewCreate.as_view(), name='new_create'),
    path('new_update/<int:pk>', views.NewUpdate.as_view(), name='new_update'),
    path('new_delete/<int:pk>', views.NewDelete.as_view(), name='new_delete'),
]