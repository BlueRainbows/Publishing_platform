from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from users.apps import UsersConfig
from users import views

app_name = UsersConfig.name

urlpatterns = [
    # Вход пользователя на платформу
    path('login/', views.UserLoginView.as_view(), name='login'),
    # Выход пользователя из платформы
    path('logout/', LogoutView.as_view(), name='logout'),
    # Регистрация пользователя
    path('register/', views.RegisterView.as_view(), name='register'),
    # Профиль пользователя
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # Изменение профиля пользователя
    path('change_profile/', views.ChangeProfileView.as_view(), name='change_profile'),
    # Удаление пользователя
    path('user_delete/', views.UserDeleteView.as_view(), name='user_delete'),
    # Обработка подписки
    path('subscription/', views.get_subscription, name='subscription'),
    # Подтверждение подписки
    path('subscription_info/', TemplateView.as_view(template_name='users/subscription_info.html'),
         name='subscription_info'),
]
