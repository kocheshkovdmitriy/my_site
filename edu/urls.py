from django.urls import path
from edu import views


app_name = 'edu'


urlpatterns = [
    path('list_tests/', views.TestList.as_view(), name='list_tests'),
    path('list_tasks/', views.TaskList.as_view(), name='list_tasks'),
    path('test/<int:pk>', views.TestDetail.as_view(), name='detail_test'),
    path('task/<int:pk>', views.TaskDetail.as_view(), name='detail_task'),
    path('task_create/', views.TaskCreate.as_view(), name='task_create'),
    path('task_update/<int:pk>', views.TaskUpdate.as_view(), name='task_update'),
    path('task_delete/<int:pk>', views.TaskDelete.as_view(), name='task_delete'),
    path('test_create/', views.TestCreateView.as_view(), name='test_create'),
]