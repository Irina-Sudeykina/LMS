import os

import stripe
from dotenv import load_dotenv


load_dotenv(override=True)

stripe.api_key = os.getenv("STRIPE_API_KEY")


def create_stripe_product(title):
    """Создает продукт в stripe"""

    return stripe.Product.create(name=title)


def create_stripe_price(product, amount):
    """Создает цену в stripe"""

    return stripe.Price.create(
        product=product["id"],
        currency="rub",
        unit_amount=amount * 100,
    )


def create_stripe_sessions(price):
    """Создает сессию в stripe"""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")
