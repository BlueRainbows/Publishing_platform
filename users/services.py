import random

import stripe
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail

from config.settings import SECRET_KEY_STRIPE, HTTP_SUCCESS, EMAIL_HOST_USER

st = stripe.api_key = SECRET_KEY_STRIPE


def create_product(pk, data):
    description = str(pk) + "дата платежа" + str(data)
    subscription = stripe.Product.create(
        name=pk,
        description=description,
    )
    return subscription.get('id')


def create_price(product):
    price = stripe.Price.create(
        currency="rub",
        unit_amount=2000 * 100,
        nickname="Покупка",
        product=product,
    )
    return price


def create_session(price):
    session = stripe.checkout.Session.create(
        success_url=HTTP_SUCCESS + "/subscription_info/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def get_verification(request, user):
    """
    Функция формирует токен для пользователя при помощи бибилиотеки random,
    перемешивает значение строки через метод shuffle, склеивает строку из 10 символов.
    Деактивирует пользователя и добавляет к нему сформированный токен.
    Формирует и отправляет письмо с ссылкой для активации пользователя на основе сформированного токена.
    """
    str1 = '123456789'
    str2 = 'qwertyuiopasdfghjklzxcvbnm'
    str3 = str2.upper()
    str4 = str1 + str2 + str3
    list_symbol = list(str4)
    random.shuffle(list_symbol)
    token = ''.join([random.choice(list_symbol) for _ in range(10)])
    user.is_active = False
    user.token = token
    user.save()
    current_site = get_current_site(request)
    send_mail(
        subject=f'Здравствуйте {user.first_name}! Теперь вы зарегистрированы на нашем сервисе! Подтвердите свой электронный адрес.',
        message=f'Чтобы подтвердить регистрацию в нашем сервисе перейдите по ссылке: http://{current_site}/activate/{token}',
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False,
    )