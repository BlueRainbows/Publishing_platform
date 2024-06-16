import stripe
from config.settings import SECRET_KEY_STRIPE, HTTP_SUCCESS

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
