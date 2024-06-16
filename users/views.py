from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from users.forms import UserProfileForm, UserRegisterForm, UserLoginForm
from users.models import User, Subscription
from users.services import create_price, create_session, create_product


def get_subscription(request):
    """ Функция для создания сессии подписки и редиректа на страницу платежа """
    if request.method == 'GET':
        if request.user.is_authenticated:
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
    success_url = reverse_lazy('users:login')


class ProfileView(LoginRequiredMixin, DetailView):
    """
    Контроллер для изменения профиля пользователя.
    Модель User, форма UserRegisterForm.
    При успешном изменении переходит на себя.
    """
    model = User
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user


class UserLoginView(LoginView):
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
    model = User
    success_url = reverse_lazy('content:index')

    def get_object(self, queryset=None):
        """
        Метод возвращающий текущего пользователя
        """
        return self.request.user
