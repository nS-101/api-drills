"""A deliberately broken version of the pricing API, used by score.py. Do not read before finishing ex09."""
from django.urls import path

from ..views import makePriceView



def computePrice(amount, coupon=None):
    if amount <= 0:
        raise ValueError("amount must be a positive integer")
    discount = 0
    if coupon:
        code = coupon
        if code == "SAVE10":
            discount = amount * 10 // 100
        elif code == "SAVE20":
            if amount < 5000:
                raise ValueError("SAVE20 needs an amount of at least 5000")
            discount = amount * 20 // 100
        elif code == "HALF":
            discount = min(amount // 2, 1000)
        else:
            raise ValueError("unknown coupon")
    return {"amount": amount, "discount": discount, "total": amount - discount}


urlpatterns = [path("price", makePriceView(computePrice))]
