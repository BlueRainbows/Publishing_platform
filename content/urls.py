from django.urls import path

from content.apps import ContentConfig
from content import views

app_name = ContentConfig.name

urlpatterns = [
    # Главная страница (список контента)
    path('', views.ContentListView.as_view(), name='index'),
    # Создание нового контента
    path('create/', views.ContentCreateView.as_view(), name='create'),
    # Просмотр контента
    path('detail/<int:pk>/', views.ContentDetailView.as_view(), name='detail'),
    # Удаление контента
    path('delete/<int:pk>/', views.ContentDeleteView.as_view(), name='delete'),
    # Изменение контента
    path('update/<int:pk>/', views.ContentUpdateView.as_view(), name='update'),
    # Личные посты пользователя
    path('personal_list/', views.ContentPersonalListView.as_view(), name='personal_list'),
    # Обратотка лайков,
    path('likes/<int:pk>/', views.likes, name='likes'),
    # Обработка комментариев
    path('comments/<int:pk>/', views.comments, name='comments'),
    # Не опубликованные посты пользователей
    path('manager_list/', views.ContentManagerListView.as_view(), name='manager_list'),
]
