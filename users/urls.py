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
    path('register/',
         views.RegisterView.as_view(), name='register'),
    # Уведомление о подтверждение регистрации
    path('verification/',
         views.VerificationView.as_view(), name='verification'),
    # Активация пользователя
    path('activate/<str:token>/',
         views.activate, name='activate'),
    # Уведомление о успешной регистрации
    path('activate/success',
         TemplateView.as_view(template_name='users/activation_success.html'),
         name='success_activate'),
    # Уведомление о ошибке при верификации
    path('activate/error',
         TemplateView.as_view(template_name='users/activation_error.html'), name='error_activate'),

    # Профиль пользователя
    path('profile/',
         views.ProfileView.as_view(), name='profile'),
    # Изменение профиля пользователя
    path('change_profile/',
         views.ChangeProfileView.as_view(), name='change_profile'),
    # Удаление пользователя
    path('user_delete/',
         views.UserDeleteView.as_view(), name='user_delete'),

    # Обработка подписки
    path('subscription/',
         views.get_subscription, name='subscription'),
    # Подтверждение подписки
    path('subscription_info/',
         TemplateView.as_view(template_name='users/subscription_info.html'),
         name='subscription_info'),

    # Установка личности
    path('password_reset/',
         views.UserPasswordResetView.as_view(), name='password_reset'),
    # Уведомление о инструциях присланных на почту
    path('password_reset_done/',
         views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    # Прием перехода по ссылке
    path('password_reset/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # Смена пароля
    path('password_reset_complete/',
         views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete')
]
