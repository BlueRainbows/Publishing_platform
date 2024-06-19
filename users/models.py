from django.contrib.auth.models import AbstractUser
from django.db import models


class Subscription(models.Model):
    product_id = models.CharField(
        max_length=255,
        verbose_name='Индицикатор страйпа',
        blank=True,
        null=True
    )
    payment_data = models.DateField(
        auto_now=True,
        verbose_name='Дата оплаты',
        blank=True,
        null=True
    )
    payment_session = models.CharField(
        max_length=200,
        verbose_name='Сессия платежа',
        blank=True,
        null=True
    )
    payment_url = models.URLField(
        max_length=400,
        verbose_name='Ссылка для оплаты',
        blank=True,
        null=True
    )


class User(AbstractUser):
    """ Модель пользователя """
    username = None
    phone = models.CharField(
        max_length=12,
        verbose_name='Номер телефона',
        unique=True
    )
    avatar = models.ImageField(
        upload_to='users/',
        verbose_name='Аватар',
        default='/users/796d02684eadafba407faf81a4fd697d.png'
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Фамилия'
    )
    subscription = models.OneToOneField(
        Subscription,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
