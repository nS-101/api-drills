from django.urls import path

from .pricing import computePrice
from .views import makePriceView

urlpatterns = [
    path("price", makePriceView(computePrice)),
]
