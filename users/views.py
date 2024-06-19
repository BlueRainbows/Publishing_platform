from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, TemplateView

from users.forms import UserProfileForm, UserRegisterForm, UserLoginForm
from users.models import User, Subscription
from users.services import create_price, create_session, create_product, get_verification


def get_subscription(request):
    """
    Функция для создания сессии подписки.
    Доступна для авторизованных пользователей,
    Не имеющих подписку.
    Редирект на страницу платежа.
     """
    if request.method == 'GET':
        if not request.user.is_authenticated:
            raise PermissionDenied
        if request.user.subscription:
            raise PermissionDenied
        else:
            user = User.objects.get(pk=request.user.pk)
            sub = Subscription.objects.create(payment_data=datetime.now())
            product = create_product(sub.pk, sub.payment_data)
            price = create_price(product)
            session, payment_url = create_session(price)
            sub.payment_session = session
            sub.payment_url = payment_url
            user.subscription = sub
            user.save()
            sub.save()
            return HttpResponsePermanentRedirect(sub.payment_url)


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя.
    Модель User, форма UserRegisterForm.
    При регистрации предусмотрена верификация.
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:verification')

    def form_valid(self, form):
        """
        При успешном создании пользователя формирует токен,
        добавляет токен в базу данных и формирует сообщение для отправки на почту.
        """
        user = form.save(commit=False)
        get_verification(self.request, user)
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Контроллер профиля пользователя.
    Модель User.
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class UserLoginView(LoginView):
    """
    Контроллер для авторизации пользователя.
    """
    model = User
    form_class = UserLoginForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('content:index')


class ChangeProfileView(LoginRequiredMixin, UpdateView):
    """
    Контроллер для изменения профиля пользователя.
    Модель User, форма UserRegisterForm.
    При успешном изменении переходит на себя.
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/change_profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    """
    Контроллер для удаления пользователя.
    """
    model = User
    success_url = reverse_lazy('content:index')

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class VerificationView(TemplateView):
    """
    Контроллер перенаправляющий на уведомление о верификации через почту.
    """
    template_name = 'users/verification.html'


def activate(request, token):
    """
    Функция принимает токен, сверяет его с токенами по базе данных.
    При успешном нахождении пользователя активирует его, перенаправляет на уведомление о успешной верификации.
    Если токен не найден или ссылка повреждена перенаправляет на уведомление о ошибке.
    """
    user_model = get_user_model()
    try:
        user = user_model.objects.get(token=token)
    except (TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user is not None and user.token == token:
        user.is_active = True
        user.save()
        return redirect(reverse('users:success_activate'))
    else:
        return redirect(reverse('users:error_activate'))


class UserPasswordResetView(PasswordResetView):
    """
    Контроллер для востановления пароля.
    Принимает почту пользователя.
    Формирует сообщение в шаблоне для отправки на почту в 'users/password_reset_email.html'.
    Переходит на уведомление о отправке сообщения на почту.
    """
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    """
    Контроллер перенаправляющий на уведомление о отправке сообщения на почту для изменении пароля.
    """
    template_name = 'users/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Контроллер для востановления пароля.
    Принимает почту для востановления пароля, переопределяет новый пароль.
    Переходит на уведомление о успешной смена пароля.
    """
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """
    Контроллер перенаправляющий на уведомление о успешном изменении пароля.
    """
    template_name = 'users/password_reset_complete.html'
